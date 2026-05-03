# Obsidian Kanban Contract

## Canonical board path

```text
issue-tracker/<project-name>/board.md
```

## Required columns

- `Needs Triage`
- `Ready`
- `In Progress`
- `Blocked`
- `Done`

## Card format

Prefer a minimal list item linking to an issue note:

```markdown
- [[issues/001-some-issue]]
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
- If issue note metadata disagrees with board location, the board wins
