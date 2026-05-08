---
name: triage
description: Move wave and PRD cards across a project's Obsidian Kanban board. Use when the user wants to review waves, prepare work for implementation, reconcile board state with GitHub PR state, or evaluate PRD completion in issue-tracker/<project>/board.md.
---

# Triage Obsidian

Move wave and PRD cards through the board state machine. Always runs full-board in three phases: wave readiness, GitHub reconciliation, then PRD evaluation.

## Before you start

Read:
- [workflow](../../docs/workflow.md)
- [kanban contract](../../docs/obsidian-kanban-contract.md)
- [state model](../../docs/state-model.md)

## Project resolution

Ask for the project name if it is not explicit.

Ensure the target project exists before triaging.

## Canonical states

### Wave states

- `Needs Triage`
- `Ready`
- `In Progress`
- `Blocked`
- `PR Drafted`
- `Pending Review`
- `Done` (terminal — wave PR has been merged to `main`)

### PRD states

- `Needs Triage`
- `Ready`
- `In Progress`
- `Blocked`
- `Done` (terminal — PRD requirements are satisfied)

PRDs do not enter `PR Drafted` or `Pending Review`.

## Source of truth

The board column is canonical for both wave and PRD state.

If wave or PRD note frontmatter disagrees with the board, the board wins. You may update note status best-effort after moving a card, but do not treat note metadata as authoritative.

---

## Phase 1: Wave readiness triage

Evaluate all wave cards in `Needs Triage`. For each wave, drill into every issue linked in the wave file and verify all of the following:

- the issue is actionable as written
- the issue is small enough for a single implementation slice
- acceptance criteria are clear enough for `tdd`
- the work is not blocked on missing decisions
- the wave has a `prd` frontmatter field pointing to a valid PRD file — if missing, flag as malformed and do not move
- the wave has a `branch_name` frontmatter field — if missing, flag as malformed and do not move

A wave moves to `Ready` only when **all** its constituent issues pass every check.

If some issues pass but others do not, keep the wave in `Needs Triage` and note specifically which issues need work and why.

> **Note:** Wave `depends_on` is informational at triage time. Do not block a wave from reaching `Ready` based on whether its dependency waves are complete — that gate is enforced by the dispatcher at execution time.

---

## Phase 2: GitHub-backed wave state reconciliation

For all wave cards in `PR Drafted` or `Pending Review`, load the wave's `pr_url` frontmatter field and query GitHub via `gh` CLI.

### Missing `pr_url`

If a wave is in `PR Drafted` or `Pending Review` but `pr_url` is missing or empty:
- Move the wave to `Blocked`
- Report: "Wave is in `<state>` but has no `pr_url` — cannot reconcile with GitHub."

### PR state transitions

For waves with a valid `pr_url`:

| Current state | PR condition | Action |
|---|---|---|
| `PR Drafted` | PR is no longer a draft (ready for review) | Move to `Pending Review` |
| `PR Drafted` | PR has merge conflicts | Move to `Blocked` |
| `PR Drafted` | PR was closed without merge | Move to `Blocked` |
| `Pending Review` | PR has been merged | Move to `Done` |
| `Pending Review` | PR has merge conflicts | Move to `Blocked` |
| `Pending Review` | PR was closed without merge | Move to `Blocked` |

Use the following `gh` commands for inspection:

```bash
# Get PR state (draft status, merged status, state)
gh pr view <pr_url> --json state,isDraft,merged,mergeable

# mergeable values: MERGEABLE, CONFLICTING, UNKNOWN
```

---

## Phase 3: PRD evaluation

After completing the wave phases, evaluate all PRD cards that are not in `Done`.

### Needs Triage → Ready gating

For each PRD in `Needs Triage`:

1. Discover associated waves by scanning all wave files for `prd` fields matching this PRD
2. Check whether all current PRD requirements are captured by associated waves
3. If all requirements are covered **and** all associated waves are in `Ready` (or later): move PRD to `Ready`
4. If requirements are not fully covered: leave in `Needs Triage` and report which requirements lack corresponding waves

### PRD state derivation

For PRDs not in `Needs Triage`, derive state from associated wave states:

| PRD State | Condition |
|---|---|
| `Ready` | All associated waves are `Ready` or later |
| `In Progress` | At least one associated wave is `In Progress`, `PR Drafted`, or `Pending Review` |
| `Blocked` | At least one associated wave is `Blocked` (and none are `In Progress` / `PR Drafted` / `Pending Review`) |
| `Done` | See semantic completion evaluation below |

### Semantic PRD completion evaluation

A PRD can move to `Done` only when:
1. All current PRD requirements are semantically satisfied
2. That satisfaction is provided by waves that are already in `Done`
3. There are no stale linked waves still open on the board

This evaluation should be a best-effort semantic judgment.

**If the PRD appears requirements-complete but stale waves exist:**

Do not move the PRD to `Done`. Leave it in `In Progress` and report:

> PRD XXXXX appears requirements-complete, but cannot move to Done because the following stale waves are still in non-Done states.

Include a markdown table:

| Wave | Current State | Why Stale |
|---|---|---|
| `WAVE_...` | `Pending Review` | Requirements already appear satisfied by other completed waves |
| `WAVE_...` | `Needs Triage` | No remaining unmet PRD requirement appears to map to this wave |

The human remains the final decision-maker for PRD completion.

---

## Editing rules

- Move **wave** and **PRD** cards across board columns — never create or move individual issue cards on the board
- Preserve Obsidian Kanban markdown structure
- Move cards conservatively
- Prefer minimal edits over rewriting the whole board
- Show a summary of proposed moves and confirm before applying

## Output

Summarize:

**Phase 1 — Wave readiness:**
- wave cards moved to `Ready` (from `Needs Triage`)
- waves that were not ready and why (including which specific issues failed which checks)
- waves flagged as malformed (missing `prd` or `branch_name`)

**Phase 2 — GitHub reconciliation:**
- wave cards moved (from/to columns) based on PR state
- waves flagged for missing `pr_url`
- any GitHub query errors

**Phase 3 — PRD evaluation:**
- PRD cards moved (from/to columns)
- PRDs with no associated waves (left in `Needs Triage`)
- PRDs with incomplete requirement coverage
- stale wave reports (if any)
- final board state snapshot (card counts per column)
