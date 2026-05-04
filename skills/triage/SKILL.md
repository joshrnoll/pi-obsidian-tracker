---
name: triage
description: Move actionable wave cards across a project's Obsidian Kanban board. Use when the user wants to review waves, prepare work for implementation, or change workflow state in issue-tracker/<project>/board.md.
---

# Triage Obsidian

Move wave cards through the board state machine.

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

The board column is canonical for wave state.

If wave note frontmatter disagrees, the board wins. You may update note status best-effort after moving the card, but do not treat note metadata as authoritative.

## Triage questions

When deciding whether a **wave** can move to `Ready`, drill into each issue linked in the wave file and verify all of the following for every issue:

- the issue is actionable as written
- the issue is small enough for a single implementation slice
- acceptance criteria are clear enough for `tdd`
- the work is not blocked on missing decisions

A wave moves to `Ready` only when **all** its constituent issues pass every check.

If some issues pass but others do not, keep the wave in `Needs Triage` and note specifically which issues need work and why.

> **Note:** Wave `depends_on` is informational at triage time. Do not block a wave from reaching `Ready` based on whether its dependency waves are complete — that gate is enforced by the dispatcher at execution time.

## Editing rules

- Move **wave** cards across board columns — do not create or move individual issue cards on the board
- Preserve Obsidian Kanban markdown structure
- Move cards conservatively
- Prefer minimal edits over rewriting the whole board
- Keep PRDs off the board

## Output

Summarize:
- project name
- wave cards moved
- from/to columns
- any waves that were not ready and why (including which specific issues failed which checks)
