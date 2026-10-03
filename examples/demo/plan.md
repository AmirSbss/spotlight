# Plan: spotlight README demo (brag, landscape 1920×1080, 25 s, English, no AI)

**Angle.** spotlight's own pipeline, shown on the repo's own material: its test page goes in, a video comes out, `footage.py check` catches a real flaw in that video and then passes it, a fresh critic reviews it. The punchline: this video went through the same pipeline.

**Hook (0–3.82 s).** Frame 0 is finished and names the product:
- the "spotlight." wordmark with "A skill for AI coding agents";
- the repo's real test page ("Boats for cats") in a browser card whose address is `tests/fixtures/site/index.html`, labelled "Input · its test page";
- the README tagline.

The card pushes in and a warm beam sweeps the stage from the first frame.

**Tone.** default (punchy, clean), hard cuts on the beat, one wipe into the end card. The look is dark, with the kit's amber accent; the end card stays dark so it doesn't flash for dark-mode README readers.

## Music
- **Track:** A, [montage.mp3](https://opengameart.org/content/montage), "Montage" by wipics (CC0, OpenGameArt). 110 BPM, steady, with a natural fade from 41 to 44 s.
- **Window:** track 17.47 → 42.47 s (video 0 → 25). 17.47 s is a strong cue (a downbeat), so the beat grid lands on video 0 + k × 0.5454 s.
- **Shaping (`work/mix.wav`):**
  - 60 ms fade-in;
  - a −6 dB dip under the critic beat (ramps 12.30–12.55 s down, 15.74–15.82 s back up), so the punchline lands on the full track; the dip lifts the loudness range from 2.3 to 3.1 LU;
  - the track's own fade starts at video ≈ 23.5 s, after the end card has landed (wipe 20.18–20.60 s, CTA landed by 21.12 s);
  - a 0.7 s fade-out ends on the last frame.
- **Cuts on the track's strong cues** (from `footage.py track`; video time = track − 17.47):
  - 3.82 s (track 21.29);
  - 7.10 s (24.57);
  - 12.55 s (beat 23);
  - 15.82 s (33.30);
  - end card at 20.18 s (37.65).

## Shots
| # | Time | Source | Motion | On-screen text (verbatim) | Transition |
|---|---|---|---|---|---|
| 1 | 0.00–3.82 | `work/stills/s1-input.png`: a 1000×578 crop below the nav bar of `work/site2x/site/screens/01.png` (`site.mjs` capture of `tests/fixtures/site/index.html` at 2160×3840), in a browser card drawn by `work/stills.mjs` | push 1 → 1.05; beam sweep | "spotlight." / "A skill for AI coding agents"; "Input · its test page"; "Point it at a website, / some footage or a topic." (all on screen from frame 0) | cut on cue 3.82 |
| 2 | 3.82–7.10 | `work/frames/s02`: 98 frames of `work/mini/mini.mp4` from 1.5 s (`footage.py shot … 1.5 3.28 1080x1920 0.5`), as a panel on the right | panel push 0.82 → 0.95; beam sweep | kicker "Output · from its test page"; "Get a video that / brags, promotes / or explains." | cut on cue 7.10 |
| 3 | 7.10–12.55 | `work/stills/mini-check-sheet.jpg`: `footage.py check`'s contact sheet of `mini.mp4`, blurred and dimmed as a backdrop | kit card push and drift; beam sweep | kicker "footage.py check"; "It checks its own render."; "A 2.2 s hold, caught and fixed."; typed terminal: the first check's warning, then the re-check ("frozen 0s") | cut on beat 23 |
| 4 | 12.55–15.82 | `work/stills/s4-critic.png`: `references/critic.md` from its heading and its bold sentence to the end of that paragraph, verbatim, typeset in JetBrains Mono (`work/stills.mjs`) | push 1.12 → 1.26 from the bold line; a light pool sweeps onto "The builder never grades its own work." and reads along it | kicker "references/critic.md"; "Then a fresh critic reviews it." | cut on cue 15.82 (music returns) |
| 5 | 15.82–20.18 | `work/stills/self-sheet.jpg`: `footage.py check`'s contact sheet of the previous render of this video, as a panel at the top | panel push 0.66 → 0.72; beam sweep | kicker "footage.py check · this video"; "This video? spotlight made it too."; "Every picture from its own repo." | wipe up into the end card on cue 20.18 |
| End | 20.18–25.00 | dark end card (#0E1424), accent #E4B53B | wipe in, then lines land | "spotlight."; "A skill for AI coding agents"; "github.com/AmirSbss/spotlight" | — |

Durations: 3.82 + 3.28 + 5.45 + 3.27 + 4.36 + 4.82 = 25.00 s.

**Type.** Space Grotesk (display), Inter (body), JetBrains Mono (terminal and docs). All are SIL OFL, downloaded as woff2 into `work/fonts/`.

**The mini video (`work/mini/`).** A 6 s vertical brag of the test page, made with the same kit:
- the `site.mjs` screen, a "How it works / Pick a boat. We deliver it." caption, and an end card with the page's logo, "Get a boat" and "Boats from one fish." (all from `site/copy.json`), in the colours from `site/brand.json` (#0f172a, #f8fafc, #f59e0b);
- music: the same Montage track, 0.29–6.29 s;
- its first render held still for 2.2 s, and `check` flagged it (`chk-v1/check.txt`); a stronger push fixed it (`chk/check.txt`).

The mini was frozen after that, so the numbers on screen match its final render.

## AI assets
| File | Prompt | Purpose | Shot |
|---|---|---|---|
| none | `--no-ai` | — | — |

Privacy: no people, licence plates, addresses or personal data. Only relative paths appear on screen.

## Critic rounds
- **Round 1** (`work/critic-1.md`): ONE MORE PASS. Fixed in round 2:
  - removed the third-party credit from the critic.md shot (it now starts at the bold sentence);
  - named the product in frame 0;
  - the input page now sits in a labelled browser card, cropped below its unstyled nav;
  - the punchline now plays over this video's own contact sheet, with "Every picture from its own repo.";
  - a shorter critic beat and a gentler dip (−6 dB instead of −7);
  - cuts and the end card moved to strong cues;
  - a dark end card;
  - a bigger terminal over a softened backdrop, a "caught and fixed" line, and `sources.md` now calls the terminal an excerpt.
- **Round 2** (`work/critic-2.md`): **SHIP**. All of round 1's blockers are verified fixed. The remaining notes are cosmetic and were left as they are:
  - the test page's own blue nav links in the output panel;
  - a sparse but real output panel;
  - the 6 dB dip;
  - section 5 about 1 s longer than needed;
  - dim lines clipped at the right edge of the critic shot;
  - two short fade frames at 7.10 and 12.50.

  One text fix was made: `sources.md` now lists both sentences left out of the critic.md excerpt.
