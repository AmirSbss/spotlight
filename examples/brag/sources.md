# Sources: every line of on-screen text and every number

Repo paths are relative to the spotlight repo (github.com/AmirSbss/spotlight). `notes.md` is `showcase/notes.md`. `cafe/` is the Mahoor Coffee promo's output folder (`cafe/spotlight-output/` and `cafe/spotlight-output-fa/`).

## Our captions and card labels
| Time | On screen | Source |
|---|---|---|
| 0–4.0 | "spotlight · a skill for AI coding agents" | `README.md` line 9: "spotlight is a skill for AI coding agents"; the promo is a spotlight run (`cafe/spotlight-output/plan.md`; the coordinator's brief: "a 20 s vertical promo spotlight made for Mahoor Coffee") |
| 0–4.0 | "A café promo from 12 phone clips and a logo." | `cafe/spotlight-output/sources.md`: "Inputs: twelve phone clips from the café (video_*.mov) and the logo (mahoor-logo.jpg), both from the owner"; `cafe/work/manifest.jsonl` lists 12 clips. (The promo uses five of them; "from" names its inputs.) |
| 0–7.0 | card bar "Mahoor Coffee", tags "Promo · 20 s", "English", "Persian" | the café's name (cafe `sources.md`, the owner's brief); its length (20.0 s, ffprobe); the two cuts (`cafe/spotlight-output/` English, `cafe/spotlight-output-fa/` Persian) |
| 4.0–7.0 | "The same timeline" / "…and a Persian cut." | `cafe/spotlight-output/plan.md`: "Persian cut: the same frames and mix, with captions in Persian (Vazirmatn) running right to left" |
| 4.0–7.0 | "Right to left, letters joined." | `cafe/spotlight-output/plan.md` ("running right to left"); `README.md`: "Persian or Arabic letters stay joined and run right to left"; cafe `work/critic-3.md`: "The text is still right-aligned and joined" |
| 7.0–13.0 | "Data in, explainer out" | chapter card standing for notes.md: Codex "made this 25 s narrated explainer … from two small CSV files" |
| 7.0–13.0 | "Same prompt, same sample data." | notes.md: Hermes "did the same from the same prompt and data", "two small CSV files of SAMPLE data"; `docs/other-agents.md`: "from the same headless prompt and the same two small CSV files" |
| 7.5–13.0 | "Codex CLI, about 12 minutes" | notes.md: "It took about 12 minutes"; `docs/other-agents.md`: "full pipeline in about 12 minutes" |
| 10.1–13.0 | "Hermes Agent, about 27 minutes" | notes.md: "in about 27 minutes"; `docs/other-agents.md`: "full pipeline in about 27 minutes" |
| 7.0–13.0 | card bars "codex-sample-explainer.mp4", "hermes-sample-explainer.mp4", tag "Sample data · fictional courier" | the file names in `showcase/`; notes.md: "SAMPLE data about a fictional courier ('Northwind Parcels')" |
| 13.0–19.5 | card bar "explain-why-spotlight-checks-its-own-videos.mp4" · "60 s · explainer" | the file name; notes.md: "a 60 s narrated explainer" |
| 13.0–19.5 | "Before you see it" | `README.md` intro: "has a second agent critique it before you see it" |
| 13.0–19.5 | "spotlight measures every render." | `README.md`: "measures the result"; the explainer's own section title "It measures every render" (`examples/explain/sources.md`) |
| 13.0–19.5 | "Then a critic reviews it, up to three rounds." | `README.md` "How it works": "… This goes on for up to three rounds."; `docs/other-agents.md`: "Every run went through `footage.py check` and a critic review" |
| 19.5–24 | "spotlight." | the project's name (`skills/spotlight/SKILL.md`) |
| 19.5–24 | "Finished short videos from your AI coding agent." | `README.md` line 3: "Point your AI agent at a website, some footage or a topic, and get back a finished short video."; line 9: "spotlight is a skill for AI coding agents" |
| 19.5–24 | "github.com/AmirSbss/spotlight" | the repo URL (`README.md` install lines) |
| 19.5–24 | "Tested on Claude Code, Codex CLI and Hermes Agent" | `README.md` Install: "It has been tested end to end on Claude Code, Codex CLI and Hermes Agent." |

## Text burned into the source clips (inside the cards, never captioned over)
| Card | Window (source s) | Burned-in text | Source |
|---|---|---|---|
| Café, English | 0.0–4.0 and 4.5–7.5 (shown at 0–4.0 and 4.0–7.0) | "MAHOOR COFFEE", "Some days need a good coffee.", then "Today is one of them." (the café's own mood lines; this video never quotes them) | `cafe/spotlight-output/video.mp4` (re-captioned at the owner's request); traced in `cafe/spotlight-output/sources.md` |
| Café, Persian | 4.5–7.5 (shown at 4.0–7.0) | «امروز از همون روزاست.» | `cafe/spotlight-output-fa/video.mp4`; `cafe/spotlight-output/sources.md` (Persian cut table) |
| Codex | 4.0–7.0, cropped to the chart panel | "01 · 2025 parcels by hub", "12,400", "9,850", "6,320", "Dubai", "London", "Toronto", "Source: hubs.csv" | `showcase/codex-sample-explainer.mp4`; fictional sample data (notes.md) |
| Hermes | 7.6–10.6 | "Connecting routes · routes.csv", "Inter-Hub Transit Flows", "4,100 parcels DXB → LHR · 2,750 parcels LHR → YYZ", "Toronto (YYZ)", "London (LHR)", "Dubai (DXB)" | `showcase/hermes-sample-explainer.mp4`; fictional sample data (notes.md) |
| Loop | 40.2–42.6 + 43.5–47.6, cropped to the diagram and darkened | "Render", "Measure", "Fresh critic", "Fix", "3 rounds max", "SHIP" | `showcase/explain-why-spotlight-checks-its-own-videos.mp4` (= `examples/explain/video.mp4`), loop diagram only |

## Numbers on screen
12 (clips): cafe `sources.md` and manifest. 20 s (the promo's length): the file. 12 and 27 (minutes): notes.md, `docs/other-agents.md`. "two" (CSV files, agents): notes.md. "three rounds": `README.md`. Inside the cards only: the fictional sample values above; "3 rounds max" from the explainer.

## People and permission
The café footage in the windows used shows a barista's arm and gloved hands and the café's wall art (a painted face on a screen); no customer faces. The owner approved publishing the promo, faces included (the coordinator's brief). Mahoor Coffee appears only as their own promo, never as a customer or endorsement.

## Music and effects
`skills/spotlight/assets/music/upbeat.mp3`: "Happy Beats & Business Moves Vol. 1", music by Sascha Ende at ende.app, CC BY 4.0 (`assets/music/LICENSES.md`), track 16.02–40.02 s. Effects (CC0): `assets/sfx/whoosh-1.ogg`, `whoosh-2.ogg`, `whoosh-3.ogg`, `chime-2.ogg`. The café promo's own sound is not used.

## Fonts
Space Grotesk, Inter, JetBrains Mono (SIL OFL), from Google Fonts. The Persian text is the Persian cut's own pixels (Vazirmatn, per cafe `plan.md`).

## AI ledger
| File | Prompt | Purpose | Shot |
|---|---|---|---|
| — | — | none | — |
