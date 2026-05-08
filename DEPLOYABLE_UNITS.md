# Planning: Wave-Centric PR Workflow

## Goal

Replace the PRD-level `merge-branch` model with a wave-centric workflow where each wave is its own merge/review unit.

This change is motivated by the current `merge-branch` approach creating large, muddied PRs that are hard to review.

## Core paradigm shift

### Old model

- A PRD owned a `merge-branch`
- All waves for that PRD merged into the `merge-branch`
- The PRD effectively acted as the merge/release unit

### New model

- Remove `merge-branch` entirely
- A wave is the deployable / reviewable unit
- Each wave has its own semantic branch name
- Each wave is landed independently, either:
  - through a GitHub PR, or
  - directly into `main` for small personal projects after review
- A PRD is no longer a merge artifact; it is a requirements-tracking artifact

## Artifact semantics

### PRD

A PRD tracks whether its requirements have been satisfied.

It is:
- not a branch
- not a PR
- not a merge target
- a planning and requirements artifact with a board lifecycle

### Wave

A wave is:
- the implementation unit
- the branch unit
- the PR unit
- the unit that moves through code review and merge

## Frontmatter changes

### Remove from PRD frontmatter

- `merge-branch`

### Add to wave frontmatter

- `branch_name`: semantic branch name assigned by `to-issues` at creation time
- `pr_url`: written once a draft PR is created

`branch_name` should be semantic and reviewer-friendly, for example:
- `feat/healthcheck-api-endpoint`
- `fix/session-timeout-handling`

## Branch and PR naming

### Branches

Do not use wave IDs as branch names.

Use semantic branch names throughout.

Wave IDs remain important for tracker traceability, but should not be the primary reviewer-facing Git artifact.

### PR titles

PR titles should be human-first and reviewer-friendly.

Do not lead with wave IDs like `WAVE_00011`.

### PR body

The PR body should follow a standard format and include tracker traceability in the body, not the title.

Suggested shape:
- Summary
- What changed
- How to review
- Related issues / acceptance notes
- Tracker metadata footer
  - Wave: `WAVE_...`
  - PRD: `PRD_...`

## Board state model

The board remains shared between PRDs and waves, but PRDs and waves no longer share the exact same lifecycle.

### Wave states

- `Needs Triage`
- `Ready`
- `In Progress`
- `Blocked`
- `PR Drafted`
- `Pending Review`
- `Done`

### PRD states

- `Needs Triage`
- `Ready`
- `In Progress`
- `Blocked`
- `Done`

PRDs do not enter:
- `PR Drafted`
- `Pending Review`

A single shared board is still acceptable even though some columns are wave-only.

## State semantics

### Wave semantics

- `In Progress`: implementation is actively happening on the wave branch
- `PR Drafted`: implementation is complete, committed locally, and a draft PR has been created
- `Pending Review`: the PR has been marked ready for review
- `Done`: the PR has been merged to `main`

`Done` replaces the old wave `Merged` state.

### PRD semantics

- `Done` means the PRD's requirements have been satisfied
- PRD `Done` is not tied to a PRD-level merge event
- There is no PRD `Merged` state anymore

## Wave transition rules

### `In Progress` → `PR Drafted`

Triggered automatically by the working subagent when:
- implementation is complete
- work is committed locally
- a draft PR is created

The subagent must also write `pr_url` into the wave frontmatter.

### `PR Drafted` → `Pending Review`

Handled by `triage`.

`triage` should use `gh` CLI to inspect the PR referenced by `pr_url`.

If the PR is no longer a draft and is ready for review, move the wave to `Pending Review`.

### `Pending Review` → `Done`

Handled by `triage`.

`triage` should use `gh` CLI to inspect the PR referenced by `pr_url`.

If the PR has been merged, move the wave to `Done`.

### `PR Drafted` or `Pending Review` → `Blocked`

Handled by `triage`.

If the PR was closed without being merged, the wave should move to `Blocked`.

## PRD completion rules

PRD completion must not be a naive aggregate of wave statuses.

Reason:
- some requirements may not yet have corresponding waves/issues
- the PRD may have changed after `to-issues` was run
- linked waves may become stale or redundant

### PRD `Done` requirements

A PRD can move to `Done` only when:
1. all current PRD requirements are semantically satisfied
2. that satisfaction is provided by waves that are already in `Done`
3. there are no stale linked waves still open on the board

This evaluation should be a best-effort semantic judgment by the LLM.

The human remains the final decision-maker.

## Stale wave handling

If a PRD appears requirements-complete, but some linked waves are still open and appear stale:
- do not move the PRD to `Done`
- do not automatically modify the stale waves
- leave the PRD in `In Progress`
- report the stale waves clearly for human review

Suggested reporting language:

> PRD XXXXX appears requirements-complete, but cannot move to Done because the following stale waves are still in non-Done states.

The report should include a markdown table such as:

| Wave | Current State | Why Stale |
|---|---|---|
| `WAVE_...` | `Pending Review` | Requirements already appear satisfied by other completed waves |
| `WAVE_...` | `Needs Triage` | No remaining unmet PRD requirement appears to map to this wave |

## Triage responsibilities

`triage` now has two kinds of responsibility:

### 1. GitHub-backed wave state reconciliation

For waves in `PR Drafted` or `Pending Review`:
- load `pr_url`
- query GitHub via `gh`
- reconcile board state based on PR status

Rules:
- ready-for-review PR => `Pending Review`
- merged PR => `Done`
- closed-unmerged PR => `Blocked`

If a wave is in `PR Drafted` or `Pending Review` but `pr_url` is missing, the wave is malformed and should be flagged.

### 2. Semantic PRD completion evaluation

For each PRD:
- inspect linked waves
- inspect current PRD requirements
- make a best-effort semantic judgment about whether completed waves satisfy the requirements
- detect likely stale open waves
- report ambiguity rather than silently resolving it

## Skill-level implications

### `to-prd`

- stop writing `merge-branch`
- continue creating PRDs as requirements artifacts

### `to-issues`

- assign `branch_name` for each wave at creation time
- branch names should be semantic, not tracker-ID-based

### `tdd`

- still executes a wave from `Ready` through implementation
- should work on the wave's semantic `branch_name`
- when implementation is complete, create a draft PR automatically
- write `pr_url` back to wave frontmatter
- move the wave to `PR Drafted`

### `triage`

- must understand wave-only review states
- must reconcile wave state with GitHub PR state via `gh`
- must semantically evaluate PRD completeness
- must report stale waves in markdown tables when relevant

### `merge-waves`

This skill likely becomes obsolete or must be repurposed, since there is no PRD-level merge branch anymore.

### `merge-prd`

This skill becomes obsolete, since PRDs are no longer merge artifacts.

## Summary

This redesign makes the workflow more honest and review-friendly:
- PRDs track requirements completion
- waves track implementation, review, and merge
- GitHub PR state becomes part of canonical wave progression
- semantic branch names improve reviewer experience
- PRD completion becomes a semantic evaluation, not just a branch-topology event
