# State Model

## Canonical workflow states

- `Needs Triage`
- `Ready`
- `In Progress`
- `Blocked`
- `Done`
- `Merged`

## Source of truth

The board column is canonical.

Issue note frontmatter should be updated best-effort, but all skills should treat the board location as authoritative.

## Responsibility split

- `to-issues` creates work and inserts cards into `Needs Triage`
- `triage` prepares work for execution
- `tdd` executes only `Ready` work
- `merge-issues` moves `Done` cards to `Merged` after merging into the project's merge branch

## TDD gate

`tdd` must refuse or redirect when an issue is not in `Ready`.

## Merged is terminal

`Merged` is the final resting place for cards. No further state transitions occur after `Merged`.
