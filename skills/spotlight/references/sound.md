# Sound

Music, effects, live clip sound and narration, mixed by one script. Run it from `$OUT/work`:
`uv run <skill-dir>/scripts/mix.py mix.json` → `mix.wav`, `music-only.wav`, `mix-report.txt`.
The first run downloads its Python packages into uv's cache (about a minute); nothing is written into the skill folder.

## Music

The user's track always wins (`--music <file>`, or an audio file in the inputs). `--music none` renders a silent track. Otherwise, pick one bundled track by what the buyer's *customers* would want to hear, not by "tech launch":

Take the track for the tone; switch only when the customers clearly expect something else (a café launch is warm, not techno). The tone decides, not the subject: an explainer about a developer tool in `clear` still takes `calm.mp3`.

| Tone | Track |
|---|---|
| brag `default`, `chaotic`, `app-store`; promo `energetic`, `recap` | `assets/music/upbeat.mp3` (more in the same style: `upbeat-9`, `-12`, `-11`, `-10`; driving rock for a short opener: `upbeat-rock`) |
| brag `polished`, `yc-parody`; explain `keynote`; promo `default` for software or a developer product | `assets/music/minimal-tech.mp3` |
| promo `default` (cafés, shops, people, services) | `assets/music/warm.mp3` |
| brag `deadpan`; promo `premium`; explain `clear` | `assets/music/calm.mp3` |
| brag and promo `cinematic`; explain `documentary` | `assets/music/cinematic.mp3` |

Every track except `minimal-tech.mp3` is by Sascha Ende (ende.app), under CC BY 4.0: put "Music by Sascha Ende at ende.app" in `sources.md`, and in `caption.txt` when there's room. Never register a video's music with Content ID. `minimal-tech.mp3` is CC0. `assets/music/LICENSES.md` has every file's source and licence.

Measured shapes (track time). Start the window where the music already moves, unless the hook is meant to build into a lift:

| Track | Tempo | Length | Shape | Use |
|---|---|---|---|---|
| `upbeat.mp3` | 120 BPM | 164 s | full beat from the first bar, very even (−14 to −17 LUFS per 10 s); a short dip at 110–120 s; fades out 160–164 s | any start; strong cues run from 16 s; ends usable at 159 s |
| `upbeat-9.mp3` | ~115 BPM | 114 s | on the beat from 1 s; punchier (−12 to −13 LUFS at 20–50 s and 70–100 s); a dip at 50–60 s; ends at 110 s | a busier alternative for `chaotic` or `energetic` |
| `upbeat-12.mp3` | ~110 BPM | 117 s | lighter start 0–10 s, builds to its fullest at 80–100 s; ends at 115 s | start ~70 s so the lift lands on the reveal |
| `upbeat-11.mp3` | ~115 BPM | 88 s | even from the start; eases off in the last 10 s | a short alternative |
| `upbeat-10.mp3` | ~110 BPM | 60 s | one even loop, start to end | for videos ≤ 55 s |
| `upbeat-rock.mp3` | 120 BPM | 56 s | guitar riff from 5 s; full 10–50 s; ends at 52 s | for an energetic opener ≤ 45 s; start at 5 s |
| `minimal-tech.mp3` | ~120 BPM | 193 s | steady kick from the first second to 192 s | any start; long enough for a 180 s explainer, like `calm` and `cinematic` |
| `warm.mp3` | ~96 BPM | 145 s | lighter intro 0–20 s; full 20–80 s; a softer stretch 80–100 s; full 100–130 s; eases out 130–140 s | start at 20 s or later (a strong cue every 2.54 s from 20.2 s) |
| `calm.mp3` | ~110 BPM | 215 s | soft 0–30 s, building to full by 40 s; steady 40–190 s; eases out 190–210 s | start at 0–12 s to build under a hook, or at 40 s or later for a steady bed; covers a 180 s explainer |
| `cinematic.mp3` | uncertain | 239 s | soft 0–20 s, builds to ~40 s, then swings between soft and full; fullest 170–200 s; eases out 200–235 s | start at 0–20 s to build under a hook, or ~150 s so the peak lands on the reveal |

`assets/music/cues/<name>.json` holds each track's per-second loudness, tempo and strong cues (the output of `$F track --json`), so you can choose the window without measuring. For the user's own track, run `python3 $F track <file>`.
- Start where the track already moves (a pulse even when chill), so frame 0 isn't a fade-in from nothing: use the table's "Use" column, then fine-tune with the cue file.
- Let the lift land on the reveal or the CTA.
- For energetic tones, cut on the beats.
- No vocals and no epic risers.
- The music keeps playing until the end card has landed: never fade early. `fade_out` covers the last seconds of `duration`; keep it ≤ 1 s, so it starts after the end card is up.
- The window must reach the end. If `mix-report.txt` says `music runs out`, start earlier or pick a longer track.

## Effects (`--no-sfx` turns them off)

| File | Sound | Use |
|---|---|---|
| `assets/sfx/whoosh-1.ogg` | soft card swish, 0.6 s | a calm transition |
| `assets/sfx/whoosh-2.ogg` | fuller air swoosh, 0.5 s | an energetic transition |
| `assets/sfx/whoosh-3.ogg` | airy bright swell, 0.7 s | a reveal, a section change |
| `assets/sfx/click-1.ogg` | soft UI click | a button press |
| `assets/sfx/click-2.ogg` | light tick | a checkbox, a small selection |
| `assets/sfx/click-3.ogg` | crisp mouse click | a cursor click |
| `assets/sfx/click-4.ogg` | button press | a tap |
| `assets/sfx/type-1.ogg` | 2.5 s of real typing | a typed line (trim with the shot) |
| `assets/sfx/type-2.ogg` | one keystroke | short typing, one per key |
| `assets/sfx/toggle-1.ogg` | switch toggle | a toggle on |
| `assets/sfx/toggle-2.ogg` | brighter toggle | a toggle off, a second toggle |
| `assets/sfx/pop-1.ogg` | rounded pop | a pin or badge landing |
| `assets/sfx/pop-2.ogg` | softer, longer pop | a card appearing |
| `assets/sfx/pop-3.ogg` | short bright pluck | a number or tag appearing |
| `assets/sfx/chime-1.ogg` | soft confirmation chime | done, sent, booked |
| `assets/sfx/chime-2.ogg` | warmer, lower chime | a calmer confirmation |
| `assets/sfx/thud-1.ogg` | soft low thud | a heavy element settling |
| `assets/sfx/thud-2.ogg` | light knock | a light element settling |

- One short, soft whoosh per *real* transition: a change of scene or section, not every cut.
- Clean UI ticks only on simulated actions: a click, typing, a toggle.
- A pop on a pin, a badge or a number landing.
- A soft chime on a confirmation: done, sent, booked.
- Density follows the tone. Deadpan, premium, polished, clear and documentary are sparse (2–4 effects in a 20 s video); chaotic and energetic are dense.
- Never a sting over a music resolve, and nothing on the end card's last second.

Put each effect's `t` on the frame where the action happens (`frame / 30`). Whooshes swell to their peak 0.3–0.4 s in, so give every whoosh `"align": "peak"`: its loudest moment then lands on `t` (put `t` on the cut). Clicks, pops and chimes start on their hit, so leave them at the default.

`mix.py` sets every gain itself. In the effect's own frequency band, its peak sits `target_db` (+3.5 dB) over the music's peak in the same 150 ms, within caps: at most +4 dB in the 2–8 kHz band, and a broadband peak at most `cap_db` (+6 dB) over the music's. Over a quiet passage a `floor` lifts it to a level that stays audible, which can exceed those caps. But no effect ever peaks over the music's loudest moment (`music's top`): encode sets the music's loudness, so the music's top already sits at the true-peak ceiling, and anything louder would come out of encode's limiter crushed. The defaults are deliberately subtle: they sit with the music, the way a polished video sounds. For an effect that must punch (a `chaotic` tone, a big reveal), set its `"target_db": 6` (up to 9) and, if the report then says `peak cap`, `"cap_db": 9`.

## Live sound from clips

Add a clip's own sound only where it helps: a crowd, an espresso machine, a laugh. The entry is `{"file": "<clip>", "start": <in-point s>, "dur": <s>, "t": <s on the timeline>}`. `gain_db` is relative to the music bed. The default `-15` keeps it under the music; use `-6` for a moment that should be heard, such as the crowd at the peak. Clips fade in and out over 60 ms on their own.

## Narration (`--voice`)

Narration is off unless asked for, and the captions stay on screen either way. It suits `explain` best.
1. Right after the plan, write `work/lines.json`: `[{"id": "s1", "text": "…", "lang": "en"}, …]`, one entry per sentence or beat, with the text exactly as it should be spoken. Write numbers, years, prices and abbreviations the way they're said. Spell Latin brand names inside Persian or Arabic text in that script, as they're pronounced: Piper reads Latin words in those languages badly.
2. Run `python3 <skill-dir>/scripts/voice.py lines.json` → `voice/<id>.wav` (levelled to −16 LUFS) and `durations.json`. The first use of a voice downloads it, 60–115 MB, into `~/.cache/spotlight/piper/`. Piper never says a line the same way twice (a new take moves its length and pauses by up to 0.3 s), so a re-run speaks only the lines whose text or voice changed and keeps the other takes; delete `voice/<id>.wav` to force a new take of one line. It exits 2 with the install command when Piper is missing: tell the user, and render without narration.
3. Time the shots to the lines: each beat lasts at least its line's duration plus about 0.3 s, and lines never overlap. A caption that carries the same sentence lands with its line. Each wav starts on its first syllable and ends on its last. To land a bar, a row or a node on a word inside a line, split the line there, or find the line's pauses with `ffmpeg -i voice/<id>.wav -af silencedetect=n=-35dB:d=0.12 -f null -`.
4. Add each line to `mix.json` as `{"file": "voice/<id>.wav", "t": <s>}`. The music ducks under it on its own.
5. If `voice.py` prints a `credit` line, put it in `sources.md` and `caption.txt`.

The default voice for each language was chosen for its licence. A narrated promo is commercial use, and most Piper voices are fine-tuned from a research-only base.

| `lang` | Voice | Licence | Note |
|---|---|---|---|
| `en` | `en_US-ljspeech-high` | public domain | clear US female narrator |
| `fa` | `fa_IR-gyro-medium` | CC0 dataset (as declared) | understandable, but flat and sometimes wrong on ezafe and homographs: tell the user before you narrate in Persian |
| `it` | `it_IT-serena-high` | CC BY 4.0 | prints a credit line |
| `nl` | `nl_NL-alex-medium` | CC0 | |
| `uk` | `uk_UA-ukrainian_tts-medium` (speaker 0) | CC0 | |

- **Arabic, Turkish, Spanish, Portuguese, Russian, Polish, Chinese, Hindi:** no Piper voice with a clean licence. Render without narration unless the user names a voice and accepts its licence.
- **German, French:** the `de_DE-mls-medium` / `fr_FR-mls-medium` voices are CC BY 4.0 with hundreds of speakers. Set `"voice"` and `"speaker"` on the line after listening to a few.

For any other voice, set `"voice"` to a Piper voice name (huggingface.co/rhasspy/piper-voices) or to a local `.onnx` path, and check its model card's licence first.

## mix.json

Paths are relative to `mix.json` (so `voice/s1.wav` works) or absolute (bundled assets: `<skill-dir>/assets/…`).

```json
{
  "music": {"file": "<skill-dir>/assets/music/upbeat.mp3", "start": 12.0, "fade_in": 0.2, "fade_out": 0.8},
  "sfx":   [{"file": "<skill-dir>/assets/sfx/whoosh-1.ogg", "t": 3.0, "align": "peak"},
            {"file": "<skill-dir>/assets/sfx/click-1.ogg", "t": 6.4}],
  "clips": [{"file": "clips/IMG_0042.MOV", "start": 1.2, "dur": 2.0, "t": 8.0, "gain_db": -15}],
  "voice": [{"file": "voice/s1.wav", "t": 0.5}],
  "duration": 20.0
}
```

`duration` is the video's length (`duration` in `timeline.js`). Read `mix-report.txt` after every run, and fix the timing and re-run if any of these fails:
- no effect says `skipped`;
- there is no `music runs out` line;
- no voice line `runs past the end`.

An effect's line reads `gain -16.2 dB  in-band peak +9.6 dB (floor -22.0 dBFS: the music is quiet here); 2729-10917 Hz, 150 ms body  hf +7.3 dB  peak -9.2 dB`. Every dB after the gain compares the effect's peak with the music's in the same 150 ms: in the effect's own band (`in-band peak`), in 2–8 kHz (`hf`) and across all frequencies (`peak`). The bracket says what set the gain: `target`, `hf cap`, `peak cap`, `music's top`, or `floor`, a fixed level in dBFS that takes over where the music is quiet in that band (under narration, or in a calm track). Effects at `floor` are normal and audible, and their numbers over the music run high because the music is quiet there.

## Deliver

`mix.wav` goes into `video.mp4`. When the mix has effects or narration, also encode `music-only.wav` into `music-only.mp4`, with the same frames and poster. That is the version for a platform where the user adds their own sound or voice, so its music isn't ducked.
