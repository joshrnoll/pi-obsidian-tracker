---
type: prd
project: {{project-name}}
title: {{title}}
status: draft
created: {{created}}
tags:
  - prd
  - {{project-name}}
---

# PRD: {{title}}

## Problem Statement

Describe the problem from the user's perspective.

## Solution

Describe the proposed solution from the user's perspective.

## User Stories

Provide a long, numbered list of user stories in this format:

1. As an <actor>, I want a <feature>, so that <benefit>

Include primary flows, edge cases, operational concerns, and any meaningful user or operator interactions.

## Implementation Decisions

List the implementation decisions already made.

Include things like:
- modules or subsystems that will be built or modified
- interface boundaries that matter
- architectural decisions
- schema or data model changes
- API contracts
- technical clarifications
- interaction details

Do not include file paths or code snippets.

## Testing Decisions

Describe the testing strategy.

Include:
- what makes a good test for this work
- which modules or behaviors should be tested
- any relevant prior art or existing testing patterns in the codebase

## Out of Scope

List the things intentionally excluded from this PRD.

## Further Notes

Add any additional notes, risks, follow-up ideas, or unresolved observations.
