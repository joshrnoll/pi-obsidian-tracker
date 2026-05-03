# Workflow

This package implements a small Obsidian-vault workflow for planning, triage, and implementation.

## Sequence

1. `setup`
   - Ask for vault path
   - Create/adopt vault
   - Scaffold shared tracker directories and templates
2. `to-prd`
   - Create a PRD note in `prds/`
3. `to-issues`
   - Break a PRD into actionable issue notes in `issues/`
   - Add cards to `Needs Triage`
4. `triage`
   - Move issue cards across board columns
5. `tdd`
   - Start only from `Ready`
   - Move through `In Progress` to `Done`

## Design rules

- One board per project
- PRDs stay off the execution board
- Board columns are canonical state
- Issue notes carry detail; board cards stay minimal
