---
name: dispatch-ready-waves
description: Launch one interactive pi subagent in its own tmux session for each Ready wave on an Obsidian project board. Use when you want parallel wave execution, dependency-aware waiting, and automatic handoff to tdd and merge-issues.
---

# Dispatch Ready Waves

Launch one interactive `pi` instance per `Ready` wave in separate tmux sessions.

## Before you start

Read:
- `/var/home/josh/github/pi-obsidian-tracker/docs/workflow.md`
- `/var/home/josh/github/pi-obsidian-tracker/docs/obsidian-kanban-contract.md`
- `/var/home/josh/github/pi-obsidian-tracker/docs/state-model.md`
- `/var/home/josh/github/pi-obsidian-tracker/skills/tdd/SKILL.md`
- `/var/home/josh/github/pi-obsidian-tracker/skills/merge-issues/SKILL.md`
- `scripts/watch-wave-deps.py`

## Inputs

You need the project directory under `issue-tracker/<project>/`.

Resolve and read:
- `board.md`
- `config.md`

From `config.md`, extract:
- project name
- repo path
- merge branch

## What this skill does

1. Read `board.md`
2. Collect all wave cards under `## Ready`
3. Launch one interactive `pi` subagent per Ready wave in its own tmux session
4. In each session:
   - if the wave has dependencies, run the deterministic dependency watcher before any implementation work
   - use the `tdd` skill with the explicit wave file path
   - after the wave is completed, use the `merge-issues` skill to merge into the configured merge branch

## Dependency watcher contract

Use `scripts/watch-wave-deps.py` exactly for dependency waiting.

Rules:
- The board column is canonical
- A dependency is satisfied only when its wave card is under `## Merged`
- Do not begin implementation until all dependency waves are in `Merged`
- If a wave has no dependencies, do not run the watcher

Invocation:

```bash
python3 <skill-dir>/scripts/watch-wave-deps.py <board-path> <wave-file> [--interval 10]
```

The script exits `0` only when all dependencies of the target wave are in `Merged`.
It exits non-zero on malformed input or missing files.

## tmux session rules

- Launch interactive sessions only; do not use `--print`
- Use one session per wave
- Name each session after the wave stem, prefixed with `wave-`
  - Example: `wave-001-auth-wave`
- If a target session already exists, stop and ask whether to reuse or replace it

## Session prompt template

For each wave, instruct the subagent to do all of the following:

- Use the `tdd` skill to handle each issue in the wave
- Use the explicit path to the wave file
- Follow the `tdd` skill strictly
- Treat the project as the resolved project from `config.md`
- Do not ask the user for the wave path
- If the wave has dependencies, first run the deterministic watcher script and wait until dependencies are `Merged`
- Do not begin work on the wave until dependencies are merged
- When the wave reaches `Done`, use the `merge-issues` skill to merge the completed wave into the configured merge branch
- Be proactive and complete the workflow end-to-end

## Suggested launch flow

1. Resolve the skill directory and watcher script path
2. Parse Ready waves from the board
3. For each Ready wave:
   - resolve its wave file path
   - read the wave file and inspect `depends_on`
   - build the prompt
   - start a tmux session in the repo path from `config.md`
4. Report created session names

## Output

Summarize:
- project name
- repo path
- merge branch
- Ready waves dispatched
- tmux session names created
- any waves skipped and why
