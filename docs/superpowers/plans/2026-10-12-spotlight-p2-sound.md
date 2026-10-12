# spotlight P2 (sound) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every spotlight video gets real sound with no extra input:
- a bundled CC0 music bed matched to the tone;
- levelled sound effects on transitions and actions;
- live clip audio at a known level under the music;
- optional local narration (`--voice`).

All of it is mixed by `mix.py` and delivered with a music-only fallback.

**Architecture:**
- **`mix.py`** (exists, from PR #1/#2, numpy/scipy via the scripts' uv project) becomes the standard sound step. P2 makes it safe for an agent to drive: paths resolve from `mix.json`, the implied length covers every event, an effect at the very end is skipped instead of failing the mix, clip audio is levelled relative to the bed, clips fade, and it warns when the music runs out.
- **`voice.py`** (new, stdlib only) calls a separately installed Piper. It downloads one voice per language into `~/.cache/spotlight/piper/` and writes levelled line WAVs plus `durations.json`.
- **`assets/music/` and `assets/sfx/`** hold the bundled CC0 library. Each folder has `LICENSES.md`, and every track has a cue preset.
- **`references/sound.md`** carries the sound rules. `SKILL.md` §5 points at it.

**Tech Stack:**
- Python 3.8+ stdlib for `voice.py` and the tests run with plain `python3`;
- numpy/scipy/soundfile through `uv run --project skills/spotlight/scripts` for `mix.py` and its test;
- ffmpeg 4.4+;
- Piper (`piper-tts`, installed by the user; never bundled);
- bash.

**Spec:** `docs/superpowers/specs/2026-10-02-spotlight-design.md`: sections "mix.py", "voice.py", "Sound design rules", "Assets and licences", "Testing" and "Phases" (P2). Read them first.

## Global Constraints

- **Only CC0 or public-domain audio is committed.** Every bundled file appears in its folder's `LICENSES.md` with its own source page URL, author, the verbatim licence statement and the retrieval date. Pixabay and Incompetech are out (not CC0), as are Pexels, Mixkit and "royalty free" without CC0/PD.
- **Music:** 4–6 tracks covering calm, warm-acoustic, upbeat, minimal-tech and cinematic, with no vocals and no epic risers. Total under ~15 MB.
- **SFX:** a curated Kenney (CC0) subset plus verified CC0 whooshes. Total under ~1.5 MB.
- **Piper is not bundled,** and neither are its voices. Voices carry their own licences: a default voice must allow commercial use of its output.
- **`voice.py`:** input `lines.json` (`[{id, text, lang}]`), output `voice/<id>.wav` + `durations.json`. Voices are downloaded on first use into `~/.cache/spotlight/piper/`. Without Piper it prints the install command and exits 2. Without `--voice`, the skill never calls it.
- **`mix.py`:** input `work/mix.json` with `music {file, start, fade_in, fade_out, gain_lufs}`, `sfx [{file, t, target_db, cap_db}]`, `clips [{file, start, dur, t, gain_db}]`, `voice [{file, t}]` and `duration`. Output `mix.wav`, `music-only.wav` and `mix-report.txt`. Music is ducked −8 dB with 150 ms ramps under voice. SFX sit at +3.5 dB in their own band, the 2–8 kHz lift is capped at 4 dB, and the peak at +6 dB over the local music peak. Final loudness is left to `encode` (−14 LUFS).
- **`music-only.mp4`** is delivered when SFX or voice are present.
- **Sound rules:** music matches the buyer's customers, not "tech launch". It is calm for services and has a pulse even when chill. One soft whoosh per real transition; UI ticks only on simulated actions; pops on pins/badges; a soft chime on confirmation; density follows the tone. Never a sting over a music resolve. The music must not fade before the logo lands.
- `footage.py` stays Python stdlib only. `voice.py` is stdlib only. New Python dependencies go only into `skills/spotlight/scripts/pyproject.toml`; none are needed.
- **uv becomes a required tool** (it runs `mix.py`). `doctor.sh` fails without it.
- Every frame is a pure function of t. The kit and `capture.mjs` are untouched in P2.
- Commit messages end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Each task commits to `main`. The phase is pushed to `origin main` once all suites pass (the user's push policy).

## Review Focus

1. **`mix.json` with relative paths, `mix.py` run from another folder:** paths resolve from `mix.json`'s folder, not the shell's. Pinned in Task 1.
2. **A narration-only or clips-only mix with no `duration` and no music:** the implied length covers the whole voice line and the whole clip, not just their start times. Pinned in Task 1.
3. **An effect placed on the very last frames** (a chime on the end card): the mix still renders, and the report says the effect was skipped. Pinned in Task 1.
4. **A video longer than its music window** (explain runs 60–180 s): the report says where the music runs out, and the bundled library has a track long enough for a 180 s explainer. Pinned in Tasks 1 and 2.
5. **Persian narration text with a ZWNJ, Latin brand names or digits:** it reaches Piper byte-exact over stdin. The docs tell the agent to write numbers as words and spell brand names the way they're said. Pinned in Tasks 3 and 4.

---

## File Structure

```
skills/spotlight/
├── SKILL.md                    Task 4: options (--music default, --voice, --no-sfx), §3 narration, §5 sound, deliver music-only.mp4
├── references/
│   ├── sound.md                Task 4 (new): library tables, effect rules, narration, mix.json, report reading
│   ├── explain.md              Task 4: narration line points at sound.md
│   └── critic.md               Task 4: sound check covers effects and narration
├── scripts/
│   ├── mix.py                  Task 1: paths, implied length, end-of-mix effects, clip levelling + fades, warnings
│   ├── voice.py                Task 3 (new)
│   └── doctor.sh               Task 1: uv required; Task 3: piper install hint
└── assets/                     Task 2 (new)
    ├── music/<mood>.mp3, cues/<mood>.json, LICENSES.md
    └── sfx/<kind>-<n>.ogg, LICENSES.md
tests/
├── test_mix.py                 Task 1: edge cases; Task 2: bundled library end to end (mix → encode → check)
├── test_assets.py              Task 2 (new, stdlib)
├── test_voice.sh               Task 3 (new; skips without piper)
├── test_doctor.sh              Task 1: names uv when missing
└── test_docs.py                Task 4: sound docs ↔ assets ↔ scripts
README.md · NOTICE.md · docs/other-agents.md     Task 5
```

---

### Task 1: `mix.py` safe to drive, uv required

**Files:**
- Modify: `skills/spotlight/scripts/mix.py` (`mix()`, new `src()` and `level()` helpers, constants)
- Modify: `skills/spotlight/scripts/doctor.sh`
- Test: `tests/test_mix.py` (new `edges()` case), `tests/test_doctor.sh`

**Interfaces:**
- Produces:
  - `mix.json` paths are relative to `mix.json`'s folder (absolute and `~` paths also work).
  - `clips[].gain_db` now means *dB relative to the bed level* (`music.gain_lufs`, default −23 LUFS), default `CLIP_DB = -15`.
  - Report lines are `music runs out at <s>s, <s>s before the end: …`, `sfx <n> <name> @ <t>s  skipped: …`, `voice <n> @ <t>s runs <s>s past the end: trimmed` and `clip <n> <name> @ <t>s -> <LUFS> LUFS (<gain> dB)`.
  - `level(target, measured)` returns the gain in dB, or 0.0 when `measured` is silent.

- [ ] **Step 1: Write the failing edge-case test.** In `tests/test_mix.py`, add `import shutil` to the imports, and call `edges(d)` at the end of the `with` block in `main()`, after the sfx 3 assertions:

```python
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
```

- [ ] **Step 2: Run it and watch it fail**

Run: `uv run --project skills/spotlight/scripts python tests/test_mix.py`
Expected: FAIL. `mix.py` exits non-zero with `cannot read`/`No such file` for `music.wav` (relative paths resolve from `/`).

- [ ] **Step 3: Implement.** In `skills/spotlight/scripts/mix.py`:

1. Below `BODY = 0.15 ...`, add:
```python
CLIP_DB = -15.0           # live clip audio, in dB relative to the bed level: present but under the music
CLIP_FADE = 0.06          # clips fade in and out, so their edges never click
SILENT = -60.0            # a measure at or below this is silence (ebur128 gates at -70): never level it up
```
2. After `integrated_lufs`, add:
```python
def level(target, measured):
    # the gain that brings a measured level to target; silence stays silence instead of a +40 dB blow-up
    return target - measured if math.isfinite(measured) and measured > SILENT else 0.0
```
3. Replace the top of `mix()`, from `outdir = Path(outdir)` through `report = [f"duration {duration:.2f}s"]`, with:
```python
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
```
4. In the `if track is not None:` block, delete the line `bed_lufs = float(music.get("gain_lufs") or BED_LUFS)`, and replace `gain = bed_lufs - measured if math.isfinite(measured) else 0.0  # a silent bed stays silent` with `gain = level(bed_lufs, measured)  # a silent bed stays silent`. Replace `+ (", bed measures silent" if not math.isfinite(measured) else "")` with `+ (", bed measures silent" if measured <= SILENT else "")`. Directly after `bed[:len(seg)] = seg ...`, add:
```python
            if len(seg) < n:
                report.append(f"music runs out at {len(seg) / SR:.2f}s, {duration - len(seg) / SR:.2f}s before the end: "
                              "start earlier or pick a longer track")
```
5. Delete the old voice-decoding loop (`voice_lines = []  # (t, samples) ...` and the `for i, v in enumerate(cfg.get("voice") ...` loop). Keep the `if voice_lines: report.append(...)` line.
6. Replace the clip loop (from `for i, c in enumerate(cfg.get("clips") or []):` through `place(mixdown, s[a:a + d], float(c["t"]), g)`) with:
```python
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
```
7. In the SFX loop, replace
```python
            gain, r = solve_sfx(s, t, mixdown, float(e.get("target_db") or TARGET_DB),
                                float(e.get("cap_db") or CAP_DB))
```
with
```python
            try:
                gain, r = solve_sfx(s, t, mixdown, float(e.get("target_db") or TARGET_DB),
                                    float(e.get("cap_db") or CAP_DB))
            except RuntimeError as err:  # one bad effect never costs the whole mix
                report.append(f"sfx {i + 1} {Path(e['file']).name} @ {t:.2f}s  skipped: {err}")
                continue
```
Also change `s = decode(e["file"], tmp, f"sfx{i}")` to `s = decode(src(e["file"]), tmp, f"sfx{i}")`.
8. Replace the final voice placement loop with:
```python
        for i, (t, samples) in enumerate(voice_lines):  # never ducked or levelled here: that is voice.py's job
            over = t + len(samples) / SR - duration
            if over > 1e-3:
                report.append(f"voice {i + 1} @ {t:.2f}s runs {over:.2f}s past the end: trimmed")
            place(mixdown, samples, t)
```
9. In the module docstring, change the clips line to `"clips":  [{"file": str, "start": s, "dur": s, "t": s, "gain_db": dB under/over the bed, default -15}],` and add after the `mix.json` block: `Paths are relative to mix.json's folder (or absolute).`

- [ ] **Step 4: Run the test**

Run: `uv run --project skills/spotlight/scripts python tests/test_mix.py`
Expected: `mix: all checks passed`. If the clip-level assertion is off by more than 1 LU, print `lufs` and the `clip 1` report line before changing anything: the report gives the target the solver used.

- [ ] **Step 5: Make uv required in `doctor.sh`.** Replace the `opt "uv (music tempo and cues)" ...` line with:
```bash
req "uv (sound mix, music tempo and cues)" "command -v uv" "curl -LsSf https://astral.sh/uv/install.sh | sh  (or brew install uv)"
```
In `tests/test_doctor.sh`, after the `grep -q "MISS.*ffmpeg"` line, add:
```bash
grep -q "MISS.*uv" <<< "$out" || { echo "FAIL: uv not named"; echo "$out"; exit 1; }
```
Run: `bash tests/test_doctor.sh`. Expected: `doctor: ok`.

- [ ] **Step 6: Commit**
```bash
git add skills/spotlight/scripts/mix.py skills/spotlight/scripts/doctor.sh tests/test_mix.py tests/test_doctor.sh
git commit -q -m "fix(mix): paths from mix.json, full implied length, end-of-mix effects skip, clips levelled under the bed with fades; uv required

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: The bundled CC0 library

**Files:**
- Create: `skills/spotlight/assets/music/{calm,warm-acoustic,upbeat,minimal-tech,cinematic}.mp3`, `assets/music/cues/<same>.json`, `assets/music/LICENSES.md`
- Create: `skills/spotlight/assets/sfx/<kind>-<n>.ogg`, `assets/sfx/LICENSES.md`
- Create: `tests/test_assets.py`
- Modify: `tests/test_mix.py` (new `bundled()` case)

**Interfaces:**
- Consumes: the staged, licence-checked files from the sourcing pass (`$SCRATCH/assets-staging/out/`, with its `REPORT.md`).
- Produces:
  - `assets/music/<mood>.mp3` for the five moods.
  - `assets/music/cues/<mood>.json`, the exact output of `python3 scripts/footage.py track <mp3> --json` (`duration`, `per_second`, `tempo`, `strong_cues`).
  - SFX named `whoosh-N`, `click-N`, `type-N`, `toggle-N`, `pop-N`, `chime-N`, `thud-N` (`.ogg`).
  - Each `LICENSES.md` has one table row per file, with the file name in backticks.

- [ ] **Step 1: Review the staged files before anything enters the repo.** Read `REPORT.md` and both `LICENSES.md`. For every file, open its source page URL (WebFetch) and confirm three things: the licence statement on the page says CC0 or public domain, it matches the quote, and the author matches. Drop any file that fails. Check every music track's measurements: true peak ≤ 0 dBTP, length ≥ 60 s, and at least one track ≥ 180 s (an explainer's maximum). If no track reaches 180 s, note it in `sound.md` (Task 4): "for an explainer longer than the longest track, chain two tracks with a 2 s crossfade at a section break", and add a `music2` follow-up to P3.

- [ ] **Step 2: Write the failing test** `tests/test_assets.py`:

```python
#!/usr/bin/env python3
"""The bundled library: every file licensed CC0/PD with its own source, real audio, within the size budget.

Run: python3 tests/test_assets.py
"""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "skills/spotlight/assets"
AUDIO = {".mp3", ".ogg", ".wav"}
MOODS = {"calm", "warm-acoustic", "upbeat", "minimal-tech", "cinematic"}
KINDS = {"whoosh", "click", "pop", "chime"}  # the effects sound.md promises; more kinds may exist


def probe(f):
    out = json.loads(subprocess.run(["ffprobe", "-v", "error", "-of", "json", "-show_streams", "-show_format", str(f)],
                                    capture_output=True, text=True, check=True).stdout)
    return out["streams"], float(out["format"]["duration"])


def main():
    for kind, budget in (("music", 15e6), ("sfx", 1.5e6)):
        d = A / kind
        files = sorted(p for p in d.iterdir() if p.suffix in AUDIO)
        lic = (d / "LICENSES.md").read_text()
        rows = {m[0]: m[1] for m in re.findall(r"^\|[^|\n]*`([\w.-]+\.(?:mp3|ogg|wav))`[^|\n]*\|(.+)$", lic, re.M)}
        assert set(rows) == {p.name for p in files}, (kind, sorted(set(rows) ^ {p.name for p in files}))
        for name, row in rows.items():
            assert re.search(r"\bCC0\b|[Pp]ublic [Dd]omain", row), f"{name}: no CC0/PD licence in its row"
            assert "https://" in row, f"{name}: no source page"
        assert sum(p.stat().st_size for p in files) <= budget, f"{kind} over {budget / 1e6:.1f} MB"
        for p in files:
            streams, dur = probe(p)
            assert [s["codec_type"] for s in streams] == ["audio"], f"{p.name}: not a single audio stream (cover art?)"
            assert dur > 0.05, p.name
            if kind == "music":
                assert 60 <= dur <= 240, f"{p.name}: {dur:.0f}s"
                cue = json.loads((d / "cues" / f"{p.stem}.json").read_text())
                assert abs(cue["duration"] - dur) < 0.5 and len(cue["per_second"]) >= dur - 2, p.name
                assert cue.get("tempo"), f"{p.name}: cue preset has no tempo (run footage.py track with uv on PATH)"
            else:
                assert dur <= 3.0, f"{p.name}: {dur:.1f}s is long for an effect"
        if kind == "music":
            assert {p.stem for p in files} == MOODS, sorted(p.stem for p in files)
        else:
            assert KINDS <= {p.stem.rsplit("-", 1)[0] for p in files}, sorted(p.stem for p in files)
    print("assets: all checks passed")


if __name__ == "__main__":
    main()
```

Run: `python3 tests/test_assets.py`
Expected: FAIL with `FileNotFoundError` (no `assets/` yet).

- [ ] **Step 3: Copy the approved files in and generate the cue presets**
```bash
S=/tmp/claude-0/-root-spotlight/2716cf63-a105-4bb6-83d8-8ad984a343cc/scratchpad/assets-staging/out
A=skills/spotlight/assets
mkdir -p $A/music/cues $A/sfx
cp $S/music/*.mp3 $S/music/LICENSES.md $A/music/
cp $S/sfx/*.ogg $S/sfx/LICENSES.md $A/sfx/
for f in $A/music/*.mp3; do python3 skills/spotlight/scripts/footage.py track "$f" --json > "$A/music/cues/$(basename "${f%.mp3}").json"; done
python3 tests/test_assets.py
```
Expected: `assets: all checks passed`. A file that fails is fixed at its source: re-transcode it without cover art (`-map 0:a -c:a libmp3lame -b:a 160k`), or drop it and its row.

- [ ] **Step 4: Add the end-to-end wiring case to `tests/test_mix.py`.** The bundled track and effects go through `mix.py`, then `footage.py encode`, then `footage.py check`, the way the skill runs them. Add the function, and call `bundled(d)` after `edges(d)`:

```python
def bundled(d):
    # the real path: bundled track + bundled effects -> mix.py -> footage.py encode -> footage.py check passes
    A = ROOT / "skills/spotlight/assets"
    music = sorted((A / "music").glob("*.mp3"))[0]
    fx = {k: sorted((A / "sfx").glob(f"{k}-*.ogg"))[0] for k in ("whoosh", "click", "chime")}
    w = d / "bundled"
    (w / "out").mkdir(parents=True)
    (w / "mix.json").write_text(json.dumps({
        "music": {"file": str(music), "start": 4.0, "fade_in": 0.3, "fade_out": 1.0},
        "sfx": [{"file": str(fx["whoosh"]), "t": 1.0}, {"file": str(fx["click"]), "t": 2.5},
                {"file": str(fx["chime"]), "t": 4.6}],
        "duration": 6.0}))
    r = subprocess.run([sys.executable, MIXPY, w / "mix.json"], capture_output=True, text=True)
    assert r.returncode == 0, (r.stdout, r.stderr)
    report = (w / "mix-report.txt").read_text()
    assert "skipped" not in report and "runs out" not in report, report
    ff("-f", "lavfi", "-i", "testsrc2=size=540x960:rate=30:duration=6", "-q:v", "3", w / "out" / "%05d.jpg")
    F = S / "footage.py"
    subprocess.run(["python3", F, "encode", w / "out", w / "mix.wav", w / "video.mp4"], check=True)
    r = subprocess.run(["python3", F, "check", w / "video.mp4", "--out", w], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    loud = json.loads((w / "check.json").read_text())["loudness"]
    assert abs(loud["integrated"] + 14) <= 1.0 and loud["true_peak"] <= -1.0, loud
```

Before running, confirm the key names: `python3 -c "import json;print(json.load(open('<any check.json>'))['loudness'])"`. Use whatever `footage.py check` writes (look at `check()` in `footage.py`) and fix the two key names above to match.

Run: `uv run --project skills/spotlight/scripts python tests/test_mix.py`
Expected: `mix: all checks passed`.

- [ ] **Step 5: Commit**
```bash
git add skills/spotlight/assets tests/test_assets.py tests/test_mix.py
git commit -q -m "feat(assets): bundled CC0 music (5 moods, cue presets) and effects, each with its own licence record

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: `voice.py`, local narration with Piper

**Research behind it** (2026-10-12): rhasspy/piper is archived, and `piper-tts` ≥ 1.3 comes from OHF-Voice/piper1-gpl (GPL-3.0). It is always run as a separate program and never imported.

The command is `printf '%s\n' "$TEXT" | piper -m <voice>.onnx -f out.wav --sentence_silence 0.25 [-s N]`. These are the only flags that both the new Python CLI and the old C++ binary accept. The new CLI reads unknown flags aloud as text. Text is joined into one line, because the new CLI puts no pause between lines.

Voices come from `huggingface.co/rhasspy/piper-voices`, pinned to revision `c10ece1aade47bb51c153c893d14e5bf8e5b7117` and checked against the size and md5 in `voices.json`. Corrupt downloads have been reported.

Most voices are fine-tuned from `en_US-lessac` (Blizzard 2013, research only), and the low-quality ones from ryan (CC BY-NC-SA). So the defaults are only voices trained from scratch on PD, CC0 or CC BY data:

| Language | Default voice | Licence |
|---|---|---|
| en | `en_US-ljspeech-high` | PD |
| fa | `fa_IR-gyro-medium` | CC0 dataset as declared; provenance thin |
| it | `it_IT-serena-high` | CC BY 4.0, with a credit line |
| nl | `nl_NL-alex-medium` | CC0 |
| uk | `uk_UA-ukrainian_tts-medium`, speaker 0 | CC0 |

- No default for `ar`: the only voice has no dataset licence and is lessac-derived.
- No default for tr, es, pt, ru, pl, zh or hi: nothing clean.
- de and fr MLS voices are CC BY with hundreds of speakers. They stay opt-in per line (`"voice"`, `"speaker"`) until a speaker is chosen by listening.

The full report is in the session scratchpad (`piper-research.md`).

**Files:**
- Create: `skills/spotlight/scripts/voice.py` (stdlib only), `tests/test_voice.sh`
- Modify: `skills/spotlight/scripts/doctor.sh` (piper hint: `uv tool install --python 3.12 "piper-tts>=1.3"`)

**Interfaces:**
- Produces:
  - `voice.py <lines.json>` writes `voice/<id>.wav` (48 kHz float, levelled to −16 LUFS) and `durations.json` (`{id: seconds}`) next to `lines.json`.
  - A line may set `"voice"` (a Piper name or a local `.onnx` path) and `"speaker"`.
  - Exit codes: 2 when Piper is missing (the message carries the install command); 1 for an unknown language with no voice set (`no default voice for 'xx'`); 0 otherwise.
  - CC BY voices print a `credit (put it in sources.md and caption.txt): …` line.
  - `VOICES` in `voice.py` is the default map that `sound.md`'s table must mirror (Task 4's doc check).

- [x] **Step 1: Write the failing test** `tests/test_voice.sh`. It covers:
  - Without `piper` on PATH: exit 2 and the install command.
  - A fake `piper` that records its stdin, model and speaker: a Persian line with a ZWNJ, a Latin name and a newline reaches it as exactly `"اسپات‌لایت با Spotlight\n"`. The local-model path and the speaker pass through. `durations.json` is right, and the line is at −16 ± 1 LUFS.
  - Unknown language: exit 1, and the message names the language.
  - With a real Piper: an en line and a fa line download their default voices and come out at −16 ± 1 LUFS, each 1–12 s long.
- [x] **Step 2: Run it.** It failed with `voice.py` missing.
- [x] **Step 3: Implement `voice.py`.** The checked-in file is the implementation; read it alongside this plan.
- [x] **Step 4: Run it.** First the fake-piper part (`voice: ok (real piper skipped: not installed)`). Then install Piper with `uv tool install --python 3.12 "piper-tts>=1.3"` (piper-tts 1.8.0) and run it for real (`voice: ok`; the voices download once, ~180 MB).
- [ ] **Step 5: Commit**
```bash
git add skills/spotlight/scripts/voice.py skills/spotlight/scripts/doctor.sh tests/test_voice.sh
git commit -q -m "feat(scripts): voice.py — local Piper narration, licence-checked default voices, levelled lines + durations

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: `sound.md` and the skill text

**Files:**
- Create: `skills/spotlight/references/sound.md`
- Modify: `skills/spotlight/SKILL.md` (options table, line 33 "Read exactly one mode file…", §3 Plan, §5 Sound, §6 Encode, §8 Deliver)
- Modify: `skills/spotlight/references/explain.md:15`, `skills/spotlight/references/critic.md:14`, `skills/spotlight/references/promo.md` (any mention of music only from the inputs)
- Test: `tests/test_docs.py`

**Interfaces:**
- Consumes: the asset names from Task 2, the `voice.py` CLI from Task 3, and the `mix.py` report lines from Task 1.

- [ ] **Step 1: Write the failing doc checks.** In `tests/test_docs.py`, before `print("docs: all checks passed")`, add:

```python
    # P2: sound is a real step, not a promise
    assert "sound.md" in refs, "references/sound.md is missing"
    for flag in ("--voice", "--no-sfx", "--music"):
        assert flag in skill, f"SKILL.md options don't name {flag}"
    assert "music-only.mp4" in skill, "SKILL.md doesn't deliver music-only.mp4"
    assert "phase 2" not in every.lower(), "a doc still says phase 2 is coming"
    mixes = re.findall(r"[^\n`]*scripts/mix\.py[^\n`]*", every)
    assert mixes and all("uv run --project" in m for m in mixes), mixes
    for path in set(re.findall(r"assets/(?:music|sfx)/[\w.-]+\.(?:mp3|ogg|wav|json|md)", every)):
        assert (SK / path).exists(), f"docs name {path}, which doesn't exist"
    sound = refs["sound.md"]
    for p in sorted((SK / "assets/music").glob("*.mp3")) + sorted((SK / "assets/sfx").glob("*.ogg")):
        assert p.name in sound, f"sound.md never offers {p.name}"
    voice = (SK / "scripts/voice.py").read_text()
    assert "voice.py" in sound and "durations.json" in sound and "lines.json" in sound
    for lang in re.findall(r'^\s+"([a-z]{2})": "', voice, re.M):
        assert f"`{lang}`" in sound, f"sound.md's voice table misses {lang}"
```

Run: `python3 tests/test_docs.py`
Expected: FAIL with `references/sound.md is missing`.

- [ ] **Step 2: Write `skills/spotlight/references/sound.md`.** Fill the two tables from the real files: the music table's mood, fit, tempo (from `cues/*.json`) and length, and the effects table's names and descriptions (from `assets/sfx/LICENSES.md`). Fill the voice table from `VOICES` in `voice.py`. Structure and wording:

```markdown
# Sound

Music, effects and narration, all mixed by one script. Run from `$OUT/work`:
`uv run --project <skill-dir>/scripts python <skill-dir>/scripts/mix.py mix.json` → `mix.wav`, `music-only.wav`, `mix-report.txt`.
The first run downloads its Python packages (about a minute).

## Music

The user's track always wins (`--music <file>`, or an audio file in the inputs). `--music none` renders silence. Otherwise pick one bundled track by what the buyer's *customers* would want to hear, not by "tech launch":

| File | Mood | Fits | Tempo | Length |
|---|---|---|---|---|
| `assets/music/calm.mp3` | … | services, clinics, explainers in `clear` | … BPM | … s |
| … one row per bundled track … |

`assets/music/cues/<name>.json` holds each track's per-second loudness, tempo and strong cues (the output of `$F track --json`), so you can choose the window without measuring. For a user's track, run `python3 $F track <file>`.
- Start where the track already moves (a pulse even when chill), so frame 0 isn't a fade from nothing. Let the lift land on the reveal or the CTA, and cut on its beats for energetic tones.
- No vocals and no epic risers. The music must not fade before the end card lands: `fade_out` covers the last seconds of `duration`, so keep it ≤ 1 s and make sure the end card is already up when it starts.
- The window must reach the end. If `mix-report.txt` says `music runs out`, start earlier or pick a longer track.

## Effects (`--no-sfx` turns them off)

| File | Use |
|---|---|
| `assets/sfx/whoosh-1.ogg` | … |
| … one row per bundled effect … |

- One short, soft whoosh per *real* transition (a scene change, not every cut).
- Clean UI ticks only on simulated actions: a click, typing, a toggle.
- A pop on a pin, a badge or a number landing.
- A soft chime on a confirmation (done, sent, booked).
- Density follows the tone. Deadpan, premium, polished, clear and documentary are sparse (2–4 in a 20 s video); chaotic and energetic are dense.
- Never a sting over a music resolve, and nothing on the end card's last second.
- Put each effect's `t` on the frame the action happens (`frame / 30`). `mix.py` sets every gain itself; leave `target_db` and `cap_db` out unless the report says an effect is buried.

## Live sound from clips

Add a clip's own sound only when it helps (a crowd, an espresso machine, a laugh): `{"file": "<clip>", "start": <in-point s>, "dur": <s>, "t": <s on the timeline>}`. `gain_db` is relative to the music bed. The default `-15` keeps it under the music; use `-6` for a moment that should be heard (a crowd at the peak). Clips fade in and out over 60 ms on their own.

## Narration (`--voice`)

Off unless asked; captions stay on screen either way. Narration suits `explain` best.
1. Right after the plan, write `work/lines.json`: `[{"id": "s1", "text": "…", "lang": "en"}]`, one entry per sentence or beat, with text exactly as it should be spoken. Write numbers as words in the line's language ("twelve thousand", not 12,000), and spell brand names and abbreviations the way they're said. Piper reads digits and Latin words inside Persian or Arabic text badly.
2. Run `python3 <skill-dir>/scripts/voice.py lines.json` → `voice/<id>.wav` and `durations.json`. It exits 2 with the install command if Piper is missing; then say so, and render without narration.
3. Time the shots to the lines: each beat is at least its line's duration plus about 0.3 s. Lines never overlap.
4. Add each line to `mix.json` as `{"file": "voice/<id>.wav", "t": <s>}`. The music ducks under it on its own.

| `lang` | Voice | Licence |
|---|---|---|
| … one row per entry in `VOICES` in `voice.py` … |

For any other language, pass a Piper voice name per line (`"voice": "<name>"`, from huggingface.co/rhasspy/piper-voices); check its model card's licence before using it in a commercial video.

## mix.json

Paths are relative to `mix.json` (so `voice/s1.wav` works) or absolute (bundled assets: `<skill-dir>/assets/…`).

    {
      "music": {"file": "<skill-dir>/assets/music/upbeat.mp3", "start": 12.0, "fade_in": 0.2, "fade_out": 0.8},
      "sfx":   [{"file": "<skill-dir>/assets/sfx/whoosh-1.ogg", "t": 3.0}, {"file": "<skill-dir>/assets/sfx/click-1.ogg", "t": 6.4}],
      "clips": [{"file": "clips/IMG_0042.MOV", "start": 1.2, "dur": 2.0, "t": 8.0, "gain_db": -15}],
      "voice": [{"file": "voice/s1.wav", "t": 0.5}],
      "duration": 20.0
    }

`duration` is the video's length (`timeline.js` `duration`). Read `mix-report.txt` every time:
- every effect says `target`, `hf cap`, `peak cap` or `floor`, and none says `skipped`;
- no `music runs out`;
- no voice line `runs past the end`.

Fix the timing and re-run if any of those appear.

## Deliver

Encode `mix.wav` into `video.mp4`. When the mix has effects or narration, also encode `music-only.wav` into `music-only.mp4` (same frames, same poster): the fallback for platforms where the user adds their own sound or voice.
```

- [ ] **Step 3: Update `SKILL.md`**
  - **Options table:**
    - Replace the `--music` row with: `| `--music <file>\|none` | an audio file in the inputs, otherwise a bundled track matched to the tone (`references/sound.md`) |`.
    - Add: `| `--voice` | off; on reads narration aloud with local Piper TTS (`references/sound.md`) |`.
    - Add: `| `--no-sfx` | effects on, placed by the sound rules |`.
  - **Line 33:** add `references/sound.md` to the files read: "…plus `references/quality-bar.md`, `references/critic.md` and `references/sound.md` when you reach those steps."
  - **§3 Plan:** add the music track and window, the effects list (time → file → why) and, with `--voice`, the narration lines. With `--voice`, run `voice.py` right after the plan, because the line durations set the shot timing.
  - **§5 Sound:** replace the whole section with:
```markdown
## 5. Sound
Follow `references/sound.md`: pick the music (the user's track, else a bundled one), place the effects (unless `--no-sfx`), add live clip sound where it helps, and the narration lines with `--voice`. Write `work/mix.json` and run, from `$OUT/work`, `uv run --project <skill-dir>/scripts python <skill-dir>/scripts/mix.py mix.json` → `mix.wav`, `music-only.wav`, `mix-report.txt`. Read the report and fix anything it flags. The music must not fade before the end card lands.
```
  - **§6 Encode:** after the `encode … video.mp4` sentence, add: "With effects or narration in the mix, also run `python3 $F encode out music-only.wav $OUT/music-only.mp4 --poster $OUT/poster.jpg`."
  - **Deliverables line (line 24) and §8:** add `music-only.mp4` (when the mix has effects or narration).
- [ ] **Step 4: Update the other references**
  - `explain.md:15`: `- **Narration** (`--voice`) carries the argument, read by local TTS (`references/sound.md`); on-screen text still carries it on mute. Keep reading time ≥ 0.3 s per word.`
  - `critic.md:14`: `3. Sound: does the audio land on the cuts; is every effect on a real transition or action, never a sting over a resolve; is the narration clear over the music; does the music fade before the end card lands?`
  - `promo.md`: wherever audio files in the inputs are called "music candidates", keep that, and add "(none given → a bundled track, `references/sound.md`)".
  - `grep -rn -i "phase 2\|until the phase" skills/` must return nothing.
- [ ] **Step 5: Run the doc checks**
Run: `python3 tests/test_docs.py`
Expected: `docs: all checks passed`.
- [ ] **Step 6: Commit**
```bash
git add skills/spotlight/SKILL.md skills/spotlight/references tests/test_docs.py
git commit -q -m "docs(skill): sound.md (bundled music, effects, narration, mix.json); SKILL §5 runs mix.py, delivers music-only.mp4

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: P2 acceptance, README, NOTICE, push

**Files:**
- Modify: `README.md` (what you get, how it works, install requirements, Status, Tests), `NOTICE.md`, `docs/other-agents.md` (if it lists tools)

- [ ] **Step 1: Docs.**
  - **README:**
    - add `music-only.mp4` to "What you get";
    - add `mix.py` and `voice.py` to "How it works";
    - make **uv required** in Install ("ffmpeg …, ImageMagick …, Python 3.8+, Node 18+, Chromium or Chrome, and uv; Piper is optional, for narration");
    - Status: "Phase 2 of 4 is done: a bundled CC0 music and sound-effects library, levelled effects, and optional local narration. Phase 3 brings charts, diagrams and 3D scenes, and phase 4 more demos.";
    - Tests: add `python3 tests/test_assets.py` and `bash tests/test_voice.sh`.
  - **NOTICE.md:** replace "No music or sound effects are bundled with the skill yet…" with: "The bundled music (`skills/spotlight/assets/music/`) and sound effects (`skills/spotlight/assets/sfx/`) are CC0 or public domain; each file's author, source page and licence statement are in the `LICENSES.md` beside it. Piper (narration) and its voices are not bundled; each voice carries its own licence (`references/sound.md`)."
  - `grep -n "uv" docs/other-agents.md`: where it lists required tools, add uv.
- [ ] **Step 2: Run every suite**
```bash
python3 tests/test_footage.py && python3 tests/test_check.py && python3 tests/test_docs.py && python3 tests/test_assets.py
uv run --project skills/spotlight/scripts python tests/test_mix.py
bash tests/test_capture.sh && bash tests/test_kit.sh && bash tests/test_site.sh
bash tests/test_doctor.sh && bash tests/test_bridge_image.sh && bash tests/test_voice.sh
```
Expected: every line ends in `passed`/`ok` (`test_voice.sh` runs for real here, since Piper is installed in Task 3).
- [ ] **Step 3: The stranger test.** A fresh subagent that never saw this plan runs the skill from `skills/spotlight/SKILL.md` alone, in a scratch folder, on two jobs, one after the other (never in parallel: ~3 GB RAM free):
  1. `brag` of the fixture site served by `python3 tests/site_server.py`, 20 s vertical, no music given (so a bundled track), with effects.
  2. `explain`, `--voice --lang en --duration 60 --format landscape`, on the topic "why spotlight checks its own videos", using only the repo's README as the source.

  With `CAPTURE_WORKERS=2`, each must end with `check` passing, `mix-report.txt` clean, and `music-only.mp4` present. Every place the agent had to guess, hit an error, or did something the docs didn't say gets fixed in the docs or scripts, with a test where one fits. Re-run Step 2.
- [ ] **Step 4: Commit and push**
```bash
git add README.md NOTICE.md docs/other-agents.md
git commit -q -m "docs: P2 sound shipped: bundled CC0 library, mix.py as the sound step, optional narration; uv required

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git pull --rebase origin main && git push origin main
```
