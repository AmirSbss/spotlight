# Critic 2: spotlight brag (square primary + landscape)

The evidence is in `brag/r2critic2/`:
- every frame of both renders (`sq/`, `ls/`);
- 0.25 s sheets (`sheet-{sq,ls}-*.jpg`);
- every frame around each transition (`tr-t1…t7-{sq,ls}.jpg`);
- native crops (`c-*.png`, `n-*.png`) and a phone-size strip (`phone390.png`);
- per-frame luma (`yavg-*.txt`) and the audio null tables (`null-table.txt`, `wavnull.txt`, `musnull.txt`).

## 1. Round-1 items

### Gating
1. **Square kickers wrap: FIXED.**
   - "1 · A LAUNCH VIDEO" runs 3.23–8.0 and "2 · A CAFÉ PROMO" runs 8.03–11.0. Each is one line in both renders, and neither repeats the body line.
2. **sources.md re-cite: FIXED.**
   - The README lines it cites now match the current README: 1, 3, 15, 16, 108, 111, 117.
   - Its other citations hold too:
     - `docs/other-agents.md` "Which agents were tested?" (line 55);
     - `budtech/…/plan.md` line 3, "the language picker is tapped…";
     - `cafe/…/plan.md` line 34, "the same frames and mix, with captions in Persian…";
     - SKILL.md "### Text in any language" (line 64) and its "by word" rule (line 70);
     - the budtech sources lines (3, 15, 21, 37).
   - ffprobe gives 20.0 s for all three source videos and 60.0 s for the explainer. The manifest lists 12 clips.
   - The People section now covers the hook's arm and wall art, the gloved hand (8–11) and the hands at the counter (11–14).

### Optional
3. **Loop.**
   - Inset: **FIXED.** At 16.0 the square card sits about 70 px in from each side.
   - Backdrop: **STILL PRESENT.** `BACK` is still `brightness(.32)`. Mean luma is 32 in the square and 29 in landscape for 14–18.5 (30 in round 1), and 43/37 on the end card. The last 9 s are still the darkest 40% of the video.
   - Caption: **PARTLY.** "Before you see it / Measured, then reviewed by a second AI agent." now carries README line 3. "Up to three rounds." still restates the diagram's "3 rounds max".
4. **End card "Free and open source": FIXED.** It is visible from 19.23 and full by 19.43.
5. **Hook tags: STILL PRESENT.** Only the case changed ("Launch video", "Promo"). They are about 20 px pills, about 7 px at 390 px phone width (`phone390.png`), and can't be read muted.
6. **Website end and timing.**
   - BudTech's own end card at 5.5–8.0: **FIXED.** It shows its logo, "Request a quote" (the press ring first appears at 6.700 and the click is at 6.70) and budtech.om. That is its own video, so the rules allow it.
   - Earlier captions: **PARTLY.** Critic 1 asked for 3.05 and 11.05.
     - Website: the kicker first shows at 3.233 and the body at 3.333.
     - Persian: the kicker first shows at 11.133 and the body at 11.233.
     - The caption-free stretches are now about 0.23 s and 0.13 s.
   - "spotlight." at 18.8: **FIXED.** It first shows at 18.833.
   - Empty navy: **FIXED.** It has shrunk from 18.77–18.93 to two frames, 18.767–18.800.

### Smaller round-1 points
- **Truncated labels: FIXED.** At 3.067 the label reads "BudTech · Launch video · 20 s", and at 11.033 "Mahoor Coffee · Promo · 20 s" (`c-sq-3.067.png`, `c-sq-11.033.png`).
- **"60 S"/"20 S": FIXED.** They now read "60 s explainer" and "· 20 s".
- **"skill" jargon: FIXED.** The kicker now reads "spotlight · videos made by your AI agent".
- **"Right to left, letters joined.": STILL PRESENT** (optional).
- **Source audio left out: FIXED, now measured.**
  - `music-only.wav`, nulled against the bundled `upbeat-rock.mp3` rebuilt from `mix.json` (5.0 s in, −10.7 dB, 0.05/0.8 s fades), comes out −inf everywhere except the fade edges (−56 dB).
  - `mix.wav − music-only.wav` is −inf everywhere except the nine effect windows.
  - So the mix holds only the bundled track and the effects, with no clip audio.
  - The square and landscape audio streams null to −inf: they are identical.

## 2. New defects
No glitch frames, overlaps, clipped text or unsupported claims.
- **Luma scan:** frame-to-frame jumps over 4/255 happen only at 1.5 (BudTech's own cut), 3.0, 5.5, 8.0 and 14.0, all planned cuts.
- **Pops:** the 35% opacity of the cards' first frames at 8.000 and 14.000 is the designed pop, not a glitch.
- **Holds:** every frozen hold is 0.2 s or less, within budget.
- **Layout:** in both renders, every card fits whole in 1080x1080 and no caption of ours touches a clip.

Minor and non-blocking:
- **Frame 0, square:** the line breaks as "A website and phone clips / in. Finished videos out.", which splits "clips in.". The column has room for "…clips in." on line 1 (about 790 of 936 px).
- **Landscape hook kicker:** it wraps as "spotlight · videos / made by your AI agent". Round 1's kicker wrapped too, so this isn't a regression.
- **5.5–8.0:** "Switched to Arabic through its own menu." stays up over BudTech's end card, after the menu is gone.

**Claims:** every line on screen traces to sources.md, and each source was re-read: the README, other-agents.md, SKILL.md, both businesses' plans and sources, and ffprobe. None of our text quotes either business's captions.

## 3. Sound
- **Levels:** both renders measure −14.1 LUFS, −2.5 dBTP, LRA 3.9.
- **Timing:**
  - Whoosh peaks land at 2.95, 8.0, 10.95, 14.0 and 18.65.
  - The click (3.85) and toggle (4.15) match the menu.
  - click-3 (6.70) lands on the button's ring.
  - The chime (16.8) plays as SHIP fills (16.833–17.0).
- whoosh-2 at 10.95 is still the faintest effect (residual peak −21 dBFS, against −12 for whoosh-3), as in round 1. It is not buried.

## 4. Captions: do they add what the picture can't?
Mostly yes. They add:
- the inputs ("A website and phone clips in");
- that the site was live and the menu its own;
- "12 phone clips and a logo";
- "the same timeline";
- that a second AI agent reviews the video before you see it;
- "free and open source" and the agents it was tested on.

Two lines only name what's on screen: "Right to left, letters joined." and "Up to three rounds."

## 5. Verdict
**SHIP.** Both gating items are fixed, and nothing new blocks. Optional polish, none of it blocking:
1. Break the frame-0 line after "in.".
2. Make the hook tags 28 px or larger, or tag the cards "From a website" / "From phone clips".
3. Raise the loop backdrop from .32 to about .5.
