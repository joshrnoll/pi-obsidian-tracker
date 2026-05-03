# State Model

## Canonical workflow states

- `Needs Triage`
- `Ready`
- `In Progress`
- `Blocked`
- `Done`

## Source of truth

The board column is canonical.

Issue note frontmatter should be updated best-effort, but all skills should treat the board location as authoritative.

## Responsibility split

- `to-issues` creates work and inserts cards into `Needs Triage`
- `triage` prepares work for execution
- `tdd` executes only `Ready` work

## TDD gate

`tdd` must refuse or redirect when an issue is not in `Ready`.
