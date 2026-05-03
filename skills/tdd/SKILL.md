---
name: tdd
description: Implement work with TDD from a project's Obsidian Kanban board. Use when the user wants to execute a Ready issue with red-green-refactor while updating board state from Ready to In Progress to Done.
---

# TDD Obsidian

Implement one issue using TDD while participating strictly in the Obsidian workflow.

## Before you start

Read:
- [workflow](../../docs/workflow.md)
- [kanban contract](../../docs/obsidian-kanban-contract.md)
- [state model](../../docs/state-model.md)

## Project resolution

Ask for the project name if it is not explicit.

## Hard gate

You may only start from an issue card currently in `Ready`.

If the requested issue is in any other column:
- refuse to start implementation from it
- explain which column it is in
- direct the user to `triage` or to move it to `Ready` first

## Starting work

When starting valid work:
1. identify the target issue from the board
2. read the linked issue note
3. use the issue's acceptance criteria as the implementation target
4. move the board card from `Ready` to `In Progress`
5. implement using red-green-refactor

## Finishing work

When acceptance criteria are satisfied:
- move the card from `In Progress` to `Done`
- optionally update issue note status best-effort
- summarize tests written and behavior implemented

## If blocked

If progress halts on an external dependency or unresolved decision:
- move the card from `In Progress` to `Blocked`
- explain the blocking reason clearly

## Rules

- Do not start from `Needs Triage`
- Treat the board as the workflow source of truth
- Execute one issue at a time
- Keep implementation anchored to acceptance criteria

## Output

Summarize:
- project name
- issue chosen
- board transitions performed
- tests added/updated
- final state (`Done` or `Blocked`)
