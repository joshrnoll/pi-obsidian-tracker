---
type: wave
project: { { project-name } }
title: { { title } }
status: { { status } }
prd: "[[prds/{{prd-file}}]]"
board: "[[board]]"
branch_name: { { branch-name } }
pr_url:
depends_on:
  - "[[waves/{{prerequisite-wave}}]]"
created: { { created } }
tags:
  - wave
  - {{project-tag}}
  - {{prd-tag}}
---

# {{title}}

## Issues

- [[issues/{{issue-file}}]]
