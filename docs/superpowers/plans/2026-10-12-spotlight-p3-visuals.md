# spotlight P3 (visuals) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Explainers and launches can show evidence, not just say it:
- **Charts** that grow from the given data only: bar, line, number, donut.
- **Diagrams** whose lines draw in.
- **Deterministic Three.js scenes:** a routes globe or map, and an extruded logo.

Every frame is still a pure function of t, and parallel capture stays pixel-identical.

**Architecture:**
- **Charts and diagrams** are DOM/SVG inside the existing caption system (`.cap` containers give visibility; `[data-at]` gives timing). `kit.js` builds each chart's DOM once at load and sets its state from t every frame.
- **Three.js scenes** are a new shot kind, `three`. `kit.js` imports the module once per shot, gives it its own canvas, and calls `render(t - a)` every frame. Modules may return screen anchors, so DOM labels (any language, the page's fonts) follow 3D points.
- **three.js** is vendored, pinned and self-contained (`0.170.0`, one `three.module.min.js`). The page loads modules from `file://`, so `browser.mjs` launches Chromium with `--allow-file-access-from-files`. WebGL comes from SwiftShader; `--enable-unsafe-swiftshader` keeps it on in Chrome builds that no longer fall back to it automatically.

**Tech Stack:** plain JS (classic `kit.js`, ES modules under `kit/three/`), three.js 0.170.0 (MIT), Natural Earth 110 m land (public domain) baked into land dots, playwright-core + Chromium, bash tests.

**Spec:** `docs/superpowers/specs/2026-10-02-spotlight-design.md`, section "Kit additions" (chart, diagram, three) and Phases (P3).

## Global Constraints

- Every frame is a pure function of t: no clocks, no unseeded randomness, no physics history, no CSS transitions or animations. Frame N is the same whether it's rendered first or after frame N+1. `CAPTURE_WORKERS=1` and `CAPTURE_WORKERS=n` produce identical files.
- Charts plot only the given data. Every number shown at the settled time is the exact string from `data-values` / `data-value`, with the same digits, separators and units.
- Text in any language and script, including right-to-left: chart labels and 3D labels are DOM text, so the kit's `lang`/`dir`/`<bdi>` rules apply. No letter-spacing on Arabic script.
- Safe zones and type scale come from the kit's `--k`, `--safe-*` and `--side` variables. Formats are vertical, landscape and square at 30 fps.
- Vendored code is pinned and credited in `NOTICE.md` (three.js MIT; Natural Earth public domain).
- `footage.py` stays stdlib only. No npm dependency beyond the per-run `playwright-core`.
- Memory: ~3 GB free on the build box, so tests use small sizes (≤ 540 px) and run captures serially.
- Commit messages end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. The phase is pushed to `origin main` once all suites pass.

## Review Focus

1. **A WebGL scene captured in parallel:** frames are identical to a serial capture, and nothing is blank (`preserveDrawingBuffer`, rendering synchronously before the screenshot). Pinned in Task 1.
2. **Persian digits and separators in chart data** (`"۱۲٬۴۰۰"`): the settled text is the exact source string, and counting up uses the same digit set. Pinned in Task 3.
3. **A chart in landscape and in vertical:** it stays inside the side margins at both sizes. Pinned in Task 3.
4. **A routes scene whose label anchor turns to the back of the globe:** the label hides instead of floating over the ocean. Pinned in Task 2.
5. **Module load failure** (a typo in the `three` path): capture exits non-zero with a message naming the file, not a blank shot. Pinned in Task 1.

---

## File Structure

```
skills/spotlight/
├── scripts/browser.mjs        Task 1: --allow-file-access-from-files, --enable-unsafe-swiftshader
├── kit/
│   ├── kit.js                 Task 1: three shots + anchors; Task 3: charts; Task 4: diagrams
│   ├── scene.html             Task 1: label style; Task 3: chart styles; Task 4: diagram styles
│   └── three/
│       ├── three.module.min.js   Task 1: vendored three@0.170.0 (MIT)
│       ├── LICENSE               Task 1: three.js licence text
│       ├── land-dots.js          Task 2: Natural Earth 110 m land baked into ~12k dots (PD)
│       ├── routes.js             Task 2: dot globe / flat map, great-circle routes, points, anchors
│       ├── SVGLoader.js          Task 5: vendored three@0.170.0 addon, import rewritten to ./three.module.min.js
│       └── extrude.js            Task 5: extruded SVG logo/shape with a slow camera move
tests/
├── test_three.sh              Tasks 1, 2, 5
├── test_kit.sh                Tasks 3, 4: charts and diagrams
└── test_docs.py               Task 6
SKILL.md · references/explain.md · brag.md · promo.md · README.md · NOTICE.md    Task 6
```

---

### Task 1: `three` shots in the kit, deterministic WebGL capture

**Interfaces:**
- **Shot:** `{ a, b, three: "three/routes.js", params: {...} }`. The path is relative to `work/`; the agent copies `<skill-dir>/kit/three/` to `work/three/`.
- **Module contract:** `export async function create(canvas, params, { width, height, css })` returns `{ render(tLocal, p) }`.
  - `css(name)` reads a brand token from `:root`, e.g. `css("--accent")`.
  - `render` draws synchronously and may return `{ anchors: { <id>: [x, y, visible] } }` in output pixels.
- **Kit:**
  - Imports each distinct module once at ready, with one canvas per three shot (`<canvas class="three">`, absolute, full frame, under the grain).
  - Shows the active shot's canvas and calls its `render`.
  - Moves every `[data-anchor="<id>"]` element to its anchor (`transform: translate(x, y)`, centred), with `opacity` 0 when not visible.
  - A failed import or create throws `three shot <path>: <message>` from `window.ready`, so capture fails loudly.
- **`browser.mjs`** always adds `--allow-file-access-from-files` and `--enable-unsafe-swiftshader`.

- [ ] Step 1: write `tests/test_three.sh`, starting with a fixture module `tests/fixtures/three-spin.js` (a lit cube turning with t, colour from `--accent`). Check four things at 320×568, 2 s:
  - **No blank frames:** the centre pixel of frame 30 is not the background.
  - **Determinism:** `CAPTURE_WORKERS=1` and `CAPTURE_WORKERS=3` md5s are identical.
  - **Motion:** frames 0 and 59 differ.
  - **Clear errors:** a misspelt module path makes `capture.mjs` exit non-zero, with the path in its stderr.
- [ ] Step 2: run it. It fails (`three` is ignored, so the frames are blank).
- [ ] Step 3: vendor `three@0.170.0/build/three.module.min.js` plus its `LICENSE` into `kit/three/`, change `browser.mjs`, and add the three path to `kit.js`. In each three module, create `THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true })` with `setPixelRatio(1)`.
- [ ] Step 4: run `test_three.sh`, `test_kit.sh` and `test_capture.sh` (the new flags must not change the existing pixel checks). Record the ms per frame and the peak RSS per worker at 1080×1920 for the spin fixture in the commit message.
- [ ] Step 5: commit.

### Task 2: `routes.js`, a dot globe or flat map with routes

**Interfaces:** `params`:
- `view`: `"globe"` (default) or `"flat"`.
- `points`: `[{ id, lat, lon, at }]`.
- `routes`: `[{ from, to, at, dur = 1.2 }]`, where `from` and `to` are point ids.
- `center`: `[lat, lon]`, or `{ from: [lat, lon], to: [lat, lon] }`. It defaults to the points' centroid; the camera eases from → to over the shot.
- `zoom` (default 1).
- `colors`: `{ land, ocean, route, point }`, defaulting to the tokens `--paper` (land dots at 60%), `--ink` (ocean), `--accent` (routes and points).

Points pop in at `at`. Each route is a great-circle tube that lifts with distance and draws in from `at` over `dur`. Anchors are returned for every point id; on the globe, a point on the far side is not visible.

`land-dots.js` exports a base64 Int16 array of lat/lon ×100, made once from Natural Earth `ne_110m_land` by sampling a 40 000-point Fibonacci sphere. The header comment records the generator and the source URL.

- [ ] Step 1: extend `test_three.sh`. Use a routes scene (Dubai → London, Dubai → Tehran) at 320×568, 3 s, and check:
  - **Routes draw in:** accent-coloured pixels are absent at 0.1 s and present along the route at 2.9 s.
  - **Labels follow their points:** the `data-anchor="lon"` label's centre lies within 12 px of the projected London point.
  - **Hidden on the far side:** a second scene centred on the far side of the globe gives the London anchor opacity 0.
  - **Determinism:** serial and parallel captures are identical.
- [ ] Step 2: fail, implement, pass, commit.

### Task 3: charts

**Interfaces:** in `scene.html`, inside a `.cap` (which gives visibility):
- `<div class="chart" data-kind="bar|line|donut" data-values='["12,400", "30.5%", 18]' data-labels='["2023","2024","2025"]' data-at="3.2" data-dur="1.0"></div>`
- `<div class="chart" data-kind="number" data-value="۱۲٬۴۰۰" data-at="3.2"></div>`

Values may be numbers or strings. A string is shown verbatim at the settled time and parsed for its size: Persian or Arabic-Indic digits, `,`/`٬` grouping, `.`/`٫` decimals, and a prefix or suffix such as `$` or `%`. While counting up, the number uses the same digits, grouping, decimals and affixes.

Each kind's motion:
- **bar:** bars rise one after another, 0.1 s apart.
- **line:** the line draws in.
- **donut:** the segments sweep around.
- **number:** counts up over `data-dur` (default 1.0 s) with an out-cubic ease.

Colours come from `--accent` (the highlighted series) and its tints; type uses the scene's fonts and `--k`.

- [ ] Step 1: extend `test_kit.sh` with a page holding a bar chart (`[10, 20, 40]`) and a number (`"۱۲٬۴۰۰"`), in vertical and landscape. Use a small node script with playwright to check five things:
  - **Settled bars:** at the settled time, the bar heights are in ratio 1:2:4 (±2 %).
  - **Settled number:** the number's text is exactly `۱۲٬۴۰۰`.
  - **Counting up:** halfway through the count, the number is a smaller Persian-digit number.
  - **Margins:** every chart box sits within the side margins in both formats.
  - **Determinism:** serial and parallel captures are identical.
- [ ] Step 2: fail, implement in `kit.js` (build once at ready; per-frame state from t) and `scene.html` (styles), pass, commit.

### Task 4: diagrams

**Interfaces:** `<svg class="diagram" viewBox="…">` inside a `.cap`. `path`, `line` and `polyline` elements with `data-at` draw in (normalised with `pathLength="1"`, dash offset over `data-dur`, default 0.6 s). Every other element with `data-at` (circle, rect, text, g) fades and rises like caption lines.

- [ ] Step 1: extend `test_kit.sh`. A `path` with `data-at="0.5"` shows no stroke pixels at 0.4 s, part of its length at 0.8 s and all of it at 1.2 s. A `circle` node is invisible before its `at` and visible after it.
- [ ] Step 2: fail, implement, pass, commit.

### Task 5: `extrude.js`, an extruded logo or shape

**Interfaces:** `params`:
- `svg`: a path relative to `work/`, read with XHR (`fetch` can't read `file://`).
- `depth` (default 0.18 of the shape's width).
- `color` (default `--accent`) and `background` (default `--ink`).
- `turn`: `[deg0, deg1]`, the yaw over the shot (default `[-25, 20]`).
- `tilt` (default 12°).

The shape is centred and scaled to 62 % of the short side, with soft key and rim lights, and the camera moves linearly so it never reads as frozen.

- [ ] Step 1: extend `test_three.sh` with `tests/fixtures/site/logo.svg`. Check that the centre region is not background, that frames 0 and end differ, and that serial and parallel captures are identical.
- [ ] Step 2: vendor `SVGLoader.js` (three@0.170.0 `examples/jsm/loaders/`) with its `from 'three'` rewritten to `from './three.module.min.js'`. Then fail, implement, pass, commit.

### Task 6: docs, acceptance, push

- [ ] Docs:
  - **`SKILL.md` "The page":** add `three` shots (copy `kit/three/`, the module contract, `params` per module, `[data-anchor]` labels), plus charts and diagrams in the caption system.
  - **`explain.md`:** charts replace the "2–4 big numbers until the chart layer" rule. Add diagrams for mechanisms and `routes` for geography.
  - **`brag.md`:** an `extrude` logo reveal on the end card, used sparingly.
  - **`promo.md`:** `routes` for travel, delivery and logistics.
  - **`test_docs.py`:** the kit documents `three`, `params` and the chart kinds; every module named in the docs exists in `kit/three/`.
  - **README:** Status and Tests.
  - **NOTICE:** three.js and Natural Earth.
- [ ] Run every suite.
- [ ] **Stranger test:** a fresh subagent makes a 60 s landscape `explain` from a small public-domain CSV with one bar chart, one number card, one diagram and one routes shot. It must pass `check`. Fix whatever the agent tripped on.
- [ ] Commit and push to `origin main`.
