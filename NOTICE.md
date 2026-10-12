# Third-party work in spotlight

| What | Where | Licence |
|---|---|---|
| brag (latent-spaces/brag): creative rules, music-cue analyser | `skills/spotlight/scripts/analyze_music_cues.py`, `references/brag.md` | MIT |
| motion-video-kit (echris6/motion-video-kit): critic loop, quality bar, frozen-time measurement approach, SFX gain solver and offline mix | `references/critic.md`, `references/quality-bar.md`, `footage.py check`, `scripts/mix.py` | MIT |
| gpt-image-bridge (oakplank/gpt-image-bridge): optional, not bundled | used only if installed | MIT |
| three.js 0.170.0 (mrdoob/three.js): `three.module.min.js` and the `SVGLoader` addon | `skills/spotlight/kit/three/` (licence in `LICENSE` there) | MIT |
| Natural Earth 1:110m land (naturalearthdata.com, v5.1.2), baked into land dots | `skills/spotlight/kit/three/land-dots.js` | Public domain |
| "Montage" by wipics ([OpenGameArt](https://opengameart.org/content/montage)): music, 17.47 to 42.47 s | `examples/demo/video.mp4` (audio only; the track itself isn't in the repo) | CC0 |
| "Documentary Music - Small Signs of Change", music by Sascha Ende at ende.app (bundled as `assets/music/calm.mp3`): 11.84 to 71.84 s | `examples/explain/video.mp4` | CC BY 4.0 |
| Piper voice `en_US-ljspeech-high`, trained on LJ Speech: narration | `examples/explain/video.mp4` | Public domain |
| BudTech's website pages, photos and logo (budtech.om) | `examples/website/`, and the BudTech video shown inside `examples/brag/` | © BudTech LLC, the author's company, used with permission; not covered by spotlight's MIT licence |
| "Happy Beats & Business Moves Vol. 1", music by Sascha Ende at ende.app (bundled as `assets/music/upbeat.mp3`), edited on bar lines | `examples/website/video.mp4` | CC BY 4.0 |
| Inter and Noto Kufi Arabic (Google Fonts) | rendered into `examples/website/` | SIL OFL 1.1 |
| Footage and logo of Mahoor Coffee (@mahoor_hills) | `examples/promo/` (video.mp4, video-fa.mp4, poster.jpg, preview.gif), and the café promo shown inside `examples/brag/` | © Mahoor Coffee, used with permission; not covered by spotlight's MIT licence |
| "Sunday Morning Coffee", music by Sascha Ende at ende.app (bundled as `assets/music/warm.mp3`): 20.76 to 40.76 s | `examples/promo/video.mp4`, `examples/promo/video-fa.mp4` | CC BY 4.0 |
| "The Show Begins Vol. 8", music by Sascha Ende at ende.app (bundled as `assets/music/upbeat-rock.mp3`), from 5.0 s | `examples/brag/video.mp4`, `examples/brag/video-square.mp4` | CC BY 4.0 |
| Cinzel, Cormorant Garamond, Jost, Vazirmatn (Google Fonts) | rendered into `examples/promo/` | SIL OFL 1.1 |
| Space Grotesk, Inter, JetBrains Mono (Google Fonts) | rendered into `examples/demo/`, `examples/explain/` and `examples/brag/` | SIL OFL 1.1 |

The bundled sound effects (`skills/spotlight/assets/sfx/`) are CC0. The bundled music (`skills/spotlight/assets/music/`) is by Sascha Ende at ende.app, licensed CC BY 4.0, except `minimal-tech.mp3`, which is CC0. The `upbeat` tracks 1, 9, 10, 11 and 12 are the same files the brag skill bundles. Each file's author, source page and licence statement are in the `LICENSES.md` beside it.

Piper (narration, `piper-tts`, GPL-3.0) is not bundled. `voice.py` runs it as a separate program, and downloads voices on first use; each voice carries its own licence (`skills/spotlight/references/sound.md`).
