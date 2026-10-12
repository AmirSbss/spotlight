# Critic 2: Mahoor Coffee promo (EN + FA)

I checked a frame every 0.25 s and every frame within 0.25 s of each cut, in both cuts, plus 1× crops. Both cuts share the same frames and audio (md5 identical): −14.0 LUFS, true peak −2.5 dB, LRA 0.8.

## Critic 1's changes
1. **Third-party marks.**
   - **s1: PARTLY.** "CIMBALI" is blurred. Below the box, "~ M23" and the swoosh are still readable at 1× from 0.0 to 0.6 s and fade by about 1.0 s (x≈780–840, y≈1010–1040). This is frame 0 of the hook.
   - **CAFFINA cup and barista shot: FIXED.** Both shots were dropped. I found no legible lettering in s2–s6.
2. **Cookie shot: FIXED.** It was dropped.
3. **End on a payoff: FIXED.** The finished latte runs 13.0–16.0. A blurred arm crosses the top at 15.4–16.0 (cosmetic).
4. **Captions raised: FIXED.** The lowest descender is at y=1355 (EN) and y=1334 (FA), so baselines sit at about 1325.
5. **Counter reframe (now 10.0–13.0): PARTLY.**
   - The drinks sit centre.
   - Frames 300–302 (10.00–10.07) still show two black gloves over the bottom ~450 px, faint on 303. That is a 3-frame flash on the cut.
   - A chin and beard show at the top right at 11.7–12.5. Cosmetic, since faces were approved.
6. **Sound.**
   - **Music shift: FIXED.** Strong hits now fall on the .0/.5 grid (mean onset z 3.95, against 2.89 on .25/.75). Every cut has an onset within 9 ms. At 2.0, 10.0 and 16.0 the hit 0.25 s earlier is 0.1–0.4 z stronger (cosmetic).
   - **Pop and handle at 17.0: FIXED.** The pop's onset has z 5.5 at 16.997.
   - **End-card drift: FIXED.** freezedetect finds no hold of 0.5 s or more.
   - **Live sound:** not done, with a stated reason (the clips' audio is the café's music). Accepted.
   - **s1 shaker motion blur and the TV-art eye:** still present, both cosmetic.

## New defects
**Real**
- **FA only: captions may sit under the Reels action rail.** Every Persian line and the kicker end at x=1004–1005 (y≈1110–1334), leaving the template's symmetric 75 px margin. The like/comment/share column sits at about x≈970–1060 there (estimated), covering each line's first letters. English starts at x=80, clear of UI.

**Cosmetic**
- The kicker sits at y≈1295 in s1, fades at 1.9 s, then returns at y≈1050 at 2.1 s. It reads as a blink and a jump.
- The logo's image edge shows as a 1–2 px line on the end card: luminance 240 against the card's 237. Effectively invisible.

No other glitch frames, no caption overlaps across cuts, no clipped text. The wipe at 16.0–16.33 is clean.

## Persian cut
- The letters are joined and run right to left, right-aligned to one edge.
- The first word of each line is the rightmost one: روی، کمی، ما.
- The Arabic comma sits at the left end of «اسپرسو،».
- «دست‌ساز» breaks correctly at the ZWNJ.
- Two-line order is correct.
- Nothing is reversed or clipped.
- MAHOOR COFFEE, the logo and @mahoor_hills are intact in Latin.
- The CTA «ما را در اینستاگرام دنبال کنید» is legible.

## Verdict: ONE MORE PASS
1. **s1:** extend the fascia blur box about 50 px down in source coordinates for all of 0–2 s, to cover "~ M23" and the swoosh.
2. **s5:** move the in-point of video_718a775c1040.mov from 0.30 to about 0.45 s, keeping the cut at 10.0, to drop the glove frames.
3. **FA:** give the right-aligned captions and the kicker a right inset of about 150 px, keeping them right-aligned.

The rest is preference.
