#!/usr/bin/env python3
"""Self-check for `mix.py`: bed levelling, ducking under voice, and the SFX gain solver.

Run: uv run --project skills/spotlight/scripts python tests/test_mix.py   (needs ffmpeg)

With a plain python3 that lacks numpy/scipy/soundfile the test skips, so the README's
python3 suites stay green; the real check always runs under the scripts' uv project.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / "skills/spotlight/scripts"
sys.path.insert(0, str(S))

try:
    import numpy as np
    import soundfile as sf
    from scipy.signal import butter, sosfiltfilt
except ImportError:
    print("mix: skipped (run under uv: uv run --project skills/spotlight/scripts python tests/test_mix.py)")
    raise SystemExit(0)

SR, MIXPY = 48000, S / "mix.py"


def ff(*args):
    subprocess.run(["ffmpeg", "-y", "-v", "error", *map(str, args)], check=True)


def band_peak(x, lo, hi):
    sos = butter(4, [lo, hi], btype="band", fs=SR, output="sos")
    return float(np.max(np.abs(sosfiltfilt(sos, x[:, 0]))))


def rms_db(x):
    return 20 * np.log10(max(float(np.sqrt(np.mean(x ** 2))), 1e-9))


def win(x, a, b):
    return x[round(a * SR):round(b * SR)]


def edges(d):
    # mix.json in its own folder with relative paths, run from somewhere else: a video longer than its music,
    # an effect on the very last frames, a voice line that runs past the end
    w = d / "work dir"
    w.mkdir()
    for f in ("music.wav", "click.wav", "voice.wav", "clip.wav"):
        shutil.copy(d / f, w / f)
    (w / "mix.json").write_text(json.dumps({
        "music": {"file": "music.wav", "gain_lufs": -23},
        "sfx": [{"file": "click.wav", "t": 13.97}],
        "voice": [{"file": "voice.wav", "t": 13.0}],
        "duration": 14.0}))
    r = subprocess.run([sys.executable, MIXPY, w / "mix.json"], capture_output=True, text=True, cwd="/")
    assert r.returncode == 0, (r.stdout, r.stderr)
    report = (w / "mix-report.txt").read_text()
    assert "music runs out at 12.00s, 2.00s before the end" in report, report
    assert re.search(r"^sfx 1 click\.wav @ 13\.97s  skipped", report, re.M), report
    assert "voice 1 @ 13.00s runs 1.00s past the end: trimmed" in report, report

    # no music, no duration: the length covers the whole clip and the whole voice line, plus 0.5 s
    (w / "mix.json").write_text(json.dumps({
        "clips": [{"file": "clip.wav", "t": 0.5, "gain_db": -6}],
        "voice": [{"file": "voice.wav", "t": 3.0}]}))
    r = subprocess.run([sys.executable, MIXPY, w / "mix.json"], capture_output=True, text=True, cwd="/")
    assert r.returncode == 0, (r.stdout, r.stderr)
    out, _ = sf.read(w / "mix.wav", always_2d=True)
    assert len(out) == round(5.5 * SR), len(out) / SR
    assert rms_db(win(out, 3.2, 4.8)) > -20, "the voice line is missing or cut"
    # the live clip lands 6 dB under the -23 LUFS bed level, and fades in instead of starting on a step
    from mix import integrated_lufs
    with tempfile.TemporaryDirectory() as t2:
        lufs = integrated_lufs(win(out, 0.6, 1.9), t2, "clip")
    assert abs(lufs - (-29.0)) <= 1.0, lufs
    assert np.max(np.abs(win(out, 0.5, 0.5 + 10 / SR))) < 0.05 * np.max(np.abs(win(out, 1.0, 1.1))), "clip edge clicks"


def bundled(d):
    # the real path: bundled track + bundled effects -> mix.py -> footage.py encode -> footage.py check passes
    A = ROOT / "skills/spotlight/assets"
    music = A / "music" / "upbeat.mp3"
    fx = {k: sorted((A / "sfx").glob(f"{k}-*.ogg"))[0] for k in ("whoosh", "click", "chime")}
    w = d / "bundled"
    (w / "out").mkdir(parents=True)
    (w / "mix.json").write_text(json.dumps({
        "music": {"file": str(music), "start": 12.0, "fade_in": 0.3, "fade_out": 1.0},
        "sfx": [{"file": str(fx["whoosh"]), "t": 1.0}, {"file": str(fx["click"]), "t": 2.5},
                {"file": str(fx["chime"]), "t": 4.6}],
        "duration": 6.0}))
    r = subprocess.run([sys.executable, MIXPY, w / "mix.json"], capture_output=True, text=True)
    assert r.returncode == 0, (r.stdout, r.stderr)
    report = (w / "mix-report.txt").read_text()
    assert "skipped" not in report and "runs out" not in report, report
    # a literal '%' in the folder name must be doubled in ffmpeg's image pattern
    ff("-f", "lavfi", "-i", "testsrc2=size=540x960:rate=30:duration=6", "-q:v", "3", str(w / "out").replace("%", "%%") + "/%05d.jpg")
    F = S / "footage.py"
    subprocess.run(["python3", F, "encode", w / "out", w / "mix.wav", w / "video.mp4"], check=True)
    r = subprocess.run(["python3", F, "check", w / "video.mp4", "--out", w], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    loud = json.loads((w / "check.json").read_text())["loudness"]
    assert abs(loud["I"] + 14) <= 1.0 and loud["TP"] <= -1.0, loud


def main():
    with tempfile.TemporaryDirectory(prefix="mix test 50% ٪ ") as tmp:  # spaces, a literal '%' and non-Latin
        d = Path(tmp)
        # pink noise at a known loudness is the bed: energy in every band, so in-band solving is real
        ff("-f", "lavfi", "-i", "anoisesrc=color=pink:seed=7:sample_rate=48000:duration=12",
           "-af", "loudnorm=I=-20:TP=-2:LRA=11", "-ar", "48000", "-ac", "2", d / "music.wav")
        # a 4.2 kHz click (band ~= the 2-8 kHz HF band) and a 300 Hz thump (band outside HF)
        ff("-f", "lavfi", "-i", "aevalsrc=exp(-t*45)*sin(2*PI*4200*t):s=48000:d=0.06", "-ac", "2", d / "click.wav")
        ff("-f", "lavfi", "-i", "aevalsrc=exp(-t*18)*sin(2*PI*300*t):s=48000:d=0.35", "-ac", "2", d / "thump.wav")
        ff("-f", "lavfi", "-i", "sine=f=190:sample_rate=48000:duration=2", "-af", "volume=6dB", "-ac", "2", d / "voice.wav")
        ff("-f", "lavfi", "-i", "sine=f=600:sample_rate=48000:duration=1.5", "-af", "volume=-6dB", "-ac", "2", d / "clip.wav")
        (d / "mix.json").write_text(json.dumps({
            "music": {"file": str(d / "music.wav"), "start": 1.0, "fade_in": 0.5, "fade_out": 1.0, "gain_lufs": -20},
            "sfx": [{"file": str(d / "click.wav"), "t": 2.0, "target_db": 3.5},       # pure target: +3.5 dB
                    {"file": str(d / "click.wav"), "t": 6.0, "target_db": 12.0},      # HF lift caps at 4 dB
                    {"file": str(d / "thump.wav"), "t": 8.5, "target_db": 12.0, "cap_db": -2.0}],  # a tight peak cap binds
            "clips": [{"file": str(d / "clip.wav"), "start": 0.2, "dur": 1.0, "t": 4.0, "gain_db": -15}],
            "voice": [{"file": str(d / "voice.wav"), "t": 9.0}],
            "duration": 12.0}, ensure_ascii=False))
        r = subprocess.run([sys.executable, MIXPY, d / "mix.json"], capture_output=True, text=True)
        assert r.returncode == 0, (r.stdout, r.stderr)

        mix, sr1 = sf.read(d / "mix.wav", always_2d=True)
        bed, sr2 = sf.read(d / "music-only.wav", always_2d=True)
        assert sr1 == sr2 == SR and mix.shape == bed.shape == (12 * SR, 2), (sr1, mix.shape, bed.shape)
        report = (d / "mix-report.txt").read_text()
        assert "music-only: bed + clips" in report and "duck -8.0 dB with 150 ms ramps" in report

        # the bed lands on its target: fade-in opens from (near) silence, then holds a steady level
        assert rms_db(win(bed, 0, 0.08)) < rms_db(win(bed, 2, 3)) - 14, "fade-in does not open from silence"

        # ducking: fully ducked (-8 dB, 150 ms ramps) under the voice line at 9-11 s
        ducked = rms_db(win(bed, 9.5, 10.3)) - rms_db(win(bed, 5.2, 5.9))
        assert abs(ducked + 8.0) <= 0.7, ducked

        # voice is in the mix and not in the fallback
        assert rms_db(win(mix, 9.5, 10.3)) > rms_db(win(bed, 9.5, 10.3)) + 3

        # sfx 1: solved to the target, confirmed in the rendered audio (click window, own band).
        # mix - music-only is the placed sfx on its own: peaks of a sum fold phases together and read high
        lines = {int(m[0]): m for m in re.findall(r"^sfx (\d+) (.+)$", report, re.M)}
        assert set(lines) == {1, 2, 3}, report
        band = (2100.0, 8400.0)
        sfx_only = win(mix - bed, 2.0, 2.15)
        lift = 20 * np.log10(band_peak(sfx_only, *band) / band_peak(win(bed, 2.0, 2.15), *band))
        assert abs(lift - 3.5) <= 1.0, f"rendered in-band lift {lift:.1f} dB, want 3.5 +-1"
        assert "in-band +3.5 dB (target" in lines[1][1], lines[1][1]

        # sfx 2: asking for 12 dB, the 2-8 kHz lift is capped at 4 dB
        m = re.search(r"in-band ([+-][0-9.]+) dB \(hf cap", lines[2][1])
        assert m and float(m[1]) <= 4.1, lines[2][1]
        hf = float(re.search(r"hf ([+-][0-9.]+) dB", lines[2][1]).group(1))
        assert hf <= 4.05, hf

        # sfx 3: a tight cap_db is honoured -- the broadband peak is held at cap_db over the local bed peak
        m = re.search(r"in-band ([+-][0-9.]+) dB \(peak cap ([+-][0-9.]+)", lines[3][1])
        assert m and float(m[1]) > float(m[2]), lines[3][1]  # the cap held the effect below its target lift
        assert float(re.search(r"peak ([+-][0-9.]+) dB", lines[3][1]).group(1)) <= float(m[2]) + 0.05, lines[3][1]
        edges(d)
        bundled(d)
    print("mix: all checks passed")


if __name__ == "__main__":
    main()
