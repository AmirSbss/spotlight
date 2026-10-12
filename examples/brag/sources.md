# Sources: every line of on-screen text and every number

Repo paths are relative to the spotlight repo (github.com/AmirSbss/spotlight). `budtech/` and `cafe/` are the two source videos' output folders.

## Our captions and card labels
| Time | On screen | Source |
|---|---|---|
| 0–3.0 | "spotlight · videos made by your AI agent" | `README.md` line 1: "spotlight: short videos made by your AI coding agent" |
| 0–3.0 | "A website and phone clips in. Finished videos out." | the two videos' inputs: BudTech from the live website (`budtech/spotlight-output/sources.md`: "captured from the live site … https://budtech.om/en/ … and https://budtech.om/ar/"); Mahoor Coffee from phone clips (`cafe/spotlight-output/sources.md`: "twelve phone clips from the café"); `README.md` line 3: "turns a website, a folder of phone clips or a spreadsheet into a finished short video" |
| 0–8.0 | card bar "BudTech" · "Launch video" / "Launch video · 20 s" | the site name (`budtech/…/sources.md`: og:site_name); `budtech/…/plan.md`: "brag", 20.0 s (ffprobe) |
| 0–14.0 | card bar "Mahoor Coffee" · "Promo", "Promo · 20 s", "English", "Persian" | the café's name (`cafe/…/sources.md`, the owner's brief); its length (20.0 s, ffprobe); the two cuts (`cafe/spotlight-output/`, `cafe/spotlight-output-fa/`) |
| 3.0–8.0 | "1 · A launch video" | the BudTech video is a brag (launch) video (`budtech/…/plan.md`); `README.md` line 15: "BudTech launch video … the live website budtech.om … brag, vertical, 20 s" |
| 3.0–8.0 | "Built from the live site, budtech.om." | `budtech/…/sources.md`: "All captured from the live site on 2026-10-12: https://budtech.om/en/ … and https://budtech.om/ar/"; its photos "downloaded from https://media.budtech.om/ (the site's own media)" |
| 3.0–8.0 | "Switched to Arabic through its own menu." | `budtech/…/plan.md` shots 3–5: "the language picker is tapped, 'العربية' is chosen, and the page flips to Arabic"; `sources.md`: the menu captured "after a real click on the picker" |
| 8.0–11.0 | "2 · A café promo" | `cafe/…/plan.md` ("promo"); `README.md` line 16: "Mahoor Coffee promo … twelve phone clips and a logo … promo, vertical, 20 s" |
| 8.0–11.0 | "From 12 phone clips and a logo." | `cafe/spotlight-output/sources.md`: "Inputs: twelve phone clips from the café (video_*.mov) and the logo (mahoor-logo.jpg), both from the owner"; `cafe/work/manifest.jsonl` lists 12 clips |
| 11.0–14.0 | "The same timeline" / "…and a Persian cut." | `cafe/spotlight-output/plan.md`: "Persian cut: the same frames and mix, with captions in Persian (Vazirmatn) running right to left" |
| 11.0–14.0 | "Right to left, letters joined." | `cafe/…/plan.md` ("running right to left"); `README.md` line 3: "captions in your language (Arabic and Persian included)"; `skills/spotlight/SKILL.md` ("Text in any language": Persian runs right to left, joined scripts animate by word so letters stay joined) |
| 14.0–18.5 | card bar "explain-why-spotlight-checks-its-own-videos.mp4" · "60 s explainer" | the file in `showcase/`; `showcase/notes.md`: "a 60 s narrated explainer" |
| 14.0–18.5 | "Before you see it" | `README.md` line 3: "Every one is measured and reviewed by a second AI agent before you see it." |
| 14.0–18.5 | "Measured, then reviewed by a second AI agent." | `README.md` line 3 (above); line 108: "Twice over: once by measurement, once by a critic." |
| 14.0–18.5 | "Up to three rounds." | `README.md` line 111: "This runs for up to three rounds." |
| 18.5–23 | "spotlight." | the project's name (`skills/spotlight/SKILL.md`) |
| 18.5–23 | "Finished short videos from your AI coding agent." | `README.md` line 1 ("short videos made by your AI coding agent") and line 3 ("a finished short video") |
| 18.5–23 | "Free and open source" | `README.md` line 3: "spotlight is a free, open-source Agent Skill" |
| 18.5–23 | "github.com/AmirSbss/spotlight" | the repo URL (`README.md` install lines) |
| 18.5–23 | "Tested on Claude Code, Codex CLI and Hermes Agent" | `README.md` line 117: "Codex CLI and Hermes Agent were each tested end to end … and Claude Code made every example here."; `docs/other-agents.md` "Which agents were tested?" table (Claude Code, Codex CLI, Hermes Agent) |

## Text burned into the source videos (inside the cards, never captioned over or quoted)
| Card | Window (source s) | Burned-in text | Source |
|---|---|---|---|
| BudTech | 0.0–5.5, then its end card 16.4–18.9 (shown at 0–5.5 and 5.5–8.0) | "BudTech · Muscat, Oman", "From IT infrastructure", "to custom software"; the live site's own page (EN H1 "BudTech, your technology partner in Oman and the GCC", its hero paragraph, "Request a quote", the menu "English / العربية", the AR H1 and button); its end card: logo, "BudTech", "براعم التقنية", "Request a quote" (tapped at source 17.6 = our 6.7), "budtech.om", "Muscat, Oman" | `budtech/spotlight-output/video.mp4`; traced in `budtech/spotlight-output/sources.md` |
| Mahoor Coffee (hook) | 0.0–3.0 | "MAHOOR COFFEE", "Some days need a good coffee." | `cafe/spotlight-output/video.mp4`; `cafe/…/sources.md` (the café's own mood lines) |
| Mahoor Coffee | 4.5–7.5, 10.0–13.0 | "Today is one of them.", "Better with a friend." | the same |
| Mahoor Coffee, Persian | 10.0–13.0 | «با رفیق، بهتره.» | `cafe/spotlight-output-fa/video.mp4`; `cafe/…/sources.md` (Persian cut table) |
| Loop | 43.5–48.0, cropped to the diagram, darkened | "Render", "Measure", "Fresh critic", "Fix", "3 rounds max", "SHIP" | `showcase/explain-why-spotlight-checks-its-own-videos.mp4` (= `examples/explain/video.mp4`) |

## Numbers on screen
12 (clips): `cafe/…/sources.md`, manifest, `README.md` line 16. 20 s (both videos' length): ffprobe (20.0 s each). "three rounds": `README.md` line 111. 60 s: ffprobe (60.0 s), `showcase/notes.md`.

## People and permission
- BudTech: a man at his screens, from the back (the site's own photo, 1.5–3.0). The owner's own company and site.
- Mahoor Coffee: in the hook (0–3.0) a barista's arm and the café's wall art (a painted face on a screen); at 8–11 a gloved hand pouring; at 11–14 a customer's hands and arm at the counter. The owner approved publishing the promo, faces included (the coordinator's brief).
- Both businesses appear only as their own videos, never as customers or endorsements of spotlight.

## Music and effects
- Music: `skills/spotlight/assets/music/upbeat-rock.mp3`, "The Show Begins Vol. 8" by Sascha Ende (https://ende.app/en/song/12952-the-show-begins-vol-8), CC BY 4.0 (`assets/music/LICENSES.md`), track 5.0–28.0 s. **Music by Sascha Ende at ende.app.**
- Effects: `assets/sfx/whoosh-2.ogg`, `whoosh-3.ogg`, `click-2.ogg`, `toggle-1.ogg`, `chime-2.ogg` (bundled, `assets/sfx/LICENSES.md`).
- The source videos' own audio is not used.

## Fonts
Space Grotesk, Inter, JetBrains Mono (SIL OFL), from Google Fonts. The Arabic and Persian text is the source videos' own pixels.

## AI ledger
| File | Prompt | Purpose | Shot |
|---|---|---|---|
| — | — | none | — |
