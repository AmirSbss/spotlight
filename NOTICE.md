# Third-party work in spotlight

| What | Where | Licence |
|---|---|---|
| brag (latent-spaces/brag): creative rules, music-cue analyser | `skills/spotlight/scripts/analyze_music_cues.py`, `references/brag.md` | MIT |
| motion-video-kit (echris6/motion-video-kit): critic loop, quality bar, frozen-time measurement approach, SFX gain solver and offline mix | `references/critic.md`, `references/quality-bar.md`, `footage.py check`, `scripts/mix.py` | MIT |
| gpt-image-bridge (oakplank/gpt-image-bridge): optional, not bundled | used only if installed | MIT |
| three.js 0.170.0 (mrdoob/three.js): `three.module.min.js` and the `SVGLoader` addon | `skills/spotlight/kit/three/` (licence in `LICENSE` there) | MIT |
| Natural Earth 1:110m land (naturalearthdata.com, v5.1.2), baked into land dots | `skills/spotlight/kit/three/land-dots.js` | Public domain |
| "Montage" by wipics ([OpenGameArt](https://opengameart.org/content/montage)): music, 17.47 to 42.47 s | `examples/demo/video.mp4` (audio only; the track itself isn't in the repo) | CC0 |
| "Dancing" by Holizna (bundled as `assets/music/calm.mp3`): music, 18.5 to 78.5 s | `examples/explain/video.mp4` | CC0 |
| Piper voice `en_US-ljspeech-high`, trained on LJ Speech: narration | `examples/explain/video.mp4` | Public domain |
| Footage and logo of Mahoor Coffee (@mahoor_hills) | `examples/promo/` (video.mp4, video-fa.mp4, poster.jpg, preview.gif) | © Mahoor Coffee, used with permission; not covered by spotlight's MIT licence |
| "Love Train" by Loyalty Freak Music (bundled as `assets/music/warm-acoustic.mp3`): music, 46.25 to 66.25 s | `examples/promo/video.mp4`, `examples/promo/video-fa.mp4` | CC0 |
| Cinzel, Cormorant Garamond, Jost, Vazirmatn (Google Fonts) | rendered into `examples/promo/` | SIL OFL 1.1 |
| Space Grotesk, Inter, JetBrains Mono (Google Fonts) | rendered into `examples/demo/video.mp4` and `examples/explain/video.mp4` | SIL OFL 1.1 |

The bundled music (`skills/spotlight/assets/music/`) and sound effects (`skills/spotlight/assets/sfx/`) are CC0. Each file's author, source page and licence statement are in the `LICENSES.md` beside it.

Piper (narration, `piper-tts`, GPL-3.0) is not bundled. `voice.py` runs it as a separate program, and downloads voices on first use; each voice carries its own licence (`skills/spotlight/references/sound.md`).
