# promo mode: real footage first

## Inventory and look

1. List the folder's media, subfolders included: photos, videos, audio files (music candidates), `logo.*`, and a brief file. Skip dotfiles and any `spotlight-output*/` folder from earlier runs (`prep` drops them too).
2. Run `python3 $F prep $OUT/work <files...>`. It writes:
   - `work/manifest.jsonl`: one line per file with `index`, `kind`, display `width`/`height` (rotation applied), `fps`, `duration`, `hdr`, `has_audio`, `cuts` (hard cuts inside a clip, in seconds), or `error` when a file can't be read. Tell the user which files failed and carry on without them.
   - `work/stills/NNN.jpg`: every photo decoded (HEIC, GIF and BMP too), upright, converted to sRGB (iPhone photos are Display P3) and metadata stripped so GPS never travels.
   - `work/sheets/`: contact sheets. `photos-NN.jpg` holds 12 photos labelled by index; `video-NNN.jpg` holds 12 frames per clip (the opening frame, then its scene cuts, up to 11, then evenly spaced frames) with the index and timestamp burned in.
3. **Look at the sheets, not the originals.** Read every sheet first. Only then open full-size stills, or pull a frame (`python3 $F shot <clip> <t> 0.034 <W>x<H> 0.5 work/peek/` at the clip's own size from the manifest, which tone-maps HDR the way the render will), for the candidates. This keeps big folders affordable. Judge like an editor: sharp, steady, well lit, subject clear, something happening. Drop blurry, shaky, dark and near-duplicate shots.
4. **The words.** Footage has no copy, so the text comes from:
   - the brief (`--brief`, or `brief.md` / `brief.txt` in the folder): name, what it is / the offer, who it's for, CTA (phone, URL, address, handle), lines that must appear, colors, font, language, don'ts;
   - text visible in the footage (signs, packaging, menus, screens);
   - the brand's own website, when the user points you at it: scrape a few key pages (home, about, services, contact) and quote them. Prefer its own wording in the promo's language (many sites have `/fa`, `/ar` versions) over translating.
   If the name, the CTA or the language is still unknown, ask **one** question that lists everything missing. Never guess a phone number, a price or an address.
5. Before planning, answer: What is it (one sentence)? Who is it for? What's the offer? What's the hero shot? What order tells the story? What's the CTA? Which tone? What does the story need that the footage doesn't show? What's the one-line caption?

## Shape

**Shape:** Hook (the strongest moving shot, 1–2s, not a logo) → what it is → 2–4 best moments → the offer or proof → CTA end card, held ≥2s. A starting shape, not a template.

**Everyone on screen when asked.** List every distinct person in the footage (by appearance, never by guessed name) and give each a clear, sharp moment, using a wide panel shot for group scenes so nobody is cropped out. Pre-edited clips (light leaks, dissolves) are usable only after their transitions; check the first frame after the cut.

Not enough material for the target length? Hold shots longer or make it shorter (15s is fine). Don't loop a shot, and don't pad with AI images.

## Tones

Presets are defaults. A freeform direction ("90s VHS travel ad") refines or overrides them.

| Tone | Feel | Cutting |
|---|---|---|
| `default` | Warm, upbeat, clean | 6–8 shots; soft cuts landing on beats |
| `premium` | Slow, elegant, lots of space | 4–5 long shots; slow push-ins; slow fades |
| `energetic` | Fast and punchy | 10–14 shots, some under 1s; hard cuts and zoom punches on beats |
| `recap` | Event highlights building to a peak | Many short shots, rough chronology; crowd sound up at the peak |
| `cinematic` | Trailer-scale | Wide shots, big type, dramatic wipes |

## Footage

- **Clips:** `python3 $F shot <clip> <start_s> <dur_s> <W>x<H> <cx> work/frames/<shot>/` writes exactly round(dur×30) upright JPGs (`00001.jpg`…), HDR tone-mapped to SDR, scaled to cover the frame and cropped at horizontal position `cx` (0 = left, 0.5 = center, 1 = right). Pick `cx` per shot so the subject stays in frame when landscape footage goes vertical. The manifest's `cuts` lists the hard cuts inside each clip; keep shots from straddling them. Start shots on stable, sharp moments.
- **Photos:** use `work/stills/NNN.jpg` as `still` shots and let the kit move them with a slow push-in (`push`; `origin` sets where it zooms toward, so an off-centre origin reads as a drift). It doesn't pan a cropped photo sideways: for a landscape photo in a vertical promo use `panel`. Don't pre-render photo motion with `zoompan`; it jitters. Next to video, give photos a little grain (`grain: 0.06`) so they sit in the same world.
- **Other-aspect media** (a landscape clip or photo in a vertical promo, or the reverse): `panel: true` shows the whole frame over a blurred copy of itself instead of cropping people out. Cut the clip at its own aspect (e.g. `1080x608` for 16:9 in vertical).
