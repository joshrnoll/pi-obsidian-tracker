---
name: triage
description: Move actionable issue cards across a project's Obsidian Kanban board. Use when the user wants to review issues, prepare work for implementation, or change workflow state in issue-tracker/<project>/board.md.
---

# Triage Obsidian

Move issue cards through the board state machine.

## Before you start

Read:
- [workflow](../../docs/workflow.md)
- [kanban contract](../../docs/obsidian-kanban-contract.md)
- [state model](../../docs/state-model.md)

## Project resolution

Ask for the project name if it is not explicit.

Ensure the target project exists before triaging.

## Canonical states

- `Needs Triage`
- `Ready`
- `In Progress`
- `Blocked`
- `Done`
- `Merged` (terminal — do not move cards out of this column)

## Source of truth

The board column is canonical.

If issue note frontmatter disagrees, the board wins. You may update note status best-effort after moving the card, but do not treat note metadata as authoritative.

## Triage questions

When deciding whether work can move to `Ready`, verify:
- the issue is actionable as written
- the issue is small enough for a single implementation slice
- acceptance criteria are clear enough for `tdd`
- the work is not blocked on missing decisions

If not, keep it in `Needs Triage` or move it to `Blocked` if appropriate.

## Editing rules

- Preserve Obsidian Kanban markdown structure
- Move cards conservatively
- Prefer minimal edits over rewriting the whole board
- Keep PRDs off the board

## Output

Summarize:
- project name
- cards moved
- from/to columns
- any issues that were not ready and why
