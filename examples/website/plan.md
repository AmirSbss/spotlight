# Plan: BudTech, brag (default tone), 1080x1920, 20.0 s (pass 3, after critics 1 and 2)

**Angle:** the site's own sentence is the script. "From IT infrastructure to custom software, we set it up, run it, and grow it with you." The hook quotes its first half over two of the site's photos, under a "BudTech · Muscat, Oman" tag. The real phone-width site appears; the language picker is tapped, "العربية" is chosen, and the page flips to Arabic. The three verbs land one per beat. The close is the differentiator ("a system you fully own and control"), then the site's own CTA, tapped.

**Hook (first 2 s):** frame 0 already reads "BudTech · Muscat, Oman" and "From IT infrastructure" over a server rack in blue light, with the music's full beat from the first frame. On the downbeat at 1.5 s it cuts to a developer at his code and "to custom software" lands.

## Shots
| # | Time (s) | Source | Motion | On-screen text | In |
|---|---|---|---|---|---|
| 1 | 0.0–1.5 | work/media/pf-ruby-v2.webp, crop 506x900+430+0 -> work/stills/hookA.jpg | push 1.00->1.08 | tag "BudTech · Muscat, Oman" (with logo); "From IT infrastructure" (frame 0) | (frame 0) |
| 2 | 1.5–3.0 | work/media/svc-software-om.webp, crop +560 -> work/stills/hookB.jpg | push 1.00->1.07 | "to custom software" (lands 1.5) | cut on the beat |
| 3 | 3.0–4.0 | live https://budtech.om/en/ at 390 css px (work/hero.mjs -> work/web/en390.png, faded to paper below "Request a quote" -> en390-cut.png), shown as a rounded card on an ink backdrop with a brand glow | push 0.86->0.892, page moved down 280 px | the page's own H1; tap on the language picker at 3.85 | cut + whoosh |
| 4 | 4.0–4.5 | same page with the language menu open (work/menu.mjs, a real click -> en390-menu-cut.png) | push ->0.908 | the menu "English / العربية"; tap on "العربية" at 4.15 | cut (menu opens) |
| 5 | 4.5–5.5 | live https://budtech.om/ar/ at 390 css px (ar390-cut.png, faded below its primary button) | push ->0.94 | the page's own Arabic H1 | cut on the beat |
| 6 | 5.5–8.0 | work/media/svc-network-v2.webp, crop +380 -> work/stills/setup.jpg | push 1.00->1.07 | tag "IT services and infrastructure"; "Set it up." (high) | cut + whoosh |
| 7 | 8.0–10.5 | work/media/svc-managed-om.webp, crop +560 -> work/stills/run.jpg | push 1.00->1.07 | tag "Managed IT and support"; "Run it." | cut on the beat |
| 8 | 10.5–13.0 | work/media/svc-consulting-om.webp, crop +180 -> work/stills/grow.jpg | push 1.04->1.10 from bottom-left | tag "IT consulting and strategy"; "Grow it with you." | cut on the beat |
| 9 | 13.0–16.0 | work/media/svc-endtoend-v2.webp, crop +600 -> work/stills/own.jpg, graded brighter, grain 0.08 | push 1.00->1.10, drift 0->-3% | tag "End-to-end"; "A system you fully own and control." | cut + whoosh |
| end | 16.0–20.0 | work/logo.png (owner's budnobg.png, trimmed) | wipe up | logo, "BudTech", "براعم التقنية", button "Request a quote" (pressed at 17.6), "budtech.om", "Muscat, Oman" | wipe + whoosh |

Durations: 1.5+1.5+1+0.5+1+2.5+2.5+2.5+3+4 = 20.0 s. All cuts are hard cuts on beats (no dips).

## Music
`<skill-dir>/assets/music/upbeat.mp3` (brag default), cut into `work/music/bed.wav` on bar lines so the drums run under every shot: track 16.02–28.02, then the bar 26.02–28.02 once more, then 28.02–34.2 (12 ms crossfades). The kick starts on frame 0 and runs to 15.5 s; the track's breakdown arrives with the end card at 16.0. Every cut at 1.5, 3.0, 4.0, 4.5, 5.5, 8.0, 10.5, 13.0 and 16.0 lands on a beat. mix.json: start 0, fade_in 0.02, fade_out 0.8 (after the end card has landed).
LRA measures about 1 LU, under the quality bar's 3 LU for energetic pieces. This is deliberate: pass 1 used a low-passed intro build that reached 3.1 LU, but critic 1 ranked the missing kick under the hook as its top defect, and critic 2 asked for the drums to run to the end card. This track is too even to reach 3 LU in 20 s any other way.

## Effects
| t (s) | File | Why |
|---|---|---|
| 3.0 | whoosh-3.ogg (align peak) | the reveal: cut into the real site |
| 3.85 | click-2.ogg | tap on the language picker |
| 4.15 | toggle-1.ogg (target +5) | "العربية" chosen |
| 5.5 | whoosh-1.ogg (align peak) | section change into the three verbs |
| 13.0 | whoosh-2.ogg (align peak, target +8, cap +9) | section change to the differentiator (fuller whoosh; whoosh-1 sat under the HF cap) |
| 16.0 | whoosh-3.ogg (align peak) | the end card wipes in |
| 17.6 | click-3.ogg | tap on "Request a quote" |

## AI assets
None. The site's own photography covers every beat (the bridge is available but was not needed).

## Privacy / third parties
Two people appear in profile on the consulting photo (the site's own image). The floating WhatsApp button is hidden in the phone-width captures, and each page fades to its background below the primary "Request a quote" button, so the "Chat on WhatsApp" button is out of frame. No licence plates, no addresses beyond "Muscat, Oman", no phone numbers.
