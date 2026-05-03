# pi-obsidian-tracker

Pi skills for running a lightweight Obsidian-vault issue tracker workflow.

## Included skills

- `setup`
- `to-prd`
- `to-issues`
- `triage`
- `tdd`

## Workflow

Each project lives under:

```text
issue-tracker/<project-name>/
  board.md
  issues/
  prds/
```

Canonical board columns:

- `Needs Triage`
- `Ready`
- `In Progress`
- `Blocked`
- `Done`

Rules:
- PRDs are planning artifacts and stay in `prds/`
- PRDs use a richer product-style structure: problem statement, solution, user stories, implementation decisions, testing decisions, out of scope, and further notes
- The board column is the source of truth for workflow state
- `tdd` only starts from `Ready`

## Install in Pi

From a local checkout:

```bash
pi install /var/home/josh/github/pi-obsidian-tracker
```

Or add the path to settings/packages manually.

## Notes

- This repo is skill-only; no custom extension code yet.
- Templates live in `templates/`.
- Explanatory docs live in `docs/`.
