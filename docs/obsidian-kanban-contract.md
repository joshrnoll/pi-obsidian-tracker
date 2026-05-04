# Obsidian Kanban Contract

## Canonical board path

```text
issue-tracker/<project-name>/board.md
```

## Project structure

```text
issue-tracker/<project-name>/
  board.md
  config.md
  issues/       ← issue notes (not linked directly from the board)
  waves/        ← wave files (board cards link here)
  prds/
```

## Required columns

- `Needs Triage`
- `Ready`
- `In Progress`
- `Blocked`
- `Done`
- `Merged`

## Card format

Board cards link to **wave files**, not issue files:

```markdown
- [[waves/001-some-wave]]
```

Issue files are linked from within wave files, not from the board directly.

## Wave file format

```markdown
---
type: wave
project: <project-name>
title: <title>
status: <status>
depends_on:
  - "[[waves/000-prerequisite-wave]]"
created: <ISO-8601>
tags:
  - issue-tracker
  - <project-name>
---

# <title>

## Issues

- [[issues/001-first-issue]]
- [[issues/002-second-issue]]
```

## Board frontmatter

```yaml
---
kanban-plugin: basic
project: <project-name>
type: board
---
```

## Notes

- Preserve heading order
- Preserve blank lines between sections
- Prefer append/move operations over board rewrites
- If wave note metadata disagrees with board location, the board wins
- Issue cards must not appear directly on the board
