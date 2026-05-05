# Obsidian Kanban Contract

## Canonical board path

```text
issue-tracker/<project-name>/board.md
```

## Project structure

```text
issue-tracker/<project-name>/
  board.md
  issues/       ← issue notes (not linked directly from the board)
  waves/        ← wave files (board cards link here)
  prds/         ← PRD files (board cards link here)
```

## Required columns

- `Needs Triage`
- `Ready`
- `In Progress`
- `Blocked`
- `Done`
- `Merged`

## Card format

Board cards link to **wave files** or **PRD files**. Issue files never appear on the board.

Wave card:
```markdown
- [[waves/WAVE_00001_PRD_00001_descriptive-slug]]
```

PRD card:
```markdown
- [[prds/PRD_00001_descriptive-title]]
```

Cards are flat within each column — no nesting or grouping. Wave and PRD cards are distinguished by their filename prefix (`WAVE_` vs `PRD_`).

## Naming conventions

All artifact numbers are **5-digit zero-padded** and **flat per-project** (sequences do not reset per PRD or wave).

| Artifact | Pattern |
|---|---|
| PRD | `PRD_00001_descriptive-title.md` |
| Wave | `WAVE_00001_PRD_00001_descriptive-slug.md` |
| Issue | `ISSUE_00001_WAVE_00001_PRD_00001_descriptive-slug.md` |

The PRD and wave numbers embedded in wave and issue filenames are **associative** — they identify the parent artifact. Wave numbers are globally unique within a project; issue numbers are globally unique within a project.

## Wave file format

```markdown
---
type: wave
project: <project-name>
title: <title>
status: <status>
prd: "[[prds/PRD_00001_descriptive-title]]"
depends_on:
  - "[[waves/WAVE_00001_PRD_00001_prerequisite-slug]]"
created: <ISO-8601>
tags:
  - issue-tracker
  - <project-name>
---

# <title>

## Issues

- [[issues/ISSUE_00001_WAVE_00001_PRD_00001_descriptive-slug]]
- [[issues/ISSUE_00002_WAVE_00001_PRD_00001_descriptive-slug]]
```

## PRD file format

```markdown
---
type: prd
project: <project-name>
title: <title>
status: <status>
merge-branch: <branch-name>
created: <ISO-8601>
tags:
  - prd
  - <project-name>
---
```

## Board frontmatter

```yaml
---
kanban-plugin: basic
project: <project-name>
repo: <repo-path>
type: board
---
```

## Notes

- Preserve heading order
- Preserve blank lines between sections
- Prefer append/move operations over board rewrites
- If wave note metadata disagrees with board location, the board wins
- If PRD note metadata disagrees with board location, the board wins
- Issue cards must not appear directly on the board
- PRD → wave association is discovered by scanning wave `prd` frontmatter fields — PRD files do not maintain a list of their waves
