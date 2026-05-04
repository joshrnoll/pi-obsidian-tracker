---
name: to-issues
description: Break a PRD or plan into actionable Obsidian issue notes and waves, then add wave cards to a project's Kanban board. Use when the user wants to turn planning work into independently actionable issue notes grouped into waves under issue-tracker/<project>.
---

# To Issues Obsidian

Break a PRD or plan into actionable issues grouped into waves.

## Before you start

Read:
- [workflow](../../docs/workflow.md)
- [kanban contract](../../docs/obsidian-kanban-contract.md)
- [state model](../../docs/state-model.md)
- [issue template](../../templates/issue.md)
- [wave template](../../templates/wave.md)

## Project resolution

Ask for the project name if it is not explicit.

If the project directory does not exist under `issue-tracker/`, **stop and direct the user to run the `new-project` skill first**. Do not lazily scaffold projects — `new-project` is required to capture repo and merge-branch config.

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

## Wave grouping rules

After decomposing issues, group them into waves:

- A **wave** is a set of issues that share a dependency chain or are tightly related enough to share a branch.
- Issues that depend on issues from another wave do not carry a direct cross-wave `depends_on` — instead the **wave** carrying the dependent issue lists the other wave in its own `depends_on`.
- Issues within a wave that have ordering constraints carry `depends_on` pointing to other issues **within the same wave only**.
- Issues with no ordering constraints within their wave have an empty `depends_on`.
- Waves are named descriptively and numbered with a stable prefix: `001-wave-name`.

## What to write

### Issue notes
- Write issue notes to `issue-tracker/<project-name>/issues/`
- Use stable numbered filenames: `001-issue-name.md`
- Populate `depends_on` in frontmatter with intra-wave issue wikilinks only (e.g. `[[issues/001-prior-issue]]`)
- Link issues back to the PRD under `## Links` when applicable

### Wave files
- Write wave files to `issue-tracker/<project-name>/waves/`
- Use stable numbered filenames: `001-wave-name.md`
- Populate wave `depends_on` with wikilinks to prerequisite waves (e.g. `[[waves/001-prior-wave]]`)
- List all issues in the wave under `## Issues` as wikilinks

### Board
- Insert one wave card per wave under `## Needs Triage` in `board.md`:
  ```markdown
  - [[waves/<wave-file>]]
  ```
- Do **not** put issue cards on the board

## Rules

- Insert new work into `Needs Triage`, never directly into `Ready`
- Preserve existing board formatting
- Do not add PRDs to the board
- Issue cards must not appear on the board — only wave cards

## Output

Summarize:
- project name
- issue files created (grouped by wave)
- wave files created (with their `depends_on`)
- board cards inserted
- source PRD or context used
