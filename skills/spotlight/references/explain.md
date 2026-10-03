# explain mode: a presentation as a video

Input is a topic, an argument, data files (`*.csv`, `*.json`), and optionally a website or footage. Output is a 60–180 s explainer (default 90 s, landscape) that someone can play in a meeting or post.

## Brief
Write the one sentence the viewer should leave with, the audience, and 3–5 claims that support it. **Every claim has a source in `sources.md`:** the description you were given, a file, a page of the site, or a line in the data. A number on screen must be in the data exactly as shown.

## Shape
Hook question (≤ 6 s) → 3–5 sections, each a claim with one piece of evidence → the takeaway → CTA or next step. Give each section a short chapter card (number + 2–5 words). Sections run 12–30 s. Vary the evidence: a site page (`web` shot), footage, a big-number card, a list card, a quote from the source.

## Evidence on screen
- **Numbers:** a big-number card shows the value verbatim from the data with its unit and source line ("Source: survey.csv, 2025"). Until the chart layer arrives (phase 3), comparisons are 2–4 big numbers side by side, never a hand-drawn chart.
- **Lists:** at most 5 rows, each ≤ 5 words, equal spacing, aligned left edges.
- **Pages:** scroll the real page (`web`) to the part that proves the claim and end on it for ≥ 1.5 s, still scrolling slowly (a short `scroll` range), so it never sits frozen.
- **Narration** (`--voice`, phase 2) carries the argument; until then, on-screen text carries it. Keep reading time ≥ 0.3 s per word.

## Tones
| Tone | Feel | Pacing |
|---|---|---|
| `clear` (default) | Calm, plain, confident | Sections 15–25 s; soft cuts; one idea per screen |
| `documentary` | Footage-led, measured | Longer holds on footage; captions low; slow pushes |
| `keynote` | Big type, bold reveals | Short punchy sections; hard cuts on the music |
