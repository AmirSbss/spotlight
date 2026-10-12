# Using spotlight with other agents

spotlight is a plain [Agent Skill](https://agentskills.io): a `SKILL.md` with instructions, a few reference files the agent reads when it needs them, and scripts it runs from the shell. Any agent that can read files and run long shell commands can use it.

## What the agent needs

- Shell access with ffmpeg, ImageMagick, Python 3, Node, Chromium and uv installed. Run `bash skills/spotlight/scripts/doctor.sh` to check.
- Permission to run commands outside a sandbox. spotlight installs `playwright-core` with npm, launches Chromium and writes frames to disk, and a sandbox without network or process access blocks that.
- Time. A 25-second narrated explainer with a chart and a globe took Codex about 12 minutes and Hermes about 27; Claude Code takes 30 to 60 with a full critic loop. Single commands (a frame capture, an encode) can run for a few minutes, so long commands must be allowed.
- Optionally, a way to start a fresh sub-agent, which spotlight uses as the critic. Without one, the agent reviews its own render on freshly extracted frames against the same checklist. In our latest runs Claude Code started a sub-agent critic, while Codex and Hermes reviewed their own renders.

## Installing

The [skills CLI](https://github.com/vercel-labs/skills) installs spotlight for the agents you name:

```bash
npx skills add https://github.com/AmirSbss/spotlight --skill spotlight -a codex -a hermes-agent -g -y
```

That puts one copy in `~/.agents/skills/spotlight`, which Codex reads, and links it into Hermes's skills folder. Leave out `-a` and the CLI asks which of the agents it finds you want.

To do it by hand, copy (or link) `skills/spotlight/` into the agent's skills folder:

| Agent | Skills folder |
|---|---|
| Claude Code | `~/.claude/skills/`, or install the plugin (see the README) |
| Codex CLI | `~/.agents/skills/` |
| Hermes Agent | `~/.hermes/skills/` |

Inside this repo, agents that look for project skills find spotlight through the links in `.claude/skills/`, `.agents/skills/` and `.opencode/skills/`.

For an agent with no skills support, paste `skills/spotlight/SKILL.md` into its instructions and keep the repo on disk, so it can open `skills/spotlight/references/` and run `skills/spotlight/scripts/`.

## Running it

Interactively, ask for a video in plain words ("make a launch video for https://your-app.com") or name the skill: `/spotlight` in Claude Code and Hermes, `$spotlight` in Codex.

To run it unattended, give the agent a prompt that says nobody can answer questions, so it takes the name and call to action from your material instead of asking:

```bash
# Codex: stdin must be closed, or `codex exec` waits for more input
codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check -C ~/videos/launch \
  '$spotlight https://your-app.com --mode brag (headless: nobody can answer questions)' < /dev/null

# Hermes: preload the skill, approve commands, and allow enough turns
hermes chat -q 'Make a brag video of https://your-app.com (headless: nobody can answer questions)' \
  --oneshot --yolo -s spotlight --max-turns 300

# Claude Code
claude -p --max-turns 300 '/spotlight https://your-app.com --mode brag (headless: nobody can answer questions)'
```

Run these only in a folder and on a machine where you're happy for the agent to run commands without asking.

## Tested

On 2026-10-12, with sound and visuals in place, Codex and Hermes each made a 25-second narrated explainer from the same headless prompt and the same two small CSV files: a bar chart of the data, a globe with the routes drawn between real cities, and Piper narration over a bundled track. Claude Code made the README's demo and the examples in `examples/`. Every run went through `footage.py check` and a critic review.

| Agent | Version | Result |
|---|---|---|
| Claude Code | 2.1, Claude Opus 5.5 | full pipeline with sub-agent critics; made the README's demo and the examples |
| Codex CLI | 0.154, gpt-5.6-sol | full pipeline in about 12 minutes: chart, globe and narration; `check` clean (−14.1 LUFS, −2.4 dBTP, 0 s frozen); it reviewed its own render rather than starting a sub-agent |
| Hermes Agent | 0.21.5 | full pipeline in about 27 minutes: chart, globe and narration; `check` clean (−14.2 LUFS, −2.2 dBTP, 0 s frozen); it reviewed its own render rather than starting a sub-agent |
