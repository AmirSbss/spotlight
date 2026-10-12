# Plan: "Why spotlight checks its own videos"

**Angle:** spotlight doesn't ship a video on trust. It measures every render, it even flagged its own README demo, and because
numbers can pass while a video isn't ready, a fresh critic watches it too; the loop repeats until it ships.
**Hook:** the user's own title as a question, landed on frame 0. **Format:** 1920x1080, 30 fps, 60.0 s, explain / `clear`.
**Material:** no pictures were given (and no AI images), so every shot is one of the user's files rendered as an editor page
(`work/gen_pages.py` → `work/pages/*.html` → `site.mjs` → `work/src/<name>/site/full.png`) and scrolled at ~90 px/s.
Cited lines are highlighted. The check JSONs show only the cited keys (`loudness`, `frozen`, `warnings`, `failures`):
their `file`/`sheet` keys are local paths. The README page drops the badge and image lines.

| # | Time | Source (backdrop) | Motion | On-screen text | Narration (voice t) | Transition |
|---|---|---|---|---|---|---|
| Hook | 0.0–3.6 | src/readme (README.md top; its first line "Point your AI agent at…" highlighted) | scroll 0→300, push 1→1.04 | "Why does spotlight check its own videos?" (right column, frame 0) | h1 @ 0.5 | — |
| 01a | 3.6–10.1 | src/quality (quality-bar.md, Measured table highlighted) | scroll 200→760 | 01 · Measured / It measures every render / rows: Frozen time ≤ 1 s per 30 s · Loudness −14 LUFS · Frames Exactly duration × 30 | a1 @ 3.9; rows on "frozen frames" 6.45, "loudness" 7.35, "frame count" 8.4 | dip 0.4 |
| 01b | 10.1–18.3 | src/checks (check-readme-demo.json: total 0.8, budget 0.72, warning highlighted) | scroll 260→1000 | README demo · frozen / **bar chart** Frozen 0.8s (amber) vs Budget 0.72s (grey), grows 10.3, values shown only once settled (11.3) / the warning verbatim (12.9) / Source | a2 @ 10.4 | dip 0.4 |
| 02a | 18.3–25.8 | src/checks (check-brag-draft.json: total 0, holds [], failures [] highlighted) | scroll 2560→3060, push 1→1.05 | 02 · A draft / The numbers passed / `"holds": []` `"failures": []` (18.8) / Source | b1 @ 18.7 | dip 0.4 |
| 02b | 25.8–34.2 | src/critic (critic-round-1-brag.md: Dead air, Effects highlighted) | scroll 3300→4060 | Critic · round 1 / A critic sees the rest / Dead air in the hook. (26.4) / The same words appear twice (29.9) / Five of eight are buried · effects (31.3) | b2 @ 25.9 | dip 0.4 |
| 02c | 34.2–36.9 | src/critic (the ONE MORE PASS line highlighted) | scroll 5250→5500 | Verdict / ONE MORE PASS. (34.65) | b3 @ 33.5 | dip 0.4 |
| 03 | 36.9–48.3 | src/readme ("How it works", blurred) | scroll 7700→8750 | 03 · The loop / **diagram** Render (37.0) → Measure (39.3) → Fresh critic (39.9) → Fix (40.6) ↺ Render (41.25) · 3 rounds max (43.5); a pulse runs the loop 43.7–46.3 and out to SHIP (46.3; readable ~46.7–48.05) | c1 @ 37.1 | dip 0.4 |
| Take | 48.3–52.8 | src/readme ("Ground rules", blurred) | scroll 9900→10920 (keeps going under the end card; the page's end never shows) | "A video ships only after it passes its own checks" / README.md · Ground rules | t1 @ 48.5 | dip 0.4 |
| End | 52.8–60.0 | end card (dark), breathes 1.00→1.03 | — | spotlight / Point your AI agent at a website, some footage or a topic, and get back a finished short video. / github.com/AmirSbss/spotlight | e1 @ 53.3 | wipe |

**Music:** `assets/music/calm.mp3` (explain `clear`), track 18.5–78.5 s (the steady groove starts at ~18 s, so frame 0 already
moves), fade in 0.2, fade out 0.8 (the last 0.8 s, after the end card has landed). Ducked under the narration by mix.py.
**Cue times cut on:** the cuts follow the narration, not the beat (calm, clear tone).
**Effects (sparse, clear tone):** 3.6 whoosh-1 (peak; section 01) · 10.75 pop-3 (chart values land) · 18.3 whoosh-1 (peak; section 02)
· 34.65 pop-2 (verdict lands) · 36.9 whoosh-1 (peak; section 03) · 46.3 chime-2 (SHIP: done) · 52.8 whoosh-3 (peak; end card reveal).
**Narration (`work/lines.json`, en_US-ljspeech-high, public domain):** 9 lines, 46.9 s of speech; starts and checks in `work/timing.py`.
**AI assets:** none.

## How it was made

A stranger's run of the skill (an agent that knew spotlight only from `SKILL.md`), then two more critic rounds:

```
/spotlight "Why spotlight checks its own videos" ./inputs --mode explain --voice --lang en --duration 60
```

`inputs/` held the README, `quality-bar.md`, `critic.md`, three real `check.json` files and a real critic report from earlier spotlight runs.

## Critic rounds
- **Round 1** (`critics/critic-1.md`): ONE MORE PASS. Fixed: the 02 beat said the opposite of its point, the opener was dark, a near-empty frame at 38 s, a static stretch at 46–50 s, count-up values that aren't in the data, and the video never said what spotlight is.
- **Round 2** (`critics/critic-2.md`, a fresh verification critic): ONE MORE PASS. Fixed: the pulse ran over the box labels (it now runs under the boxes and lights each one it passes), SHIP held still (it now pushes in), and the first critic finding lands with its title. Also two backdrops that scrolled past their file's end, larger source lines, and two rows added to `sources.md`.
- **Round 3** (`critics/critic-3.md`, the last round): ONE MORE PASS, with two one-number fixes and no further round needed. pop-3 now lands with the bar values (10.75 s, not 11.3), and the takeaway's backdrop stops scrolling before the page's end comes into view. Then a re-check of the measurements. Left as they are (style or cosmetic, per the critic): the dips through black, a dark opener, small source lines on a phone, and the bed-only stretch at 45–48 s.
