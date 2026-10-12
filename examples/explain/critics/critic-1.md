# Critic 1: "Why spotlight checks its own videos"

Measured: 1800 frames, −14.5 LUFS, TP −2.3, 0 holds. Mean luma is Y 21–45 (of 255) until 54.5 s, then 219 on the end card.

## 1. Sections
**0–4.5 Hook.** White question over a README dimmed nearly black (Y≈25). It is dark and inert: the backdrop scroll can't be seen, against quality-bar.md's "Openers are bright and clear". The voice ends at 2.81, leaving 1.7 s of an unchanged card.

**4.5–11.2 Measured.** Clean and readable. Highlighted backdrop lines are clipped at the pane edge ("no hold over 0.6 s w").

**11.2–19.5 Demo flagged.**
- The panel idles with only its label until the bars arrive at 13.9.
- The bars count up through 0.20s, 0.4s, 0.54s, 0.67s and 0.71s (13.9–14.85). These values aren't sourced, and the brief says no invented numbers.
- Both bars are the same yellow, so "over" isn't shown.
- Backdrop line 27 is clipped.

**19.5–27.0 Draft passed.**
- The title "A critic sees the rest" sits over `"holds": []` / `"failures": []`. On mute that reads as "the critic found nothing", which inverts the point.
- "BRAG DRAFT" is jargon.
- The evidence arrives late, at 23.3.
- From about 23 s the backdrop scrolls into **check-brag-final.json** under a "draft" label.

**27.0–38.0 Critic + verdict.** Only the label shows for 2.5 s. "Five of eight are buried": five of eight *what*? "ONE MORE PASS." is strong.

**38.0–49.5 Loop.**
- 38.0–39.4 is near empty: a tiny corner label on a Y≈21 frame, against "No empty frames".
- The diagram is good, but it is finished at 45.8, and from 46.1 to 49.3 it holds static with no voice.

**49.5–54.5 Takeaway.** Readable; 49.5–50.0 is black.

**54.5–60 End card.** The URL is large and on screen for 5.5 s. The light card is a hard style break.

No collisions, faces or third-party logos.

## 2. Message
On mute, a stranger gets "it measures, a critic reviews, it loops, github URL". Neither the screen nor the voice ever says spotlight *makes videos*. The 02 beat inverts the core pivot. I grep-checked every on-screen string against `inputs/`; all are sourced except the count-up values.

## 3. Sound
- Narration sits 13–16 dB over the ducked bed on every line and is clear.
- The music plays to 59.2, then fades over 0.8 s, which is correct.
- **No effect is buried.** Each one is 15–25 dB over its masker in at least one band above 1 kHz.
- The whooshes peak within 10 ms of the cuts at 4.5, 19.5, 38.0 and 54.5.
- pop-2 (verdict) and the chime (SHIP) sit on real actions, not stings.
- **pop-3 fires at 14.99, 7 frames before its warning line appears (15.23).**
- Cosmetic only:
  - cut-to-beat offsets of 0.15–0.25 s at 19.5, 38.0 and 54.5
  - pop-2 is the loudest effect (−16.6 dBFS) and lands on the spoken "one"

## 4. Top 6 changes
1. **Fix the 02 pivot.** Title 19.5–27.0 "The numbers passed" and use "02 · A draft" as the label. Move "A critic sees the rest" to 27.0. End the backdrop scroll before the check-brag-final.json header enters (`[1800, 2470]` → ≤ ~2000).
2. **Bright, moving opener.** Open on a page at EV brightness with a push-in on the demo's highlighted warning, and put the question over it. Cut at about 3.3 and pull a1 forward.
3. **Evidence at the cut, no count-up.** Bars at their final values by 11.6, holds/failures by 20.3, critic item 01 by 27.6, Render box by 38.3. Wrap backdrop lines (`pre-wrap`).
4. **Fill or cut 46.1–50.0.** Either run a pulse around the loop and out to SHIP, or start t1 at about 47.0 and pull the end card up about 2.5 s. Drop the black frames at 49.5.
5. **Say what it is.** Under the URL, add README line 3: "Point your AI agent at a website, some footage or a topic, and get back a finished short video."
6. **pop-3 to 15.23**, or bring the warning line in at 15.0.

**ONE MORE PASS.** The inverted 02 pivot, the dark opener, the near-empty 38.0 frame and the 46–50 lull each break the message or a quality-bar line.
