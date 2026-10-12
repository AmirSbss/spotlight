# Sources

Inputs: `inputs/README.md`, `inputs/quality-bar.md`, `inputs/critic.md`, `inputs/check-readme-demo.json`,
`inputs/check-brag-draft.json`, `inputs/check-brag-final.json`, `inputs/critic-round-1-brag.md`. Nothing was changed in them.

## On-screen text
| Time | Text | Source |
|---|---|---|
| 0–3.6 | Why does spotlight check its own videos? | The user's brief, "Why spotlight checks its own videos", as a question (authored hook) |
| 3.7 | 01 · Measured | Chapter label (authored), from quality-bar.md heading "## Measured" |
| 3.85 | It measures every render | Authored chapter title; README.md "renders, measures the result"; quality-bar.md "`footage.py check` measures the first block" |
| 6.45 | Frozen time · ≤ 1 s per 30 s | quality-bar.md, Measured table: "Frozen time \| ≤ 1 s per 30 s; …" |
| 7.35 | Loudness · −14 LUFS | quality-bar.md: "Loudness \| −14 LUFS integrated (±1); …" |
| 8.4 | Frames · Exactly duration × 30 | quality-bar.md: "Frames \| Exactly duration × 30" |
| 10.15 | README demo · frozen | check-readme-demo.json is the README demo's check (its `file` is examples/demo/video.mp4; the path is not shown) |
| 10.3 | Bar chart: Frozen "0.8s", Budget "0.72s" | check-readme-demo.json `frozen.total` 0.8, `frozen.budget` 0.72; the strings "0.8s" / "0.72s" are verbatim from its `warnings[0]` |
| 12.9 | frozen 0.8s, over the budget of 0.72s (1s per 30s) | check-readme-demo.json `warnings[0]`, verbatim (a warning: `failures` is `[]`) |
| 18.4 | 02 · A draft | check-brag-draft.json (file name: a brag draft) |
| 18.55 | The numbers passed | Authored title for check-brag-draft.json `failures: []`, `holds: []` (it has one warning, about loudness range, so not "every check") |
| 18.8 | "holds": [] / "failures": [] | check-brag-draft.json `frozen.holds` and `failures`, verbatim |
| 25.9 | Critic · round 1 | critic-round-1-brag.md title "Critic 1: …"; it reviews the same render as check-brag-draft.json (its Sound section quotes "-14.0 LUFS, TP -2.4, LRA 1.4", the draft's numbers) |
| 26.05 | A critic sees the rest | Authored chapter title; README.md "has a second agent critique it before you see it" |
| 26.4 | Dead air in the hook. | critic-round-1-brag.md, §3: "**Dead air in the hook.**" |
| 29.9 | The same words appear twice | critic-round-1-brag.md, §1 S2: "The same words appear twice, in two serifs." |
| 31.3 | Five of eight are buried · effects | critic-round-1-brag.md, §3 Effects: "But five of eight are buried, in-band against the bed" (capitalised) |
| 34.3 | Verdict | Authored label for the critic's closing verdict line below |
| 34.65 | ONE MORE PASS. | critic-round-1-brag.md, last line: "**ONE MORE PASS.**" |
| throughout | Source: <file> (under each claim) | The input file each claim on that screen is quoted from, named as in `inputs/` |
| 36.95 | 03 · The loop | Chapter label (authored) |
| 37.0–46.3 | Render → Measure → Fresh critic → Fix → (back to Render) … SHIP | README.md "How it works": "After the render, a fresh agent that didn't build the video looks through its frames and measurements and writes down what's wrong. The builder fixes those things, and another fresh agent confirms the fixes."; critic.md "Stop at SHIP" |
| 43.5 | 3 rounds max | README.md "This goes on for up to three rounds."; critic.md "At most 3 rounds." |
| 48.35 | A video ships only after it passes its own checks | README.md, Ground rules, verbatim (sentence continues ": nothing sits still …") |
| 48.9 | README.md · Ground rules | file and heading |
| 53.05 | spotlight | README.md title |
| 53.35 | github.com/AmirSbss/spotlight | The user's request ("End on github.com/AmirSbss/spotlight"); README.md install lines name `AmirSbss/spotlight` |
| 53.2 | Point your AI agent at a website, some footage or a topic, and get back a finished short video. | README.md line 3, verbatim |
| backdrops | the scrolled files | README.md, quality-bar.md, the three check JSONs (keys loudness/frozen/warnings/failures only), README minus its badge, image and examples/ link lines, critic-round-1-brag.md, rendered verbatim |

## Narration (`work/lines.json`)
| Line | Text | Source |
|---|---|---|
| h1 | Why does spotlight check its own videos? | the brief |
| a1 | First, it measures every render: frozen frames, loudness, and the exact frame count. | quality-bar.md Measured block |
| a2 | It even flagged its own demo video: zero point eight seconds frozen, over a budget of zero point seven two. | check-readme-demo.json warnings[0] |
| b1 | But numbers can pass while a video still isn't ready. This draft had no frozen holds, and no failures. | check-brag-draft.json (`holds: []`, `failures: []`) + the critic's verdict on it |
| b2 | Then a fresh critic watched it, and found dead air in the hook, the same words twice, and five of eight effects buried. | critic-round-1-brag.md §3 and §1 |
| b3 | Its verdict: one more pass. | critic-round-1-brag.md, last line |
| c1 | So the loop goes: render, measure, critique, fix. Then a new critic confirms the fixes, for up to three rounds. | README.md "How it works" |
| t1 | A video ships only after it passes its own checks. | README.md Ground rules |
| e1 | spotlight makes finished short videos. It's on GitHub. | README.md line 3 ("get back a finished short video") / install lines / the user's CTA |

Voice: Piper `en_US-ljspeech-high`, public domain (LJ Speech). voice.py printed no credit line.

## Charts and diagrams
- Bar chart (10.1–18.3): check-readme-demo.json, keys `frozen.total` (0.8) and `frozen.budget` (0.72); value strings from `warnings[0]`.
- Diagram (36.9–48.3): README.md "How it works" (last paragraph), critic.md (SHIP, at most 3 rounds).

## AI ledger
None.

## Music and effects
Music: `calm.mp3`, "Documentary Music - Small Signs of Change", music by Sascha Ende at ende.app (CC BY 4.0). The effects are spotlight's bundled CC0 effects.
