---
name: dispatch-ready-waves
description: Launch one interactive pi subagent in its own tmux session for each Ready wave on an Obsidian project board. Use when you want parallel wave execution with dependency-aware waiting and automatic PR drafting.
---

# Dispatch Ready Waves

Launch one interactive `pi` instance per `Ready` wave in separate tmux sessions. Fire and forget.

## Before you start

Read:
- [workflow](../../docs/workflow.md)
- [kanban contract](../../docs/obsidian-kanban-contract.md)
- [state model](../../docs/state-model.md)
- [tdd skill](../tdd/SKILL.md)
- `scripts/watch-wave-deps.py`

## Inputs

You need the project directory under `issue-tracker/<project>/`.

Resolve and read `board.md`. Extract from its frontmatter:
- `project` — project name
- `repo` — repo path

If the user has not specified a model for the subagent, ask which model to use before dispatching. Pass it to `pi` via `--model <model>`.

## What this skill does

1. Read `board.md`
2. Collect all wave cards under `## Ready`
3. Launch one interactive `pi` subagent per Ready wave in its own tmux session
4. In each session:
   - if the wave has dependencies, run the deterministic dependency watcher before any implementation work
   - use the `tdd` skill with the explicit wave file path

## Dependency watcher contract

Use `scripts/watch-wave-deps.py` exactly for dependency waiting.

Rules:
- The board column is canonical
- A dependency is satisfied only when its wave card is under `## Done`
- Do not begin implementation until all dependency waves are in `Done`
- If a wave has no dependencies, do not run the watcher

Invocation:

```bash
python3 <skill-dir>/scripts/watch-wave-deps.py <board-path> <wave-file> [--interval 10]
```

The script exits `0` only when all dependencies of the target wave are in `Done`.
It exits non-zero on malformed input or missing files.

## tmux session rules

- Launch interactive sessions only; do not use `--print`
- Use one session per wave
- Name each session after the wave stem, prefixed with `wave-`
  - Example: `wave-WAVE_00001_PRD_00001_auth-foundation`
- If a target session already exists, stop and ask whether to reuse or replace it

## Session prompt template

For each wave, instruct the subagent to do all of the following:

- Use the `tdd` skill to handle each issue in the wave
- Use the explicit path to the wave file
- Follow the `tdd` skill strictly
- Treat the project as resolved from board frontmatter
- Do not ask the user for the wave path
- If the wave has dependencies, first run the deterministic watcher script and wait until dependencies are `Done`
- Do not begin work on the wave until dependencies are satisfied
- Be proactive and complete the workflow end-to-end (implementation → PR draft → CI babysitting)

## Output

Summarize:
- project name
- repo path
- Ready waves dispatched (with their associated PRD and branch name)
- tmux session names created
- any waves skipped and why
