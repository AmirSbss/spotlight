# Plan: spotlight launch video v2 (brag, 24 s, English, no AI, no narration), one timeline in two formats

- **Square 1080x1080** (LinkedIn, primary, muted autoplay): `spotlight-output-reel/`.
- **Landscape 1920x1080** (README): `spotlight-output-v2/`. Same `scene.html`, frames and `mix.wav`; only `width`/`height` in `timeline.js` differ.

**Angle.** Real footage first: a real café's promo that spotlight cut from the owner's phone clips (and its Persian cut), then explainers two other agents made from data, then the check loop every render goes through, then the repo.

**Hook (0–4 s).** Frame 0 is finished: the Mahoor Coffee promo playing in a 9:16 player card (its shaker flip, its own "MAHOOR COFFEE" title), beside "spotlight · a skill for AI coding agents / A café promo from 12 phone clips and a logo."

**Layout.** Cards sit in slots that `scene.html` places per format (`#slot-v`, `#slot-va`/`#slot-vb`, `#slot-h`); `draw()` measures them once and moves the cards between them.
- 9:16 card: 450x800 + a 44 px bar.
- The pair: 2 × 360x640 in square, 2 × 450x800 in landscape.
- 16:9 card: 992 wide with a 52 px bar (its 26 px sample-data tag reads at phone size); the Codex clip is cropped to its chart panel (x 214–1706, y 238–840 of 1920x1080; 992x400).
- The loop: the explainer cropped to its diagram (x 140–1800, y 356–836), its faint backdrop text darkened (`-level 10%`); 1040 wide in both formats (square: caption block centred under it; landscape: right of the caption column), so it fits 1080x1080 like every other card.
- Every card fits whole in 1080x1080.
- Captions sit in a column left of the cards (landscape, and square beside the single 9:16 card) or under the cards (square, the pair and the 16:9 cards). They never lie over a clip.

## Shots
| # | Time | Source | In–out (source s) | Motion | On-screen text (ours) | Transition |
|---|---|---|---|---|---|---|
| Hook | 0.0–4.0 | `cafe/spotlight-output/video.mp4` (EN promo) in the 9:16 card | 0.0–4.0 (the shaker flip, then espresso at the bar) | card push 1 → 1.012 | kicker (36 px) "spotlight · a skill for AI coding agents"; "A café promo from 12 phone clips and a logo." (frame 0); bar "Mahoor Coffee" · "Promo · 20 s" | on 4.0 the card moves left (0.2 s) |
| Persian | 4.0–7.0 | EN card + `cafe/spotlight-output-fa/video.mp4` sliding in beside it (4.1–4.35, opaque by 4.2) | both play the promo's 4.5–7.5 (the pour; its own cuts at 4.5 and 7.5 land on our 4.0 and 7.0; the café's own mood line in English and Persian) | the pair | kicker "The same timeline" (4.15); "…and a Persian cut."; "Right to left, letters joined."; bars "Mahoor Coffee" · "English" / "Persian" | hard cut on 7.0, card pops (0.94 → 1) |
| Codex | 7.0–10.0 | `showcase/codex-sample-explainer.mp4` | 4.0–7.0 (bar chart grows), cropped to the chart panel | pop, drift | kicker "Data in, explainer out"; "Same prompt, same sample data."; "Codex CLI, about 12 minutes"; tag "Sample data · fictional courier" | hard cut on 10.0, pop (the caption stays) |
| Hermes | 10.0–13.0 | `showcase/hermes-sample-explainer.mp4` | 7.6–10.6 (globe, routes drawing) | pop, drift | the same caption + "Hermes Agent, about 27 minutes" (10.1); tag "Sample data · fictional courier" | hard cut on 13.0 (breakdown starts), pop |
| Loop | 13.0–19.5 | `showcase/explain-why-spotlight-checks-its-own-videos.mp4`, cropped to the diagram (x 140–1800, y 356–836), darkened | 40.2–42.6 + 43.5–47.6 (the diagram builds; a 0.9 s still stretch of the finished diagram is trimmed at the join; "3 rounds max", the pulse, SHIP lands at source 46.3 = video 18.2) | pop, drift | kicker "Before you see it"; "spotlight measures every render."; "Then a critic reviews it, up to three rounds." | wipe into the end card at 19.5 |
| End | 19.5–24.0 | dark end card | — | wipe 19.5–19.92; lines land 19.95, 20.1 (after the wipe); URL at 21.0 with the drums' return; "Tested on…" at 21.1 | "spotlight."; "Finished short videos from your AI coding agent."; "github.com/AmirSbss/spotlight"; "Tested on Claude Code, Codex CLI and Hermes Agent" | — |

Durations: 4.0 + 3.0 + 3.0 + 3.0 + 6.5 + 4.5 = 24.0 s. `end` = 19.5, so `--end-card 4.5`.

**Backdrops.** Kit `clip` shots of the same clip, blurred 40 px and dimmed (.32), plus a warm beam crossing at a constant ~350 px/s (it turns round at 1.0, 6.5, 12.0 and 17.5 s, inside shots whose clips move).

**Mahoor Coffee.** Shown only as their own promo: labelled "Mahoor Coffee" with "Promo", "English", "Persian". No quote, logo-as-endorsement or "customer" wording. The café's own captions and blur box are untouched, inside the card.

## Music and effects
- `assets/music/upbeat.mp3` ("Happy Beats & Business Moves Vol. 1", music by Sascha Ende at ende.app, CC BY 4.0), track 16.02 → 40.02 s: its beat grid starts at 16.02 s, so every cut lands on a beat (re-mixed after the owner found the earlier CC0 track harsh).
- The breakdown (track 72–80) sits under the check loop (13.0–21.0), and the drums return at 21.0 as the URL lands.
- Cuts on the beat grid: 4.0, 7.0, 10.0, 13.0, 19.5, and the URL at 21.0.

| t (s) | File | Why |
|---|---|---|
| 3.95 | whoosh-2 (peak, target +6) | the card moves to make room for the Persian cut |
| 6.95 | whoosh-2 (peak, target +6) | café → data |
| 13.0 | whoosh-1 (peak) | data → the check loop |
| 18.2 | chime-2 | SHIP lands |
| 19.65 | whoosh-3 (peak) | end-card wipe |

No live sound: the café promo's own music would clash with the track.

## AI assets
| File | Prompt | Purpose | Shot |
|---|---|---|---|
| none | — | real footage covers every beat | — |

## Critic rounds
- **Round 1** (`critics/critic-1.md`): ONE MORE PASS. Fixed:
  - the hook now says what spotlight is at phone size (a 36 px kicker: "spotlight · a skill for AI coding agents");
  - the sample label reads at phone size (26 px tag on a 52 px bar) and the caption says "same sample data";
  - the loop excerpt is darkened so its faint install lines vanish, and the crop moved down;
  - the 4.0 s move is quicker (0.3 s), the Persian card arrives opaque by 4.25, the tag swaps mid-move, the pair lines up (the push eases back), and the caption lands at 4.3;
  - the loop is 1040 wide in square with its caption centred under it, and 1500 wide in landscape with the caption below; the line names spotlight;
  - the Codex card is cropped to its chart panel; the data caption fits one line, leaving ≥ 60 px above it in square; the landscape pair is 2 × 450x800; the end-card lines land after the wipe.
  Also: landscape measured a 0.8 s hold at 14.1 s (the finished diagram sitting still, its faint backdrop now darkened), so the loop clip trims that stretch and the beam's turnarounds moved into moving shots.
- **Round 2** (`critics/critic-2.md`, a fresh verification critic): ONE MORE PASS (3 fixes). Round 1's changes were FIXED except the 4.0 s transition (PARTLY). Fixed:
  - the landscape loop card was ~1520 px wide, breaking the fit-in-1080 rule: it is now 1040 wide in both formats;
  - from 4.0 both café cards play the promo from its 4.5 s cut, so its own cuts land on ours, and the caption lands at 4.15 (the move takes 0.2 s, so nothing collides);
  - "Tested on…" lands after the URL (21.1).
- **Round 3** (`critics/critic-3.md`, a fresh verification critic, the last round): **SHIP**. All three round 2 fixes are visible in both renders, and every rule holds in both. Left as they are (cosmetic): 5 text-free frames during the 4.0 s move, the card fade-ins at 7.0 and 13.0, the landscape hook kicker wrapping to two lines, a one-frame truncated card label at 4.03 s, and the landscape loop labels at about two-thirds their earlier size (the cost of the fit-in-1080 rule).
