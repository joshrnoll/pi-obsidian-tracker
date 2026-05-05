---
name: merge-waves
description: Merge all Done waves from a project's Kanban board into the project's configured merge branch. Moves merged wave cards to Merged, conflicted wave cards to Blocked. Use when the user wants to integrate completed wave branches into the target branch.
---

# Merge Waves

Merge all `Done` waves for a project into its configured merge branch.

## Before you start

Read:

- [workflow](../../docs/workflow.md)
- [kanban contract](../../docs/obsidian-kanban-contract.md)
- [state model](../../docs/state-model.md)

## Project resolution

Ask for the project name if it is not explicit.

## Read project config

Load `issue-tracker/<project>/board.md` and extract `repo` from frontmatter.

If `repo` is absent from board frontmatter, stop and direct the user to run `new-project` or fix the board manually.

Each wave carries its own `merge-branch` via its `prd` frontmatter field. Resolve the merge branch per wave at merge time (see Merge loop below).

## Situational awareness

Before merging anything, print a summary of:

- Any wave cards currently in `In Progress`
- Any wave cards currently in `Blocked`

Do not touch these cards. This is informational only.

## Collect Done waves

Read all wave cards from the `## Done` column of `board.md`.

Resolve each card to its wave file in `issue-tracker/<project>/waves/`.

For each wave, load its `prd` frontmatter field and resolve the linked PRD file. Extract `merge-branch` from the PRD frontmatter. If a wave is missing a `prd` field, or the linked PRD is missing `merge-branch`, stop and report the malformed file — do not process any waves.

Sort waves in `depends_on` order: waves with no `depends_on` (or whose dependency waves are already `Merged`) come first. Process waves in that order so that upstream branches are present in the merge branch before downstream waves are merged.

If `Done` is empty, report that and exit cleanly.

## Prepare the merge branch

Waves in a single run may belong to different PRDs with different merge branches. Group waves by their `merge-branch` and process each group independently.

For each unique merge branch, in the repo at `repo`:

1. Fetch from remote if a remote exists (`git fetch` — ignore silently if no remote)
2. Check whether the merge branch exists locally or on remote
3. If it does not exist:
   - Check for `main` branch — use it as the base if present
   - Otherwise check for `master` — use it as the base if present
   - If neither exists, stop and ask the user which branch to base the merge branch on
   - Create the merge branch from the chosen base: `git checkout -b <merge-branch> <base>`
4. Check out the merge branch: `git checkout <merge-branch>`

## Merge loop

For each Done wave in dependency order:

1. Resolve the worktree path: `<repo>/.worktrees/<wave-id>` where `wave-id` is the wave filename stem (e.g. `WAVE_00001_PRD_00001_auth-foundation`)
2. Identify the local branch for the wave worktree (`git -C <worktree> branch --show-current`)
3. Attempt the merge: `git merge --no-ff <wave-branch>`
4. **On success:**
   - Delete the worktree: `git worktree remove <worktree-path>`
   - Delete the local branch: `git branch -d <wave-branch>`
   - Move the wave board card from `Done` to `Merged`
   - Update the wave note `status` frontmatter to `merged`
5. **On conflict:**
   - Abort the merge: `git merge --abort`
   - Leave the worktree in place
   - Move the wave board card from `Done` to `Blocked`
   - Update the wave note `status` frontmatter to `blocked`
   - Append a conflict note to the wave file:
     ```
     **Merge conflict** ({{date}}): Conflict merging into `{{merge-branch}}`. Worktree left at `.worktrees/{{wave-id}}` for manual resolution.
     ```
   - Continue to the next wave

## Rules

- Only touch `Done` wave cards — never `In Progress`, `Blocked`, `Ready`, or `Needs Triage`
- Process waves in `depends_on` order (upstream first)
- Never force-merge or auto-resolve conflicts
- Preserve all existing board formatting when moving cards
- Treat board frontmatter as the sole authority for repo path
- Treat each wave's linked PRD frontmatter as the sole authority for merge branch
- Hard error if any wave is missing its `prd` field or the linked PRD is missing `merge-branch`

## Output

Summarize:

- project name
- merge branches used (grouped by PRD)
- waves merged successfully (with branch names)
- waves that conflicted and were moved to `Blocked`
- final board state snapshot (Done, Merged, Blocked counts)
