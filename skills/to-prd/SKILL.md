---
name: to-prd
description: Turn the current conversation context into a PRD note in an Obsidian project tracker. Use when the user wants to create a PRD for a project stored under issue-tracker/<project>/prds.
---

# To PRD Obsidian

Create a PRD note for a specific project.

## Before you start

Read:
- [workflow](../../docs/workflow.md)
- [state model](../../docs/state-model.md)
- [prd template](../../templates/prd.md)

## Project resolution

Ask for the project name if it is not explicit.

Ensure this project exists, creating it lazily if needed:

```text
issue-tracker/<project-name>/
  board.md
  issues/
  prds/
```

If creating the project lazily, scaffold `board.md` from [../../templates/board.md](../../templates/board.md).

## What to create

Write a PRD note into:

```text
issue-tracker/<project-name>/prds/
```

The PRD should:
- capture the current conversation context
- follow the structure in [../../templates/prd.md](../../templates/prd.md)
- include a clear problem statement and solution
- include a long, numbered list of user stories
- record implementation and testing decisions
- stay a planning artifact
- not be added to the board by default

## Rules

- Do not interview the user unless key information is missing
- Prefer a stable, human-readable title and filename
- Link to related issue notes only if they already exist
- Do not include file paths or code snippets in the PRD
- Keep PRDs off the execution board

## Output

Summarize:
- project name
- PRD file path
- title used
- whether project scaffolding was created lazily
