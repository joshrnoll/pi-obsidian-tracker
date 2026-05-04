---
name: merge-issues
description: Merge all Done issues from a project's Kanban board into the project's configured merge branch. Moves merged cards to Merged, conflicted cards to Blocked. Use when the user wants to integrate completed work into the target branch.
---

# Merge Issues

Merge all `Done` issues for a project into its configured merge branch.

## Before you start

Read:
- [workflow](../../docs/workflow.md)
- [kanban contract](../../docs/obsidian-kanban-contract.md)
- [state model](../../docs/state-model.md)

## Project resolution

Ask for the project name if it is not explicit.

## Read project config

Load `issue-tracker/<project>/config.md` and extract:
- `repo` — path to the local git repo
- `merge-branch` — branch to merge issues into

If `config.md` is missing or either field is absent, stop and direct the user to run `new-project` or fix the config manually.

## Situational awareness

Before merging anything, print a summary of:
- Any cards currently in `In Progress`
- Any cards currently in `Blocked`

Do not touch these cards. This is informational only.

## Collect Done issues

Read all cards from the `## Done` column of `board.md`.

Sort them numerically by issue number (e.g. `001-auth-routes` before `002-db-schema`).

If `Done` is empty, report that and exit cleanly.

## Prepare the merge branch

In the repo at `repo`:

1. Fetch from remote if a remote exists (`git fetch` — ignore silently if no remote)
2. Check whether `merge-branch` exists locally or on remote
3. If it does not exist:
   - Check for `main` branch — use it as the base if present
   - Otherwise check for `master` — use it as the base if present
   - If neither exists, stop and ask the user which branch to base the merge branch on
   - Create the merge branch from the chosen base: `git checkout -b <merge-branch> <base>`
4. Check out the merge branch: `git checkout <merge-branch>`

## Merge loop

For each Done issue in numerical order:

1. Resolve the worktree path: `<repo>/.worktrees/<issue-id>`
2. Identify the local branch for the issue worktree (`git -C <worktree> branch --show-current`)
3. Attempt the merge: `git merge --no-ff <issue-branch>`
4. **On success:**
   - Delete the worktree: `git worktree remove <worktree-path>`
   - Delete the local branch: `git branch -d <issue-branch>`
   - Move the board card from `Done` to `Merged`
   - Update the issue note `status` frontmatter to `merged`
5. **On conflict:**
   - Abort the merge: `git merge --abort`
   - Leave the worktree in place
   - Move the board card from `Done` to `Blocked`
   - Update the issue note `status` frontmatter to `blocked`
   - Append a conflict note to the `## Notes` section of the issue file:
     ```
     **Merge conflict** ({{date}}): Conflict merging into `{{merge-branch}}`. Worktree left at `.worktrees/{{issue-id}}` for manual resolution.
     ```
   - Continue to the next issue

## Rules

- Only touch `Done` cards — never `In Progress`, `Blocked`, `Ready`, or `Needs Triage`
- Process issues strictly in numerical order
- Never force-merge or auto-resolve conflicts
- Preserve all existing board formatting when moving cards
- Treat `config.md` as the sole authority for repo path and merge branch

## Output

Summarize:
- project name
- merge branch used
- issues merged successfully (with branch names)
- issues that conflicted and were moved to `Blocked`
- final board state snapshot (Done, Merged, Blocked counts)
