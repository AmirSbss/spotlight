# Using spotlight with other agents

Agents that discover skills read this repo directly: Codex CLI and Antigravity (`.agents/skills/spotlight`), opencode (`.opencode/skills/spotlight`), Claude Code (`.claude/skills/spotlight` or the plugin). For other agents:
1. **Custom instructions:** paste `skills/spotlight/SKILL.md`, and keep the repo on disk so the agent can open `skills/spotlight/references/` and run `skills/spotlight/scripts/`.
2. **A skills folder:** copy `skills/spotlight/` into it (`cp -r skills/spotlight ~/.your-agent/skills/`).
The agent must be able to run shell commands (ffmpeg, python3, node). Run `bash skills/spotlight/scripts/doctor.sh` first.
