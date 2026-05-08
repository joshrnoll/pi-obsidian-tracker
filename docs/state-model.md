# State Model

## Wave states

- `Needs Triage`
- `Ready`
- `In Progress`
- `Blocked`
- `PR Drafted`
- `Pending Review`
- `Done` (terminal — wave PR has been merged to `main`)

## PRD states

- `Needs Triage`
- `Ready`
- `In Progress`
- `Blocked`
- `Done` (terminal — PRD requirements are satisfied)

PRDs do not enter `PR Drafted` or `Pending Review`.

## Source of truth

The board column is canonical for **wave** and **PRD** state.

Issue note frontmatter (`status`, `depends_on`) should be updated best-effort, but all skills treat the board location of the wave card as authoritative for execution gating.

## Wave state semantics

- `In Progress`: implementation is actively happening on the wave branch
- `PR Drafted`: implementation is complete, committed locally, and a draft PR has been created
- `Pending Review`: the PR has been marked ready for review (by the human)
- `Done`: the PR has been merged to `main`

## PRD state semantics

- `Done` means the PRD's requirements have been semantically satisfied by waves in `Done`
- PRD `Done` is not tied to a merge event — PRDs are requirements-tracking artifacts, not merge artifacts

## PRD state rules

PRD state is derived from associated wave states and semantic evaluation. `triage` enforces these rules.

| PRD State | Condition |
|---|---|
| `Needs Triage` | PRD has no waves yet, or requirements are not fully captured by waves |
| `Ready` | All requirements are captured by waves, and all associated waves are `Ready` or later |
| `In Progress` | At least one associated wave is `In Progress`, `PR Drafted`, or `Pending Review` |
| `Blocked` | At least one associated wave is `Blocked` (and none are in active states) |
| `Done` | All current PRD requirements are semantically satisfied by waves in `Done`, with no stale open waves |

PRD state is managed by `triage`. PRD `Done` requires semantic evaluation — it is not a naive aggregate of wave states. The human is the final decision-maker.

## Wave transition rules

| Transition | Trigger |
|---|---|
| `Needs Triage` → `Ready` | `triage` validates all issues are actionable and wave metadata is complete |
| `Ready` → `In Progress` | `tdd` starts implementation |
| `In Progress` → `PR Drafted` | `tdd` completes implementation, pushes branch, creates draft PR |
| `In Progress` → `Blocked` | `tdd` encounters a blocking issue |
| `PR Drafted` → `Pending Review` | `triage` detects PR is no longer a draft on GitHub |
| `PR Drafted` → `Blocked` | `triage` detects PR closed without merge, merge conflicts, or missing `pr_url`; or `tdd` encounters terminal CI failure |
| `Pending Review` → `Done` | `triage` detects PR has been merged on GitHub |
| `Pending Review` → `Blocked` | `triage` detects PR closed without merge or merge conflicts |

## Dependency model

| Level | Field | Meaning |
|---|---|---|
| Wave → Wave | `depends_on` in wave frontmatter | Inter-wave ordering. Wave B may not start until all waves in its `depends_on` are `Done`. |
| Issue → Issue | `depends_on` in issue frontmatter | Intra-wave ordering only. An issue may not start until its listed dependencies within the same wave are `Done`. Cross-wave issue dependencies are expressed at the wave level. |

## Association model

| Artifact | Field | Points to |
|---|---|---|
| Wave | `prd` | Parent PRD wikilink |
| Wave | `branch_name` | Semantic branch name for this wave |
| Wave | `pr_url` | GitHub PR URL (written by `tdd` after draft PR creation) |
| Issue | `prd` | Parent PRD wikilink |

PRD → wave association is discovered by scanning all wave files for a matching `prd` field. PRD files do not maintain a reverse list of waves.

## Tag model

- All project-derived and parent-derived tags must be kebab-case
- PRD files must carry `PRD` plus the project tag
- Wave files must carry `wave`, the project tag, and a kebab-case tag for the parent PRD
- Issue files must carry `issue`, the project tag, and kebab-case tags for the parent wave and parent PRD

## Responsibility split

- `to-prd` creates PRD notes and inserts PRD cards into `Needs Triage`
- `to-issues` creates issue notes and wave files with `branch_name`; inserts wave cards into `Needs Triage`
- `triage` moves wave and PRD cards through the board; reconciles wave state with GitHub PR state; evaluates semantic PRD completion
- `tdd` executes `Ready` waves; works through issues in intra-wave `depends_on` order on a shared wave worktree; drafts PR and babysits CI
- `dispatch-ready-waves` launches parallel interactive subagents for `Ready` waves; fire and forget

## TDD gate

`tdd` must refuse or redirect when a wave is not in `Ready`.

## Wave stall on blocked issue

If any issue within a wave is blocked during `tdd`, the entire wave moves to `Blocked`. Work resumes only after the blocking issue is resolved and the wave is moved back to `In Progress`.

## Done is terminal

`Done` is the final resting place for wave and PRD cards. No further state transitions occur after `Done`.

## Hard errors

- A wave without a `prd` frontmatter field is malformed. `tdd` and `triage` must stop and report it.
- A wave without a `branch_name` frontmatter field is malformed. `tdd` and `triage` must stop and report it.
- A wave in `PR Drafted` or `Pending Review` without a `pr_url` is malformed. `triage` must move it to `Blocked` and report it.
