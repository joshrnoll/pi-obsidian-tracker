---
name: dispatch-ready-waves
description: Launch one interactive pi subagent in its own tmux session for each Ready wave on an Obsidian project board whose dependencies are already met. Use when you want parallel wave execution with automatic PR drafting.
---

# Dispatch Ready Waves

Launch one interactive `pi` instance per dispatchable `Ready` wave in separate tmux sessions. Fire and forget.

## Before you start

Read:
- [workflow](../../docs/workflow.md)
- [kanban contract](../../docs/obsidian-kanban-contract.md)
- [state model](../../docs/state-model.md)
- [tdd skill](../tdd/SKILL.md)

## Inputs

You need the project directory under `issue-tracker/<project>/`.

Resolve and read `board.md`. Extract from its frontmatter:
- `project` — project name
- `repo` — repo path

If the user has not specified a model for the subagent, ask which model to use before dispatching. Pass it to `pi` via `--model <model>`.

## What this skill does

1. Read `board.md`
2. Collect all wave cards under `## Ready`
3. For each Ready wave, read its `depends_on` frontmatter field
4. A wave is **dispatchable** if it has no dependencies, or every dependency wave card is currently under `## Done` on the board
5. Skip waves whose dependencies are not yet met — report them as skipped
6. Launch one interactive `pi` subagent per dispatchable wave in its own tmux session using the `tdd` skill

## Dependency filtering

Before dispatching, read each Ready wave file and check its `depends_on` list.

- If `depends_on` is empty or absent: dispatchable
- If all listed dependency waves have their board card under `## Done`: dispatchable
- If any listed dependency wave is not yet in `Done`: skip and report

The board column is canonical for dependency state.

## tmux session rules

- Launch interactive sessions only; do not use `--print`
- Use one session per wave
- Name each session after the wave stem, prefixed with `wave-`
  - Example: `wave-WAVE_00001_PRD_00001_auth-foundation`
- If a target session already exists, stop and ask whether to reuse or replace it

## Session prompt template

For each dispatchable wave, instruct the subagent to do all of the following:

- Use the `tdd` skill to handle each issue in the wave
- Use the explicit path to the wave file
- Follow the `tdd` skill strictly
- Treat the project as resolved from board frontmatter
- Do not ask the user for the wave path
- Be proactive and complete the workflow end-to-end (implementation → PR draft → CI babysitting)

## Output

Summarize:
- project name
- repo path
- waves dispatched (with their associated PRD and branch name)
- tmux session names created
- waves skipped due to unmet dependencies (list each wave and which dependency is blocking it)
