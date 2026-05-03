---
name: to-issues
description: Break a PRD or plan into actionable Obsidian issue notes and add them to a project's Kanban board. Use when the user wants to turn planning work into independently actionable issue notes under issue-tracker/<project>/issues.
---

# To Issues Obsidian

Break a PRD or plan into actionable issues.

## Before you start

Read:
- [workflow](../../docs/workflow.md)
- [kanban contract](../../docs/obsidian-kanban-contract.md)
- [state model](../../docs/state-model.md)
- [issue template](../../templates/issue.md)

## Project resolution

Ask for the project name if it is not explicit.

Ensure this project exists, creating it lazily if needed:

```text
issue-tracker/<project-name>/
  board.md
  issues/
  prds/
```

## Inputs

Use one of:
- an existing PRD note
- the current conversation context

If both exist, prefer the explicit PRD note.

## Decomposition rules

Each issue must be:
- independently actionable
- a small vertical slice
- specific enough for triage
- suitable for `tdd` once moved to `Ready`

Avoid creating giant umbrella tasks.

## What to write

- Issue notes in `issue-tracker/<project-name>/issues/`
- Matching board cards under `## Needs Triage` in `board.md`

Use minimal board cards, preferably:

```markdown
- [[issues/<issue-file>]]
```

Link issues back to the PRD when applicable.

## Rules

- Insert new work into `Needs Triage`, never directly into `Ready`
- Preserve existing board formatting
- Prefer stable numbered filenames if practical
- Do not add PRDs to the board

## Output

Summarize:
- project name
- issue files created
- board cards inserted
- source PRD or context used
