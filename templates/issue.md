---
type: issue
project: { { project-name } }
title: { { title } }
status: { { status } }
prd: "[[prds/{{prd-file}}]]"
wave: "[[waves/{{wave-file}}]]"
board: "[[board]]"
created: { { created } }
depends_on: []
tags:
  - issue
  - {{project-tag}}
  - {{wave-tag}}
  - {{prd-tag}}
---

# {{title}}

## Summary

{{summary}}

## Why

{{why}}

## Scope

-

## Out of scope

-

## Acceptance criteria

-

## Notes

> `depends_on`: intra-wave only — links to other issues within the same wave that must be `Done` before this issue starts. Cross-wave dependencies are expressed at the wave level.
>
> `tags`: always use kebab-case tags. Include `issue`, the project tag, the parent wave tag, and the parent PRD tag.
