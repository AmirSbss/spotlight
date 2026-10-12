# Critic 2: spotlight launch v2 (square reel + landscape)

**Method:**
- Pulled all 720 frames of both files. Built 0.25 s sheets and every-frame strips at 3.73–4.73, 6.77–7.23, 9.77–10.23, 12.77–13.23, 19.27–20.07 and 20.77–21.23.
- Checked the loop card for leftover explainer text by raising its brightness 4× and 10×.
- Measured cap heights for the phone-size check.
- Ran a frame-to-frame difference scan for one-frame flashes.
- Measured 10 ms RMS of the mix against music-only: across the whole range, and within each effect's frequency band.
- Files are in `v2critic2/`.

Both `video.mp4` files have the same audio (same MD5). All five landscape every-frame strips match the square's timing.

The two `music-only.mp4` files decode to different MD5s, but they carry the same bed:
- their overall RMS is −16.87 and −16.96 dB;
- the difference between them is at least 21 dB under the music (−35 to −48 dB, following the bed);
- they were muxed separately, at 11:04 for v2 and 11:06 for the reel.

This is not a defect.

## 1. Round-1 top changes

| # | Round-1 ask | Status | Evidence |
|---|---|---|---|
| 1 | Hook says what spotlight is | **FIXED** | From frame 0 to 3.8 s an amber kicker reads "spotlight · a skill for AI coding agents". Its cap height is 26 px, about 9 px on a 375 px phone. It fades out from 3.80 to 4.00. |
| 2 | Sample label readable; caption "same sample data" | **FIXED** | The amber tag "SAMPLE DATA · FICTIONAL COURIER" shows on both cards, Codex 7.0–10.0 and Hermes 10.0–13.0. Its cap height is 20 px, about 7 px on a phone; round 1 measured about 5. The caption reads "Same prompt, same sample data." |
| 3 | Darken the explainer's ghost text; move the crop down | **FIXED** | At normal brightness the card is black around the diagram in both formats (f405, f470, f560). At 10× there are dots of at most 5/255 left of "Fix", and a sliver of at most 13/255 on rows 258–262 at the crop's top edge (square). Neither is visible in normal viewing. The "claude plugin install…" and "npx skills add…" lines are gone. |
| 4 | Fix 4.0–4.5 | **PARTLY** | See the breakdown below this table. |
| 5 | Loop layout and wording | **FIXED** | Square: the card is 1040 wide (x 20–1060). The gap from card to kicker is about 62 px, and the card and caption block runs from y 205 to 780. Landscape: the card is about 1520 wide. The line reads "spotlight measures every render." |
| 6 | Framing | **FIXED** | See the breakdown below this table. |

**Item 4, 4.0–4.5:**
- Fixed:
  - The tag swaps mid-move (f122, 4.07).
  - The Persian card ghosts for only 2 frames while it slides (f125 at about 17%, f126 at 50%). It is opaque by f128 (4.27).
  - The pair lines up: both cards are 360 wide with their tops at y 87 (f150).
- Still present:
  - **No text from f120 to f129 (4.00–4.30).** The kicker only starts at f130 (4.33) and the headline becomes legible around f134 (4.47). Round 1 asked for 4.05.
  - **The café promo's own cut still lands at f134→f135 (4.50).** That is 50 ms after the Persian slide settles (4.45) and on the frame the headline arrives. Move, slide and hard cut happen within 0.5 s. This is the largest frame difference in 0–7 s outside our own cuts (27.4).

**Item 6, framing:**
- Codex now starts on the cropped chart panel with the bars growing. The grey table is gone.
- Hermes has a 62 px gap (card bottom 698, kicker 760).
- The landscape pair is 2 × about 450 wide (x 840–1760).

**Round-1 blocking defects:**
- The sample label unreadable on a phone: **FIXED** (row 2 of the table).
- The explainer excerpt showing more than the diagram: **FIXED** (row 3 of the table).

**Other round-1 notes:**
- **f592 wipe sliced "spotlight.": FIXED.** The wipe runs 19.53–19.90 over the loop. "spotlight." only fades in from f599 (19.97), after the wipe ends.
- **"Tested on…" lands before the URL fills the gap above it: STILL PRESENT.** "Tested on…" lands f611–f616 (20.37–20.53). The URL lands f631 (21.03). For 0.5 s there is an empty hole of about 90 px between the tagline and "Tested on…".
- **7.00–7.10, grey card with an empty chart: FIXED** (no more grey table). What remains is the designed pop: f210, f211 and f212 show the card at 35%, 61% and 82% opacity, with the bars near zero and no caption. Together with the caption fading out at f207–f209, the cut reads as a 5-frame dip. The same happens at 13.0 (f387–f392). This is polish, not a glitch.
- **The loop implied Codex and Hermes used a fresh critic: FIXED in our text.**
  - Our caption is generic ("spotlight measures every render. Then a critic reviews it, up to three rounds.").
  - "Fresh critic" is the diagram's own text.
  - `docs/other-agents.md` line 57 says "Every run went through `footage.py check` and a critic review", so nothing on screen is false.
- **"12 phone clips" while the promo uses 5: unchanged.** sources.md sources it as the inputs. Not flagged.

## 2. New defects

- **No glitch frames** in either file.
  - The only frame-to-frame spikes are planned cuts or edits inside the café promo: f60 (café, 2.0), f135 (café, 4.5), f210, f300 and f390.
  - The card move shows as a smooth ramp (f121–f127).
  - The one flash candidate in square, f80, is the café camera moving: f79→f81 differs more than either single step.
- **No overlaps or clipped text.**
  - Every caption sits off the clips.
  - The labels fit in the 360 px pair cards.
  - SHIP stays inside the 1040 px card.
  - The café's lines stay inside the card. Their current renders match by MD5 (`cafe-md5.txt`).
- **Minor: the exit at 19.5 has about 0.5 s with no text.** The caption fades out at f582–f584, f585 shows the bare card, the wipe runs, and f593–f598 are plain navy. "spotlight." then fades in from 19.97. It reads as a breath and needs no fix.
- **Cosmetic, landscape:** the hook kicker wraps onto two lines ("spotlight · a skill for / AI coding agents") although there is about 400 px of free space beside it.

## 3. Rules

- **Codex CLI and Hermes Agent are named in text only.** The cards show their output videos, labelled as samples, with no product logos or UI. Pass.
- **Every card fits whole in 1080x1080 and no caption lies over a clip's text.** **FAIL in landscape. Square passes.**
  - The landscape loop card is about 1520 × 520 (x 200–1720 in ls/f560), so it does not fit in 1080x1080.
  - Neither the brief's Don't #1 nor the plan ("Every card fits whole in 1080x1080") limits the rule to the square.
  - Every other card keeps to it: the 16:9 cards are 992 wide in both formats, the landscape pair is 2 × 450, and the square loop is 1040.
  - Round 1's "about 1300" would also have broken it. A critic's suggestion does not override the user's rule.
  - The fix is a slot change only.
- **Only the explainer's loop diagram is used.** Pass; any residue is at most 13/255 and invisible.
- **Northwind Parcels is labelled as a sample wherever its data shows** (7.0–13.0, both cards). It is not on the end card. Pass.
- **Mahoor Coffee appears only as their own promo**, labelled "Mahoor Coffee · Promo / English / Persian". There is no customer or endorsement wording, and our text never quotes the café's lines ("Some days need a good coffee.", "Today is one of them."). Pass.

## 4. Sound (unchanged mix, both files)

- **Cuts:** every cut and the URL landing have a music onset at x.98 s, within 20 ms (4.0, 7.0, 10.0, 13.0, 19.5, 21.0).
- **Effects, measured against music-only:**

| Effect | Where it peaks | Level over the music |
|---|---|---|
| Whoosh-2 | 3.95 and 6.95 | about +11 to +12 dB broadband |
| Whoosh-1 | 12.99 | +14.6 dB in its band (2.7–11 kHz), so in-band it is not weak |
| Chime | rises from 18.21, peaks 18.33 | +28 dB in its band, over the quiet breakdown |
| Whoosh-3 | 19.64, mid-wipe | +17 dB in its band |

- **The chime sits on SHIP**, which fades in over f547–f553 (18.23–18.43).
- **Fade:** the bed holds through the URL and fades from 23.2 to 24.0.
- **Loudness:** −14.0 LUFS integrated and 4.2 LU loudness range, measured on both files. The −1.8 dBTP true peak is taken from check.json.

## 5. Phone-size reading (375 px feed width)

| Text | Cap height at 1080 | On the phone |
|---|---|---|
| Headline | about 36–42 px | about 13 px |
| Kicker | 26 px | about 9 px |
| "Tested on…" | about 24 px | about 8 px |
| Sub-lines ("Codex CLI, about 12 minutes", "Right to left, letters joined.", "Then a critic reviews it…") | 22 px | about 7.6 px, small but readable |
| Sample tag | 20 px | about 7 px, dark on amber |

The story reads on mute from the first frame: what spotlight is, a real café's promo, a Persian cut, two agents on sample data, the check loop, and the URL from 21.03.

## 6. Verdict

**Fixed:** both round-1 blockers.

**Clean:**
- the square (primary) breaks no rule;
- the audio is clean;
- there are no glitch frames.

**Still failing:** the landscape README render breaks the "fits whole in 1080x1080" rule with its 1520-wide loop card.

**Polish left:**
- the 0.33 s gap with no text at 4.0;
- the café's own cut stacked at 4.5;
- the 0.5 s hole above "Tested on…".

**ONE MORE PASS** (3 fixes):

1. **Landscape loop card: 1080 wide or less.**
   - Use the square's 1040, with the caption below.
   - It is a slot change in `scene.html` only; the timeline is shared.
2. **4.0–4.5:** play both café cards from 4.0 at café source t + 0.5 (4.5–7.5), and bring "THE SAME TIMELINE" in at 4.05.
   - **Why:**
     - the café's 4.5 cut then hides inside our 4.0 move;
     - its next cut, at 7.5 (scene scan: 2.0, 4.5, 7.5, 10, 13), lands on our 7.0 hard cut.
   - **What this needs:**
     - re-extract `frames/cafe_en`, which stops at source 7.0, and `frames/cafe_fa`, which covers 4.0–7.0, so both reach 7.5;
     - update the burned-in-text windows in sources.md. The Persian first line (fading out at 4.0–4.5) no longer shows.
3. **End card:** land "Tested on…" with or after the URL at 21.0, rather than at 20.35 (it is in place by 20.53).

If the user confirms the 1080x1080 rule applies to the square only, this is **SHIP** as is, and fixes 2 and 3 are optional polish.

Dropped as the weakest: the opacity pops at 7.0 and 13.0 (f210, f390).
