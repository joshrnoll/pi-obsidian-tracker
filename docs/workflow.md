# Workflow

This package implements a small Obsidian-vault workflow for planning, triage, and implementation. Each project maps 1:1 to a repository.

## Sequence

1. `setup`
   - Ask for vault path
   - Create/adopt vault
   - Scaffold shared tracker directories and templates
2. `new-project`
   - Create a project with `board.md`, `issues/`, `waves/`, and `prds/`
   - Prompts for project name and repo path only — no merge branch
   - Delegates to `setup` if the vault is not yet initialized
3. `to-prd`
   - Create a PRD note in `prds/` with a `merge-branch` field
   - Insert the PRD card into `Needs Triage` on the board
4. `to-issues`
   - Break a PRD into actionable issue notes in `issues/`
   - Group issues into waves based on dependency relationships
   - Create wave files in `waves/` with an explicit `prd` wikilink field
   - Populate wave `depends_on` (inter-wave) and issue `depends_on` (intra-wave)
   - Add wave cards (not issue cards, not PRD cards) to `Needs Triage` on the board
5. `triage`
   - **Wave phase**: move wave cards across board columns; validates individual issues within each wave against readiness criteria
   - **PRD phase**: derive PRD state from aggregate wave states; move PRD cards to correct columns
   - Always runs full-board; always runs wave phase before PRD phase
6. `tdd`
   - Start only from a `Ready` wave
   - Uses a shared worktree per wave (not per issue); worktree named after the full wave stem
   - Sequences issues within the wave by intra-wave `depends_on` order
   - Moves the wave card through `In Progress` to `Done`
   - Stalls the entire wave (moves to `Blocked`) if any issue is blocked
   - Reads `repo` from board frontmatter; reads `merge-branch` from the wave's `prd` frontmatter field
7. `merge-waves`
   - Merge all `Done` wave branches into each wave's PRD `merge-branch`
   - Merges in `depends_on` order (waves with no unmerged dependencies first)
   - Reads `repo` from board frontmatter; reads `merge-branch` from each wave's `prd` field
   - Move merged wave cards to `Merged`; move conflicted wave cards to `Blocked`
   - Hard error if any wave is missing its `prd` field
8. `merge-prd`
   - Merge a PRD's `merge-branch` into `main`/`master`
   - Hard gate: PRD card must be in `Merged` **and** all associated waves must be in `Merged`
   - Deletes the `merge-branch` after a successful merge

## Design rules

- One board per project; one project per repository
- PRDs are on the board — they represent groups of effort (feature branches)
- Waves are on the board — they represent implementation batches within a PRD
- Issues are never on the board
- Board columns are canonical state for both waves and PRDs
- Wave files carry the issue list; board cards stay minimal (`[[waves/WAVE_00001_PRD_00001_slug]]`)
- Issue notes carry implementation detail; issues are ordered within waves via `depends_on`
- Wave `depends_on` expresses inter-wave ordering; issue `depends_on` expresses intra-wave ordering only
- Cross-wave issue dependencies are expressed at the wave level — never directly between issues in different waves
- `repo` is stored in board frontmatter; it is the canonical source for the repo path
- `merge-branch` is stored in PRD frontmatter; it is the canonical source for the feature branch
- Skills must never assume `main` as the merge branch — always read from the PRD file
- PRD → wave association is discovered by scanning wave `prd` fields (not a reverse list on the PRD)
- Tags must be written consistently: project-derived tags are kebab-case; waves and issues carry parent artifact tags in kebab-case; PRDs carry the literal `PRD` tag

## Naming conventions

All numbers are 5-digit zero-padded and flat per-project (sequences do not reset per PRD or wave).

| Artifact | Pattern |
|---|---|
| PRD | `PRD_00001_descriptive-title.md` |
| Wave | `WAVE_00001_PRD_00001_descriptive-slug.md` |
| Issue | `ISSUE_00001_WAVE_00001_PRD_00001_descriptive-slug.md` |
