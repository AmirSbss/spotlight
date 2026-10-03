#!/usr/bin/env python3
"""Self-check for `footage.py check`: frozen stretches, loudness, frame count, contact sheet.

Run: python3 tests/test_check.py   (needs ffmpeg/ffprobe)
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
F = ROOT / "skills/spotlight/scripts/footage.py"


def ff(*args):
    subprocess.run(["ffmpeg", "-y", "-v", "error", *map(str, args)], check=True)


def check(*args, ok=True):
    r = subprocess.run([sys.executable, F, "check", *map(str, args)], capture_output=True, text=True)
    assert (r.returncode == 0) == ok, (r.returncode, r.stdout, r.stderr)
    return r


def main():
    with tempfile.TemporaryDirectory(prefix="check test 50% ٪ ") as tmp:  # spaces, a literal '%' and non-Latin in the path
        d = Path(tmp)
        # 3 s moving, 2 s frozen (last frame cloned), 1 s moving; a tone mastered near -14 LUFS
        ff("-f", "lavfi", "-i", "testsrc2=size=320x568:rate=30:duration=3", "-f", "lavfi", "-i", "testsrc2=size=320x568:rate=30:duration=1",
           "-f", "lavfi", "-i", "sine=f=330:d=6:sample_rate=48000",
           "-filter_complex", "[0:v]tpad=stop_mode=clone:stop_duration=2[a];[a][1:v]concat=n=2:v=1[v];[2:a]loudnorm=I=-14:TP=-2[s]",
           "-map", "[v]", "-map", "[s]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", d / "held.mp4")
        check(d / "held.mp4", "--out", d / "out")
        r = json.loads((d / "out" / "check.json").read_text())
        assert r["frames"] == 180 and r["size"] == [320, 568], r
        assert len(r["frozen"]["long_holds"]) == 1, r["frozen"]
        a, b = r["frozen"]["long_holds"][0]
        assert abs(a - 3.0) < 0.25 and abs(b - 5.0) < 0.25, (a, b)
        assert abs(r["frozen"]["total"] - 2.0) < 0.35, r["frozen"]
        assert abs(r["loudness"]["I"] + 14) < 1.0 and r["loudness"]["TP"] <= -1.0, r["loudness"]
        assert r["failures"] == [] and any("hold" in w for w in r["warnings"]), r
        assert (d / "out" / "check-sheet.jpg").exists()

        # the end card is exempt: a 2 s hold at the very end passes with --end-card 2
        ff("-f", "lavfi", "-i", "testsrc2=size=320x568:rate=30:duration=4", "-vf", "tpad=stop_mode=clone:stop_duration=2",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", d / "endcard.mp4")
        check(d / "endcard.mp4", "--end-card", "2")
        r = json.loads((d / "check.json").read_text())
        assert r["frozen"]["long_holds"] == [], r["frozen"]
        check(d / "endcard.mp4")
        r = json.loads((d / "check.json").read_text())
        assert len(r["frozen"]["long_holds"]) == 1, r["frozen"]
        # --end-card is the end card's length: a start time passed by mistake (5 of 6 s) is called out, not silently trusted
        check(d / "endcard.mp4", "--end-card", "5")
        r = json.loads((d / "check.json").read_text())
        assert any("--end-card" in w and "length" in w for w in r["warnings"]), r["warnings"]

        # no audio stream: loudness is None, not a failure
        assert r["loudness"] is None and r["failures"] == [], r

        # a silent track (what encode writes for mix=none) reads at the -70 LUFS floor: a warning, not a failure
        ff("-f", "lavfi", "-i", "testsrc2=size=320x568:rate=30:duration=2", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", d / "silent.mp4")
        check(d / "silent.mp4")
        r = json.loads((d / "check.json").read_text())
        assert r["failures"] == [] and any("silent" in w for w in r["warnings"]), r

        # far too loud: true peak above -1 dBTP is a hard failure (exit 1)
        ff("-f", "lavfi", "-i", "testsrc2=size=320x568:rate=30:duration=2", "-f", "lavfi", "-i", "sine=f=440:d=2:sample_rate=48000",
           "-af", "volume=18dB", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", d / "loud.mp4")
        check(d / "loud.mp4", ok=False)
        r = json.loads((d / "check.json").read_text())
        assert any("true peak" in x for x in r["failures"]), r["failures"]

        # prep under a '%' path still writes its video contact sheets (image2 would read '%' as a frame pattern)
        r = subprocess.run([sys.executable, F, "prep", d / "prep work", d / "held.mp4"], capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        m = json.loads((d / "prep work" / "manifest.jsonl").read_text().splitlines()[0])
        assert "error" not in m and Path(m["sheet"]).exists(), m

        # a very short clip (audio too short for the loudness gate) passes and still gets a contact sheet
        ff("-f", "lavfi", "-i", "testsrc2=size=320x568:rate=30:duration=0.4", "-f", "lavfi", "-i", "sine=f=330:d=0.3:sample_rate=48000",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", d / "short.mp4")
        check(d / "short.mp4", "--out", d / "short")
        assert (d / "short" / "check-sheet.jpg").exists()

        # track: per-second short-term loudness shows where the music lifts
        ff("-f", "lavfi", "-i", "aevalsrc='if(lt(t,5),0.01,0.5)*sin(2*PI*220*t)':s=48000:d=10", d / "lift.wav")
        r = subprocess.run([sys.executable, F, "track", d / "lift.wav", "--json"], capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        t = json.loads(r.stdout)
        assert len(t["per_second"]) >= 9 and t["per_second"][7] - t["per_second"][2] > 15, t
        # ...in the second it happens, and the soft opening reads as soft, not as silence (no 3 s window lag)
        assert t["per_second"][5] - t["per_second"][4] > 15 and abs(t["per_second"][0] - t["per_second"][3]) < 2, t
    print("check: all checks passed")


if __name__ == "__main__":
    main()
