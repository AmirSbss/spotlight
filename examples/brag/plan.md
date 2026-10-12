# Plan: spotlight LinkedIn demo (brag, 23 s, English, no AI, no narration), one timeline in two formats

- **Square 1080x1080** (LinkedIn, primary, muted autoplay): `spotlight-output-reel2/`.
- **Landscape 1920x1080** (README): `spotlight-output-v3/`. Same `scene.html`, frames and `mix.wav`; only `width`/`height` in `timeline.js` differ.

**Angle.** Real material in, finished videos out. Two real businesses' videos, each made by spotlight from what the business had: a live website, and a folder of phone clips. Then the check every render goes through, then the repo.

**Hook (0–3 s).** Frame 0 is finished: both videos play side by side in 9:16 player cards ("BudTech · Launch video", "Mahoor Coffee · Promo") under "spotlight · videos made by your AI agent / A website and phone clips in. Finished videos out."

**Layout.** The slot system from v2. 9:16 card 450x800 (+44 px bar); the pair 2 × 360x640 in square, 2 × 450x800 in landscape; the loop diagram 1040 wide in landscape, 936 in square (inset to the 72 px side margin). Every card fits whole in 1080x1080. Captions sit left of the cards (landscape; square beside a single card) or under them (square, the pair and the loop). None lies over a clip.

## Shots
| # | Time | Source | In–out (source s) | Motion | On-screen text (ours) | Transition |
|---|---|---|---|---|---|---|
| Hook | 0.0–3.0 | `budtech/spotlight-output/video.mp4` (A) + `cafe/spotlight-output/video.mp4` (B), the pair | BudTech 0.0–3.0; café 0.0–3.0 | clips play | kicker (36 px) "spotlight · videos made by your AI agent"; "A website and phone clips in. Finished videos out." (frame 0) | B fades 2.9–3.0, A moves to the single slot 3.0–3.2 |
| Website | 3.0–8.0 | BudTech (A), single | 3.0–5.5, continuous from the hook: the live site (3.0), the language menu tapped (3.85), Arabic (4.5); then its own end card, source 16.4–18.9 ("Request a quote" tapped at our 6.7) | the move | kicker "1 · A launch video"; "Built from the live site, budtech.om."; "Switched to Arabic through its own menu." (3.2–3.8, after the move) | hard cut, card pops |
| Clips | 8.0–11.0 | café (A), single | 4.5–7.5 (the pour) | pop | kicker "2 · A café promo"; "From 12 phone clips and a logo." | at 11.0 A moves aside (0.2 s) |
| Persian | 11.0–14.0 | café (A) + `cafe/spotlight-output-fa/video.mp4` (B) sliding in (11.1–11.35) | both 10.0–13.0 (the counter; the jump is to the promo's own 10.0 s cut) | the pair | kicker "The same timeline"; "…and a Persian cut."; "Right to left, letters joined." (11.12–11.55) | hard cut, card pops |
| Loop | 14.0–18.5 | `showcase/explain-why-spotlight-checks-its-own-videos.mp4`, cropped to the diagram (x 140–1800, y 356–836), faint backdrop text darkened | 43.5–48.0 ("3 rounds max", the pulse, SHIP at source 46.3 = video 16.8) | pop, drift | kicker "Before you see it"; "Measured, then reviewed by a second AI agent."; "Up to three rounds." | wipe into the end card at 18.5 |
| End | 18.5–23.0 | dark end card | — | wipe 18.5–18.92; lines land 18.8, 18.95, 19.2, 19.6; URL 19.5 | "spotlight."; "Finished short videos from your AI coding agent."; "Free and open source"; "github.com/AmirSbss/spotlight"; "Tested on Claude Code, Codex CLI and Hermes Agent" | — |

Durations: 3.0 + 5.0 + 3.0 + 3.0 + 4.5 + 4.5 = 23.0 s. `end` = 18.5, so `--end-card 4.5`.

**Backdrops.** Kit `clip` shots of the BudTech, café and loop frames, blurred 40 px and dimmed (.32), plus a warm beam crossing at ~350 px/s (turning round inside moving shots).

**The two businesses.** Shown only as their own videos, labelled with their names and "Launch video" / "Promo" / "English" / "Persian". Our text quotes neither video's captions and makes no claim about either business beyond what the videos are and what they were made from.

## Music and effects
- `assets/music/upbeat-rock.mp3` ("The Show Begins Vol. 8", Sascha Ende, CC BY 4.0), track 5.0 → 28.0 s: the riff under the hook, the full band from video 6, a breath at video 14 (the check loop), full again to the end. fade_in 0.05, fade_out 0.8. Loudness range 4.2 LU. A first mix on `upbeat.mp3` (45–68 s) measured 0.7 LU, flat for an upbeat piece.
- Every cut lands on its beat (120 BPM from track 8.01): 3.0, 8.0, 11.0, 14.0, 18.5.

| t (s) | File | Why |
|---|---|---|
| 2.95 | whoosh-2 (peak) | the pair becomes one card |
| 3.85 | click-2 | the language menu is tapped (on screen in the BudTech card) |
| 4.15 | toggle-1 | "العربية" chosen |
| 6.7 | click-3 | "Request a quote" tapped on BudTech's end card |
| 8.0 | whoosh-3 (peak) | website → phone clips |
| 10.95 | whoosh-2 (peak) | the card moves aside for the Persian cut |
| 14.0 | whoosh-3 (peak) | → the check loop |
| 16.8 | chime-2 | SHIP lands |
| 18.65 | whoosh-3 (peak) | end-card wipe |

No live sound: the source videos' own audio stays out.

## AI assets
| File | Prompt | Purpose | Shot |
|---|---|---|---|
| none | — | real videos cover every beat | — |

## Critic rounds
- **Round 1** (`critics/critic-1.md`): ONE MORE PASS. Fixed:
  - the square's kickers wrapped badly and repeated the lines: now "1 · A launch video", "2 · A café promo";
  - `sources.md` cited README lines removed in the README rewrite: every row is re-cited to the current README (lines 1, 3, 15–16, 108, 111, 117) and docs, and its People section now lists every shot;
  - the loop caption repeated the diagram's labels: now "Measured, then reviewed by a second AI agent. / Up to three rounds."; the square loop card is inset to the 72 px margins;
  - the end card gives a reason to click: "Free and open source";
  - "skill" was jargon in the hook: "spotlight · videos made by your AI agent";
  - the BudTech card's last 2.5 s show its own end card (the site's name, Arabic name, "Request a quote" tapped, budtech.om) instead of a stock-looking photo;
  - captions land sooner after the moves (3.2, 11.12), the mark at 18.8; tags keep their own case ("20 s", not "20 S").
- **Round 2** (`critics/critic-2.md`, a fresh verification critic): **SHIP**. Both gating fixes hold, and the music-only track was measured to match the bundled track, so no source audio is in the mix. Left as they are (cosmetic, per the loop's stop-at-SHIP rule): frame 0's line breaks as "…phone clips / in. Finished videos out.", the hook's "Launch video"/"Promo" tags are small at phone size, the loop backdrop is dark (32/255), "Up to three rounds." echoes the diagram's "3 rounds max", the landscape hook kicker wraps, and the Arabic-menu line stays up over BudTech's end card.
