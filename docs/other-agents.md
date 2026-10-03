# Using spotlight with other agents

spotlight is a plain [Agent Skill](https://agentskills.io): a `SKILL.md` with instructions, a few reference files the agent reads when it needs them, and scripts it runs from the shell. Any agent that can read files and run long shell commands can use it.

## What the agent needs

- Shell access with ffmpeg, ImageMagick, Python 3, Node and Chromium installed. Run `bash skills/spotlight/scripts/doctor.sh` to check.
- Time. A 20-second video takes 20 to 40 minutes of agent work, and a single frame capture or encode can take a few minutes, so long-running commands must be allowed.
- Optionally, the ability to start a fresh sub-agent. spotlight uses one as the critic. Without it, the agent reviews its own render against the same checklist.

## Installing

The [skills CLI](https://github.com/vercel-labs/skills) installs spotlight into whichever supported agents it finds on your machine, Codex and Hermes Agent among them:

```bash
npx skills add https://github.com/AmirSbss/spotlight --skill spotlight
```

To do it by hand, copy `skills/spotlight/` into the agent's skills folder:

```bash
cp -r skills/spotlight ~/.your-agent/skills/
```

When working inside this repo, agents that look for project skills find spotlight through the links in `.claude/skills/`, `.agents/skills/` and `.opencode/skills/`.

For an agent with no skills support, paste `skills/spotlight/SKILL.md` into its instructions and keep the repo on disk, so it can open `skills/spotlight/references/` and run `skills/spotlight/scripts/`.

## Tested so far

| Agent | Status |
|---|---|
| Claude Code | tested end to end (plugin and project skill) |
| Codex CLI | in testing |
| Hermes Agent | in testing |
