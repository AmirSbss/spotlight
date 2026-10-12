# spotlight P4 (release) Plan

**Goal:** Publish one polished example per mode plus a square showcase reel for LinkedIn, all made with spotlight itself. Prove the published install works from a clean machine.

**Spec:** `docs/superpowers/specs/2026-10-02-spotlight-design.md`, Phases (P4) and Testing (Acceptance).

## Decisions (from the user, 2026-10-12)

| Topic | Decision |
|---|---|
| Push policy | Straight to `main` once every suite passes. |
| promo example | The user's own café footage (12 phone clips), with the user's brief: name, offer, CTA. Faces and publishing still need confirming. |
| explain example | "Why spotlight checks its own videos". Numbers come from real `check` runs and a real critic report, so `sources.md` cites them. |
| brag example | spotlight about itself, from its repo, landscape for the README. |
| LinkedIn | A square 1080×1080 English showcase reel cut from the three examples, plus a draft post for the user to approve. Claude never posts. |

## Acceptance for each example

- `footage.py check` passes: −14 LUFS ±1, TP ≤ −1.5 dBTP, frame count exact, no hold over 0.6 s outside the end card, frozen time within budget.
- One critic round (a fresh sub-agent with `references/critic.md`), the fixes, then a verification critic. Ship at SHIP or after 3 rounds.
- `sources.md` lists every line on screen. No AI images, or any used are labelled.
- The deliverables go to `examples/<mode>/`: `video.mp4`, `poster.jpg`, `plan.md`, `sources.md` and `caption.txt` (plus `preview.gif` for the README). No `work/`.

## Release checks

- [x] `npx skills add https://github.com/AmirSbss/spotlight --skill spotlight` into a clean HOME. The music and effects are real audio (ffprobe durations match). The installed `mix.py` and `footage.py track` run with a fresh uv cache, and no `.venv` appears in the skill folder.
- [x] `claude plugin marketplace add AmirSbss/spotlight` + `claude plugin install spotlight@spotlight` into a clean HOME: installed, and the audio is real.
- [x] Plugin version bumped to 0.3.0 so existing installs are offered the update.
- [ ] Re-run the headless end-to-end checks for Codex CLI and Hermes Agent that `docs/other-agents.md` claims, with P2/P3 in place, or narrow the claim.
- [ ] README gallery: one entry per example, with the command that made it.
