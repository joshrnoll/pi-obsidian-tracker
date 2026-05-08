---
name: to-prd
description: Turn the current conversation context into a PRD note in an Obsidian project tracker. Use when the user wants to create a PRD for a project stored under issue-tracker/<project>/prds.
---

# To PRD Obsidian

Create a PRD note for a specific project and add it to the board.

## Before you start

Read:
- [workflow](../../docs/workflow.md)
- [state model](../../docs/state-model.md)
- [kanban contract](../../docs/obsidian-kanban-contract.md)
- [prd template](../../templates/prd.md)

## Project resolution

Ask for the project name if it is not explicit.

If the project directory does not exist under `issue-tracker/`, **stop and direct the user to run the `new-project` skill first**. Do not lazily scaffold projects — `new-project` is required to capture repo config.

## PRD numbering

Scan existing files in `issue-tracker/<project>/prds/` to determine the next PRD number. Numbers are 5-digit zero-padded and flat per-project (e.g. `PRD_00001`, `PRD_00002`).

## What to create

Write a PRD note to:

```text
issue-tracker/<project-name>/prds/PRD_<nnnnn>_<descriptive-title>.md
```

The PRD should:
- follow the structure in [../../templates/prd.md](../../templates/prd.md)
- capture the current conversation context
- include a clear problem statement and solution
- include a long, numbered list of user stories
- record implementation and testing decisions
- set `status` to `needs-triage` in frontmatter
- set `tags` so the project tag is kebab-case and the artifact tag is exactly `PRD`

## Add to board

Insert the PRD card into `## Needs Triage` in `board.md`:

```markdown
- [[prds/PRD_<nnnnn>_<descriptive-title>]]
```

## Rules

- Do not interview the user unless key information is missing
- Prefer a stable, human-readable title and filename
- Always write tags in the required format; derived tags must be kebab-case
- Link to related issue notes only if they already exist
- Do not include file paths or code snippets in the PRD

## Output

Summarize:
- project name
- PRD file path
- board card inserted
