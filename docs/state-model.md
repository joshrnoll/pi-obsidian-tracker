# State Model

## Canonical workflow states

Both waves and PRDs share the same state vocabulary and the same board columns. Issues share the state vocabulary but are not tracked on the board.

- `Needs Triage`
- `Ready`
- `In Progress`
- `Blocked`
- `Done`
- `Merged`

## Source of truth

The board column is canonical for **wave** and **PRD** state.

Issue note frontmatter (`status`, `depends_on`) should be updated best-effort, but all skills treat the board location of the wave card as authoritative for execution gating.

## PRD state rules

PRD state is derived from the aggregate state of its associated waves. `triage` enforces these rules when evaluating PRD cards.

| PRD State | Condition |
|---|---|
| `Needs Triage` | At least one associated wave or issue needs triage; or PRD has no waves yet |
| `Ready` | All associated waves are in `Ready` state |
| `In Progress` | At least one associated wave is `In Progress` |
| `Blocked` | At least one associated wave is `Blocked` |
| `Done` | All associated waves are `Done` |
| `Merged` | All associated waves are `Merged` into the PRD's `merge-branch` |

PRD state is **manually managed** via the `triage` skill. Skills that transition wave state do not automatically move PRD cards — `triage` must be re-run after wave state changes to bring PRD cards into sync.

## Wave state rules

Wave state is determined by the aggregate state of its constituent issues and execution progress.

## Dependency model

| Level | Field | Meaning |
|---|---|---|
| Wave → Wave | `depends_on` in wave frontmatter | Inter-wave ordering. Wave B may not start until all waves in its `depends_on` are `Merged`. |
| Issue → Issue | `depends_on` in issue frontmatter | Intra-wave ordering only. An issue may not start until its listed dependencies within the same wave are `Done`. Cross-wave issue dependencies are expressed at the wave level. |

## Association model

| Artifact | Field | Points to |
|---|---|---|
| Wave | `prd` | Parent PRD wikilink |
| Issue | `prd` | Parent PRD wikilink |

PRD → wave association is discovered by scanning all wave files for a matching `prd` field. PRD files do not maintain a reverse list of waves.

## Responsibility split

- `to-prd` creates PRD notes and inserts PRD cards into `Needs Triage`
- `to-issues` creates issue notes and wave files; inserts wave cards into `Needs Triage`
- `triage` moves both wave cards and PRD cards: wave phase first, then PRD phase
- `tdd` executes only `Ready` waves; works through issues in intra-wave `depends_on` order on a shared wave worktree
- `merge-waves` merges `Done` wave branches into the wave's PRD `merge-branch`; moves wave cards to `Merged`
- `merge-prd` merges a PRD's `merge-branch` into `main`/`master`; hard-gates on PRD card being `Merged` and all associated waves being `Merged`

## TDD gate

`tdd` must refuse or redirect when a wave is not in `Ready`.

## Wave stall on blocked issue

If any issue within a wave is blocked during `tdd`, the entire wave moves to `Blocked`. Work resumes only after the blocking issue is resolved and the wave is moved back to `In Progress`.

## Merged is terminal

`Merged` is the final resting place for wave and PRD cards. No further state transitions occur after `Merged`.

## Hard errors

- A wave without a `prd` frontmatter field is malformed. `tdd`, `merge-waves`, and `triage` must stop and report it.
- A PRD without a `merge-branch` frontmatter field is malformed. `merge-waves` and `merge-prd` must stop and report it.
