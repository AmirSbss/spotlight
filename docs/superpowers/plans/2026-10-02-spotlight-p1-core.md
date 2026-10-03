# spotlight P1 (core) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the private `/promo` plugin (v1.1, `/root/promo`) into a new repo `/root/spotlight`. It's one agent-agnostic `/spotlight` skill with three modes (brag, promo, explain), website input, a `check` command, text cards that never freeze, a critic loop and a `sources.md` deliverable. The repo has a fresh history with no client data, ready for the later phases (P2 sound, P3 visuals, P4 public release).

**Architecture:** One skill folder, `skills/spotlight/`. A lean `SKILL.md` carries the shared pipeline and loads one `references/<mode>.md`. The deterministic plumbing is:
- `scripts/footage.py`: Python stdlib plus ffmpeg/ImageMagick: prep, shot, encode, **check**, **track**;
- `scripts/capture.mjs` and **`scripts/site.mjs`**, both on a shared **`scripts/browser.mjs`**;
- `kit/` (`scene.html` + `kit.js`): a page where every frame is a pure function of t.

The model does the creative work. The scripts and kit do everything that has sharp edges.

**Tech Stack:** Python 3.8+ (stdlib only in `footage.py`), ffmpeg/ffprobe 4.4+ with zscale (tested on 5.1), ImageMagick 6 or 7, Node 18+ with `playwright-core` installed per run, Chromium, bash.

**Spec:** `docs/superpowers/specs/2026-10-02-spotlight-design.md` (in `/root/promo` now; Task 1 copies it into the new repo). Read it before starting.

## Global Constraints

- Project, skill and command are named `spotlight`. The repo will be `AmirSbss/spotlight` (it isn't created or pushed in P1). License MIT.
- **No client data anywhere in `/root/spotlight` or its history:** no names, domains, footage, phone numbers or paths from the user's client folders (named only in the private `/root/promo` copy of this plan). `/root/promo`'s git history and its `docs/superpowers/` (except the two spotlight files) must not be copied.
- **No third-party media whose licence isn't CC0 or public domain** gets committed. brag's bundled ende.app music is **not** copied. Music arrives in P2.
- `footage.py` stays Python stdlib only. No new pip or npm dependencies are committed. `playwright-core` is installed per run with `npm i --prefix . playwright-core`.
- Formats: vertical 1080×1920 (default for brag and promo), landscape 1920×1080 (default for explain), square 1080×1080, all at 30 fps.
- Deliverables go in `spotlight-output/` (timestamped `spotlight-output-YYYY-MM-DD-HHmmss/` if it exists): `video.mp4`, `poster.jpg`, `caption.txt`, `plan.md`, `sources.md`, `work/`.
- Encode targets −14 LUFS integrated, with true peak ≤ −1.5 dBTP after AAC. `encode` already uses two-pass loudnorm at TP −2.5.
- Quality bar (spec): frozen time ≤ 1 s per 30 s; no hold > 0.6 s without motion except the end card; frame 0 is a finished composition; the CTA is readable ≥ 1.5 s.
- Every frame is a pure function of t; parallel capture must not change any pixel.
- Commit messages end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Review Focus

1. **A website that never stops loading or scrolls forever** (consent walls, infinite feeds): `site.mjs` must finish within its time cap and keep what it got, with at most 12 screens and the full-page height capped. Pinned in Task 4 (infinite-scroll fixture).
2. **A right-to-left, non-Latin website** (Persian or Arabic): `copy.json` must keep the exact UTF-8 strings, and `brand.json` the fonts. Pinned in Task 4 (an RTL page in the fixture site).
3. **A video with no audio stream, or a very short one**, given to `check`: no crash and no false loudness failure, and a contact sheet is still written. Pinned in Task 2.
4. **Paths with spaces, `%` or non-Latin characters** in the `site.mjs` work dir and in `check` output: these must work. Pinned in Tasks 2 and 4.
5. **Text cards over a blurred still** (the "What we do" list): these must not register as frozen. Pinned in Task 5 (kit, capture, encode and check together).

---

## File Structure

```
/root/spotlight/                         new git repo (fresh history), branch main
├── skills/spotlight/
│   ├── SKILL.md                         Task 6: core workflow + mode table + rules
│   ├── references/
│   │   ├── brag.md                      Task 6: brag structure, laws, tones
│   │   ├── promo.md                     Task 6: footage-first workflow, people coverage, tones
│   │   ├── explain.md                   Task 6: explainer structure, evidence, tones
│   │   ├── critic.md                    Task 6: critic prompts (adapted from motion-video-kit, MIT)
│   │   └── quality-bar.md               Task 6: measured + visual + message checks
│   ├── scripts/
│   │   ├── footage.py                   Task 1 port; Task 2 check; Task 3 track
│   │   ├── browser.mjs                  Task 4: shared playwright-core/chromium launch
│   │   ├── capture.mjs                  Task 1 port; Task 4 uses browser.mjs
│   │   ├── site.mjs                     Task 4: URL → work/site/{copy.json, brand.json, screens/, full.png, assets/}
│   │   ├── doctor.sh                    Task 7
│   │   └── analyze_music_cues.py, pyproject.toml, uv.lock   Task 1 (copied, logic unchanged; brag MIT)
│   └── kit/
│       ├── scene.html                   Task 1 port; Task 5 adds #web
│       └── kit.js                       Task 1 port; Task 5 adds web shots + card drift
├── tests/
│   ├── test_footage.py                  Task 1 port (synthetic music beds)
│   ├── test_check.py                    Task 2 (+ Task 3 track cases)
│   ├── test_capture.sh                  Task 1 port
│   ├── test_kit.sh                      Task 1 port; Task 5 adds web + card-motion cases
│   ├── test_site.sh                     Task 4
│   ├── test_doctor.sh                   Task 7
│   ├── test_docs.py                     Task 6: SKILL/reference ↔ scripts consistency
│   ├── test_bridge_image.sh, rtl-check.html   Task 1 port
│   └── fixtures/  color-scene.html, fps25-scene.html, landscape-scene.html (port) · site/ (Task 4)
├── docs/
│   ├── other-agents.md                  Task 8
│   └── superpowers/specs/2026-10-02-spotlight-design.md, plans/2026-10-02-spotlight-p1-core.md   Task 1
├── .claude-plugin/plugin.json, marketplace.json      Task 8
├── .claude/skills/spotlight, .agents/skills/spotlight, .opencode/skills/spotlight → ../../skills/spotlight   Task 8
├── .gitattributes, .gitignore           Task 1 (.gitignore), Task 8 (.gitattributes)
└── README.md · LICENSE · NOTICE.md      Task 8
```

---

### Task 1: New repo, port and rename

**Files:**
- Create: `/root/spotlight/` (git init), with everything listed under "Task 1" above
- Modify (after copying): `tests/test_footage.py`, `tests/test_capture.sh`, `tests/test_kit.sh`, `skills/spotlight/kit/kit.js`, `skills/spotlight/kit/scene.html`, `skills/spotlight/scripts/footage.py`, `skills/spotlight/scripts/capture.mjs`, `skills/spotlight/scripts/analyze_music_cues.py`

**Interfaces:**
- Produces: `window.SPOTLIGHT` (renamed from `window.PROMO`) as the timeline global read by `kit.js`. The environment variable `SPOTLIGHT_SRGB_ICC` replaces `PROMO_SRGB_ICC`. The skip rule drops `spotlight-output*` folders (was `promo-output*`). `tests/test_footage.py` defines `make_bed(dst, seconds, quiet_until=0.0)`.

- [ ] **Step 1: Create the repo and copy the sources**

```bash
mkdir /root/spotlight && cd /root/spotlight && git init -q -b main
mkdir -p skills/spotlight/scripts skills/spotlight/kit skills/spotlight/references tests/fixtures docs/superpowers/specs docs/superpowers/plans
S=/root/promo
cp $S/skills/promo/SKILL.md skills/spotlight/SKILL.md
cp $S/skills/promo/kit/kit.js $S/skills/promo/kit/scene.html skills/spotlight/kit/
cp $S/skills/promo/scripts/footage.py $S/skills/promo/scripts/capture.mjs $S/skills/promo/scripts/analyze_music_cues.py \
   $S/skills/promo/scripts/pyproject.toml $S/skills/promo/scripts/uv.lock skills/spotlight/scripts/
cp $S/tests/test_footage.py $S/tests/test_capture.sh $S/tests/test_kit.sh $S/tests/test_bridge_image.sh $S/tests/rtl-check.html tests/
cp $S/tests/fixtures/*.html tests/fixtures/
cp $S/docs/superpowers/specs/2026-10-02-spotlight-design.md docs/superpowers/specs/
cp $S/docs/superpowers/plans/2026-10-02-spotlight-p1-core.md docs/superpowers/plans/
printf '__pycache__/\n.venv/\nnode_modules/\nspotlight-output*/\n' > .gitignore
ls -R skills tests | head -40
```
Expected: the tree above. There must be **no** `assets/` folder: the brag music isn't copied.

- [ ] **Step 2: Rename promo → spotlight in code and tests**

```bash
cd /root/spotlight
sed -i 's|skills/promo|skills/spotlight|g' tests/test_footage.py tests/test_capture.sh tests/test_kit.sh
sed -i 's|window\.PROMO|window.SPOTLIGHT|g; s|PROMO\.grain|SPOTLIGHT.grain|g; s|PROMO\.end|SPOTLIGHT.end|g; s|const P = window\.PROMO|const P = window.SPOTLIGHT|; s|^// /promo render kit|// spotlight render kit|' skills/spotlight/kit/kit.js
sed -i 's|<!-- /promo scene template|<!-- spotlight scene template|; s|at PROMO\.end|at SPOTLIGHT.end|' skills/spotlight/kit/scene.html
sed -i 's|Footage plumbing for /promo|Footage plumbing for spotlight|; s|PROMO_SRGB_ICC|SPOTLIGHT_SRGB_ICC|g; s|"promo-output"|"spotlight-output"|; s|earlier /promo output|earlier spotlight output|; s|earlier promo-output|earlier spotlight-output|; s|promo-output\*|spotlight-output*|g' skills/spotlight/scripts/footage.py
sed -i 's|// Capture a /promo page|// Capture a spotlight page|' skills/spotlight/scripts/capture.mjs
sed -i 's|at /promo run time|at spotlight run time|; s|write /promo cue presets|write spotlight cue presets|' skills/spotlight/scripts/analyze_music_cues.py
grep -rn 'promo' skills/spotlight/kit skills/spotlight/scripts/footage.py skills/spotlight/scripts/capture.mjs tests/*.sh | grep -v 'promo\b.*mode' || echo "no promo leftovers in code"
```
Expected: `no promo leftovers in code`. If any line remains, fix it by hand. The word "promo" may only survive where it names the *mode* (that comes later, in Task 6).

- [ ] **Step 3: Replace the bundled-music fixtures with synthetic beds**

In `tests/test_footage.py`, delete the two lines
```python
MUSIC = sorted((ROOT / "skills/spotlight/assets/music").glob("*.mp3"))[0]
MUSIC12 = next((ROOT / "skills/spotlight/assets/music").glob("*vol-12-*.mp3"))
```
and add, after `def ff(*args): ...`:
```python
def make_bed(dst, seconds, quiet_until=0.0):
    """A music-like test bed: a pulsing chord with sharp noise hits on the beat, quiet until `quiet_until`, then a lift.
    Stands in for real music (none is bundled): the lift is what makes one-pass loudnorm drift, and the hits are what
    make AAC overshoot a true-peak target."""
    q = quiet_until
    expr = (f"(if(lt(t,{q}),0.08,0.45))*(0.5*sin(2*PI*220*t)+0.3*sin(2*PI*277.2*t)+0.2*sin(2*PI*329.6*t))"
            f"*(0.55+0.45*pow(abs(sin(PI*2*t)),8))"
            f"+(if(lt(t,{q}),0.02,0.3))*(2*random(0)-1)*pow(abs(sin(PI*2*t)),40)")
    ff("-f", "lavfi", "-i", f"aevalsrc='{expr}':s=48000:d={seconds}", "-ac", "2", dst)
```
Replace the music uses:
- `ff("-ss", "30", "-i", MUSIC, "-t", "4", work / "mix.wav")` → `make_bed(work / "mix.wav", 4)`
- `ff("-t", "30", "-i", MUSIC12, "-af", "afade=t=out:st=29:d=1", work / "bed.wav")` → `make_bed(work / "bed.wav", 30, quiet_until=8)`

Then rename the output-folder fixtures to the new skip rule:
```bash
sed -i 's|d / "promo-output" / "promo.mp4"|d / "spotlight-output" / "video.mp4"|; s|"promo-output-archive"|"spotlight-output-archive"|; s|named promo-output-\*|named spotlight-output-*|; s|work / "promo.mp4"|work / "video.mp4"|; s|d / "50% off" / "promo.mp4"|d / "50% off" / "video.mp4"|' tests/test_footage.py
grep -n 'MUSIC\|promo' tests/test_footage.py || echo clean
```
Expected: `clean`.

- [ ] **Step 4: Run every ported test**

Run:
```bash
cd /root/spotlight && python3 tests/test_footage.py && bash tests/test_capture.sh && bash tests/test_kit.sh && bash tests/test_bridge_image.sh
```
Expected: `footage.py: all checks passed`, `capture.mjs: ok`, `kit: ok`, and `bridge --image: ok` or `bridge --image: skipped …`.

- [ ] **Step 5: Prove the synthetic beds still catch the two audio regressions**

These tests only matter if they fail on the old behaviour. Mutation check, reverted right after:
```bash
cd /root/spotlight && cp skills/spotlight/scripts/footage.py /tmp/footage.keep
sed -i 's|    if "inf" in m\["input_i"\]:  # silent mix: nothing to normalize|    return f"{fit},loudnorm={target}"  # MUTATION: one-pass\n    if "inf" in m["input_i"]:|' skills/spotlight/scripts/footage.py
python3 tests/test_footage.py 2>&1 | tail -1      # Expected: AssertionError (loudness off by > 0.35 LU)
cp /tmp/footage.keep skills/spotlight/scripts/footage.py
sed -i 's|TP=-2.5:LRA=11"|TP=-1.5:LRA=11"|' skills/spotlight/scripts/footage.py
python3 tests/test_footage.py 2>&1 | tail -1      # Expected: AssertionError (true peak above -1.5)
cp /tmp/footage.keep skills/spotlight/scripts/footage.py && python3 tests/test_footage.py | tail -1
```
Expected: two `AssertionError` lines, then `footage.py: all checks passed`. If a mutation **passes**, the bed isn't discriminating. Make the hits sharper in `make_bed` (raise the `0.3` hit gain or the `40` exponent) or lengthen the quiet intro, until both mutations fail. Then re-run Step 4.

- [ ] **Step 6: Commit**

```bash
cd /root/spotlight && git add -A && git commit -q -m "chore: start spotlight from promo v1.1 (renamed, no bundled music, synthetic test beds)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && git log --oneline
```

---

### Task 2: `footage.py check`

**Files:**
- Modify: `skills/spotlight/scripts/footage.py`: add the `frozen_samples`, `holds`, `loudness` and `check` functions and a `check` subcommand
- Test: `tests/test_check.py`

**Interfaces:**
- Consumes: `run`, `probe`, `FPS` (already in `footage.py`).
- Produces:
  - `check(video, end_card=0.0, target=-14.0, out=None) -> dict`. It writes `<out>/check.json` and `<out>/check-sheet.jpg`; `out` defaults to the video's folder.
  - The dict keys are `file`, `duration`, `fps`, `frames`, `size`, `video_codec`, `audio_codec`, `loudness` (`{"I","LRA","TP"}` or `None`), `frozen` (`{"total","holds","long_holds","budget"}`), `warnings` (list of str), `failures` (list of str) and `sheet` (path str).
  - CLI: `python3 footage.py check <video> [--end-card S] [--target LUFS] [--out DIR]` prints a summary and exits 1 when `failures` is non-empty.

- [ ] **Step 1: Write the failing test**: `tests/test_check.py`

```python
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

        # no audio stream: loudness is None, not a failure
        assert r["loudness"] is None and r["failures"] == [], r

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

        # a very short clip still gets a contact sheet
        ff("-f", "lavfi", "-i", "testsrc2=size=320x568:rate=30:duration=0.4", "-c:v", "libx264", "-pix_fmt", "yuv420p", d / "short.mp4")
        check(d / "short.mp4", "--out", d / "short")
        assert (d / "short" / "check-sheet.jpg").exists()
    print("check: all checks passed")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run it and watch it fail**

Run: `cd /root/spotlight && python3 tests/test_check.py`
Expected: an AssertionError from `check(...)`, with stderr containing `invalid choice: 'check'`.

- [ ] **Step 3: Implement**

In `skills/spotlight/scripts/footage.py`, add above `def main():`:
```python
def frozen_samples(video, threshold=0.35):
    # luma difference between consecutive frames sampled at 10 fps (approach from motion-video-kit, MIT):
    # a sample under the threshold means nothing visible moved in that 0.1 s
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(video), "-map", "0:v:0", "-vf",
                        "fps=10,scale=320:-2,format=gray,tblend=all_mode=difference,signalstats,"
                        "metadata=print:key=lavfi.signalstats.YAVG", "-an", "-f", "null", "-"],
                       capture_output=True, text=True)
    values = [float(v) for v in re.findall(r"YAVG=([0-9.]+)", r.stderr)]
    return [round((i + 1) / 10, 2) for i, v in enumerate(values) if v < threshold]


def holds(times, step=0.1):
    # consecutive frozen samples -> [start, end] stretches
    out = []
    for t in times:
        if out and t - out[-1][1] <= step + 1e-6:
            out[-1][1] = t
        else:
            out.append([round(t - step, 2), t])
    return out


def loudness(video):
    data = json.loads(run(["ffprobe", "-v", "error", "-of", "json", "-show_streams", video]))
    if not any(s.get("codec_type") == "audio" for s in data.get("streams", [])):
        return None
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(video), "-map", "0:a:0", "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True)
    tail = r.stderr[r.stderr.rfind("Summary:"):]
    grab = lambda k: float(re.search(rf"{k}:\s+(-?[0-9.]+|-inf)", tail).group(1).replace("-inf", "-99"))
    return {"I": grab("I"), "LRA": grab("LRA"), "TP": grab("Peak")}


def check(video, end_card=0.0, target=-14.0, out=None):
    video = Path(video)
    out = Path(out) if out else video.parent
    out.mkdir(parents=True, exist_ok=True)
    data = json.loads(run(["ffprobe", "-v", "error", "-of", "json", "-count_packets", "-show_streams", video]))
    v = next(s for s in data["streams"] if s["codec_type"] == "video" and not s.get("disposition", {}).get("attached_pic"))
    a = next((s for s in data["streams"] if s["codec_type"] == "audio"), None)
    num, den = (v.get("avg_frame_rate") or "0/0").split("/")
    fps = int(num) / int(den) if int(den) else FPS
    frames = int(v["nb_read_packets"])
    dur = float(v.get("duration") or frames / fps)
    stretches = [h for h in holds(frozen_samples(video)) if h[0] < dur - end_card - 1e-6]
    stretches = [[s, min(e, dur - end_card)] for s, e in stretches]
    total = round(sum(e - s for s, e in stretches), 2)
    long_holds = [[s, e] for s, e in stretches if e - s > 0.6]
    budget = round(max(dur - end_card, 0) / 30, 2)
    loud = loudness(video)
    warnings, failures = [], []
    if abs(frames - round(dur * fps)) > 1:
        failures.append(f"frame count {frames} doesn't match {dur:.3f}s at {fps:g} fps")
    if loud:
        if loud["TP"] > -1.0:
            failures.append(f"true peak {loud['TP']} dBTP is above -1")
        if abs(loud["I"] - target) > 1.0:
            failures.append(f"integrated loudness {loud['I']} LUFS is more than 1 LU from {target}")
        if loud["LRA"] < 3:
            warnings.append(f"loudness range {loud['LRA']} LU is under 3 (fine for calm pieces, flat for energetic ones)")
    if total > budget:
        warnings.append(f"frozen {total}s, over the budget of {budget}s (1s per 30s)")
    for s, e in long_holds:
        warnings.append(f"hold without motion {s:.1f}-{e:.1f}s ({e - s:.1f}s > 0.6s)")
    sheet = out / "check-sheet.jpg"
    vf = (f"fps={24 / max(dur, 0.1)},scale=270:-2,"
          "drawtext=text='%{pts\\:hms}':x=6:y=6:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6,tile=6x4")
    run(["ffmpeg", "-y", "-v", "error", "-i", video, "-map", "0:v:0", "-vf", vf, "-frames:v", "1", "-update", "1", sheet])
    result = {"file": str(video), "duration": round(dur, 3), "fps": round(fps, 3), "frames": frames,
              "size": [v["width"], v["height"]], "video_codec": v.get("codec_name"), "audio_codec": a and a.get("codec_name"),
              "loudness": loud, "frozen": {"total": total, "holds": stretches, "long_holds": long_holds, "budget": budget},
              "warnings": warnings, "failures": failures, "sheet": str(sheet)}
    (out / "check.json").write_text(json.dumps(result, indent=2, ensure_ascii=False))
    return result
```

In `main()`, add the subcommand next to the others:
```python
    p = sub.add_parser("check", help="measure a render: frozen holds, loudness, frames, contact sheet")
    p.add_argument("video")
    p.add_argument("--end-card", type=float, default=0.0, help="seconds at the end exempt from the frozen check")
    p.add_argument("--target", type=float, default=-14.0)
    p.add_argument("--out")
```
and in the dispatch (before the final `else` that runs `encode`):
```python
        elif a.cmd == "check":
            r = check(a.video, a.end_card, a.target, a.out)
            loud = r["loudness"] or {}
            print(f"{r['duration']}s {r['frames']} frames {r['size'][0]}x{r['size'][1]} · I {loud.get('I')} LRA {loud.get('LRA')} "
                  f"TP {loud.get('TP')} · frozen {r['frozen']['total']}s (budget {r['frozen']['budget']}s) · sheet {r['sheet']}")
            for w in r["warnings"]:
                print("warning:", w)
            for f in r["failures"]:
                print("FAIL:", f)
            if r["failures"]:
                raise SystemExit(1)
```
In `prep`, add `"-update", "1",` right before `info["sheet"]` in the ffmpeg call that writes each video's contact sheet (`... "-frames:v", "1", "-update", "1", info["sheet"]]`), so a work folder with `%` in its name doesn't break it.

Update the module docstring with the line:
`  check  <video> [--end-card s] [--target LUFS] [--out dir]    frozen holds, loudness, frames, contact sheet -> check.json`

If the existing dispatch ends with a bare `else:` for `encode`, convert that to `elif a.cmd == "encode":`, so `check` doesn't fall into it.

- [ ] **Step 4: Run the tests until they pass**

Run: `cd /root/spotlight && python3 tests/test_check.py && python3 tests/test_footage.py | tail -1`
Expected: `check: all checks passed` and `footage.py: all checks passed`.

- [ ] **Step 5: Run it on a real render** (sanity check; the files stay local)

Run: `python3 skills/spotlight/scripts/footage.py check <an earlier real render>.mp4 --end-card 4.4 --out /tmp/claude-check`
Expected: warnings listing holds around 10.5–14.3 s and 38.7–41.0 s, which are the known frozen text cards. **Don't commit anything from `/tmp` or the client folders.**

- [ ] **Step 6: Commit**

```bash
cd /root/spotlight && git add skills/spotlight/scripts/footage.py tests/test_check.py && git commit -q -m "feat(footage): check — frozen holds, loudness, frame count, contact sheet

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: `footage.py track`

**Files:**
- Modify: `skills/spotlight/scripts/footage.py`: add a `track` function and subcommand
- Test: `tests/test_check.py`: add track cases

**Interfaces:**
- Consumes: `run`.
- Produces:
  - `track(audio) -> dict` with keys `duration` and `per_second` (a list of short-term LUFS floats, one per whole second); plus `tempo` and `strong_cues` when `uv` is available and the cue analyser runs; otherwise those two keys are absent.
  - CLI: `python3 footage.py track <audio>` prints `second:LUFS` pairs and, when available, tempo and strong cues.

- [ ] **Step 1: Write the failing test**: add to `tests/test_check.py`, before `print("check: all checks passed")` and inside the `with` block:

```python
        # track: per-second short-term loudness shows where the music lifts
        ff("-f", "lavfi", "-i", "aevalsrc='if(lt(t,5),0.01,0.5)*sin(2*PI*220*t)':s=48000:d=10", d / "lift.wav")
        r = subprocess.run([sys.executable, F, "track", d / "lift.wav", "--json"], capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        t = json.loads(r.stdout)
        assert len(t["per_second"]) >= 9 and t["per_second"][7] - t["per_second"][2] > 15, t
```

- [ ] **Step 2: Run it and watch it fail**

Run: `python3 tests/test_check.py`
Expected: AssertionError with stderr containing `invalid choice: 'track'`.

- [ ] **Step 3: Implement**: add above `def main():`

```python
def track(audio):
    # short-term loudness (3 s window) at every whole second: where a track is soft, where it lifts
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(audio), "-map", "0:a:0", "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    per_second, last = [], -1
    for t, s in re.findall(r"t:\s*([0-9.]+).*?S:\s*(-?[0-9.]+|-inf)", r.stderr):
        sec = int(float(t) + 1e-6)
        if sec != last and abs(float(t) - round(float(t))) < 0.051:
            per_second.append(float(s.replace("-inf", "-99")))
            last = sec
    result = {"duration": round(float(json.loads(run(["ffprobe", "-v", "error", "-of", "json", "-show_format", audio]))["format"]["duration"]), 3),
              "per_second": per_second}
    analyzer = Path(__file__).with_name("analyze_music_cues.py")
    if shutil.which("uv") and analyzer.exists():
        with tempfile.TemporaryDirectory() as tmp:
            cue = subprocess.run(["uv", "run", "--project", str(analyzer.parent), "python", str(analyzer), str(audio),
                                  "--output-json", f"{tmp}/c.json", "--output-md", f"{tmp}/c.md", "--window-duration", "60"],
                                 capture_output=True, text=True)
            if cue.returncode == 0:
                c = json.loads(Path(f"{tmp}/c.json").read_text())
                result["tempo"] = c.get("tempo")
                result["strong_cues"] = sorted(round(x["time"], 2) for x in c.get("strongCues", []) if x["time"] < 60)
    return result
```
Add `import tempfile` to the imports. In `main()`:
```python
    p = sub.add_parser("track", help="per-second loudness (+ tempo and strong cues with uv) of a music track")
    p.add_argument("audio")
    p.add_argument("--json", action="store_true")
```
and the dispatch:
```python
        elif a.cmd == "track":
            r = track(a.audio)
            if a.json:
                print(json.dumps(r))
            else:
                print(" ".join(f"{i}:{v:.0f}" for i, v in enumerate(r["per_second"])))
                if "tempo" in r:
                    print("tempo", r["tempo"], "strong cues", r["strong_cues"])
```
Docstring line: `  track  <audio> [--json]                                     per-second loudness (+ tempo, strong cues) for picking a music window`

- [ ] **Step 4: Run it until it passes**

Run: `python3 tests/test_check.py`
Expected: `check: all checks passed`. The `uv` part may take a while on first run (librosa install). If the network is unavailable it silently skips tempo; the test doesn't depend on it.

- [ ] **Step 5: Commit**

```bash
cd /root/spotlight && git add skills/spotlight/scripts/footage.py tests/test_check.py && git commit -q -m "feat(footage): track — per-second loudness, tempo and strong cues for picking a music window

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: `browser.mjs` + `site.mjs` (website input)

**Files:**
- Create: `skills/spotlight/scripts/browser.mjs`, `skills/spotlight/scripts/site.mjs`
- Modify: `skills/spotlight/scripts/capture.mjs`: use `browser.mjs`
- Create: `tests/fixtures/site/index.html`, `tests/fixtures/site/styles.css`, `tests/fixtures/site/logo.svg`, `tests/fixtures/site/fa.html`, `tests/fixtures/site/infinite.html`
- Test: `tests/test_site.sh`

**Interfaces:**
- Produces:
  - `browser.mjs` exports `async function launch()`, which returns a playwright `Browser`. It resolves `playwright-core` from `process.cwd()` and exits 2 with an install hint when it's missing. It picks Chromium from `$CHROMIUM`, `/usr/bin/chromium`, `/usr/bin/chromium-browser`, `/usr/bin/google-chrome`, the macOS Chrome/Chromium app paths, or else playwright's own browser.
  - `site.mjs`: `node site.mjs <url-or-file> <workdir> [--size WxH]` writes `<workdir>/site/`:
    - `copy.json`: `{url, title, lang, dir, description, og:{…}, headings:[{level,text}], paragraphs:[…], ctas:[{text,href}], nav:[…]}`;
    - `brand.json`: `{background, text, accent, fonts:[…], logo, images:[…]}`;
    - `page.html`;
    - `screens/01.png …` (at most 12);
    - `full.png` (height capped at 12000 px);
    - `assets/` with the logo and up to 6 large images.

    It runs with a 45 s navigation timeout and a 90 s total cap, and exits 0 with whatever it captured.

- [ ] **Step 1: Write the fixture site**

`tests/fixtures/site/styles.css`:
```css
:root { --bg: #0f172a; --ink: #f8fafc; --accent: #f59e0b; }
html, body { margin: 0; background: var(--bg); color: var(--ink); font-family: "Fixture Sans", Georgia, serif; }
header { display: flex; align-items: center; gap: 12px; padding: 16px; }
header img { width: 48px; height: 48px; }
section { min-height: 900px; padding: 40px 24px; border-top: 1px solid #334155; }
.btn { display: inline-block; background: var(--accent); color: #111; padding: 12px 20px; border-radius: 8px; text-decoration: none; }
.cookie-banner { position: fixed; left: 0; right: 0; bottom: 0; height: 160px; background: rgb(255, 0, 255); color: #000; display: flex; align-items: center; justify-content: center; gap: 16px; }
```
`tests/fixtures/site/logo.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64"><circle cx="32" cy="32" r="28" fill="#f59e0b"/></svg>
```
`tests/fixtures/site/index.html`:
```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Fixture Co — boats for cats</title>
<meta name="description" content="Fixture Co builds small boats for cats.">
<meta property="og:title" content="Fixture Co">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<header><img class="logo" src="logo.svg" alt="Fixture Co logo"><nav><a href="#how">How it works</a> <a href="#price">Pricing</a></nav></header>
<section><h1>Boats for cats</h1><p>Every cat deserves a boat.</p><a class="btn" href="#start">Get a boat</a></section>
<section id="how"><h2>How it works</h2><p>Pick a boat. We deliver it.</p></section>
<section id="price"><h2>Pricing</h2><p>Boats from one fish.</p><button class="btn">Order now</button></section>
<div class="cookie-banner" id="cookie-consent">We use cookies <button>Accept</button></div>
<script>document.querySelector('#cookie-consent button').onclick = () => document.querySelector('#cookie-consent').remove();</script>
</body>
</html>
```
`tests/fixtures/site/fa.html`:
```html
<!doctype html>
<html lang="fa" dir="rtl">
<head><meta charset="utf-8"><title>شرکت نمونه</title><link rel="stylesheet" href="styles.css"></head>
<body>
<section><h1>یک نماینده برای همه کارها</h1><p>پاسخ از همان کسی می‌آید که کار را انجام می‌دهد.</p><a class="btn" href="#c">تماس</a></section>
</body>
</html>
```
`tests/fixtures/site/infinite.html`:
```html
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Endless</title><link rel="stylesheet" href="styles.css"></head>
<body>
<h1>Endless feed</h1>
<div id="feed"></div>
<script>
  // grows forever as you scroll: site.mjs must still finish
  const feed = document.getElementById("feed");
  const more = () => { for (let i = 0; i < 5; i++) { const s = document.createElement("section"); s.textContent = "item"; feed.append(s); } };
  more(); addEventListener("scroll", () => { if (innerHeight + scrollY > document.body.scrollHeight - 1200) more(); });
</script>
</body>
</html>
```

- [ ] **Step 2: Write the failing test**: `tests/test_site.sh`

```bash
#!/usr/bin/env bash
# Self-check for site.mjs: copy, brand, screens, full page, assets; RTL text; endless pages finish.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
IM=$(command -v magick >/dev/null && echo "magick" || echo "convert")
t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
w="$t/work dir ٪ 50%"   # spaces, '%' and non-Latin in the work path
mkdir -p "$w"
npm i --silent --prefer-offline --prefix "$w" playwright-core >/dev/null 2>&1
cd "$w"
S="$ROOT/skills/spotlight/scripts/site.mjs"
node "$S" "file://$ROOT/tests/fixtures/site/index.html" . --size 1080x1920 >/dev/null
python3 - <<'PY'
import json
c = json.load(open("site/copy.json")); b = json.load(open("site/brand.json"))
assert c["title"].startswith("Fixture Co"), c["title"]
assert c["description"] == "Fixture Co builds small boats for cats.", c
assert [h["text"] for h in c["headings"]][:3] == ["Boats for cats", "How it works", "Pricing"], c["headings"]
assert {"Get a boat", "Order now"} <= {x["text"] for x in c["ctas"]}, c["ctas"]
assert b["background"].lower() == "#0f172a" and b["accent"].lower() == "#f59e0b", b
assert any("Fixture Sans" in f for f in b["fonts"]), b["fonts"]
assert b["logo"] and b["logo"].startswith("site/assets/"), b
PY
n=$(ls site/screens/*.png | wc -l); (( n >= 2 && n <= 12 )) || { echo "FAIL: $n screens"; exit 1; }
read -r W H <<< "$($IM site/screens/01.png -format '%w %h' info:)"
[[ "$W $H" == "1080 1920" ]] || { echo "FAIL: screen size $W x $H"; exit 1; }
read -r fh <<< "$($IM site/full.png -format '%h' info:)"; (( fh > 1920 )) || { echo "FAIL: full page height $fh"; exit 1; }
# the cookie banner (pure magenta) must be gone from the screens
read -r r g b <<< "$($IM site/screens/01.png -format '%[fx:int(255*p{540,1850}.r)] %[fx:int(255*p{540,1850}.g)] %[fx:int(255*p{540,1850}.b)]' info:)"
(( !(r > 240 && g < 20 && b > 240) )) || { echo "FAIL: cookie banner still on screen"; exit 1; }
# right-to-left page: exact strings, direction recorded
rm -rf site && node "$S" "file://$ROOT/tests/fixtures/site/fa.html" . >/dev/null
python3 -c "import json; c=json.load(open('site/copy.json')); assert c['dir']=='rtl' and c['lang']=='fa' and c['headings'][0]['text']=='یک نماینده برای همه کارها', c"
# an endless page still finishes, within the caps
rm -rf site && timeout 150 node "$S" "file://$ROOT/tests/fixtures/site/infinite.html" . >/dev/null
n=$(ls site/screens/*.png | wc -l); (( n <= 12 )) || { echo "FAIL: endless page gave $n screens"; exit 1; }
read -r fh <<< "$($IM site/full.png -format '%h' info:)"; (( fh <= 12000 )) || { echo "FAIL: full page $fh px"; exit 1; }
echo "site.mjs: ok"
```

- [ ] **Step 3: Run it and watch it fail**

Run: `cd /root/spotlight && chmod +x tests/test_site.sh && bash tests/test_site.sh`
Expected: a failure with `Cannot find module …/site.mjs`.

- [ ] **Step 4: Implement `browser.mjs`**

```js
// Shared browser launch for spotlight scripts. playwright-core is installed per run in the work folder
// (npm i --prefix . playwright-core), so it resolves from the current directory.
import { createRequire } from "node:module";
import { existsSync } from "node:fs";

export async function launch(extraArgs = []) {
  const require = createRequire(process.cwd() + "/");
  let chromium;
  try {
    ({ chromium } = require("playwright-core"));
  } catch {
    console.error(`playwright-core isn't installed in ${process.cwd()}; run: npm i --prefix . playwright-core`);
    process.exit(2);
  }
  const executablePath = process.env.CHROMIUM || [
    "/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/Applications/Chromium.app/Contents/MacOS/Chromium",
  ].find(existsSync);  // undefined: playwright's own downloaded browser
  return chromium.launch({
    executablePath,
    args: ["--no-sandbox", "--force-color-profile=srgb", "--font-render-hinting=none", "--disable-gpu", ...extraArgs],
  });
}
```

In `capture.mjs`, replace the `createRequire` / `require("playwright-core")` try-block **and** the `executablePath`/`chromium.launch(...)` lines with:
```js
import { launch } from "./browser.mjs";
```
(at the top with the other imports) and
```js
const browser = await launch();
```
Then remove the now-unused `createRequire` and `existsSync` imports. Run `node --check skills/spotlight/scripts/capture.mjs && bash tests/test_capture.sh`. Expected: `capture.mjs: ok`.

- [ ] **Step 5: Implement `site.mjs`**

```js
// Capture a website as source material: node site.mjs <url-or-file://> <workdir> [--size WxH]
// Writes <workdir>/site/: copy.json, brand.json, page.html, screens/NN.png (output aspect), full.png, assets/.
// Best effort and bounded: 45 s to load, 90 s in total, at most 12 screens, full page capped at 12000 px.
import { mkdirSync, writeFileSync, copyFileSync, existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { launch } from "./browser.mjs";

const [url, workdir = ".", ...rest] = process.argv.slice(2);
if (!url) { console.error("usage: site.mjs <url-or-file://> <workdir> [--size WxH]"); process.exit(2); }
const size = (rest[rest.indexOf("--size") + 1] || "1080x1920").split("x").map(Number);
const [W, H] = rest.includes("--size") ? size : [1080, 1920];
const portrait = H > W;
// vertical renders the mobile layout (540 css px at 2x); landscape and square render desktop at 1x
const viewport = portrait ? { width: W / 2, height: H / 2 } : { width: W, height: H };
const scale = portrait ? 2 : 1;
const out = path.join(workdir, "site");
mkdirSync(path.join(out, "screens"), { recursive: true });
mkdirSync(path.join(out, "assets"), { recursive: true });
const deadline = Date.now() + 90_000;

const browser = await launch();
const page = await browser.newPage({ viewport, deviceScaleFactor: scale });
try { await page.goto(url, { waitUntil: "networkidle", timeout: 45_000 }); } catch { /* keep what loaded */ }

// dismiss consent banners: click an accepting button inside a cookie/consent element, else hide fixed overlays
await page.evaluate(() => {
  const words = /accept|agree|allow|got it|^ok$|قبول|موافق|پذیرفتن|أوافق/i;
  const boxes = [...document.querySelectorAll("[id*=cookie i],[class*=cookie i],[id*=consent i],[class*=consent i],[class*=gdpr i]")];
  for (const box of boxes) {
    const btn = [...box.querySelectorAll("button,a,[role=button]")].find((b) => words.test(b.textContent.trim()));
    if (btn) btn.click();
  }
  for (const el of document.querySelectorAll("body *")) {
    const s = getComputedStyle(el);
    if ((s.position === "fixed" || s.position === "sticky") && /cookie|consent|gdpr|newsletter|popup|modal/i.test(el.id + " " + el.className)) {
      el.style.display = "none";
    }
  }
});

// scroll once through the page so lazy and animate-on-scroll content appears (bounded for endless pages)
for (let y = 0, i = 0; i < 40 && Date.now() < deadline; i++, y += viewport.height) {
  const h = await page.evaluate((y) => { scrollTo(0, y); return document.body.scrollHeight; }, y);
  await page.waitForTimeout(150);
  if (y > h || y > 12000 / scale) break;
}
await page.evaluate(() => scrollTo(0, 0));

const data = await page.evaluate(() => {
  const txt = (e) => (e.innerText || e.textContent || "").replace(/\s+/g, " ").trim();
  const meta = (n) => document.querySelector(`meta[name="${n}"],meta[property="${n}"]`)?.content || "";
  const og = {};
  for (const m of document.querySelectorAll('meta[property^="og:"]')) og[m.getAttribute("property").slice(3)] = m.content;
  const ctas = [...document.querySelectorAll("button,[role=button],a[class*=btn i],a[class*=button i],a[class*=cta i]")]
    .map((e) => ({ text: txt(e), href: e.getAttribute("href") || "" })).filter((c) => c.text && c.text.length < 60);
  const hex = (c) => {
    const m = c.match(/\d+(\.\d+)?/g); if (!m) return null;
    const [r, g, b, a = 1] = m.map(Number); if (a === 0) return null;
    return "#" + [r, g, b].map((v) => Math.round(v).toString(16).padStart(2, "0")).join("");
  };
  const bodyBg = hex(getComputedStyle(document.body).backgroundColor) || hex(getComputedStyle(document.documentElement).backgroundColor) || "#ffffff";
  const counts = {};
  for (const e of document.querySelectorAll("a,button,[class*=btn i],[class*=accent i]")) {
    for (const p of ["backgroundColor", "color", "borderColor"]) {
      const c = hex(getComputedStyle(e)[p]);
      if (c && c !== bodyBg && c !== "#000000" && c !== "#ffffff") counts[c] = (counts[c] || 0) + 1;
    }
  }
  const accent = Object.entries(counts).sort((a, b) => b[1] - a[1])[0]?.[0] || null;
  const fonts = [...new Set([document.body, document.querySelector("h1"), document.querySelector("h2")].filter(Boolean)
    .map((e) => getComputedStyle(e).fontFamily))];
  const logo = [...document.querySelectorAll("img")].find((i) => /logo/i.test(i.alt + i.className + i.src + (i.closest("header") ? " header" : "")))?.src
    || document.querySelector('link[rel*="icon"]')?.href || null;
  const images = [...document.images].filter((i) => i.naturalWidth >= 400).sort((a, b) => b.naturalWidth * b.naturalHeight - a.naturalWidth * a.naturalHeight)
    .slice(0, 6).map((i) => i.src);
  return {
    copy: {
      url: location.href, title: document.title, lang: document.documentElement.lang || "", dir: document.documentElement.dir || getComputedStyle(document.documentElement).direction,
      description: meta("description"), og,
      headings: [...document.querySelectorAll("h1,h2,h3")].map((h) => ({ level: +h.tagName[1], text: txt(h) })).filter((h) => h.text),
      paragraphs: [...document.querySelectorAll("p")].map(txt).filter(Boolean).slice(0, 40),
      ctas, nav: [...document.querySelectorAll("nav a")].map((a) => ({ text: txt(a), href: a.getAttribute("href") || "" })),
    },
    brand: { background: bodyBg, text: hex(getComputedStyle(document.body).color), accent, fonts, logo, images },
  };
});

// download (or copy, for file://) the logo and the big images into site/assets/
async function fetchAsset(src, name) {
  try {
    const ext = (path.extname(new URL(src).pathname) || ".png").slice(0, 6);
    const dest = path.join(out, "assets", name + ext);
    if (src.startsWith("file://")) { const p = fileURLToPath(src); if (existsSync(p)) copyFileSync(p, dest); else return null; }
    else { const r = await page.request.get(src, { timeout: 15_000 }); if (!r.ok()) return null; writeFileSync(dest, await r.body()); }
    return path.join("site", "assets", name + ext);
  } catch { return null; }
}
data.brand.logo = data.brand.logo ? await fetchAsset(data.brand.logo, "logo") : null;
data.brand.images = (await Promise.all(data.brand.images.map((s, i) => fetchAsset(s, `image-${i + 1}`)))).filter(Boolean);

writeFileSync(path.join(out, "copy.json"), JSON.stringify(data.copy, null, 2));
writeFileSync(path.join(out, "brand.json"), JSON.stringify(data.brand, null, 2));
writeFileSync(path.join(out, "page.html"), await page.content());

// screens at the output aspect, one per viewport of scroll, at most 12
const height = await page.evaluate(() => document.body.scrollHeight);
for (let i = 0, y = 0; i < 12 && y < height && Date.now() < deadline; i++, y += viewport.height) {
  await page.evaluate((y) => scrollTo(0, y), y);
  await page.waitForTimeout(120);
  await page.screenshot({ path: path.join(out, "screens", String(i + 1).padStart(2, "0") + ".png") });
}
await page.evaluate(() => scrollTo(0, 0));
const clipH = Math.min(height, Math.floor(12000 / scale));
await page.screenshot({ path: path.join(out, "full.png"), fullPage: false, clip: { x: 0, y: 0, width: viewport.width, height: clipH } })
  .catch(() => page.screenshot({ path: path.join(out, "full.png"), fullPage: true }));
await browser.close();
console.log(`site captured: ${data.copy.headings.length} headings, ${data.copy.ctas.length} CTAs -> ${out}`);
```
Note: a screenshot with `clip` taller than the viewport needs `fullPage` semantics in some playwright versions. If `full.png` comes out at viewport height, temporarily set the viewport to the clip height (`await page.setViewportSize({ width: viewport.width, height: clipH })`), take the screenshot, then restore it. The test's `full page height` assertion tells you which case you're in.

- [ ] **Step 6: Run the tests until they pass**

Run: `cd /root/spotlight && node --check skills/spotlight/scripts/site.mjs && bash tests/test_site.sh && bash tests/test_capture.sh && bash tests/test_kit.sh | tail -1`
Expected: `site.mjs: ok`, `capture.mjs: ok`, `kit: ok`. If a site assertion fails, fix `site.mjs`, not the test, unless the test contradicts the Interfaces block.

- [ ] **Step 7: Commit**

```bash
cd /root/spotlight && chmod +x tests/test_site.sh && git add skills/spotlight/scripts tests && git commit -q -m "feat: site.mjs — capture a website's copy, brand, screens and assets; shared browser launch

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: Kit: `web` shots and text cards that never freeze

**Files:**
- Modify: `skills/spotlight/kit/kit.js` (`drawShot`, the header comment), `skills/spotlight/kit/scene.html` (add `#web`)
- Test: `tests/test_kit.sh`: add the web-shot and card-motion cases

**Interfaces:**
- Consumes: `footage.py check` (Task 2) and `encode`; `capture.mjs`.
- Produces two new shot forms:
  - **`{ a, b, web: "site/full.png", scroll: [y0, y1] }`**: the image is drawn at the output width and scrolled from `y0` to `y1` (output pixels) with `inOutCubic` easing.
  - **`{ a, b, still, filter, drift: [x0, x1] }`**: a horizontal drift in percent of width. **Default for stills with a `filter`** (text-card backdrops): `push: [1.10, 1.30]` and `drift: [-4, 4]`, unless overridden.

- [ ] **Step 1: Write the failing tests**: add to `tests/test_kit.sh`, before `echo "kit: ok"`:

```bash
# web shot: a tall page scrolls from y0 to y1 at the output width
k="$t/web"; mkdir -p "$k"; cp "$ROOT/skills/spotlight/kit/scene.html" "$ROOT/skills/spotlight/kit/kit.js" "$k/"; : > "$k/fonts.css"
ln -s "$t/node_modules" "$k/node_modules"
$IM -size 320x500 xc:red -size 320x1000 xc:gray50 -size 320x500 xc:blue -append "$k/full.png"
echo 'window.SPOTLIGHT = { width: 320, height: 568, duration: 1, shots: [ { a: 0, b: 1, web: "full.png", scroll: [0, 1432] } ] };' > "$k/timeline.js"
(cd "$k" && node "$ROOT/skills/spotlight/scripts/capture.mjs" stills 0 0.99 >/dev/null)
read -r r g b <<< "$(px "$k/check/t0.00.png" 160 100)"; (( r > 200 && b < 60 )) || { echo "FAIL: web shot top not red ($r $g $b)"; exit 1; }
read -r r g b <<< "$(px "$k/check/t0.99.png" 160 500)"; (( b > 200 && r < 60 )) || { echo "FAIL: web shot not scrolled to the bottom ($r $g $b)"; exit 1; }

# text card over a blurred still: never reads as frozen (no hold > 0.6 s), with grain off so it can't cheat
c="$t/card"; mkdir -p "$c"; cp "$ROOT/skills/spotlight/kit/scene.html" "$ROOT/skills/spotlight/kit/kit.js" "$c/"; : > "$c/fonts.css"
ln -s "$t/node_modules" "$c/node_modules"
ffmpeg -v error -y -f lavfi -i "testsrc2=size=640x1136" -frames:v 1 "$c/bg.jpg"
cat > "$c/timeline.js" <<'JS'
window.SPOTLIGHT = { width: 320, height: 568, duration: 4, grain: 0,
  shots: [ { a: 0, b: 4, still: "bg.jpg", filter: "blur(16px) brightness(.42)" } ] };
JS
python3 - "$c/scene.html" <<'PY'
import sys; p = sys.argv[1]; s = open(p).read()
card = '<div class="cap mid" data-a="0.2" data-b="3.9"><div class="rule"></div><div class="row" data-at="0.3"><span class="n">01</span><span class="t">First</span></div><div class="row" data-at="0.5"><span class="n">02</span><span class="t">Second</span></div></div>'
open(p, "w").write(s.replace('<div id="end">', card + '\n  <div id="end">'))
PY
(cd "$c" && node "$ROOT/skills/spotlight/scripts/capture.mjs" frames >/dev/null && python3 "$ROOT/skills/spotlight/scripts/footage.py" encode out none card.mp4 >/dev/null)
python3 "$ROOT/skills/spotlight/scripts/footage.py" check "$c/card.mp4" --out "$c/chk" >/dev/null || true
python3 -c "import json,sys; r=json.load(open('$c/chk/check.json')); h=r['frozen']['long_holds']; sys.exit(0 if not h else print('FAIL: card holds', h) or 1)"
```

- [ ] **Step 2: Run them and watch them fail**

Run: `bash tests/test_kit.sh`
Expected: `FAIL: web shot top not red`. The kit doesn't know `web` yet, so it shows a broken or empty frame. Once web is implemented, the card case fails with `FAIL: card holds [[…]]`: the current still push (1.0→1.025) is too slow to count as motion.

- [ ] **Step 3: Implement**

In `scene.html`, add `<img id="web" alt="">` right after `<img id="panel" alt="">`, and this CSS inside `<style>`:
```css
  #web { position: absolute; left: 0; top: 0; width: 100%; height: auto; opacity: 0; will-change: transform; }
```
In `kit.js`, add `web` to the lookups: `const foot = $("#foot"), panel = $("#panel"), web = $("#web"), grain = $("#grain");`. Then replace the whole `async function drawShot(t) { … }` with:
```js
  async function drawShot(t) {
    const s = P.shots.find((s) => t >= s.a && t < s.b) || P.shots[P.shots.length - 1];
    const p = clamp((t - s.a) / (s.b - s.a));
    const e = inOutCubic(p);
    const src = s.clip ? `${s.clip}/${String(frameAt(s, t)).padStart(5, "0")}.jpg` : (s.still || s.web);
    const card = Boolean(s.filter && s.still);  // a text-card backdrop: keep it visibly moving
    const [from, to] = s.push || (card ? [1.10, 1.30] : [1, 1.025]);
    const [dx0, dx1] = s.drift || (card ? [-4, 4] : [0, 0]);
    const scale = from + (to - from) * e, dx = dx0 + (dx1 - dx0) * e;
    if (s.web) {
      // the real page, scrolled: drawn at the output width, moving from scroll[0] to scroll[1] (output px)
      await show(web, src);
      const [y0, y1] = s.scroll || [0, 0];
      Object.assign(web.style, { opacity: 1, transform: `translateY(${-(y0 + (y1 - y0) * e)}px)` });
      foot.style.opacity = 0;
      panel.style.opacity = 0;
    } else if (s.panel) {
      await Promise.all([show(foot, src), show(panel, src)]);
      const fit = Math.min(P.width / panel.naturalWidth, P.height / panel.naturalHeight);
      const w = panel.naturalWidth * fit, h = panel.naturalHeight * fit;
      Object.assign(panel.style, {
        width: `${w}px`, height: `${h}px`, left: `${(P.width - w) / 2}px`, top: `${(P.height - h) / 2}px`,
        opacity: 1, transform: `scale(${scale})`, filter: s.grade || "none",
      });
      Object.assign(foot.style, { opacity: 1, filter: "blur(26px) brightness(.5)", transform: "scale(1.25)", transformOrigin: "50% 50%" });
      web.style.opacity = 0;
    } else {
      await show(foot, src);
      panel.style.opacity = 0;
      web.style.opacity = 0;
      Object.assign(foot.style, {
        opacity: 1, filter: [s.filter, s.grade].filter(Boolean).join(" ") || "none",
        transformOrigin: s.origin || "50% 50%", transform: `translateX(${dx}%) scale(${scale})`,
      });
    }
    // grain moves every frame but is still a function of t
    const f = Math.floor(t * FPS + 1e-6);
    grain.style.opacity = s.grain ?? P.grain ?? 0;
    grain.style.backgroundPosition = `${(f * 73) % 256}px ${(f * 151) % 256}px`;
  }
```
Every branch sets every style it touches, so a frame never depends on the one rendered before it (four pages capture in parallel).

In the header comment, add these two lines after the `still:` line:
```
//   web: "site/full.png", scroll: [y0, y1]   a captured page drawn at the output width and scrolled (output px)
//   drift: [x0, x1]        horizontal drift in % of width (stills with a `filter` default to push [1.10, 1.30], drift [-4, 4])
```

- [ ] **Step 4: Run the tests until they pass**

Run: `bash tests/test_kit.sh`
Expected: `kit: ok`. If the card still reports holds, raise the default text-card motion (for example `push: [1.10, 1.36]`, `drift: [-6, 6]`) until the card has no hold over 0.6 s. Grain must stay off, so the test proves real motion. Record the final numbers in the header comment.

- [ ] **Step 5: Commit**

```bash
cd /root/spotlight && git add skills/spotlight/kit tests/test_kit.sh && git commit -q -m "feat(kit): web shots (scrolled site captures) and text-card backdrops that never read as frozen

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: SKILL.md, mode references, critic and quality bar, docs consistency test

**Files:**
- Rewrite: `skills/spotlight/SKILL.md`
- Create: `skills/spotlight/references/brag.md`, `promo.md`, `explain.md`, `critic.md`, `quality-bar.md`
- Test: `tests/test_docs.py`

**Interfaces:**
- Consumes:
  - script CLIs: `footage.py prep|shot|encode|check|track`, `capture.mjs stills|frames`, `site.mjs <url> <workdir> [--size WxH]`;
  - kit shot fields: `clip n still web scroll panel push origin filter drift grade grain`;
  - the `window.SPOTLIGHT` keys: `width height duration end grain fonts shots`.
- Produces: the skill text the agent follows. `test_docs.py` pins it to the scripts.

- [ ] **Step 1: Write the failing test**: `tests/test_docs.py`

```python
#!/usr/bin/env python3
"""The skill text is the product: every command, shot field and file it names must exist.

Run: python3 tests/test_docs.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SK = ROOT / "skills/spotlight"


def main():
    skill = (SK / "SKILL.md").read_text()
    refs = {p.name: p.read_text() for p in (SK / "references").glob("*.md")}
    every = skill + "\n".join(refs.values())
    fm = re.match(r"---\nname: (\S+)\ndescription: (.+?)\n---\n", skill, re.S)
    assert fm and fm.group(1) == "spotlight", "frontmatter name"
    for word in ("brag", "promo", "explain"):
        assert word in fm.group(2).lower(), f"description should mention {word}"
    for name in re.findall(r"references/([a-z-]+\.md)", every):
        assert (SK / "references" / name).exists(), f"missing references/{name}"
    assert {"brag.md", "promo.md", "explain.md", "critic.md", "quality-bar.md"} <= set(refs), sorted(refs)
    footage = (SK / "scripts/footage.py").read_text()
    for cmd in set(re.findall(r"\$F (\w+)", every)):
        assert f'add_parser("{cmd}"' in footage, f"SKILL names footage.py {cmd}, which doesn't exist"
    for script in set(re.findall(r"scripts/([a-z]+\.(?:mjs|py|sh))", every)):
        assert (SK / "scripts" / script).exists(), f"missing scripts/{script}"
    kit = (SK / "kit/kit.js").read_text()
    for field in ("clip", "still", "web", "scroll", "panel", "push", "origin", "filter", "drift", "grade", "grain"):
        assert re.search(rf"\b{field}\b", kit), f"kit.js doesn't document {field}"
        assert f"`{field}`" in every or f"{field}:" in every, f"the skill never explains {field}"
    for out in ("video.mp4", "poster.jpg", "caption.txt", "plan.md", "sources.md", "spotlight-output"):
        assert out in skill, f"SKILL.md should name the deliverable {out}"
    for stale in ("promo-output", "/promo ", "window.PROMO", "skills/promo", "PROMO_SRGB_ICC"):
        assert stale not in every, f"stale reference: {stale}"
    print("docs: all checks passed")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run it and watch it fail**

Run: `cd /root/spotlight && python3 tests/test_docs.py`
Expected: `AssertionError: frontmatter name` (the copied SKILL.md still says `promo`).

- [ ] **Step 3: Write the references**

**`references/promo.md`**: footage-first work. Build it from `/root/promo/skills/promo/SKILL.md`. Copy these sections verbatim, then make the edits listed after them:
- under a top heading `# promo mode: real footage first`, the whole **`## 1. Inventory and look`** section, renamed `## Inventory and look`;
- from **`## 2. Plan`**, the **Shape** paragraph and the "Not enough material" paragraph;
- the **`## Tones`** table;
- under **`## 3. Build`**, the **`### Footage`** subsection.

Edits:
- Replace every `<out>` with `spotlight-output`.
- Change "`promo.jpg`" to "`poster.jpg`" and "`promo-plan.md`" to "`plan.md`".
- Drop the sentence about the bridge's `--image`; it lives in SKILL.md now.
- Add this paragraph after **Shape**:
  "**Everyone on screen when asked.** List every distinct person in the footage (by appearance, never by guessed name) and give each a clear, sharp moment, using a wide panel shot for group scenes so nobody is cropped out. Pre-edited clips (light leaks, dissolves) are usable only after their transitions; check the first frame after the cut."

**`references/brag.md`:**
```markdown
# brag mode: a launch video for something you built

Input is a code project or a website. You built it; now brag. Adapted from /brag (MIT).

## Inspect
- **Project:** read the main page, styles (exact colours and fonts), README, routes and key components. Find the 2–3 beats of the product **in use**: entry → key action → result. Import or render the project's real components, styles, fonts and images instead of rebuilding them.
- **Website:** run `node <skill-dir>/scripts/site.mjs <url> work --size <W>x<H>`. Use `site/copy.json` for words, `site/brand.json` for colours, fonts and logo, and `site/screens/` and `site/full.png` for the page itself. A `web` shot scrolls the real page. Reuse its markup and assets over flat screenshots whenever the shot needs interaction.
- Answer: what is it, who is it for, what does it do for them, what sets it apart, the most impressive or funniest true claim, the visual hook, the one-line caption.

## Shape
Hook (2–3 s) → reveal (2–4 s) → 2–3 sharp highlights → punchline / CTA (2–4 s). A starting shape, not a template. 15–25 s; 18–22 is the sweet spot.

## Laws
- **The hook is everything.** Plan the first 2 seconds first.
- **Show the thing.** Real UI, copy, images and flows from the source, never abstract filler. Small illustrative UI text in a simulated flow is fine (a filename, an "Exported" toast); invented claims, numbers or testimonials are not.
- **Make it alive.** Things that appear one by one, simulated clicks, swipes and typing beat static slides.
- **Funny earns its place.** Humour comes from the project's own absurdity.
- **No generic SaaS language** ("streamline your workflow" is banned).

## Tones
| Tone | Feel | Pacing / transitions |
|---|---|---|
| `default` | Punchy, playful, clean | 4–5 scenes; soft transitions |
| `polished` | Serious, elegant, restrained | 3–4 scenes, long holds; soft fades |
| `yc-parody` | Deadpan startup launch, played straight | 4–5 scenes, one claim each; hard cuts |
| `chaotic` | FAST, LOUD, ALL CAPS | 6–8 scenes, some under 2 s; flash/zoom cuts |
| `deadpan` | Calm, dry, nothing is a joke | 3–4 scenes, big empty space; slow fades |
| `cinematic` | Trailer-scale, epic claims | 4–5 scenes, big type; dramatic wipes |
| `app-store` | Clean feature cards | 4–6 scenes; smooth slides |
```

**`references/explain.md`:**
```markdown
# explain mode: a presentation as a video

Input is a topic, an argument, data files (`*.csv`, `*.json`), and optionally a website or footage. Output is a 60–180 s explainer (default 90 s, landscape) that someone can play in a meeting or post.

## Brief
Write the one sentence the viewer should leave with, the audience, and 3–5 claims that support it. **Every claim has a source in `sources.md`:** the description you were given, a file, a page of the site, or a line in the data. A number on screen must be in the data exactly as shown.

## Shape
Hook question (≤ 6 s) → 3–5 sections, each a claim with one piece of evidence → the takeaway → CTA or next step. Give each section a short chapter card (number + 2–5 words). Sections run 12–30 s. Vary the evidence: a site page (`web` shot), footage, a big-number card, a list card, a quote from the source.

## Evidence on screen
- **Numbers:** a big-number card shows the value verbatim from the data with its unit and source line ("Source: survey.csv, 2025"). Until the chart layer arrives (phase 3), comparisons are 2–4 big numbers side by side, never a hand-drawn chart.
- **Lists:** at most 5 rows, each ≤ 5 words, equal spacing, aligned left edges.
- **Pages:** scroll the real page (`web`) to the part that proves the claim, and hold it ≥ 1.5 s with a slow push.
- **Narration** (`--voice`, phase 2) carries the argument; until then, on-screen text carries it. Keep reading time ≥ 0.3 s per word.

## Tones
| Tone | Feel | Pacing |
|---|---|---|
| `clear` (default) | Calm, plain, confident | Sections 15–25 s; soft cuts; one idea per screen |
| `documentary` | Footage-led, measured | Longer holds on footage; captions low; slow pushes |
| `keynote` | Big type, bold reveals | Short punchy sections; hard cuts on the music |
```

**`references/critic.md`** (adapted from echris6/motion-video-kit, MIT):
```markdown
# Critic loop

Adapted from motion-video-kit's Gauntlet (MIT). **The builder never grades its own work.** If you can start a fresh sub-agent, use it. Give it only the rendered video, the brief, `check.json` and `check-sheet.jpg`, and, from round 2, the previous critic's report. Never your reasoning or a list of what you think you fixed. Without sub-agents, do the same review yourself on freshly extracted frames, not on stills you chose earlier.

Round 1 is the full-film critic. Fix the 3–6 highest-impact items, re-render, run `check`, then round 2 is a **new** verification critic. Stop at SHIP, when the remaining items are cosmetic, or after 3 rounds.

## Full-film critic prompt
You are an independent, harsh critic. You did NOT make this; judge rendered pixels and measured audio, not intentions.
Video: <path> (<duration> s, <W>x<H>, 30 fps). It is a <brag | promo | explain> video for <subject>; its one message: <message>. Brief: <path to brief.md>. Measurements: <path to check.json>, contact sheet <path to check-sheet.jpg>.
Method: extract frames yourself with ffmpeg (a contact sheet every 0.25 s, plus every frame in the 0.5 s around each cut at <cut times>). Read the measurements.
Report (≤ 700 words), also written to <work/critic-N.md>:
1. Per section: time range, what's on screen, problems ranked (holds, empty frame, collisions, text over signage or faces, unreadable text, wrong crops, dark or muddy frames, third-party logos, anything not supported by the brief or sources).
2. Message: on mute, can a stranger say what it is and what to do next? Is every claim on screen in `sources.md`?
3. Sound: does audio land on the cuts; does the music fade before the end card lands?
4. The top 6 changes by impact, concrete and implementable. End with SHIP or ONE MORE PASS.

## Verification critic prompt
You are an independent critic; you did NOT make this. New video: <path>. The previous report: <path>. For each of its top changes and defects give FIXED / PARTLY / STILL PRESENT with timestamps, then list NEW defects (glitch frames, overlaps, clipped text, regressions). End with SHIP or ONE MORE PASS (at most 3 fixes). Write it to <work/critic-N.md>.
```

**`references/quality-bar.md`:**
```markdown
# Quality bar

A video ships only when these hold. `footage.py check` measures the first block; critics judge the rest.

## Measured
| Check | Target |
|---|---|
| Frozen time | ≤ 1 s per 30 s; no hold over 0.6 s without motion, except the end card (`--end-card`) |
| Loudness | −14 LUFS integrated (±1); true peak ≤ −1.5 dBTP; loudness range ≥ 3 LU for energetic pieces |
| Frames | Exactly duration × 30 |

## Visual
- Frame 0 is a finished composition (never a half-entered word).
- No empty frames, no text collisions (also mid-transition), no captions over signage, logos or faces.
- Lists: equal spacing, aligned left edges (right edges in RTL).
- The lead subject fills most of the frame in feature shots; crop with `cx` or use `panel` for other-aspect media.
- Openers are bright and clear unless the brand says otherwise.
- Every person the user asked to feature has a clear moment; third-party brands stay out of frame.

## Message (on mute)
- A first-time viewer can say what it is and the one next action.
- Every claim on screen is in `sources.md`, or clearly labelled as illustration.
- The CTA is readable at phone size for ≥ 1.5 s.
```

- [ ] **Step 4: Rewrite `SKILL.md`**

Write `skills/spotlight/SKILL.md`. Carry over these sections from the current (copied) file **verbatim** unless an edit is listed. In each carried section, replace `<out>` with `spotlight-output`, `promo.jpg` with `poster.jpg`, and `promo.mp4` with `video.mp4`.
- "### The page" (add to the shot list sentence: `` `web: "site/full.png", scroll: [y0, y1]` `` for a scrolled site capture and `` `drift: [x0, x1]` `` for a sideways drift in % of width, and say text-card backdrops get push and drift by default);
- "### Text in any language";
- "### Brand";
- "### AI images (codex bridge)";
- "### Check before the full render" (add a first sentence: "Run `python3 $F check work/draft.mp4 --end-card <s>` on a quick draft render; fix every hold it lists before the full render.");
- "### Encode";
- "## Rules" (rename "Short." to "Length." and give the mode ranges: brag 15–25 s, promo 15–30 s, explain 60–180 s).

New text for everything else:
````markdown
---
name: spotlight
description: Turn a website, a code project, footage or photos, and a description into a short video that brags (a launch), promotes a point (a promo), or explains a topic (a presentation as a video), with music, on-screen text in any language, a poster and a caption. Use when someone says "/spotlight", "make a video about this", "launch video", "brag about this", "promo from these photos/videos", "reel from this footage", "explainer video", "presentation video", or points at a site, folder or topic and wants a video.
---

# spotlight

You make the whole video yourself: find the story, pick the material, set the type, mix the sound, render, check, and have it critiqued. The scripts and the render kit handle everything with sharp edges.

`<skill-dir>` is the folder holding this SKILL.md. Below, `F=<skill-dir>/scripts/footage.py`.

Usage: `/spotlight [url | folder | files | project | "description"]… [options]`. Flags or plain language.

| Option | Default |
|---|---|
| `--mode brag\|promo\|explain` | inferred (table below) |
| `--tone <preset or freeform>` | inferred per mode |
| `--format vertical\|landscape\|square` | vertical for brag/promo, landscape for explain; 1080×1920 / 1920×1080 / 1080×1080, 30 fps |
| `--duration <s>` | brag 20, promo 20, explain 90 |
| `--lang <code>` | from the brief → the site's `lang` → text in the footage → ask |
| `--music <file>\|none` | an audio file in the inputs, otherwise ask for a track or render with a silent track (a bundled library arrives in phase 2) |
| `--no-ai` | AI images on when the bridge works |

Deliverables go to `spotlight-output/` (timestamped `spotlight-output-YYYY-MM-DD-HHmmss/` if it exists): `video.mp4` (poster embedded as cover art), `poster.jpg`, `caption.txt`, `plan.md`, `sources.md`, and `work/`. **Never modify, move or delete anything in the user's inputs.** Before anything else run `bash <skill-dir>/scripts/doctor.sh`; if it reports a missing required tool, say which and stop.

## Modes
| Mode | When | Read |
|---|---|---|
| `brag` | a code project or a website, nothing else | `references/brag.md` |
| `promo` | footage or photos are the main material | `references/promo.md` |
| `explain` | a topic or argument, data files, or the user says presentation/explainer | `references/explain.md` |
Inputs mix freely: a promo can quote the brand's site, an explainer can use footage. Read exactly one mode file, plus `references/quality-bar.md` and `references/critic.md` when you reach those steps.

## 1. Gather
- **Media:** `python3 $F prep spotlight-output/work <files…>` → manifest, upright sRGB stills, contact sheets (see the mode file).
- **Website:** in `spotlight-output/work`, `npm i --prefix . playwright-core`, then `node <skill-dir>/scripts/site.mjs <url> . --size <W>x<H>` → `site/copy.json`, `site/brand.json`, `site/screens/`, `site/full.png`, `site/assets/`.
- **Project:** read the code the way `references/brag.md` describes.
- **Data:** read `*.csv` / `*.json` inputs; numbers on screen come only from them.

## 2. Brief → `work/brief.md`
What it is, who it's for, the one message, the one action (CTA), the facts you'll show **with their source** (brief, site page, footage file, data file), and the don'ts. If the name, the CTA or the language is still unknown, ask **one** question listing everything missing. Never guess a phone number, a price or an address.

## 3. Plan → `plan.md`
The angle, the hook, and a shot or section list. Each entry has its source (copy the path from the manifest or site files), in/out points or motion, its on-screen text (verbatim from the sources), its duration and its transition. Add the music and the cue times you'll cut on, plus the AI assets table. Durations must add up to the target. Write `sources.md` alongside: every line of on-screen text and every number → where it came from, plus the AI ledger (file, prompt, purpose, shot).

## 4. Build
<carried sections: The page, Text in any language, Brand, AI images (codex bridge)>

## 5. Sound
Until the phase 2 sound layer lands, use the user's track. Pick its window with `python3 $F track <track>`: it prints per-second loudness, plus tempo and strong cues when `uv` is available. Cut on its beats for energetic tones, and let big moments land near strong cues. Keep useful live sound from clips about 15 dB under the music, with 50–100 ms fades. Mix to `work/mix.wav`; the fade-out must end by the last frame, and the music must not fade before the end card lands.

## 6. Capture, encode, check
<carried sections: Check before the full render, Encode>
Then run `python3 $F check spotlight-output/video.mp4 --end-card <end-card seconds>` and fix every failure and every hold it lists.

## 7. Critic
Follow `references/critic.md`: a fresh critic reviews the actual render, you fix, a new critic verifies. At most 3 rounds.

## 8. Deliver
- **`poster.jpg`:** the strongest settled frame, embedded as cover art (`encode --poster`), never copied over frame 0.
- **`caption.txt`:** in the video's language, 1–3 sentences plus the CTA, optional hashtags, and a short AI-illustration label if any AI image is used.
- **`plan.md`, `sources.md`, `work/`** stay.
- **Tell the user:** where the files are, the angle in one sentence, the `check` numbers, the critic's verdict, and which shots are AI. Offer a re-cut, another tone or another format (re-using `work/`).

<carried section: Rules>
````
In the final file, replace each `<carried …>` line with the carried section text (edited as listed). No angle-bracket placeholders may remain.

- [ ] **Step 5: Run the docs test until it passes**

Run: `cd /root/spotlight && python3 tests/test_docs.py`
Expected: `docs: all checks passed`. Each failure names the stale or missing reference; fix the text, not the test.

- [ ] **Step 6: Commit**

```bash
cd /root/spotlight && git add skills/spotlight tests/test_docs.py && git commit -q -m "docs(skill): spotlight SKILL.md with brag/promo/explain modes, critic loop, quality bar, sources.md; docs test

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: `doctor.sh`

**Files:**
- Create: `skills/spotlight/scripts/doctor.sh`
- Test: `tests/test_doctor.sh`

**Interfaces:**
- Produces: `bash doctor.sh`. It prints one line per requirement and exits 1 if a required tool is missing. Required: ffmpeg + ffprobe, the zscale filter, ImageMagick (`magick` or `convert`), Python ≥ 3.8, Node ≥ 18, Chromium. Optional: uv, piper, codex + bridge.

- [ ] **Step 1: Write the failing test**: `tests/test_doctor.sh`

```bash
#!/usr/bin/env bash
# Self-check for doctor.sh: passes here, and names ffmpeg when it isn't on PATH.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
D="$ROOT/skills/spotlight/scripts/doctor.sh"
out=$(bash "$D"); grep -q "^ready" <<< "$out" || { echo "FAIL: doctor not ready here"; echo "$out"; exit 1; }
t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
for b in bash env node python3 grep ls test sed head; do ln -s "$(command -v $b)" "$t/$b"; done
if out=$(PATH="$t" bash "$D" 2>&1); then echo "FAIL: doctor passed without ffmpeg"; exit 1; fi
grep -q "MISS.*ffmpeg" <<< "$out" || { echo "FAIL: ffmpeg not named"; echo "$out"; exit 1; }
echo "doctor: ok"
```

- [ ] **Step 2: Run it and watch it fail**

Run: `cd /root/spotlight && chmod +x tests/test_doctor.sh && bash tests/test_doctor.sh`
Expected: a failure (`doctor.sh: No such file or directory`).

- [ ] **Step 3: Implement** `skills/spotlight/scripts/doctor.sh`

```bash
#!/usr/bin/env bash
# What spotlight needs. Required tools missing -> exit 1.
set -u
ok=1
have() { eval "$1" >/dev/null 2>&1; }
req() { if have "$2"; then printf '  ok    %s\n' "$1"; else printf '  MISS  %s: %s\n' "$1" "$3"; ok=0; fi; }
opt() { if have "$2"; then printf '  ok    %s (optional)\n' "$1"; else printf '  --    %s (optional): %s\n' "$1" "$3"; fi; }
echo "spotlight doctor"
req "ffmpeg + ffprobe" "command -v ffmpeg && command -v ffprobe" "install ffmpeg 4.4+ (apt install ffmpeg / brew install ffmpeg)"
req "ffmpeg zscale filter (HDR tone-mapping)" "ffmpeg -hide_banner -filters | grep -q ' zscale '" "use an ffmpeg build with libzimg"
req "ImageMagick" "command -v magick || command -v convert" "apt install imagemagick / brew install imagemagick"
req "Python 3.8+" "python3 -c 'import sys; sys.exit(sys.version_info < (3, 8))'" "install python3"
req "Node.js 18+" "node -e 'process.exit(+process.versions.node.split(\".\")[0] < 18)'" "install Node.js 18+"
req "Chromium" "test -n \"\${CHROMIUM:-}\" || command -v chromium || command -v chromium-browser || command -v google-chrome || test -d '/Applications/Google Chrome.app' || ls -d ~/.cache/ms-playwright/chromium-* ~/Library/Caches/ms-playwright/chromium-*" "install Chromium or Chrome, run 'npx playwright install chromium', or set CHROMIUM=/path/to/chrome"
opt "uv (music tempo and cues)" "command -v uv" "https://docs.astral.sh/uv/"
opt "piper (narration, phase 2)" "command -v piper" "uv tool install piper-tts"
opt "codex + gpt-image-bridge (AI images)" "command -v codex && test -x ~/.claude/skills/gpt-image-bridge/bin/gpt-image-2" "https://github.com/oakplank/gpt-image-bridge"
if [[ $ok == 1 ]]; then echo "ready"; else echo "missing required tools"; exit 1; fi
```

- [ ] **Step 4: Run it until it passes**

Run: `bash tests/test_doctor.sh`
Expected: `doctor: ok`.

- [ ] **Step 5: Commit**

```bash
cd /root/spotlight && git add skills/spotlight/scripts/doctor.sh tests/test_doctor.sh && git commit -q -m "feat: doctor.sh — required and optional tools, with install hints

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 8: Agent packaging, docs, licences; local install

**Files:**
- Create: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.gitattributes`, `README.md`, `LICENSE`, `NOTICE.md`, `docs/other-agents.md`
- Create symlinks: `.claude/skills/spotlight`, `.agents/skills/spotlight`, `.opencode/skills/spotlight` → `../../skills/spotlight`

**Interfaces:**
- Produces: the plugin `spotlight@spotlight`, installable from `/root/spotlight`, and the discovery paths for other agents.

- [ ] **Step 1: Write the manifests, licences and symlinks**

`.claude-plugin/plugin.json`:
```json
{
  "name": "spotlight",
  "description": "Turn a website, a code project, footage or photos, and a description into a short video that brags, promotes a point, or explains a topic, with music, text in any language, a poster and a caption.",
  "version": "0.1.0",
  "author": { "name": "Amirh. Co", "url": "https://github.com/AmirSbss" },
  "license": "MIT",
  "homepage": "https://github.com/AmirSbss/spotlight",
  "repository": "https://github.com/AmirSbss/spotlight",
  "keywords": ["video", "launch-video", "promo", "explainer", "presentation", "video-editing", "skill"]
}
```
`.claude-plugin/marketplace.json`:
```json
{
  "name": "spotlight",
  "description": "Point it at a site, footage or a topic; get a video that brags, promotes or explains.",
  "owner": { "name": "Amirh. Co", "url": "https://github.com/AmirSbss" },
  "plugins": [ { "name": "spotlight", "source": "./", "description": "Videos that brag, promote or explain, from a website, footage or a description." } ]
}
```
`LICENSE`: the MIT text, with these copyright lines:
```
Copyright (c) 2026 Amirh. Co (spotlight)
Copyright (c) 2026 Shunit Haviv Hakimi (brag, which spotlight builds on)
```
`NOTICE.md`:
```markdown
# Third-party work in spotlight

| What | Where | Licence |
|---|---|---|
| brag (latent-spaces/brag): creative rules, music-cue analyser | `skills/spotlight/scripts/analyze_music_cues.py`, `references/brag.md` | MIT |
| motion-video-kit (echris6/motion-video-kit): critic loop, quality bar, frozen-time measurement approach | `references/critic.md`, `references/quality-bar.md`, `footage.py check` | MIT |
| gpt-image-bridge (oakplank/gpt-image-bridge): optional, not bundled | used only if installed | MIT |

No music or sound effects are bundled yet (phase 2 adds CC0-only assets, each with its own source and licence record).
```
`.gitattributes`:
```
.claude/skills/spotlight -text
.agents/skills/spotlight -text
.opencode/skills/spotlight -text
```
Symlinks:
```bash
cd /root/spotlight && for d in .claude/skills .agents/skills .opencode/skills; do mkdir -p $d && ln -sfn ../../skills/spotlight $d/spotlight; done
```

- [ ] **Step 2: Write `README.md` and `docs/other-agents.md`**

`README.md`:
````markdown
# spotlight

**Point it at a website, some footage or a topic. Get a video that brags, promotes or explains.**

spotlight is a skill for AI coding agents (Claude Code, Codex, opencode, Cursor, Gemini CLI and anything that reads `SKILL.md`). Give it any mix of a URL, a folder of photos and videos, a code project, data files and a description. It plans the story, cuts the material, sets the type in any language (right-to-left included), mixes the sound, renders, measures and critiques its own video before handing it over.

| Mode | Give it | You get |
|---|---|---|
| **brag** | a project or a website | a 15–25 s launch video built from the real product |
| **promo** | footage and photos (+ a brief or a site) | a 15–30 s promo where the real material is the star |
| **explain** | a topic, data, optionally a site or footage | a 60–180 s explainer: a presentation as a video |

```text
/spotlight https://example.com
/spotlight ~/media/opening-night --lang fa
/spotlight "why we moved support to async" data.csv --mode explain
```

Status: phase 1 of 4. Sound effects, a CC0 music library and narration (phase 2), charts, diagrams and Three.js scenes (phase 3), and demos (phase 4) are on the way. See `docs/superpowers/specs/`.

## Install
**Claude Code:** `claude plugin marketplace add AmirSbss/spotlight && claude plugin install spotlight@spotlight`
**Any agent (skills CLI):** `npx skills add https://github.com/AmirSbss/spotlight --skill spotlight`
**Manually:** copy `skills/spotlight/` into your agent's skills folder, or see `docs/other-agents.md`.

Then run `bash skills/spotlight/scripts/doctor.sh` to check requirements: ffmpeg 4.4+ with zscale, ImageMagick, Python 3.8+, Node 18+, Chromium. Optional: uv, and [gpt-image-bridge](https://github.com/oakplank/gpt-image-bridge) for AI illustration.

## What you get
`spotlight-output/`: `video.mp4` (poster as cover art), `poster.jpg`, `caption.txt`, `plan.md`, `sources.md` (every on-screen claim and where it came from, plus an AI ledger) and `work/`.

## Tests
```bash
python3 tests/test_footage.py && python3 tests/test_check.py && python3 tests/test_docs.py
bash tests/test_capture.sh && bash tests/test_kit.sh && bash tests/test_site.sh && bash tests/test_doctor.sh
```

## Credits
Built on [brag](https://github.com/latent-spaces/brag) (MIT). Critic loop and quality bar adapted from [motion-video-kit](https://github.com/echris6/motion-video-kit) (MIT). See `NOTICE.md`.
````
`docs/other-agents.md`:
```markdown
# Using spotlight with other agents

Agents that discover skills read this repo directly: Codex CLI and Antigravity (`.agents/skills/spotlight`), opencode (`.opencode/skills/spotlight`), Claude Code (`.claude/skills/spotlight` or the plugin). For other agents:
1. **Custom instructions:** paste `skills/spotlight/SKILL.md`, and keep the repo on disk so the agent can open `skills/spotlight/references/` and run `skills/spotlight/scripts/`.
2. **A skills folder:** copy `skills/spotlight/` into it (`cp -r skills/spotlight ~/.your-agent/skills/`).
The agent must be able to run shell commands (ffmpeg, python3, node). Run `bash skills/spotlight/scripts/doctor.sh` first.
```

- [ ] **Step 3: Validate, install, and replace the old plugin**

```bash
cd /root/spotlight && claude plugin validate . | tail -1
git add -A && git add -f .claude/skills/spotlight .agents/skills/spotlight && git commit -q -m "chore: agent packaging, README, licences, other-agents guide

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
claude plugin marketplace add /root/spotlight && claude plugin install spotlight@spotlight && claude plugin details spotlight@spotlight | head -3
claude plugin uninstall promo@promo && claude plugin marketplace remove promo
```
Expected: `✔ Validation passed`; `spotlight 0.1.0` with 1 skill. The old `promo` plugin is uninstalled, so the two skills don't compete for the same requests.

- [ ] **Step 4: Trigger check**

```bash
cd /tmp && for q in "make a launch video for https://example.com" "make a promo from the videos in /tmp" "make an explainer video about why tea beats coffee"; do
  printf '%s -> ' "$q"; timeout 240 claude -p --max-turns 3 --output-format stream-json --verbose "$q" 2>/dev/null | grep -o '"skill":"[^"]*"' | sort -u | tr '\n' ' '; echo; done
```
Expected: every line shows `"skill":"spotlight:spotlight"`. A `brag` skill may also appear for the launch-video line if the brag plugin is installed; that's fine. If spotlight is missing from a line, tune the `description` in SKILL.md, run `rm -rf skills/spotlight/scripts/.venv && claude plugin uninstall spotlight@spotlight && claude plugin marketplace update spotlight && claude plugin install spotlight@spotlight`, and re-check.

---

### Task 9: P1 acceptance and final review

**Files:**
- Modify: whatever the run exposes (each script bug gets a failing test first)

- [ ] **Step 1: brag-mode run on a public fixture site**

```bash
mkdir -p /tmp/spotlight-accept && cp -r /root/.claude/plugins/marketplaces/brag/examples/horse-tinder /tmp/spotlight-accept/site
```
In a **fresh Claude Code session** (so the installed skill loads), run from `/tmp/spotlight-accept`: `/spotlight file:///tmp/spotlight-accept/site/index.html --mode brag`. Let it run end to end, including `site.mjs`, a `web` shot, `check` and one critic round.

Expected:
- `spotlight-output/video.mp4` exists;
- `check` reports no failures and no hold over 0.6 s outside the end card;
- `sources.md` lists every line of on-screen text with a source in `site/copy.json`;
- the critic's report is in `work/critic-1.md`.

- [ ] **Step 2: Regression check on the older renders**

```bash
for v in <the earlier real renders>; do
  python3 /root/spotlight/skills/spotlight/scripts/footage.py check "$v" --end-card 4 --out /tmp/spotlight-accept/regress-$(basename $(dirname $v)); done
```
Expected: no crash. Holds are reported where they're known (the text cards). Nothing from the client folders goes into `/root/spotlight`.

- [ ] **Step 3: Full suite, then a whole-branch review**

Run: `cd /root/spotlight && python3 tests/test_footage.py && python3 tests/test_check.py && python3 tests/test_docs.py && bash tests/test_capture.sh && bash tests/test_kit.sh && bash tests/test_site.sh && bash tests/test_doctor.sh && bash tests/test_bridge_image.sh`
Expected: every suite prints its ok line.

Then dispatch the final whole-branch reviewer as the execution skill describes. Then run the client-data guard:
```bash
cd /root/spotlight && git log -p | grep -iE '<client terms, listed in the private /root/promo copy of this plan>' && echo "CLIENT DATA FOUND — stop" || echo "history clean"
```
Expected: `history clean`. Any hit blocks P1 until it's rewritten out of history.

- [ ] **Step 4: Tag**

```bash
cd /root/spotlight && git tag v0.1.0-p1 && git log --oneline | head -12
```
P2 (sound) starts with its own plan: run superpowers:writing-plans against the spec's P2 section.
