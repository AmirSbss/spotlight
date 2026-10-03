# spotlight — design

Date: 2026-10-02 · Status: draft for review · Successor to /promo v1.1 (this repo), built on brag (MIT) and ideas from echris6/motion-video-kit (MIT)

## Goal

**spotlight** is a skill for any AI agent. Give it a website, some footage or photos, and a description, and it makes a video that **brags** (a launch), **promotes** a point, or **explains** a topic (a presentation). It ships as a public, MIT-licensed GitHub repo: `AmirSbss/spotlight`, command `/spotlight`.

## Decisions (from the user)

| Topic | Decision |
|---|---|
| Name | `spotlight` (repo `AmirSbss/spotlight`, skill and command `/spotlight`) |
| Release | Public GitHub repo under the user's account. PR latent-spaces/brag#44 gets closed with a note pointing at it. |
| Approach | One skill, one pipeline and render kit, three modes: `brag`, `promo`, `explain`. |
| Presentation | A longer explainer **video** (60–180 s) with sections, charts and diagrams. No live presenter or slides export. |
| Music | Bundle CC0 music, with each licence verified and recorded. A user track overrides it. |
| Voice | Optional local TTS (`--voice`) with Piper. Captions are always on screen. |
| Sound effects | Yes: a curated CC0 set, levelled per event. |
| 3D | Three.js scenes in the kit, deterministic, used where 3D explains something. |
| Agents | Portable `SKILL.md` with install paths for Claude Code, Codex, opencode, Cursor, Gemini and others. |

## Non-goals

AI video generation (image-to-video); live presenter or slide export; uploading or publishing renders; rendering several languages in one run; photoreal 3D product heroes; a GUI.

## Inputs and modes

`/spotlight [inputs…] [--mode brag|promo|explain] [--tone …] [--format vertical|landscape|square] [--duration s] [--lang code] [--voice] [--music file|none] [--no-sfx] [--no-ai]`

Inputs are any mix of:
- **a URL**, which gets captured as the brand's site (copy, colours, fonts, logo, screens);
- **a folder or files**: photos, video, audio, `logo.*`, `brief.md`, and `*.csv`/`*.json` data for charts;
- **a project directory** of code, read the way brag reads it;
- **a description in quotes**, which is the brief.

The mode is inferred and overridable:

| Mode | Inferred when | Structure | Length | Tones |
|---|---|---|---|---|
| `brag` | the input is a code project or a website and nothing else | Hook → reveal → 2–3 highlights → punchline / CTA | 15–25 s (default 20) | default, polished, yc-parody, chaotic, deadpan, cinematic, app-store |
| `promo` | footage or photos are the main material | Hook (strongest moving shot) → what it is → best moments → offer / proof → CTA | 15–30 s (default 20; longer on request) | default, premium, energetic, recap, cinematic |
| `explain` | a topic or argument, data, or the user says presentation/explainer | Hook question → 3–5 sections (claim → evidence: chart / diagram / footage / site) → takeaway → CTA | 60–180 s (default 90) | clear (default), documentary, keynote |

Formats: vertical 1080×1920 (default for brag and promo), landscape 1920×1080 (default for explain), square 1080×1080. All at 30 fps.

## Pipeline

1. **Gather.** `footage.py prep` (exists) for media. `site.mjs` for URLs. Reading code for projects. Data files are parsed for charts.
2. **Brief.** Write `brief.md`: what it is, who it's for, the one action, facts **with their source** (brief, site page, footage, data file), and don'ts. Ask one question only if the name, CTA or language is still unknown.
3. **Plan.** Write `plan.md`:
   - a shot or section list with sources and on-screen text;
   - the narration script, when there is voice;
   - the music choice and cue times;
   - the SFX plan;
   - the AI assets table.
   Durations add up to the target, and the reading-time rules hold.
4. **Build.** Fill the kit: `timeline.js` and `scene.html`. Footage shots come from `footage.py shot`, site shots from captured screens, and charts, diagrams and Three.js scenes from kit modules.
5. **Sound.** `voice.py` renders the narration lines and their durations feed back into shot timing. `mix.py` mixes music + SFX + live clip audio + voice into `mix.wav` and `music-only.wav`.
6. **Capture and encode.** `capture.mjs frames`, then `footage.py encode` (exists).
7. **Check.** `footage.py check video.mp4` gives frozen stretches, loudness (I / LRA / TP), frame count and size, and a timestamped contact sheet. All of it is measured against the quality bar.
8. **Critic loop.** If the agent can start a fresh sub-agent, that agent judges the rendered video (`references/critic.md`, full-film prompt), the fixes are made, and a new agent verifies them item by item. At most 3 rounds. Otherwise, a self-review against the same checklist using fresh frames.
9. **Deliver.** `spotlight-output/` (timestamped if it already exists) contains:
   - `video.mp4` (poster embedded as cover art);
   - `poster.jpg`;
   - `caption.txt`;
   - `plan.md`;
   - `sources.md` (every on-screen claim → its source; AI ledger);
   - `music-only.mp4` when SFX or voice are present;
   - `work/`.

## Components and interfaces

```
spotlight/                                  public repo, MIT
├── skills/spotlight/
│   ├── SKILL.md                            core workflow + rules (lean; loads one mode file)
│   ├── references/  brag.md · promo.md · explain.md · sound.md · three.md · critic.md · quality-bar.md
│   ├── scripts/
│   │   ├── footage.py      prep · shot · encode (exist) + check · track
│   │   ├── capture.mjs     stills · frames (exists)
│   │   ├── site.mjs        URL → work/site/{copy.json, brand.json, screens/NN.png, assets/}
│   │   ├── mix.py          music + sfx + clip audio + voice → mix.wav, music-only.wav, mix-report.txt
│   │   ├── voice.py        Piper TTS: lines.json → line wavs + durations.json
│   │   ├── doctor.sh       checks ffmpeg/zscale, ImageMagick, python3, node, chromium, uv, piper (optional)
│   │   └── analyze_music_cues.py, pyproject.toml, uv.lock   (from brag; uv deps for mix/voice/cues)
│   ├── kit/  scene.html · kit.js · charts.js · three/{three.module.min.js, routes.js, extrude.js}
│   └── assets/  music/{*.mp3, cues/, LICENSES.md} · sfx/{*.ogg|wav, LICENSES.md}
├── tests/          test_footage.py · test_capture.sh · test_kit.sh · test_site.sh · test_mix.py · test_voice.sh · test_three.sh · fixtures/
├── examples/       one small publishable demo per mode (video.mp4, poster.jpg, plan.md)
├── docs/           other-agents.md
├── .claude-plugin/ plugin.json, marketplace.json
├── .claude/skills/spotlight, .agents/skills/spotlight, .opencode/skills/spotlight → ../../skills/spotlight
└── README.md · LICENSE (MIT) · NOTICE.md (third-party credits and licences)
```

### `footage.py check <video> [--end-card s]`
Prints and writes `check.json`:
- duration, frames, size, fps, codecs;
- integrated loudness, LRA and true peak;
- **frozen stretches**: luma frame-difference below a threshold, sampled at 10 fps (approach from motion-video-kit). It lists holds over 0.6 s and the total, with the last `--end-card` seconds exempt;
- `check-sheet.jpg`: a contact sheet with timestamps.

Exits non-zero when a hard limit fails: frame-count mismatch, TP > −1 dBTP, or integrated loudness more than ±1 LU off target. Warnings (frozen time over budget, LRA under 3 for energetic tones) don't fail it.

### `footage.py track <audio>`
Short-term loudness per second, plus tempo and strong cues when the cue analyser is available. Used to choose a music window, for example a soft intro with the lift on the key beat.

### `site.mjs <url> <workdir> [--size WxH]`
- Loads the page in Chromium, dismisses common cookie and overlay banners (best effort), and scrolls to trigger lazy and animated content.
- Saves the rendered `page.html`.
- Saves screens at the output aspect, one per section (`screens/NN.png`), and one tall full-page capture for scrolling shots.
- Writes `copy.json`: title, meta and OG tags, headings in order, paragraphs, CTAs, nav.
- Writes `brand.json`: dominant background, text and accent colours from computed styles; font families; logo and hero image candidates, downloaded into `assets/`.

### Kit additions (`kit.js`, all pure functions of t)
- **`web` shot:** `{ web: "site/screens/full.png", scroll: [y0, y1] }`. The real site in motion: a tall capture scrolled with eased motion, with an optional cursor and click marker.
- **`chart` layer:** DOM in `scene.html`, `.chart[data-kind=bar|line|number|donut][data-values][data-a][data-b]`. Bars and lines grow, and numbers count up, from the given data only. Driven by `charts.js`.
- **`diagram` layer:** inline SVG whose `[data-at]` paths draw in (stroke-dashoffset) and whose nodes pop in at their times.
- **`three` shot or layer:** `{ three: "three/routes.js", params: {…} }`. The module exports `create(canvas, params, {width, height})` → `{ render(tLocal) }`. No clocks, no unseeded randomness, no physics history. The kit mounts a WebGL canvas and calls `render(t - a)`. It ships with:
  - `routes.js`: a globe or flat map with points and great-circle routes drawing in, plus labels projected from 3D anchors;
  - `extrude.js`: an extruded logo, word or shape with a slow camera move.
  `capture.mjs` launches with a software WebGL flag when a page uses three.
- **Text-card motion:** list and slot cards sit on a moving backdrop (a blurred clip, or a still with drift ≥ 6%) so they never read as frozen.

### `mix.py`
Input is `work/mix.json`:
- `{ music: {file, start, fade_in, fade_out, gain_lufs} }`;
- `sfx: [{file, t, target_db, cap_db}]`;
- `clips: [{file, start, dur, t, gain_db}]`;
- `voice: [{file, t}]`;
- `duration`.

Behaviour:
- **Music** is levelled to a bed target: lower under voice, with ducking −8 dB and 150 ms ramps around each voice line.
- **Each SFX gain is solved** so its peak in its own frequency band sits `target_db` (default +3.5) over the music in the same window. The 2–8 kHz lift is capped at 4 dB, the peak capped at +6 dB over the local music peak, and a level floor stops effects vanishing over quiet passages. The solver is adapted from motion-video-kit's `solve-sfx-gains.py` and `offline-mix.py` (MIT, credited).
- **Outputs:** `mix.wav`, `music-only.wav` and `mix-report.txt` (per-event in-band lift, 150 ms body, HF lift).
- Final loudness is left to `encode` (two-pass, −14 LUFS, TP −2.5).

### `voice.py`
- **Input:** `lines.json` (`[{id, text, lang}]`).
- **Output:** `voice/<id>.wav` + `durations.json`.
- Uses Piper. Voices are downloaded on first use into `~/.cache/spotlight/piper/`, one voice per language (shipped mapping: `en`, `fa`, `ar`, plus whatever Piper has for others).
- If Piper is missing, it prints the install command and exits 2. Without `--voice`, the skill never calls it.

## Sound design rules (`references/sound.md`)

Music matches the buyer's customers, not "tech launch". Calm for services, a pulse even when chill, and no vocals or epic risers.

SFX:
- one short, soft, rumble-free whoosh per real transition;
- clean UI ticks only on simulated actions (clicks, typing, toggles);
- pops on pins and badges;
- a soft chime on confirmation;
- density follows the tone (deadpan and premium are sparse; chaotic and energetic are dense).

Never add a sting over a music resolve. The music must not fade before the logo lands. A music-only fallback is always delivered.

## Assets and licences

- **Music:** 4–6 tracks covering calm, warm-acoustic, upbeat, minimal-tech and cinematic. Each one's source URL and licence statement go in `assets/music/LICENSES.md`, and only CC0 or public-domain tracks are allowed. Candidate sources: FreePD, OpenGameArt (CC0 filter), Wikimedia Commons. Pixabay and Incompetech are out (not CC0). Cue presets are generated with `analyze_music_cues.py`.
- **SFX:** a curated subset of Kenney (CC0) for UI, impacts and interface, plus verified CC0 whooshes. Each file's source goes in `assets/sfx/LICENSES.md`.
- **Code:**
  - brag (MIT): cue analyser and creative laws;
  - motion-video-kit (MIT): frozen-time and loudness approach, SFX solver, critic prompts and quality bar, all adapted with credit;
  - three.js (MIT, vendored and pinned);
  - Piper is not bundled; voices carry their own licences.
- `NOTICE.md` lists all of them.

## Rules (carried over and extended)

- **Truth.** Text, numbers and claims come only from the brief, the footage, the site, the project or the data files. Charts plot only the given data. Explainers cite their sources in `sources.md`.
- **No invented** prices, stats, testimonials or results. Third-party brands stay out of frame.
- **AI imagery** is only clearly illustrative and is labelled in the caption.
- **Privacy.** Nothing is uploaded. The only thing that leaves the machine is the optional AI prompt (and, for edits, the source still), and `--no-ai` stops it.
- **Quality bar.** Frame 0 is a finished composition. The video is clear with the sound off. Each beat lands, then exits fast. No hold over 0.6 s without motion, except the end card. Frozen time is ≤ 1 s per 30 s. The CTA is readable ≥ 1.5 s at phone size. Lists are equal-spaced and left edges aligned. Readable text stays on screen ≥ 0.3 s per word. Safe zones are respected.
- **Language.** Any language, including RTL and joined scripts. The kit rules carry over (`<bdi>`, no letter-spacing, animate by word or line).

## Testing

- Existing suites carry over: footage, capture, kit, bridge-skip.
- New tests:
  - `check` against synthetic videos with a known frozen stretch and known loudness;
  - `site.mjs` against a local fixture site (copy, colours and screen count extracted);
  - `mix.py` with synthetic music and a click (in-band lift within ±1 dB of target, HF cap respected, ducking depth under a voice line);
  - `voice.sh`, skipped without Piper (duration > 0 and the language voice resolves);
  - `three`: frame N rendered twice, in different capture orders, is pixel-identical, and the routes scene draws;
  - `charts`: bar heights match the data at the settled time.
- **Acceptance:** one demo per mode, built only from publishable material (brag: a fixture site; promo: CC0 footage; explain: a topic with a small CSV). Each passes `check`, goes through one critic round, and gets its README entry.

## Phases (each ships on its own)

1. **P1, core:** rename to spotlight; repo layout and agent packaging; mode references; `site.mjs`; `check`/`track`; text-card motion; critic loop; `sources.md`; doctor.
2. **P2, sound:** CC0 music and SFX with licences; `mix.py`; `voice.py`; sound rules.
3. **P3, visuals:** `charts.js`, diagrams, Three.js (`routes`, `extrude`) with software-WebGL capture.
4. **P4, release:** three demos, README, NOTICE, publish `AmirSbss/spotlight`, `npx skills add` check, close brag#44 with a note.

## Risks

- **WebGL in headless capture** (software rendering) may be slow. Mitigation: render three layers at their own resolution, and P3 measures it first.
- **CC0 music quality** may be limited. Mitigation: a user track always wins; choose a few good tracks rather than many.
- **Piper voice quality** varies by language (Persian is the one to check). Mitigation: voice stays opt-in, and captions are always on.
- **Scope.** Mitigation: phases ship separately; each has its own plan and tests.
