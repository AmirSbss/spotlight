#!/usr/bin/env python3
"""Self-check for `mix.py`: bed levelling, ducking under voice, and the SFX gain solver.

Run: uv run --project skills/spotlight/scripts python tests/test_mix.py   (needs ffmpeg)

With a plain python3 that lacks numpy/scipy/soundfile the test skips, so the README's
python3 suites stay green; the real check always runs under the scripts' uv project.
"""
import json
import re
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
    print("mix: all checks passed")


if __name__ == "__main__":
    main()
