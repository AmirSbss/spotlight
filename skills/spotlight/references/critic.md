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
