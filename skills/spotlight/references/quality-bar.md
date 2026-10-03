# Quality bar

A video ships only when these hold. `footage.py check` measures the first block; critics judge the rest.

## Measured
| Check | Target |
|---|---|
| Frozen time | ≤ 1 s per 30 s; no hold over 0.6 s without motion, except the end card (`--end-card`) |
| Loudness | −14 LUFS integrated (±1); true peak ≤ −1.5 dBTP; loudness range ≥ 3 LU for energetic pieces |
| Frames | Exactly duration × 30 |

## Visual
- Frame 0 is a finished composition (never a half-entered word).
- No empty frames, no text collisions (also mid-transition), no captions over signage, logos or faces.
- Lists: equal spacing, aligned left edges (right edges in RTL).
- The lead subject fills most of the frame in feature shots; crop with `cx` or use `panel` for other-aspect media.
- Openers are bright and clear unless the brand says otherwise.
- Every person the user asked to feature has a clear moment; third-party brands stay out of frame.

## Message (on mute)
- A first-time viewer can say what it is and the one next action.
- Every claim on screen is in `sources.md`, or clearly labelled as illustration.
- The CTA is readable at phone size for ≥ 1.5 s.
