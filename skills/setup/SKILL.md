---
name: setup
description: Set up or adopt an Obsidian vault as the issue tracker root for this workflow. Use when the user wants to initialize the vault-backed tracker, configure a vault path, or scaffold shared issue-tracker directories and templates.
---

# Setup Obsidian Tracker

Ask the user for the Obsidian vault path if it is not already known.

## Goal

Create or adopt an Obsidian vault and scaffold the shared tracker structure used by the other skills.

## Shared contract

Read these references before making changes:
- [workflow](../../docs/workflow.md)
- [kanban contract](../../docs/obsidian-kanban-contract.md)
- [state model](../../docs/state-model.md)
- [board template](../../templates/board.md)
- [issue template](../../templates/issue.md)
- [prd template](../../templates/prd.md)
- [config template](../../templates/config.md)

## What to scaffold

Given `<vault>`, ensure these exist:

```text
<vault>/
  issue-tracker/
  issue-tracker/_templates/
  issue-tracker/_config/
```

Write these files if missing:

- `issue-tracker/_templates/board.md`
- `issue-tracker/_templates/issue.md`
- `issue-tracker/_templates/wave.md`
- `issue-tracker/_templates/prd.md`
- `issue-tracker/_config/shipboard.md`

Populate them from this skill package's `templates/` directory.

## Rules

- Keep setup minimal
- Do not create an initial project unless the user explicitly asks
- Do not install plugins or modify Obsidian app config
- If the vault exists, adopt it conservatively
- If a target file already exists, inspect it before overwriting

## Output

At the end, summarize:
- chosen vault path
- whether the vault was newly created or adopted
- which directories/files were created
- any existing files left untouched
