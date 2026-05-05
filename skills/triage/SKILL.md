---
name: triage
description: Move wave and PRD cards across a project's Obsidian Kanban board. Use when the user wants to review waves, prepare work for implementation, or sync PRD state with wave state in issue-tracker/<project>/board.md.
---

# Triage Obsidian

Move wave and PRD cards through the board state machine. Always runs full-board in two phases: waves first, then PRDs.

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

The board column is canonical for both wave and PRD state.

If wave or PRD note frontmatter disagrees with the board, the board wins. You may update note status best-effort after moving a card, but do not treat note metadata as authoritative.

---

## Phase 1: Wave triage

Evaluate all wave cards that are not in `Merged`. For each wave, drill into every issue linked in the wave file and verify all of the following:

- the issue is actionable as written
- the issue is small enough for a single implementation slice
- acceptance criteria are clear enough for `tdd`
- the work is not blocked on missing decisions
- the wave has a `prd` frontmatter field pointing to a valid PRD file — if missing, flag as malformed and do not move

A wave moves to `Ready` only when **all** its constituent issues pass every check.

If some issues pass but others do not, keep the wave in `Needs Triage` and note specifically which issues need work and why.

> **Note:** Wave `depends_on` is informational at triage time. Do not block a wave from reaching `Ready` based on whether its dependency waves are complete — that gate is enforced by the dispatcher at execution time.

---

## Phase 2: PRD triage

After completing the wave phase, evaluate all PRD cards that are not in `Merged`.

For each PRD:

1. Discover associated waves by scanning all wave files for `prd` fields matching this PRD
2. Apply the PRD state rules from the state model:

| PRD State | Condition |
|---|---|
| `Needs Triage` | PRD has no waves yet, or at least one wave is in `Needs Triage` |
| `Ready` | All associated waves are `Ready` |
| `In Progress` | At least one associated wave is `In Progress` |
| `Blocked` | At least one associated wave is `Blocked` (and none are `In Progress`) |
| `Done` | All associated waves are `Done` or `Merged` (work is complete but `merge-branch` not yet merged into main) |
| `Merged` | Set only by `merge-prd` after the PRD's `merge-branch` is merged into main — triage never moves a PRD card to `Merged` |

3. If the computed state differs from the current board column, propose moving the PRD card

---

## Editing rules

- Move **wave** and **PRD** cards across board columns — never create or move individual issue cards on the board
- Preserve Obsidian Kanban markdown structure
- Move cards conservatively
- Prefer minimal edits over rewriting the whole board
- Show a summary of proposed moves and confirm before applying

## Output

Summarize:

**Wave phase:**
- wave cards moved (from/to columns)
- waves that were not ready and why (including which specific issues failed which checks)
- waves flagged as malformed (missing `prd` field)

**PRD phase:**
- PRD cards moved (from/to columns)
- PRDs with no associated waves (left in `Needs Triage`)
- final board state snapshot (card counts per column)
