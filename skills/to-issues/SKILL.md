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

If the project directory does not exist under `issue-tracker/`, **stop and direct the user to run the `new-project` skill first**. Do not lazily scaffold projects — `new-project` is required to capture repo config.

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
- Waves are named descriptively with a stable numeric prefix following the naming convention (e.g. `WAVE_00001_PRD_00001_descriptive-slug`).

## What to write

### Numbering

Scan existing files in the project's `issues/` and `waves/` directories to determine the next available number for each sequence. Numbers are 5-digit zero-padded and flat per-project.

- PRD number: read from the source PRD filename (e.g. `PRD_00001_...` → `00001`)
- Wave filenames: `WAVE_<nnnnn>_PRD_<prd-nnnnn>_<descriptive-slug>.md`
- Issue filenames: `ISSUE_<nnnnn>_WAVE_<wave-nnnnn>_PRD_<prd-nnnnn>_<descriptive-slug>.md`

### Issue notes
- Write issue notes to `issue-tracker/<project-name>/issues/`
- Use the naming convention: `ISSUE_<nnnnn>_WAVE_<wave-nnnnn>_PRD_<prd-nnnnn>_<descriptive-slug>.md`
- Set `prd` frontmatter field to the parent PRD wikilink: `"[[prds/PRD_<prd-nnnnn>_<title>]]"`
- Set `wave` frontmatter field to the containing wave wikilink: `"[[waves/WAVE_<wave-nnnnn>_PRD_<prd-nnnnn>_<slug>]]"`
- Set `board` frontmatter field to `"[[board]]"`
- Populate `depends_on` in frontmatter with intra-wave issue wikilinks only
- Set `tags` using kebab-case derived tags only: `issue`, the kebab-case project tag, the kebab-case parent wave tag, and the kebab-case parent PRD tag
- Do not add a `## Links` section; PRD/wave/board associations live in frontmatter

### Wave files
- Write wave files to `issue-tracker/<project-name>/waves/`
- Use the naming convention: `WAVE_<nnnnn>_PRD_<prd-nnnnn>_<descriptive-slug>.md`
- Set `prd` frontmatter field to the parent PRD wikilink: `"[[prds/PRD_<prd-nnnnn>_<title>]]"`
- Populate wave `depends_on` with wikilinks to prerequisite waves
- Set `tags` to `wave`, the kebab-case project tag, and the kebab-case parent PRD tag
- List all issues in the wave under `## Issues` as wikilinks

### Board
- Insert one wave card per wave under `## Needs Triage` in `board.md`:
  ```markdown
  - [[waves/WAVE_<nnnnn>_PRD_<prd-nnnnn>_<descriptive-slug>]]
  ```
- Do **not** put issue cards on the board
- Do **not** add another PRD card — `to-prd` already inserted it

## Rules

- Insert new work into `Needs Triage`, never directly into `Ready`
- Preserve existing board formatting
- Do not add another PRD card to the board — `to-prd` already inserted it
- Issue cards must not appear on the board — only wave cards and PRD cards
- Always normalize derived tags to kebab-case

## Output

Summarize:
- project name
- issue files created (grouped by wave)
- wave files created (with their `depends_on`)
- board cards inserted
- source PRD or context used
