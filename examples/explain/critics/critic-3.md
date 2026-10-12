# Critic 3: "Why spotlight checks its own videos"

My measurements:
- **Frames:** 1800 at 1920x1080, 30 fps.
- **Sound:** −14.2 LUFS, TP −2.2, LRA 3.0.
- **Glitches:** none; the biggest frame changes are all cut fades.
- **End card:** moves gently (53.5–60).
- **Cuts:** 3.6, 10.1, 18.3, 25.8, 34.2, 36.9 and 48.3 fade through black; 52.8 is a wipe.

## Critic-2 top changes
1. **Pulse only on connectors: FIXED.** From 43.8 to 46.0 the dot stays on the arrows and the return line, and each box fills as it arrives. Passing under "3 rounds max" (44.9–45.0), its glow clears the letters by about 5 px.
2. **Make 46.3–48.3 move: FIXED (subtle).** SHIP grows from about 150 to 157 px wide (≈1.05×), the backdrop scrolls, and the chime lands at 46.3.
3. **Critic evidence at the cut: FIXED.** The backdrop highlights "Dead air in the hook" from 25.9. Item 01 is on screen by 26.5; 02 and 03 follow the narration (30.0, 31.3).

## Critic-2's other defects
- **Pulse crossing labels: FIXED.**
- **Fades through black: STILL PRESENT (style).** One frame at Y=16 on each of 3.60, 10.10, 18.30, 25.80, 34.20, 36.90 and 48.30.
- **Half-empty frames: PARTLY (cosmetic).** The file ends at y≈820 (22–25.8) and y≈725 (34.5–36.9). That leaves 25–33% of the column empty, where critic-2 measured about 60%.
- **Takeaway over the doc column: STILL PRESENT (cosmetic).** The backdrop is blurred and dimmed (Y≈21), so the headline reads cleanly. The backdrop shows through it only in the fade at 52.6–52.9.
- **sources.md rows: FIXED.** It now has rows for "Verdict" and the "Source:" footers.
- **Phone-size text: STILL PRESENT (cosmetic).** Source lines have a cap height of about 24 px (≈33 px type). That's fine at 1080p but small in a phone feed.
- **"…buried · effects" tag: STILL PRESENT (cosmetic).**
- **pop-2 on the spoken "one" (34.65): STILL PRESENT (cosmetic).**
- **Opener: PARTLY, unchanged.** It's dark (Y≈35), with a slow scroll and no push-in.
- **Lull: PARTLY.** There's no voice from 45.0 to 48.4 (bed only, −19 to −23 LUFS), but the picture now moves.

## New defects
1. **pop-3 fires on a static chart (11.30). Real; a regression in sync.**
   - The bar values now land with the bars: "0.8s" is fully opaque at about 10.75 (frame 323), and "0.72s" at about 11.0 (frame 330).
   - From frame 331 to 347 nothing on screen changes, so the pop is 0.3–0.55 s after any visual event.
   - **Fix:** move pop-3 to about 10.75.
2. **The scrim edge rises into the takeaway (51.3–52.9). Real but faint.**
   - The blurred README backdrop scrolls past its end.
   - A lighter full-width band (Y 27.5 against 21) with a hard edge at y≈885 comes up into the bottom ~18% of the frame.
   - **Fix:** stop that scroll ~150 px sooner, or make the backdrop and scrim full height.
3. Nothing else turned up in the 0.25 s sheet or around the cuts: no overlaps, clipped text or other regressions.

## Message
On mute the story reads: question, measured, flagged its own demo, numbers passed, the critic found three things, ONE MORE PASS, the loop, the takeaway, spotlight and the URL. Every claim is sourced on screen.

## Verdict: ONE MORE PASS
Make exactly two fixes:
1. Move pop-3 to about 10.75.
2. End the takeaway backdrop scroll before the scrim edge enters, or make the backdrop and scrim full height.

Each is a one-number change, and a measure re-check is enough after that, with no further critic round. Leave everything else above alone: it's cosmetic or style.
