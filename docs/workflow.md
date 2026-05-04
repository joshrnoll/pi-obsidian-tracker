# Workflow

This package implements a small Obsidian-vault workflow for planning, triage, and implementation.

## Sequence

1. `setup`
   - Ask for vault path
   - Create/adopt vault
   - Scaffold shared tracker directories and templates
2. `new-project`
   - Create a project with `board.md`, `issues/`, `prds/`, and `config.md`
   - Delegates to `setup` if the vault is not yet initialized
   - Prompts for project name, repo path, and merge branch
3. `to-prd`
   - Create a PRD note in `prds/`
4. `to-issues`
   - Break a PRD into actionable issue notes in `issues/`
   - Add cards to `Needs Triage`
5. `triage`
   - Move issue cards across board columns
6. `tdd`
   - Start only from `Ready`
   - Move through `In Progress` to `Done`
   - Reads `config.md` for repo path and merge branch
7. `merge-issues`
   - Merge all `Done` cards numerically into the project's merge branch
   - Move merged cards to `Merged`
   - Move conflicted cards to `Blocked`

## Design rules

- One board per project
- PRDs stay off the execution board
- Board columns are canonical state
- Issue notes carry detail; board cards stay minimal
- Per-project config (`config.md`) is the canonical source for repo path and merge branch
- Skills must never assume `main` as the merge branch — always read from `config.md`
