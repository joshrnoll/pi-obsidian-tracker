# Workflow

This package implements a small Obsidian-vault workflow for planning, triage, and implementation.

## Sequence

1. `setup`
   - Ask for vault path
   - Create/adopt vault
   - Scaffold shared tracker directories and templates
2. `new-project`
   - Create a project with `board.md`, `issues/`, `waves/`, `prds/`, and `config.md`
   - Delegates to `setup` if the vault is not yet initialized
   - Prompts for project name, repo path, and merge branch
3. `to-prd`
   - Create a PRD note in `prds/`
4. `to-issues`
   - Break a PRD into actionable issue notes in `issues/`
   - Group issues into waves based on dependency relationships
   - Create wave files in `waves/` linking to their constituent issues
   - Populate wave `depends_on` (inter-wave) and issue `depends_on` (intra-wave)
   - Add wave cards (not issue cards) to `Needs Triage` on the board
5. `triage`
   - Move wave cards across board columns
   - Validates individual issues within each wave against readiness criteria
   - A wave is `Ready` only when all its issues pass
6. `tdd`
   - Start only from a `Ready` wave
   - Uses a shared worktree per wave (not per issue)
   - Sequences issues within the wave by intra-wave `depends_on` order
   - Moves the wave card through `In Progress` to `Done`
   - Stalls the entire wave (moves to `Blocked`) if any issue is blocked
   - Reads `config.md` for repo path and merge branch
7. `merge-issues`
   - Merge all `Done` wave branches into the project's merge branch
   - Merges in `depends_on` order (waves with no unmerged dependencies first)
   - Move merged wave cards to `Merged`
   - Move conflicted wave cards to `Blocked`

## Design rules

- One board per project
- PRDs stay off the execution board
- Board columns are canonical state for **waves** (not individual issues)
- Wave files carry the issue list; board cards stay minimal (`[[waves/001-wave-name]]`)
- Issue notes carry implementation detail; issues are ordered within waves via `depends_on`
- Wave `depends_on` expresses inter-wave ordering; issue `depends_on` expresses intra-wave ordering only
- Cross-wave issue dependencies are expressed at the wave level — never directly between issues in different waves
- Per-project config (`config.md`) is the canonical source for repo path and merge branch
- Skills must never assume `main` as the merge branch — always read from `config.md`
