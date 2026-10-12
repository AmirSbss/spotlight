#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy>=1.26,<3", "scipy>=1.11,<2", "soundfile>=0.12,<1"]
# [tool.uv]
# exclude-newer = "2026-09-01T00:00:00Z"
# ///
"""Sound mix for spotlight: music bed + SFX + live clip audio + voice, levelled per event.

  mix.py <work/mix.json>    -> mix.wav, music-only.wav, mix-report.txt next to mix.json

mix.json (every key but duration is optional):
  { "music":  {"file": str, "start": s, "fade_in": s, "fade_out": s, "gain_lufs": LUFS},
    "sfx":    [{"file": str, "t": s, "align": "start"|"peak", "target_db": dB, "cap_db": dB}],
    "clips":  [{"file": str, "start": s, "dur": s, "t": s, "gain_db": dB over the bed, default -15}],
    "voice":  [{"file": str, "t": s}],
    "duration": s }
Paths are relative to mix.json's folder (or absolute).

Music is levelled to a bed target (default -23 LUFS) and ducked -8 dB under voice lines,
with 150 ms ramps around each line. Every SFX gain is solved so its peak in its own
frequency band sits target_db (default +3.5 dB) over the bed in the same 150 ms window;
the 2-8 kHz lift is capped at 4 dB, the broadband peak at cap_db (default +6 dB) over the
local bed peak, and a level floor keeps effects from vanishing over quiet passages. The
solver is adapted from motion-video-kit's solve-sfx-gains.py and offline-mix.py (MIT,
credited in NOTICE.md). music-only.wav is the same bed and clip audio without voice and
effects, and not ducked: the version for adding other sound, or none. Final loudness is
left to footage.py encode (-14 LUFS).

Needs ffmpeg. Run it with `uv run mix.py mix.json`: uv reads the dependencies above and keeps their environment in
its own cache, never next to this file (the skill folder may be read-only).
"""
import argparse
import json
import math
import re
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfiltfilt

SR = 48000
BED_LUFS = -23.0          # where the music sits before encode lifts the whole mix to -14
DUCK_DB, DUCK_RAMP = -8.0, 0.15
TARGET_DB, CAP_DB = 3.5, 6.0
HF_BAND, HF_LIFT_CAP = (2000.0, 8000.0), 4.0
TOP_DB = 0.0              # an effect never peaks over the music's loudest moment: encode sets the music's loudness,
                          # so the music's top already sits at its true-peak ceiling and anything louder gets crushed
FLOOR_DBFS = -26.0        # an effect never lands below this in its own band, however quiet the bed
FLOOR_UNDER_PEAK = -12.0  # ... nor 12 dB under the bed's broadband peak: a band the music leaves empty
BODY = 0.15               # the window an effect is judged in
CLIP_DB = -15.0           # live clip audio, in dB relative to the bed level: present but under the music
CLIP_FADE = 0.06          # clips fade in and out, so their edges never click
SILENT = -60.0            # a measure at or below this is silence (ebur128 gates at -70): never level it up


def run(cmd):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"{Path(str(cmd[0])).name} failed: {r.stderr.strip()[-600:]}")
    return r.stdout


def decode(path, tmp, name):
    # any input ffmpeg reads -> float32 stereo at SR, so nothing downstream sees a format
    wav = Path(tmp) / f"{name}.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", path, "-af",
         "aformat=sample_rates=48000:channel_layouts=stereo", "-c:a", "pcm_f32le", wav])
    data, _ = sf.read(wav, dtype="float32", always_2d=True)
    return data


def integrated_lufs(samples, tmp, name):
    if not np.any(samples):
        return float("-inf")
    wav = Path(tmp) / f"{name}.wav"
    sf.write(wav, samples, SR, subtype="FLOAT")
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", wav, "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    # the summary, not the per-frame lines: those carry their own running "I:" that starts at the -70 floor
    m = re.search(r"I:\s+(-?[0-9.]+|-inf) LUFS", r.stderr[r.stderr.rfind("Summary:"):])
    if r.returncode or not m:
        raise RuntimeError(f"loudness measure failed: {r.stderr.strip()[-600:]}")
    return float(m.group(1).replace("-inf", "-99"))


def level(target, measured):
    # the gain that brings a measured level to target; silence stays silence instead of a +40 dB blow-up
    return target - measured if math.isfinite(measured) and measured > SILENT else 0.0


def place(buf, samples, t, gain=1.0):
    # sum onto the timeline; a source longer than what remains is trimmed, not skipped
    i = round(t * SR)
    n = min(len(samples), len(buf) - i)
    if n > 0:
        buf[i:i + n] += samples[:n] * gain


def band(x, lo, hi):
    sos = butter(4, [max(lo, 20.0), min(hi, SR / 2 - 1.0)], btype="band", fs=SR, output="sos")
    return sosfiltfilt(sos, x[:, 0] if x.ndim > 1 else x)


def own_band(x):
    # the octave around the energy centroid: where this effect actually lives. Weighting by magnitude instead let a
    # whoosh's faint hiss (spread over every bin) pull its band to 1.1-4.4 kHz, where it has almost no energy (its body
    # is 150-1100 Hz), so the solver saw it as quiet and lifted it far too much
    power = np.abs(np.fft.rfft(x[:, 0])) ** 2 + 1e-24
    freqs = np.fft.rfftfreq(len(x), 1 / SR)
    c = float((freqs * power).sum() / power.sum())
    return c / 2, c * 2


def peaks(x, i0, i1, lo, hi):
    seg = x[i0:i1]
    return float(np.max(np.abs(seg))), float(np.max(np.abs(band(seg, lo, hi))))


def duck_envelope(n, lines):
    env = np.ones(n, dtype=np.float32)  # float32: this multiplies the float32 bed in place
    duck = np.float32(10 ** (DUCK_DB / 20))
    r = round(DUCK_RAMP * SR)
    for t, dur in lines:
        a, b = round(t * SR), round((t + dur) * SR)
        for i in range(max(0, a - r), min(n, a)):           # fully ducked by the time the line starts
            env[i] = min(env[i], 1 - (1 - duck) * (i - (a - r)) / r)
        env[a:min(n, b)] = duck
        for i in range(min(n, b), min(n, b + r)):           # and back up only after it ends
            env[i] = min(env[i], duck + (1 - duck) * (i - b) / r)
    return env


def lift_db(a, b):
    return float(20 * np.log10(max(a, 1e-12) / max(b, 1e-12)))


def solve_sfx(sfx, t, bed, target_db, cap_db, top):
    # gain so this effect's in-band peak sits target_db over the bed in the same 150 ms body,
    # then through the HF cap, the peak cap and the floor, whichever binds first (lowest gain)
    i0, i1 = round(t * SR), min(round((t + BODY) * SR), len(bed))
    if i1 - i0 < BODY * SR / 2:
        raise RuntimeError(f"sfx at {t}s does not fit before the end of the mix")
    lo, hi = own_band(sfx)
    sfx_peak = float(np.max(np.abs(sfx)))
    sfx_band = float(np.max(np.abs(band(sfx, lo, hi))))
    sfx_hf = float(np.max(np.abs(band(sfx, *HF_BAND))))
    bed_peak = float(np.max(np.abs(bed[i0:i1])))
    bed_band = float(np.max(np.abs(band(bed[i0:i1], lo, hi))))
    bed_hf = float(np.max(np.abs(band(bed[i0:i1], *HF_BAND))))
    if sfx_band <= 1e-9:
        raise RuntimeError("sfx has no energy to place")
    gain, why = 10 ** (target_db / 20) * bed_band / sfx_band, ("target", target_db)
    if bed_hf > 1e-9:
        g = 10 ** (HF_LIFT_CAP / 20) * bed_hf / sfx_hf
        if g < gain:
            gain, why = g, ("hf cap", HF_LIFT_CAP)
    if bed_peak > 1e-9:
        g = 10 ** (cap_db / 20) * bed_peak / sfx_peak
        if g < gain:
            gain, why = g, ("peak cap", cap_db)
    # the floor, like the cap, is anchored to the local music peak: a bass-only bed must not solve a
    # tick away to nothing just because the tick's band is empty. Absolute -26 dBFS covers true silence.
    floor_level = max(10 ** (FLOOR_DBFS / 20), bed_peak * 10 ** (FLOOR_UNDER_PEAK / 20)) if bed_peak > 1e-6 \
        else 10 ** (FLOOR_DBFS / 20)
    floor = floor_level / sfx_band
    if floor > gain:
        gain, why = floor, ("floor", lift_db(floor_level, 1.0))
    # last and over everything, the floor included: no peak over the music's loudest moment (whoosh-2 floored to +9.6 dB
    # over the music came out of encode's limiter crushed by about as much)
    if top > 1e-6 and sfx_peak * gain > top * 10 ** (TOP_DB / 20):
        gain, why = top * 10 ** (TOP_DB / 20) / sfx_peak, ("music's top", TOP_DB)
    report = {"gain_db": lift_db(gain, 1.0), "band": (lo, hi), "why": why,
              "in_band": lift_db(sfx_band * gain, bed_band) if bed_band > 1e-6 else None}
    report["hf"] = lift_db(sfx_hf * gain, bed_hf) if bed_hf > 1e-9 else None
    report["peak"] = lift_db(sfx_peak * gain, bed_peak) if bed_peak > 1e-9 else None
    return gain, report


def mix(cfg, outdir):
    outdir = Path(outdir)

    def src(f):  # relative to mix.json, wherever mix.py runs from
        return outdir / Path(f).expanduser()

    with tempfile.TemporaryDirectory(prefix="spotlight mix ") as tmp:
        music = cfg.get("music") or {}
        track = decode(src(music["file"]), tmp, "music") if music.get("file") else None
        start = round(float(music.get("start") or 0) * SR) if track is not None else 0
        bed_lufs = float(music.get("gain_lufs") or BED_LUFS)
        # voice and clips are decoded first: the implied length must cover them whole, not just their start
        voice_lines = [(float(v["t"]), decode(src(v["file"]), tmp, f"voice{i}"))
                       for i, v in enumerate(cfg.get("voice") or [])]
        clips = []
        for i, c in enumerate(cfg.get("clips") or []):
            s = decode(src(c["file"]), tmp, f"clip{i}")
            a = round(float(c.get("start") or 0) * SR)
            clips.append((c, s[a:a + round(float(c["dur"]) * SR)] if c.get("dur") is not None else s[a:]))
        ends = [float(c["t"]) + len(s) / SR for c, s in clips] + [t + len(s) / SR for t, s in voice_lines]
        ends += [float(e["t"]) for e in cfg.get("sfx") or []]
        # with no explicit duration, the music runs out where it runs out, unless an event sits later
        duration = float(cfg.get("duration") or 0)
        if not duration:
            candidates = ([len(track) / SR - start / SR] if track is not None else []) + [e + 0.5 for e in ends]
            duration = max(candidates) if candidates else 0
        if duration <= 0:
            raise RuntimeError("nothing to mix: no duration, no music and no events")
        n = round(duration * SR)
        bed = np.zeros((n, 2), dtype=np.float32)
        report = [f"duration {duration:.2f}s"]
        if track is not None:
            seg = track[start:start + n]
            bed[:len(seg)] = seg        # a track shorter than the video simply runs out, like a real DJ
            if len(seg) < n:
                report.append(f"music runs out at {len(seg) / SR:.2f}s, {duration - len(seg) / SR:.2f}s before the end: "
                              "start earlier or pick a longer track")
            measured = integrated_lufs(bed, tmp, "bed")
            gain = level(bed_lufs, measured)  # a silent bed stays silent
            bed *= 10 ** (gain / 20)
            report.append(f"music: {Path(music['file']).name} track {start / SR:.2f}-{(start + len(seg)) / SR:.2f}s "
                          f"-> {bed_lufs:.1f} LUFS bed (gain {gain:+.1f} dB"
                          + (", bed measures silent" if measured <= SILENT else "")
                          + f"), fades {float(music.get('fade_in') or 0):.2f}/"
                            f"{float(music.get('fade_out') or 0):.2f}s")
            for key, ramp in (("fade_in", np.linspace(0.0, 1.0, round(float(music.get("fade_in") or 0) * SR), dtype=np.float32)),
                              ("fade_out", np.linspace(1.0, 0.0, round(float(music.get("fade_out") or 0) * SR), dtype=np.float32))):
                if len(ramp) > 0:
                    f = min(len(ramp), n)
                    region = bed[:f] if key == "fade_in" else bed[n - f:]
                    region *= ramp[:f, None]
        if voice_lines:
            report.append(f"voice: {len(voice_lines)} lines, duck {DUCK_DB:+.1f} dB with {DUCK_RAMP * 1000:.0f} ms ramps")
        # music-only is for adding other sound or no voice at all: ducking for lines it doesn't carry would pump
        music_only = bed.copy()
        env = duck_envelope(n, [(t, len(s) / SR) for t, s in voice_lines])
        bed *= env[:, None]
        mixdown = bed.copy()
        for i, (c, seg) in enumerate(clips):
            # gain_db is relative to the bed: -15 puts the live sound 15 dB under the music, however the phone recorded it
            target = bed_lufs + float(c["gain_db"] if c.get("gain_db") is not None else CLIP_DB)
            g = level(target, integrated_lufs(seg, tmp, f"clip{i}"))
            f = min(round(CLIP_FADE * SR), len(seg) // 2)
            if f:
                ramp = np.linspace(0.0, 1.0, f, dtype=np.float32)[:, None]
                seg[:f] *= ramp
                seg[len(seg) - f:] *= ramp[::-1]
            place(music_only, seg, float(c["t"]), 10 ** (g / 20))   # live sound belongs to the fallback too
            place(mixdown, seg, float(c["t"]), 10 ** (g / 20))
            report.append(f"clip {i + 1} {Path(c['file']).name} @ {float(c['t']):.2f}s -> {target:.1f} LUFS ({g:+.1f} dB)")
        report.append(f"clips: {len(cfg.get('clips') or [])} live-audio event(s)")
        top = float(np.max(np.abs(mixdown))) if n else 0.0  # the music's (and live sound's) loudest moment
        for i, e in enumerate(cfg.get("sfx") or []):
            s = decode(src(e["file"]), tmp, f"sfx{i}")
            t = at = float(e["t"])
            if e.get("align") == "peak":  # a whoosh swells: its loudest moment, not its first sample, lands on the cut
                t = max(0.0, at - float(np.argmax(np.max(np.abs(s), axis=1))) / SR)
            where = f"@ {t:.2f}s" + (f" (peak on {at:.2f}s)" if e.get("align") == "peak" else "")
            try:
                gain, r = solve_sfx(s, t, mixdown, float(e.get("target_db") or TARGET_DB),
                                    float(e.get("cap_db") or CAP_DB), top)
            except RuntimeError as err:  # one bad effect never costs the whole mix
                report.append(f"sfx {i + 1} {Path(e['file']).name} {where}  skipped: {err}")
                continue
            place(mixdown, s, t, gain)
            why, value = r["why"]
            lo, hi = r["band"]
            # every number is the effect's peak over the music's in the same 150 ms; only the floor is absolute
            setby = f"floor {value:.1f} dBFS: the music is quiet here" if why == "floor" else f"{why} {value:+.1f} dB"
            lift = (f"{r['in_band']:+.1f} dB" if r["in_band"] is not None else "n/a, the music is silent here") + f" ({setby})"
            line = (f"sfx {i + 1} {Path(e['file']).name} {where}  gain {r['gain_db']:+.1f} dB  "
                    f"in-band peak {lift}; {lo:.0f}-{hi:.0f} Hz, {BODY * 1000:.0f} ms body")
            if r["hf"] is not None:
                line += f"  hf {r['hf']:+.1f} dB"
            if r["peak"] is not None:
                line += f"  peak {r['peak']:+.1f} dB"
            report.append(line)
        for i, (t, samples) in enumerate(voice_lines):  # never ducked or levelled here: that is voice.py's job
            over = t + len(samples) / SR - duration
            if over > 1e-3:
                report.append(f"voice {i + 1} @ {t:.2f}s runs {over:.2f}s past the end: trimmed")
            place(mixdown, samples, t)
        report.append("music-only: bed + clips (no voice, no sfx, not ducked)")
        sf.write(outdir / "mix.wav", mixdown, SR, subtype="FLOAT")
        sf.write(outdir / "music-only.wav", music_only, SR, subtype="FLOAT")
        (outdir / "mix-report.txt").write_text("\n".join(report) + "\n")
        return report


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mix_json", help="work/mix.json")
    a = ap.parse_args()
    try:
        cfg = json.loads(Path(a.mix_json).read_text())
    except (json.JSONDecodeError, OSError) as e:
        raise SystemExit(f"mix.py: cannot read {a.mix_json}: {e}")
    try:
        report = mix(cfg, Path(a.mix_json).parent)
    except (RuntimeError, KeyError, OSError) as e:
        raise SystemExit(f"mix.py: {e}")
    for line in report:
        print(line)
    print(f"-> {Path(a.mix_json).parent / 'mix.wav'} (+ music-only.wav, mix-report.txt)")


if __name__ == "__main__":
    main()
