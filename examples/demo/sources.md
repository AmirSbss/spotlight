# Sources: every line of on-screen text and every number

Repo paths are relative to the spotlight repo; `work/` is this run's work folder.

## Main video
| Time | On screen | Source |
|---|---|---|
| 0–3.82 | "spotlight." / "A skill for AI coding agents" | the project's name (`SKILL.md`, `name: spotlight`); `README.md`: "spotlight is a skill for AI coding agents" |
| 0–3.82 | "Point it at a website, some footage or a topic." | `README.md`, committed tagline (line 3), verbatim. The working-tree README is being rewritten ("Point your AI agent at a website, some footage or a topic, and get back a finished short video."); if that lands, the video still matches the README's meaning but not its exact words |
| 0–3.82 | "Input · its test page"; the address `tests/fixtures/site/index.html` in the browser card | the page shown is that file in the repo, captured with `scripts/site.mjs` |
| 0–3.82 (on the page) | "Boats for cats", "Every cat deserves a boat.", "Get a boat" | `tests/fixtures/site/index.html` (`work/site2x/site/screens/01.png`) |
| 3.82–7.10 | "Output · from its test page" | this run: `work/mini/mini.mp4` was made from that page with the kit |
| 3.82–7.10 | "Get a video that brags, promotes or explains." | `README.md`, committed tagline (line 3), verbatim |
| 3.82–7.10 (in the panel) | "How it works", "Pick a boat. We deliver it.", "Get a boat", "Boats from one fish." (and the page's own nav links) | `work/mini/site/copy.json` (the test page's headings, paragraphs and CTAs) |
| 7.10–12.55 | "footage.py check", "It checks its own render." | `skills/spotlight/scripts/footage.py` (`check`: frozen holds, loudness, frames); `SKILL.md` §6 |
| 7.10–12.55 | "A 2.2 s hold, caught and fixed." | `work/mini/chk-v1/check.txt` (hold 1.1–3.3 s, 2.2 s), then `work/mini/chk/check.txt` (frozen 0s) after a stronger push in `work/mini/timeline.js` |
| 7.10–12.55 | `$ footage.py check mini.mp4 --end-card 2.4` (twice) | the command run in `work/mini/`, shortened from `python3 <skill-dir>/scripts/footage.py check mini.mp4 --end-card 2.4 --out chk` |
| 7.10–12.55 | "warning: hold without motion 1.1-3.3s (2.2s > 0.6s)" | **excerpt** of `work/mini/chk-v1/check.txt`. Also printed but not shown: the summary line with "frozen 2.7s (budget 0.12s)", "warning: loudness range 0.6 LU is under 3 (…)", "warning: frozen 2.7s, over the budget of 0.12s (1s per 30s)" |
| 7.10–12.55 | "6.0s 180 frames 1080x1920 · I -13.8 LRA 0.6 TP -2.8 · frozen 0s (budget 0.12s)" | **excerpt** of `work/mini/chk/check.txt`: its summary line without the trailing " · sheet chk/check-sheet.jpg". Also printed but not shown: "warning: loudness range 0.6 LU is under 3 (fine for calm pieces, flat for energetic ones)" |
| 7.10–12.55 (blurred backdrop) | the mini's contact sheet | `work/mini/chk/check-sheet.jpg`, written by `footage.py check` |
| 12.55–15.82 | "references/critic.md" | the file shown |
| 12.55–15.82 (in the doc) | "# Critic loop", "The builder never grades its own work. If you can start a fresh sub-agent, use it. Give it only the rendered video, the brief, `check.json` and `check-sheet.jpg`, and, from round 2, the previous critic's report. Never your reasoning or a list of what you think you fixed." | an excerpt of `skills/spotlight/references/critic.md` lines 1–3, verbatim apart from two omissions: line 3's opening credit sentence (a third-party name; the credit stays in the repo's `NOTICE.md` and `critic.md`) and its last sentence ("Without sub-agents, do the same review yourself on freshly extracted frames, not on stills you chose earlier."). The browser card and the typesetting are drawn by `work/stills.mjs` for this run |
| 12.55–15.82 | "Then a fresh critic reviews it." | `references/critic.md`: "a fresh critic reviews the actual render… a new critic verifies" (`SKILL.md` §7) |
| 15.82–20.18 | "footage.py check · this video" and the contact sheet | `footage.py check` of the previous render of this video (`work/chk-draft/check-sheet.jpg`, copied to `work/stills/self-sheet.jpg`) |
| 15.82–20.18 | "This video? spotlight made it too." / "Every picture from its own repo." | this run: every picture is the repo's test page, docs (`critic.md`), script output (`site.mjs`, `footage.py`) or render kit. Not pictures: the music (CC0 track below) and the fonts (OFL, below) |
| 20.18–25 | "spotlight." / "A skill for AI coding agents" | `README.md`: "spotlight is a skill for AI coding agents" |
| 20.18–25 | "github.com/AmirSbss/spotlight" | the brief (CTA); also `README.md` install lines |

Numbers on screen: 2.2 (the hold, in the caption and the warning), 1.1, 3.3, 0.6 (first check); 6.0, 180, 1080x1920, -13.8, 0.6, -2.8, 0, 0.12 (second check); 2.4 (the `--end-card` argument). All come from this run's real `footage.py check` output, listed above.

## Music
"Montage" by wipics, CC0 (OpenGameArt), [montage.mp3](https://opengameart.org/content/montage), provided by the user. Main video: track 17.47–42.47 s. Mini video: 0.29–6.29 s.

## Fonts
Space Grotesk, Inter and JetBrains Mono (SIL Open Font License), from Google Fonts, stored in `work/fonts/`.

## AI ledger
| File | Prompt | Purpose | Shot |
|---|---|---|---|
| — | — | none: run with `--no-ai` | — |
