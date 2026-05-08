---
name: tdd
description: Implement a wave of work with TDD from a project's Obsidian Kanban board. Use when the user wants to execute a Ready wave with red-green-refactor while updating board state from Ready to In Progress to PR Drafted (or Blocked).
---

# TDD Obsidian

Implement one wave using TDD while participating strictly in the Obsidian workflow.

## Before you start

Read:

- [workflow](../../docs/workflow.md)
- [kanban contract](../../docs/obsidian-kanban-contract.md)
- [state model](../../docs/state-model.md)

## Read project config

Load `issue-tracker/<project>/board.md` and extract `repo` from frontmatter.

Load the wave file and extract:
- `branch_name` — the semantic branch to work on
- `prd` — the linked PRD (for traceability only; no merge-branch is needed)

If `repo` is absent from board frontmatter, stop and direct the user to run `new-project` or fix the board manually.

If the wave is missing `branch_name`, stop and report the malformed file — do not proceed.

## Project resolution

Ask for the project name if it is not explicit.

## Hard gate

You may only start from a wave card currently in `Ready`.

If the requested wave is in any other column:

- refuse to start implementation from it
- explain which column it is in
- direct the user to `triage` or to move it to `Ready` first

## Starting work

When starting valid work:

1. Identify the target wave from the board
2. Read the linked wave file to get the list of issues and their `depends_on` relationships
3. Determine the execution order: issues with no `depends_on` start first; issues whose `depends_on` are all `Done` are next; and so on (topological sort within the wave)
4. Move the wave board card from `Ready` to `In Progress`
5. Create or reuse a single worktree for the entire wave:

> [!NOTE]
> All work in a wave is done on a **shared wave worktree** using the wave's `branch_name`. Example:
> Work for wave `WAVE_00001_PRD_00001_auth-foundation.md` with `branch_name: feat/auth-foundation` is done on `<repo>/.worktrees/feat/auth-foundation`
> where `<repo>` is read from board frontmatter, not inferred from the project name.
> The worktree branch is created from `main`.
> Do not create separate worktrees per issue within the wave.

6. Work through issues in dependency order using red-green-refactor for each issue
7. After completing each issue: update the issue note `status` to `Done` in its frontmatter; there are no individual issue cards on the board to move

## Finishing work

When all issues in the wave are done:

1. Ensure all work is committed using semantic commits; commits should logically group work together for a clean history
2. Rebase onto latest `main` before pushing
3. Push the branch to the remote
4. Create a draft PR via `gh pr create --draft`:
   - **Title**: human-first, reviewer-friendly — do not lead with wave IDs
   - **Body** format:
     ```
     ## Summary
     <brief summary of the wave's purpose>

     ## What changed
     <list of meaningful changes>

     ## How to review
     <suggested review strategy>

     ## Tracker metadata
     - Wave: `<wave filename>`
     - PRD: `<PRD filename>`
     ```
5. Write `pr_url` back to the wave note frontmatter
6. Move the wave card from `In Progress` to `PR Drafted`
7. Update the wave note `status` frontmatter to `pr-drafted`

### Babysit CI

After drafting the PR, attempt to babysit CI using the `babysit-ci` skill:

- If the `babysit-ci` skill is available **and** the repo has CI configured (GitHub Actions workflows exist): run `babysit-ci`
- If the `babysit-ci` skill is unavailable or the repo has no CI: skip this step entirely

**On terminal CI failure** (babysit-ci exhausts retries or encounters an unfixable failure):
- Move the wave card from `PR Drafted` to `Blocked`
- Update the wave note `status` frontmatter to `blocked`

**On CI success**: no board state change — wave stays at `PR Drafted`.

## If blocked

If progress halts on an issue due to an external dependency or unresolved decision:

- Ensure all work is committed
- Move the wave card from `In Progress` to `Blocked`
- Update the wave note `status` frontmatter to `blocked`
- Note which specific issue is the blocker and why
- The entire wave is stalled — do not continue to other issues in the wave

## Rules

- Do not start from `Needs Triage`
- Treat the board as the workflow source of truth for wave state
- Execute one wave at a time
- Use one shared worktree per wave — never create per-issue worktrees
- Keep implementation of each issue anchored to its acceptance criteria
- Issue `depends_on` is intra-wave only — do not cross wave boundaries
- PR titles must be human-first — no leading wave IDs
- Always rebase onto `main` before pushing

## Output

Summarize:

- project name
- wave chosen
- board transitions performed
- issues completed (in order) and tests added/updated per issue
- PR URL (if drafted)
- CI status (if babysit-ci ran)
- final state (`PR Drafted` or `Blocked`; if `Blocked`, name the reason)
