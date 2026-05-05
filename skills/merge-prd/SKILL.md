---
name: merge-prd
description: Merge a PRD's merge branch into main/master after all associated waves have been merged. Hard-gates on the PRD card being in Merged and all associated waves being Merged. Deletes the merge branch on success.
---

# Merge PRD

Merge a completed PRD's feature branch into `main` or `master`.

## Before you start

Read:
- [workflow](../../docs/workflow.md)
- [kanban contract](../../docs/obsidian-kanban-contract.md)
- [state model](../../docs/state-model.md)

## Project and PRD resolution

Ask for the project name and PRD if not already provided.

Read `issue-tracker/<project>/board.md` and extract `repo` from frontmatter.

Locate the PRD file in `issue-tracker/<project>/prds/` and extract:
- `merge-branch` — the feature branch to merge into main
- `title` — for reporting

## Hard gate — belt and suspenders

Before touching the repo, perform **both** checks:

### Check 1: PRD card location
Read `board.md` and confirm the PRD card (`[[prds/<prd-file>]]`) is in the `## Merged` column.

If it is not in `Merged`, stop and report:
- current column the PRD card is in
- what needs to happen before `merge-prd` can run

### Check 2: All associated waves are Merged
Scan all wave files in `issue-tracker/<project>/waves/` for files where the `prd` frontmatter field matches this PRD.

Confirm every associated wave card appears in the `## Merged` column on the board.

If any wave is not in `Merged`, stop and report:
- which waves are not yet merged
- which columns they are currently in

Both checks must pass before proceeding.

## Merge

In the repo at `repo`:

1. Fetch from remote if a remote exists (`git fetch` — ignore silently if no remote)
2. Determine the base branch:
   - Check for `main` — use it if present
   - Otherwise check for `master` — use it if present
   - If neither exists, stop and ask the user which branch to merge into
3. Check out the base branch: `git checkout <base>`
4. Merge the PRD's feature branch with a no-fast-forward merge:
   ```bash
   git merge --no-ff <merge-branch> -m "merge: <prd-title> (<merge-branch>)"
   ```
5. **On success:**
   - Delete the local merge branch: `git branch -d <merge-branch>`
   - Delete the remote branch if a remote exists: `git push origin --delete <merge-branch>` (ignore silently if remote branch does not exist)
6. **On conflict:**
   - Abort the merge: `git merge --abort`
   - Do not delete the branch
   - Report the conflict clearly and stop — do not attempt to auto-resolve

## Rules

- Never proceed if either hard gate check fails
- Never force-merge or auto-resolve conflicts
- Never assume `main` — always check for `main` then `master`
- Delete the merge branch only after a confirmed successful merge

## Output

Summarize:
- project name
- PRD title and file
- merge branch merged
- base branch merged into
- whether the merge branch was deleted locally and remotely
- or: conflict details and next steps if the merge failed
