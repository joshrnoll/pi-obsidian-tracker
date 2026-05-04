# pi-obsidian-tracker

Pi skills for running a lightweight Obsidian-vault issue tracker workflow.

## Included skills

- `setup` — initialize the vault and scaffold shared tracker structure
- `new-project` — create a new project with board, config, issues, and prds directories
- `to-prd` — capture conversation context as a PRD note
- `to-issues` — break a PRD into actionable issue notes on the board
- `triage` — move issue cards across board columns
- `tdd` — implement a `Ready` issue using red-green-refactor
- `merge-issues` — merge all `Done` issues into the project's configured merge branch

## Workflow

```
setup → new-project → to-prd → to-issues → triage → tdd → merge-issues
```

Each project lives under:

```text
issue-tracker/<project-name>/
  board.md
  config.md
  issues/
  prds/
```

### Per-project config

Each project has a `config.md` with YAML frontmatter:

```yaml
---
project: My Project Name
repo: ~/repos/my-repo
merge-branch: main
---

## Notes
```

This is the canonical source for repo path and merge branch. Skills must never
assume `main` — they always read from `config.md`.

### Canonical board columns

- `Needs Triage`
- `Ready`
- `In Progress`
- `Blocked`
- `Done`
- `Merged` ← terminal; cards do not move out of this column

### Rules

- PRDs are planning artifacts and stay in `prds/`
- The board column is the source of truth for workflow state
- `tdd` only starts from `Ready`
- `merge-issues` only touches `Done` cards, processes them numerically, and moves them to `Merged` on success or `Blocked` on conflict
- Projects must be created with `new-project` — `to-prd` and `to-issues` will not lazily scaffold a project

## Install in Pi

Clone this repo and install using `pi install`:

```bash
pi install /path/to/git/clone
```

Or add the path to settings/packages manually.

## Notes

- This repo is skill-only; no custom extension code yet.
- Templates live in `templates/`.
- Explanatory docs live in `docs/`.
