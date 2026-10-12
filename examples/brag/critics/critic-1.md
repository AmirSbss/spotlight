# Critic 1: spotlight brag (square primary + landscape)

The evidence (frames, crops, luma and audio tables) is in `brag/r2critic1/`.

## 1. Sections

**Hook 0–3.0.** Square: two cards on top, captions under them. Landscape: captions left, cards right.
- (a) The tags "LAUNCH VIDEO"/"PROMO" are about 20 px, roughly 7 pt on a phone. A muted viewer can't tell which card is "a website" and which is "phone clips".
- (b) Four text blocks compete. Ours wins on size.
- Frame 0 is complete. The native crop shows no logos: the machine lettering is still blurred, and the face is wall art.

**Website 3.0–8.0.**
- (a) The square kicker wraps "WEBSITE IN, LAUNCH / VIDEO OUT" and repeats the body line.
- (b) 5.5–8.0 is 2.5 s of a network-switch photo under "Built from the live site". The picture stops supporting the caption.
- (c) 3.0–3.4 is a card with no caption, and 3.067 shows a truncated "BudT…".
- The click and the toggle match the tap ripples (3.867, 4.167).

**Clips 8.0–11.0.**
- (a) The square kicker orphans "OUT" ("PHONE CLIPS IN, PROMO / OUT"). This is the most visible flaw on the primary.

**Persian 11.0–14.0.**
- (a) 11.0–11.17 has no caption, and 11.033 shows a truncated "Mahoor Coff…". Nothing overlaps.
- (b) "Right to left, letters joined." only names what's visible.
- Only hands are on screen.

**Loop 14.0–18.5.**
- (a) Square: the card sits 17 px from the edges, while every other gutter is 72 px.
- (b) Mean luma is 30/255. With the end card (44), the last 9 s, about 40% of the video, are near-black.
- (c) The caption restates the diagram's labels.
- (d) "60 S"/"20 S": uppercase turns the seconds unit into a capital S.
- Only the diagram is used.

**End 18.5–23.0.**
- (a) 18.77–18.93 is empty navy.
- (b) The URL has no reason or verb next to it. It is readable at phone size and holds 3.5 s.

**Both renders:** every card fits whole in the frame and no caption sits over a clip's text. Landscape transitions are as clean as the square's.

## 2. Message
On mute, a stranger can tell what it is (frame 0) and what to do next (the URL). But "skill" is jargon, and the hook's input-to-output link rests on tags nobody can read.
- **Captions:** the Website and Clips beats add what the picture can't (the live site, its own menu, 12 clips and a logo). The Persian and Loop beats only label the screen. Nothing offers a feeling or an invitation.
- **Claims:** every claim holds against the current README (lines 1, 3, 77, 111, 117), `docs/other-agents.md:57` and ffprobe (20.0 s ×3, explainer 60.0 s).
- **sources.md:** it still cites quotes that commit 3e0f1d1 deleted: "line 9", "tested end to end on…", "This goes on for…", "second agent critique it". Its People section misses the gloved hand (8–11) and the hook's arm and wall art. Fixing both is a file edit, no re-render.
- **Hook:** the structure is right, proof at frame 0.

## 3. Sound
- **Music:** it plays full under the end card and fades from 22.2.
- **Cuts:** 3.0, 8.0 and 11.0 land on hits. 14.0 lands in the planned breath (13.85–14.8), with the whoosh covering it. "spotlight." (18.95) meets the hit at 19.0.
- **Effects:** every one sits on a real action. The chime plays as SHIP fills (16.83–17.0), and nothing stings over a resolve. whoosh-2 at 10.95 is faint, but not buried.
- **Source audio:** only build evidence shows it was left out (`mix.json` has no clips, and the report says "0 live-audio event(s)"). My null test didn't align, so it isn't measured.
- **Levels:** −14.2 LUFS, −2.4 dBTP.

## 4. Top 6 changes
1. **Gating.** Square kickers: shorten them to "WEBSITE → LAUNCH VIDEO" and "PHONE CLIPS → PROMO", or widen the column, so neither wraps.
2. **Gating, file only.** Re-cite `sources.md` to the current README lines. Add the explainer's 60.0 s ffprobe and the missing people.
3. **Loop.**
   - Inset the card to 72 px gutters (about 936 wide).
   - Raise the backdrop brightness from .32 to about .5.
   - Replace the captions with "A second AI agent reviews every video before you see it." (README line 3).
4. **End card:** add "Free and open source." above the URL (README line 3).
5. **Hook:** in the pair, tag the cards "FROM A WEBSITE" / "FROM PHONE CLIPS" at 28 px or more (both sources.md), so a muted viewer maps input to output.
6. **Website 5.5–8.0:**
   - Show BudTech's own end card instead (source 16.0–18.5: logo, "Request a quote" pressed, budtech.om).
   - Start captions during the moves (3.05, 11.05) and land "spotlight." at 18.8.

**ONE MORE PASS.** Items 1 and 2 gate it. Items 3–6 are recommended.
