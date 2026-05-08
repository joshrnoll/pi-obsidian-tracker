# Workflow

This package implements a small Obsidian-vault workflow for planning, triage, and implementation. Each project maps 1:1 to a repository.

## Sequence

1. `setup`
   - Ask for vault path
   - Create/adopt vault
   - Scaffold shared tracker directories and templates
2. `new-project`
   - Create a project with `board.md`, `issues/`, `waves/`, and `prds/`
   - Prompts for project name and repo path only
   - Delegates to `setup` if the vault is not yet initialized
3. `to-prd`
   - Create a PRD note in `prds/` as a requirements-tracking artifact
   - Insert the PRD card into `Needs Triage` on the board
4. `to-issues`
   - Break a PRD into actionable issue notes in `issues/`
   - Group issues into waves based on dependency relationships
   - Create wave files in `waves/` with an explicit `prd` wikilink field and semantic `branch_name`
   - Populate wave `depends_on` (inter-wave) and issue `depends_on` (intra-wave)
   - Add wave cards (not issue cards, not PRD cards) to `Needs Triage` on the board
5. `triage`
   - **Phase 1 — Wave readiness**: move wave cards from `Needs Triage` to `Ready`; validates individual issues within each wave against readiness criteria
   - **Phase 2 — GitHub reconciliation**: reconcile wave state with GitHub PR state for waves in `PR Drafted` or `Pending Review`
   - **Phase 3 — PRD evaluation**: derive PRD state from aggregate wave states; evaluate semantic PRD completion; report stale waves
   - Always runs full-board; always runs phases in order
6. `tdd`
   - Start only from a `Ready` wave
   - Uses a shared worktree per wave (not per issue); worktree named after the wave's `branch_name`
   - Sequences issues within the wave by intra-wave `depends_on` order
   - Red-green-refactor for each issue
   - On completion: rebase onto `main`, push, create draft PR, write `pr_url` to wave frontmatter, move to `PR Drafted`
   - Babysit CI if the `babysit-ci` skill is available and the repo has CI configured
   - On terminal CI failure: move to `Blocked`
   - Stalls the entire wave (moves to `Blocked`) if any issue is blocked during implementation
   - Reads `repo` from board frontmatter; reads `branch_name` from wave frontmatter
7. `dispatch-ready-waves`
   - Launch one interactive `pi` subagent per `Ready` wave in a tmux session
   - Fire and forget — each subagent runs its full `tdd` lifecycle independently
   - Dependency gate: waves wait until all `depends_on` waves are `Done` before starting

## Design rules

- One board per project; one project per repository
- PRDs are on the board — they are requirements-tracking artifacts
- Waves are on the board — they are the deployable/reviewable unit (each wave = one PR)
- Issues are never on the board
- Board columns are canonical state for both waves and PRDs
- Wave files carry the issue list; board cards stay minimal (`[[waves/WAVE_00001_PRD_00001_slug]]`)
- Issue notes carry implementation detail; issues are ordered within waves via `depends_on`
- Wave `depends_on` expresses inter-wave ordering; issue `depends_on` expresses intra-wave ordering only
- Cross-wave issue dependencies are expressed at the wave level — never directly between issues in different waves
- `repo` is stored in board frontmatter; it is the canonical source for the repo path
- `branch_name` is stored in wave frontmatter; it is the semantic branch for that wave
- `pr_url` is stored in wave frontmatter; it is written by `tdd` after draft PR creation
- PRD → wave association is discovered by scanning wave `prd` fields (not a reverse list on the PRD)
- Tags must be written consistently: project-derived tags are kebab-case; waves and issues carry parent artifact tags in kebab-case; PRDs carry the literal `PRD` tag

## Naming conventions

All numbers are 5-digit zero-padded and flat per-project (sequences do not reset per PRD or wave).

| Artifact | Pattern |
|---|---|
| PRD | `PRD_00001_descriptive-title.md` |
| Wave | `WAVE_00001_PRD_00001_descriptive-slug.md` |
| Issue | `ISSUE_00001_WAVE_00001_PRD_00001_descriptive-slug.md` |
