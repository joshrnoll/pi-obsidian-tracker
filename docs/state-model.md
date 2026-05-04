# State Model

## Canonical workflow states

Waves are the board-level entity. Both waves and issues share the same state vocabulary, but only wave state is tracked on the board.

- `Needs Triage`
- `Ready`
- `In Progress`
- `Blocked`
- `Done`
- `Merged`

## Source of truth

The board column is canonical for **wave** state.

Issue note frontmatter (`status`, `depends_on`) should be updated best-effort, but all skills treat the board location of the wave card as authoritative for execution gating.

## Dependency model

| Level | Field | Meaning |
|---|---|---|
| Wave → Wave | `depends_on` in wave frontmatter | Inter-wave ordering. Wave B may not start until all waves in its `depends_on` are `Merged`. |
| Issue → Issue | `depends_on` in issue frontmatter | Intra-wave ordering only. An issue may not start until its listed dependencies within the same wave are `Done`. Cross-wave issue dependencies are expressed at the wave level. |

## Responsibility split

- `to-issues` creates issue notes and wave files; inserts wave cards into `Needs Triage`
- `triage` prepares waves for execution by validating all constituent issues
- `tdd` executes only `Ready` waves; works through issues in intra-wave `depends_on` order on a shared wave worktree
- `merge-issues` moves `Done` wave cards to `Merged` after merging the wave branch into the project's merge branch

## TDD gate

`tdd` must refuse or redirect when a wave is not in `Ready`.

## Wave stall on blocked issue

If any issue within a wave is blocked during `tdd`, the entire wave moves to `Blocked`. Work resumes only after the blocking issue is resolved and the wave is moved back to `In Progress`.

## Merged is terminal

`Merged` is the final resting place for wave cards. No further state transitions occur after `Merged`.
