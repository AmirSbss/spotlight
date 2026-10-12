# Critic 1: spotlight launch v2

**Method:**
- 4 fps sheets of both files.
- Every frame around each transition and around SHIP.
- Previews at phone size.
- 10 ms RMS, broadband and in band, of the mix against music-only.
- Files are in `v2critic1/`. Both renders have the same audio.

## 1. Sections

**Hook 0–4.0**
1. The only words saying what this is are the kicker "MADE WITH SPOTLIGHT", about 6 px tall on a phone. The headline is about the café. "AI" first appears at 19.75.
2. "12 phone clips" counts the inputs (sourced), but the promo uses 5.
3. Otherwise fine: the card fits, the café's text stays inside it, the blur box is intact, and no customer faces show.

**Persian 4.0–7.0**
1. 4.00–4.33 (f120–f130): there is no text, and one card slides through empty space.
2. The tag flips from PROMO to ENGLISH at f120, before the card moves.
3. f131–134: the Persian card ghosts in at partial opacity.
4. f135: both clips cut, so the whole change reads as a stutter.
5. The Persian card sits about 4 px lower and about 1% smaller, because the English card's push carries over.
6. Landscape: the pair fills under 40% of the width.

**Codex 7.0–10.0**
1. The clip's own grey table blurs about 45% of the card. At 7.00–7.10 the card is grey with an empty chart.
2. The "SAMPLE DATA · FICTIONAL COURIER" tag is about 5 px tall on a phone, which is unreadable.
3. The smaller caption lines are about 8 px tall on a phone, which is borderline.

**Hermes 10.0–13.0**
1. There is a 23 px gap between the card and the kicker; Codex had 77 px.
2. Same tag problem as Codex.

**Loop 13.0–19.5**
1. Faint explainer text shows behind the diagram, e.g. "claude plugin install spotlight@spotlight" and "npx skills add https://github.com/…". It is readable in landscape. The square crop also slices a line at its top edge.
2. Square: there is a 260 px empty band between the card and the caption. Landscape: the card fills about 16% of the frame.
3. Nothing new appears from 13.25 to 15.2.

**End 19.5–24.0**
1. f592: the wipe slices through "spotlight." for one frame.
2. "Tested on…" lands before the URL fills the gap above it.
3. The URL is readable from 21.03 to 24.0.

## 2. Message
On mute, a stranger understands it by the end card, where the URL holds for 3 s. Until 19.5 s, nothing readable on a phone says what spotlight is, and "two agents" stays vague.

Every caption is in sources.md, and the card tags match ffprobe (60 s and 20 s).

One claim is implied. `docs/other-agents.md` (lines 62–63) says Codex and Hermes each "reviewed its own render rather than starting a sub-agent". Going straight from them to "Fresh critic" suggests they got a fresh critic. The "It" in "It measures…" is unclear.

Rules:
- Pass: Codex and Hermes are named in text only, with no logos. Mahoor Coffee appears only as its own promo, and its lines are never quoted. All cards fit.
- Fail: the sample label is unreadable on a phone.
- Fail: the explainer excerpt shows more than the diagram.

## 3. Sound
- All six cuts fall within 20 ms of a music onset.
- Whooshes at 3.95 and 6.95: +7 to +12 dB.
- Whoosh at 13.0: it merges with the downbeat. Weak but harmless.
- Chime: +20 dB in its band, on SHIP at 17.97.
- Whoosh at 19.65: +16 dB in its band, mid-wipe.
- Every effect sits on a real event.
- The music holds through the URL and fades from 23.2 to 24.0. Correct.
- Loudness: −14.0 LUFS, −1.8 dBTP.

## 4. Top 6 changes
1. **Hook:** use a kicker of 30 px or more reading "Made with spotlight, a skill for AI coding agents" (README l.9), or put "spotlight" in the headline.
2. **Sample label:** change the caption to "Same prompt and sample data, two agents." and make the tag 26 px or more.
3. **Loop excerpt:** crush the ghost text (`colorlevels=rimin=.12:gimin=.12:bimin=.12` or `contrast(1.35)`), and move the crop's top edge down.
4. **4.0–4.5:**
   - Bring the kicker in at 4.05.
   - Slide the Persian card in opaque by 4.40.
   - Swap the tag with the motion.
   - Reset the English push to 1.0 so the pair aligns.
5. **Loop layout:**
   - Square: card 1040 wide, and centre the card and caption as one block (gap 80 px or less).
   - Landscape: card about 1300 wide.
   - Text: "spotlight measures every render."
6. **Framing:**
   - Start Codex at source about 4.0 and crop to the chart panel.
   - Give Hermes a gap of 60 px or more.
   - Landscape: pair at 2 × 450×800.

**ONE MORE PASS**
