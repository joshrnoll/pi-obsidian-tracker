---
name: new-project
description: Scaffold a new project in the Obsidian issue tracker. Use when the user wants to create a new project with a board, issue directory, PRD directory, and per-project config. Prompts for project name, repo path, and merge branch.
---

# New Project

Scaffold a new project under the Obsidian tracker root.

## Before you start

Read:
- [workflow](../../docs/workflow.md)
- [kanban contract](../../docs/obsidian-kanban-contract.md)
- [state model](../../docs/state-model.md)
- [board template](../../templates/board.md)
- [project-config template](../../templates/project-config.md)

## Vault check

Locate the tracker root by reading the global config at:

```text
issue-tracker/_config/pi-obsidian-tracker.md
```

If `issue-tracker/` does not exist under the vault path, **stop and instruct the user to run the `setup` skill first** before creating any projects.

## Collect project details

Ask for the following if not already provided:

1. **Project name** — human-readable, e.g. `DIBaseConfig Versioned Immutability`
2. **Repo path** — absolute or `~`-prefixed path to the local git repo, e.g. `~/repos/infra`
3. **Merge branch** — the branch issues should be merged into, e.g. `feat-dibaseconfig-versioned-immutability` or `main`

## Scaffold

Create the following structure under the vault's `issue-tracker/`:

```text
issue-tracker/<project-name>/
  board.md         ← from templates/board.md
  config.md        ← from templates/project-config.md
  issues/
  waves/
  prds/
```

Substitute template placeholders:
- `{{project-name}}` → the project name provided
- `{{repo-path}}` → the repo path provided
- `{{merge-branch}}` → the merge branch provided

## Rules

- Derive a safe directory name from the project name: lowercase, spaces to hyphens, strip special characters
- Do not overwrite an existing project directory — inspect first and warn the user
- Do not create an initial PRD or issues unless explicitly asked
- Keep the `## Notes` section in `config.md` empty

## Output

Summarize:
- project name
- directory created
- repo path recorded
- merge branch recorded
- files created
