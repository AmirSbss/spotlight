# brag mode: a launch video for something you built

Input is a code project or a website. You built it; now brag. Adapted from /brag (MIT).

## Inspect
- **Project:** read the main page, styles (exact colours and fonts), README, routes and key components. Find the 2–3 beats of the product **in use**: entry → key action → result. Import or render the project's real components, styles, fonts and images instead of rebuilding them.
- **Website:** in `spotlight-output/work`, after `npm i --prefix . playwright-core`, run `node <skill-dir>/scripts/site.mjs <url> . --size <W>x<H>`. Use `site/copy.json` for words, `site/brand.json` for colours, fonts and logo, and `site/screens/` and `site/full.png` for the page itself. A `web` shot scrolls the real page. Reuse its markup and assets over flat screenshots whenever the shot needs interaction.
- Answer: what is it, who is it for, what does it do for them, what sets it apart, the most impressive or funniest true claim, the visual hook, the one-line caption.

## Shape
Hook (2–3 s) → reveal (2–4 s) → 2–3 sharp highlights → punchline / CTA (2–4 s). A starting shape, not a template. 15–25 s; 18–22 is the sweet spot.

## Laws
- **The hook is everything.** Plan the first 2 seconds first.
- **Show the thing.** Real UI, copy, images and flows from the source, never abstract filler. Small illustrative UI text in a simulated flow is fine (a filename, an "Exported" toast); invented claims, numbers or testimonials are not.
- **Make it alive.** Things that appear one by one, simulated clicks, swipes and typing beat static slides.
- **Funny earns its place.** Humour comes from the project's own absurdity.
- **No generic SaaS language** ("streamline your workflow" is banned).

## Tones
| Tone | Feel | Pacing / transitions |
|---|---|---|
| `default` | Punchy, playful, clean | 4–5 scenes; soft transitions |
| `polished` | Serious, elegant, restrained | 3–4 scenes, long holds; soft fades |
| `yc-parody` | Deadpan startup launch, played straight | 4–5 scenes, one claim each; hard cuts |
| `chaotic` | FAST, LOUD, ALL CAPS | 6–8 scenes, some under 2 s; flash/zoom cuts |
| `deadpan` | Calm, dry, nothing is a joke | 3–4 scenes, big empty space; slow fades |
| `cinematic` | Trailer-scale, epic claims | 4–5 scenes, big type; dramatic wipes |
| `app-store` | Clean feature cards | 4–6 scenes; smooth slides |
