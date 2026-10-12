# Visuals: charts, diagrams and 3D

Evidence on screen beats a claim in a caption. All three below are pure functions of t, like the rest of the kit, so parallel capture never changes a pixel. Use them where they prove something: charts for numbers from the data, diagrams for a mechanism, a globe for geography, an extruded logo for a closing beat. Never use them as decoration.

## Charts

A chart lives inside a caption container (`.cap`), which sets when it's on screen. `data-at` sets when it starts to grow, and `data-dur` how long that takes (default 1 s):

```html
<div class="cap mid" data-a="12.0" data-b="17.5" data-scrim="bottom"><div class="rule"></div>
  <div class="kicker" data-at="12.05">Tickets per year</div>
  <div class="chart" data-kind="bar" data-values='["1,240", "2,310", "4,875"]' data-labels='["2023", "2024", "2025"]' data-at="12.3"></div>
  <div class="sub" data-at="13.6">Source: tickets.csv</div>
</div>
```

| `data-kind` | Data | Motion |
|---|---|---|
| `bar` | `data-values` + `data-labels`, ≤ 6 bars, values ≥ 0 | bars rise one after another; each value appears as its bar settles |
| `line` | `data-values` + `data-labels`, ≤ 12 points, negatives allowed | the line draws left to right, values appear as it passes |
| `donut` | `data-values` + `data-labels`, ≤ 5 parts, values ≥ 0 | arcs sweep round; each value appears as its part completes |
| `number` | `data-value` (one) | counts up from zero and lands on the value |

- **Values come from the data file exactly as written.** Write them as strings (`"12,400"`, `"30.5%"`, `"$1.2M"`, `"۱۲٬۴۰۰"`): bars, lines and donuts only ever show that string, and a `number` counts up in its own digits, separators, decimals and units before landing on it. Bars and donut parts are sizes, so a negative value stops the capture with an error: show it as a line, a number card or a list. List every chart in `sources.md` with its file and rows.
- Bars share one scale: the largest value fills the plot (or set `data-max`). Put the label you want read first (the claim) in the kicker or `.sub`, not inside the chart.
- Colours come from `--accent`, with tints for the other series. Type follows the scene's fonts and scales with the format. A chart is at most 1000 px × `--k` wide. In landscape, `.cap.left` or `.cap.right` keeps the caption and its chart to one half, and the other half shows the evidence (a scrolling file, footage).
- **Hold a settled chart** for at least 1.5 s, plus 0.3 s per word of its labels. Put it over a moving backdrop: a still with a `filter` (which pushes and drifts) or a blurred clip. A settled chart over a frozen frame measures as a hold, and a critic calls a long settled hold a lull even over a moving backdrop: past the reading time, move something on the chart or diagram itself (a pulse along a path from `SPOTLIGHT.draw`) or cut. Captions fade out over their last 0.25 s, so count the hold up to `data-b` − 0.25.

## Diagrams

Use an inline SVG with class `diagram`, inside a `.cap`. Each `path`, `line` or `polyline` with `data-at` draws in over `data-dur` (default 0.6 s). Any other element with `data-at` (a node `circle`, a `rect`, a `text` label, a `g`) fades in like a caption line:

```html
<div class="cap mid" data-a="20" data-b="26"><svg class="diagram" viewBox="0 0 900 300">
  <rect x="0" y="110" width="220" height="80" rx="16" data-at="20.2"/><text x="110" y="158" text-anchor="middle" data-at="20.3">Request</text>
  <path d="M230 150 H450" data-at="20.6"/>
  <rect x="460" y="110" width="220" height="80" rx="16" data-at="21.2"/><text x="570" y="158" text-anchor="middle" data-at="21.3">Queue</text>
</svg></div>
```

Nodes default to a dark tint of `--accent` with an accent outline and white labels; restyle in `scene.html` (`.diagram rect { fill: … }`). `text` is 22 units of the `viewBox`, so keep the viewBox about as wide as the diagram is on screen (≈ 900–1000), or set `font-size`. Draw an arrowhead as its own short `polyline` with a `data-at` just after its line's (a `marker-end` would show before its line has drawn). Keep it to one idea, ≤ 6 nodes, with labels of ≤ 3 words.

## 3D: `three` shots

Copy `<skill-dir>/kit/three/` to `work/three/`. A shot `{ a, b, three: "three/<module>.js", params: {…} }` draws a WebGL scene for its whole span. Labels are DOM elements placed on the scene's anchors: `<div class="label" data-anchor="<id>" lang="…">Name</div>`, directly inside `#stage`. They follow the kit's language rules (`dir`, `<bdi>`, fonts), and they hide when their point turns away.

**`three/routes.js`:** a dotted globe (or a flat map) with points that pop in and great-circle routes that draw in. Use it for where something goes: deliveries, flights, offices, customers.

```js
{ a: 8, b: 14, three: "three/routes.js", params: {
  view: "globe",                       // or "flat"
  points: [ { id: "dxb", lat: 25.25, lon: 55.36, at: 0.2 }, { id: "lhr", lat: 51.47, lon: -0.45, at: 0.8 } ],
  routes: [ { from: "dxb", to: "lhr", at: 1.0, dur: 1.4 } ],     // times are seconds into the shot
  center: { from: [30, 30], to: [38, 20] },                     // optional; default: the points' centre, drifting east
  zoom: 1 } }
```

**`three/extrude.js`:** an SVG logo or shape, extruded and turning slowly. It suits the last beat of a brag before the end card, at most once per video. It needs the logo as an SVG with filled shapes (strokes are ignored). Each shape keeps its own colour, unless `color` sets one for all.

```js
{ a: 16, b: 19, three: "three/extrude.js", params: { svg: "site/assets/logo.svg", turn: [-25, 20], tilt: 12 } }
```

- **Cost:** a 3D frame takes ~140 ms at 1080×1920 with 2 workers, so a 6 s globe shot adds ~25 s of capture. Keep `CAPTURE_WORKERS` at 2 on a machine with little memory.
- **Your own module:** export `create(canvas, params, { width, height, css })` returning `{ render(tLocal, p) }`. Make the `WebGLRenderer` with `preserveDrawingBuffer: true` and `setPixelRatio(1)`, and draw synchronously inside `render`. It must be a pure function of `tLocal`: no clocks, no `requestAnimationFrame`, no unseeded randomness, no state carried between frames. Return `{ anchors: { id: [x, y, alpha] } }` to place labels.
