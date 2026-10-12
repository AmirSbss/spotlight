# Critic 4: Mahoor Coffee mood-line re-cut (EN + FA)

**Method:** all 600 frames of each cut; sheets every 0.25 s; every frame within ±7 of each cut; 1x crops of captions, kicker and end card. Extents measured by differencing the two cuts.

## 1. Landing and safe zones: PASS
- Each line fades out before its cut and the next lands after it. No frame holds two captions, nothing is clipped, and there are no orphans (the lone «امروز» is the authored break).
- Fully-landed holds: hook 0.07–4.3 s; "Today is…" ~5.0–7.3; "Take your time" ~7.8–9.7; "Better with…" ~10.3–12.7; "Here's to…" ~13.3–15.7; CTA 16.75–20; handle 17.25–20. All are well over 0.3 s per word.
- Captions run y 990–1356 and the end card to y 1398, clear of the top and bottom zones.
- English spans x 70–815. Persian lines end at x 922–925 and the kicker at 914, 45 px clear of the rail.

## 2. Persian rendering: PASS
- Joined, right to left, right-aligned.
- ZWNJ correct in «قهوه‌ی» and «می‌خوان».
- The comma «،» and the full stops sit at the left end, the right way round.
- The kasra in «سلامتیِ» renders under the final ye.
- MAHOOR COFFEE and @mahoor_hills are intact.

## 3. Copy: PASS
- The English is one warm voice with an arc: need, today, slow down, share, toast. The shots illustrate the lines rather than being described by them.
- No factual claims; every string matches sources.md.
- The Persian is natural colloquial Tehrani in one register; nothing reads machine-translated.
- Weakest line: «با حوصله.» ("patiently") leans toward describing the pour rather than addressing the viewer. «سر فرصت.» is more direct. Preference.

## 4. Versus critic-3
- **Regression in margin, not a block:**
  - The Persian right inset fell from 150 px to 80 px. Lines end at x 922–925, not 843–856.
  - Rail clearance dropped from ~115 px to ~45 px. It still clears the brief's x ≈ 970.
  - Likely cause: «یه قهوه‌ی خوب می‌خوان.» is ~840 px wide.
- **Side effect:** the Persian kicker's "COFFEE" now sits over pale bottles at 2.0–4.5 s. It is softer but legible at 1x.
- **Change, not regression:** the CTA moved from «ما را در…» to «ما رو تو…», which matches the thread.
- Everything else critic-3 verified still holds.

## Verdict: SHIP
**Real defects:** none.

**Optional, if another pass happens anyway:**
1. Set the Persian lines at about 78 px, or shrink line 1 alone, to restore the 150 px inset.
2. «با حوصله.» → «سر فرصت.»
3. A firmer shadow on the Persian kicker at 2.0–4.5 s.
