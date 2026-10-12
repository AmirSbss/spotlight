# explain mode: a presentation as a video

Input is a topic, an argument, data files (`*.csv`, `*.json`), and optionally a website or footage. Output is a 60–180 s explainer (default 90 s, landscape) that someone can play in a meeting or post.

## Brief
Write the one sentence the viewer should leave with, the audience, and 3–5 claims that support it. **Every claim has a source in `sources.md`:** the description you were given, a file, a page of the site, or a line in the data. A number on screen must be in the data exactly as shown.

## Shape
Hook question (≤ 6 s) → 3–5 sections, each a claim with one piece of evidence → the takeaway → CTA or next step. Give each section a short chapter card (number + 2–5 words). Sections run 12–30 s. At 60 s that means 3 sections at about 15 s: fold the takeaway into the last section. Vary the evidence: a chart, a diagram, a site page (`web` shot), footage, a big-number card, a list card, a globe or map of routes, a quote from the source (`references/visuals.md`).

## Evidence on screen
- **Numbers:** one number is a `number` chart (it counts up and lands on the value verbatim from the data, with its unit) plus a source line ("Source: survey.csv, 2025"). A comparison is a `bar` chart, a trend a `line`, a share a `donut` (`references/visuals.md`). Every value is the data's own string, never rounded or recomputed.
- **Mechanisms:** a diagram whose lines draw in as the narration or captions name each step.
- **Geography:** `three/routes.js`, a globe or flat map where routes draw between real places.
- **Lists:** at most 5 rows, each ≤ 5 words, equal spacing, aligned left edges.
- **Pages:** scroll the real page (`web`) to the part that proves the claim and stay on it for ≥ 1.5 s while it keeps scrolling at ≥ 80 px/s (output px); a slower scroll over the page's flat bands measures frozen.
- **Only text and data files** (no footage, site or pictures): render each source document as a plain HTML page with the lines you quote highlighted, turn it into a page image with `node <skill-dir>/scripts/site.mjs pages/<doc>.html src/<doc> --size <W>x<H>` (it takes local files and writes `src/<doc>/site/full.png`), and scroll it as a `web` shot. The same image under a blur (`filter`) is the moving backdrop for charts and diagrams. Render only the keys you cite.
- **Narration** (`--voice`) carries the argument, read by local TTS (`references/sound.md`); the on-screen text still carries it on mute. Keep reading time ≥ 0.3 s per word.

## Tones
| Tone | Feel | Pacing |
|---|---|---|
| `clear` (default) | Calm, plain, confident | Sections 15–25 s; soft cuts; one idea per screen |
| `documentary` | Footage-led, measured | Longer holds on footage; captions low; slow pushes |
| `keynote` | Big type, bold reveals | Short punchy sections; hard cuts on the music |
