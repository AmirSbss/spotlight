# Critic 3 (final round): spotlight launch v2, square reel + landscape

**Method** (all files in `v2critic3/`):
- Pulled all 720 frames of both files (`sq/`, `ls/`).
- Built 0.25 s sheets (`sheet-sq-0..3.jpg`, `sheet-ls-0..3.jpg`).
- Built every-frame strips around each transition: `tr-*-t4` (3.73–4.70), `t7`, `t10`, `t13`, `t195` (19.23–20.03) and `t21` (20.73–21.27).
- Ran a frame-to-frame difference scan on both files (`d-sq.tsv`, `d-ls.tsv`).
- Diffed every third frame against round 2's frames (`chg-*.tsv`).
- Scanned pixels for card edges.
- Checked the loop card at 8× brightness for leftover explainer text.
- Measured the mix against `music-only.mp4` in 20 ms windows: broadband (`rms.tsv`) and 2.7–11.5 kHz (`hb.tsv`).

**What changed since round 2.** Only three stretches differ from round 2:
- 4.00–6.90 (both files)
- 13.0–19.7 (landscape only)
- 20.4–21.3 (both files)

Every other frame matches round 2, which round 2 already found clean.

**Audio.** Both `video.mp4` files decode to the same audio (MD5 9d34300f…), and both `music-only.mp4` files decode to the same audio (MD5 31c6b26b…). The café sources match `cafe-md5.txt`.

## 1. Round 2's three fixes

| # | Ask | Status | Evidence |
|---|---|---|---|
| 1 | Landscape loop card no wider than 1080 | **FIXED** | The card sits at x 792–1847, y 361–720 (ls/f584), so it is 1056 × 360 at its largest drift scale. The caption is in a column to its left and ends at x ≈ 712, leaving about 80 px clear. Square is 12–1068. The 16:9 cards are 994 wide in both formats. **Every card in both renders fits in 1080x1080.** |
| 2 | Café from source t + 0.5 at 4.0; caption at 4.05 | **FIXED** (the caption lands at 4.15, not 4.05) | See the breakdown below this table. |
| 3 | "Tested on…" with or after the URL | **FIXED** | The URL starts at f631 (21.03) and is solid by f633. "Tested on…" starts at f634 (21.13). The URL and "Tested on…" slots stay empty below the tagline from 20.1 to 21.0, but the tagline has nothing below it yet, so the gap does not read as a hole. |

**Fix 2 in detail:**
- The café cut now lands inside our move. f120 (4.00) cuts to the pour, the card moves from f121 to f126, and the Persian card is opaque from f126.
- **The café's 4.5 cut is gone.** The biggest frame difference anywhere in 4.3–6.97 is 2.5 (square) and 2.2 (landscape); round 2 measured 27.4 at f135.
- The café's next cut falls on our 7.0 cut (f210).
- **The two cards are in sync to the frame.**
  - The test: compare card A at frame f with card B at f−1, f and f+1, for f = 135, 150, 170, 190 and 205.
  - At the same frame the RMSE is 1.4%. One frame off either way it is 3.7–5.7%, so the cards match only at the same frame.
- The Persian card shows only «امروز / از همون روزاست.», which matches the updated `sources.md`.
- **Gap with no text:**
  - The hook fades out from 3.80; f120 to f124 (4.00–4.13) have no text at all.
  - "THE SAME TIMELINE" fades in from f125 (4.17) and can be read by f127.
  - "…and a Persian cut." can be read by f130 (4.33).
  - The gap is now 5 frames, down from 10, and it falls inside the 0.2 s card move. Not worth another pass.

## 2. Round 2's remaining notes

| Note | Status |
|---|---|
| No text for 0.33 s at 4.0 | **PARTLY**: 0.17 s now (f120–f124), during the move. Fine. |
| Café's own cut stacked at 4.5 | **FIXED** (fix 2). |
| Hole above "Tested on…" | **FIXED** (fix 3). |
| About 0.5 s with no text at the 19.5 exit (f585 bare card, f593–f598 plain navy, "spotlight." from f599) | **STILL PRESENT**, as designed. It reads as a breath. Cosmetic. |
| Landscape hook kicker wraps onto two lines ("spotlight · a skill for / AI coding agents") | **STILL PRESENT**. Cosmetic. |
| Opacity pops at 7.0 and 13.0 (f210–f212, f390–f392: the card at about 35–80% with the caption out) | **STILL PRESENT**, unchanged. Cosmetic. |
| "12 phone clips" while the promo uses 5 | Unchanged. `sources.md` sources it as the inputs. Not flagged. |

## 3. New defects

**Nothing blocks shipping.**
- **No glitch frames.** Every frame-difference spike is a planned edit:
  - f60 (2.00): the café's own cut, inside its card;
  - f120–f127: our 4.0 cut and move;
  - f210, f300 and f390: our cuts;
  - f591–f593: the wipe.
  - Outside these, nothing is above 5.6.
- **No overlaps or clipped text** in either format. In both, the captions stay clear of every clip's own burned-in text.
- **Cosmetic, square f121 (4.03), one frame:** while card A narrows mid-move it still carries "PROMO · 20 S", so its name shows truncated as "Mahoor Coff…". The tag swaps to "ENGLISH" at f122. You cannot see it at speed.
- **Cosmetic, landscape loop:** with the card narrowed to 1056, the diagram labels are about two-thirds of their old size (the "Render" box text is about 20 px high at 1920). This is the price of the 1080 rule. They read fine at README size.
- **Leftover explainer text in the loop card, landscape:**
  - It is not visible.
  - At 8× brightness, ls/f405 shows faint residue, at most 4/255 left of "Fix" and 10/255 on the row under the window bar.
  - This matches round 2.

## 4. Rules (both renders)

- **Codex CLI and Hermes Agent: pass.** They are named in text only, with no logos or UI.
- **Every card fits whole in 1080x1080: pass.** Round 2's landscape failure is fixed.
- **No caption of ours over a clip's text: pass.**
- **Only the loop diagram from the explainer: pass.**
- **Northwind Parcels is labelled as a sample: pass.**
  - "SAMPLE DATA · FICTIONAL COURIER" is on both cards from 7.0 to 13.0, in both formats.
  - It is not on the end card.
- **Mahoor Coffee appears only as their own promo: pass.**
  - The cards are labelled "Mahoor Coffee · Promo 20 s / English / Persian".
  - There is no customer, testimonial or endorsement wording.
  - Our lines ("The same timeline", "…and a Persian cut.", "Right to left, letters joined.") quote none of the café's lines.

## 5. Sound

- **Loudness:** −14.1 LUFS integrated and 4.0 LU loudness range. The true peak is −1.6 dBTP (ebur128) and the sample peak is −1.85 dBFS. This matches `check.json`.
- **Effects, measured against music-only:**

| Effect | Where it peaks | Level over the music |
|---|---|---|
| Whoosh-2 | 3.94 and 6.96 | +9.0 dB and +7.2 dB broadband |
| Whoosh-1 | 12.98 | +9.2 dB in band |
| Chime | 18.32 | +14.0 dB broadband. It sits on SHIP, which fades in over f547–f553 |
| Whoosh-3 | 19.64, mid-wipe | +17.0 dB in band |

  These are 2–5 dB lower than round 2's figures because of my method, not because the effects changed. I ran the same 20 ms residual on round 2's own `v2critic2/mix.wav` and `mo.wav`, and it reads +9.4 dB at 3.94, +7.8 at 6.96 and +13.9 at 18.32, the same as now.
- **The master is not byte-identical to round 2:**
  - round 2 measured −14.0 LUFS, 4.2 LU and −1.8 dBTP; it is now −14.1, 4.0 and −1.6;
  - this is likely a re-encode after the limiter commit;
  - the change is too small to hear, and −1.6 dBTP is still below −1.
- **Bed:** about −16 dB RMS from 0 to 13 s, then the breakdown at about −18.5 dB from 13 to 21 s, and back to −16.3 dB as the URL lands.
- **Fade:** 23.2–24.0. The music is at −35 dB by 23.88.
- **End of the audio stream:** it ends at 23.957 s, 43 ms before the picture, deep in the fade. Inaudible.

## 6. Verdict

**SHIP.**
- All three of round 2's fixes landed: the landscape loop card is 1056 wide, the café's 4.5 cut is gone, and "Tested on…" now lands after the URL.
- Both renders keep every rule.
- There are no glitch frames, overlaps or clipped text, and the audio is clean.
- The square reel, the primary, carries the story on mute.

**Cosmetic notes, for later if at all:**
- the 5 text-free frames at 4.0;
- the opacity dips at 7.0 and 13.0;
- the landscape kicker wrapping onto two lines;
- the one-frame "Mahoor Coff…" at f121.
