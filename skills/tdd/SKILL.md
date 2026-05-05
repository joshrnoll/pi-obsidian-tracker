---
name: tdd
description: Implement a wave of work with TDD from a project's Obsidian Kanban board. Use when the user wants to execute a Ready wave with red-green-refactor while updating board state from Ready to In Progress to Done.
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

Load the wave file and extract the `prd` frontmatter field. Load the linked PRD file and extract `merge-branch` — recorded for reference; `tdd` does not merge, but the worktree branch should be created from the PRD's `merge-branch`.

If `repo` is absent from board frontmatter, stop and direct the user to run `new-project` or fix the board manually.

If the wave is missing a `prd` field, or the linked PRD is missing `merge-branch`, stop and report the malformed file — do not proceed.

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
> All work in a wave is done on a **shared wave worktree** named after the wave ID. Example:
> Work for wave `WAVE_00001_PRD_00001_auth-foundation.md` is done on `<repo>/.worktrees/WAVE_00001_PRD_00001_auth-foundation`
> where `<repo>` is read from board frontmatter, not inferred from the project name.
> Do not create separate worktrees per issue within the wave.

6. Work through issues in dependency order using red-green-refactor for each issue
7. After completing each issue: update the issue note `status` to `Done` in its frontmatter; there are no individual issue cards on the board to move

## Finishing work

When all issues in the wave are done:

- Ensure all work is committed using semantic commits; commits should logically group work together for a clean history
- Move the wave card from `In Progress` to `Done`
- Update the wave note `status` frontmatter to `Done`
- Summarize tests written and behavior implemented across all issues in the wave

## If blocked

If progress halts on an issue due to an external dependency or unresolved decision:

- Ensure all work is committed
- Move the wave card from `In Progress` to `Blocked`
- Update the wave note `status` frontmatter to `Blocked`
- Note which specific issue is the blocker and why
- The entire wave is stalled — do not continue to other issues in the wave

## Rules

- Do not start from `Needs Triage`
- Treat the board as the workflow source of truth for wave state
- Execute one wave at a time
- Use one shared worktree per wave — never create per-issue worktrees
- Keep implementation of each issue anchored to its acceptance criteria
- Issue `depends_on` is intra-wave only — do not cross wave boundaries

## Output

Summarize:

- project name
- wave chosen
- board transitions performed
- issues completed (in order) and tests added/updated per issue
- final state (`Done` or `Blocked`; if `Blocked`, name the blocking issue)
