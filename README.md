# spotlight

**Point it at a website, some footage or a topic. Get a video that brags, promotes or explains.**

spotlight is a skill for AI coding agents (Claude Code, Codex, opencode, Cursor, Gemini CLI and anything that reads `SKILL.md`). Give it any mix of a URL, a folder of photos and videos, a code project, data files and a description. It plans the story, cuts the material, sets the type in any language (right-to-left included), mixes the sound, renders, measures and critiques its own video before handing it over.

| Mode | Give it | You get |
|---|---|---|
| **brag** | a project or a website | a 15–25 s launch video built from the real product |
| **promo** | footage and photos (+ a brief or a site) | a 15–30 s promo where the real material is the star |
| **explain** | a topic, data, optionally a site or footage | a 60–180 s explainer: a presentation as a video |

```text
/spotlight https://example.com
/spotlight ~/media/opening-night --lang fa
/spotlight "why we moved support to async" data.csv --mode explain
```

Status: phase 1 of 4. Sound effects, a CC0 music library and narration (phase 2), charts, diagrams and Three.js scenes (phase 3), and demos (phase 4) are on the way. See `docs/superpowers/specs/`.

## Install
**Claude Code:** `claude plugin marketplace add AmirSbss/spotlight && claude plugin install spotlight@spotlight`
**Any agent (skills CLI):** `npx skills add https://github.com/AmirSbss/spotlight --skill spotlight`
**Manually:** copy `skills/spotlight/` into your agent's skills folder, or see `docs/other-agents.md`.

Then run `bash skills/spotlight/scripts/doctor.sh` to check requirements: ffmpeg 4.4+ with zscale, ImageMagick, Python 3.8+, Node 18+, Chromium. Optional: uv, and [gpt-image-bridge](https://github.com/oakplank/gpt-image-bridge) for AI illustration.

## What you get
`spotlight-output/`: `video.mp4` (poster as cover art), `poster.jpg`, `caption.txt`, `plan.md`, `sources.md` (every on-screen claim and where it came from, plus an AI ledger) and `work/`.

## Tests
```bash
python3 tests/test_footage.py && python3 tests/test_check.py && python3 tests/test_docs.py
bash tests/test_capture.sh && bash tests/test_kit.sh && bash tests/test_site.sh && bash tests/test_doctor.sh
```

## Credits
Built on [brag](https://github.com/latent-spaces/brag) (MIT). Critic loop and quality bar adapted from [motion-video-kit](https://github.com/echris6/motion-video-kit) (MIT). See `NOTICE.md`.
