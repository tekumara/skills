# API Design Review Specification

## Intent

Review active REST API contracts for overlapping functionality, inconsistent payloads, and pragmatic design problems across resource naming, paths, identifiers, errors, idempotency, and time values. Give API owners evidence sufficient to choose compatible corrections.

## Scope

In scope:
- endpoint discovery and inventory
- duplicate, superset, and partial functional-scope overlap
- authorization comparison when requirements differ across overlapping endpoints
- collection and pagination success-response consistency
- plural resources and minimal URL paths
- representation extensions, top-level arrays, and map-shaped collections
- identifier representation and prefixes
- distinguishable not-found behavior and structured errors
- idempotency mechanisms for retryable mutations
- ISO 8601 date and time values
- explicit deprecation evidence

Out of scope:
- performance and implementation quality unrelated to the API contract
- automatic endpoint removal or compatibility migration

## Users And Trigger Context

- Primary users: API designers, maintainers, and reviewers
- Common requests: review routes, compare endpoints, find overlap, review response or pagination consistency, or run a REST API design review
- Should not trigger for: implementing one endpoint, debugging a handler, or reviewing unrelated code quality

## Runtime Contract

- Required first actions: select a revision and review boundary, discover routes within it, and verify contracts in implementation or generated specifications
- Required outputs: endpoint inventory, a difference table for each overlapping endpoint group, an optional auth column when auth differs, a status row for every REST rubric rule, evidence-backed findings, minimal compatible recommendations, and excluded deprecated routes
- Non-negotiable constraints: findings stay within the declared review boundary; supporting evidence may come from outside it; functional scope excludes auth; compare differing auth separately; do not infer deprecation; distinguish overlap from redundancy; distinguish compatibility issues from style guidance; label missing evidence
- Expected bundled files loaded at runtime: `SKILL.md` only

## Source And Evidence Model

Authoritative sources:
- route registrations and handlers
- generated OpenAPI or equivalent API specifications
- request and response models
- endpoint tests and migration documentation
- the adapted REST design rubric recorded in `SOURCES.md`

Useful improvement sources:
- positive and negative review examples
- consumer migration incidents
- issue and PR feedback
- validation results from representative APIs

Data that must not be stored:
- credentials or tokens
- customer payloads
- private identifiers unnecessary for reproduction

## Reference Architecture

- `SKILL.md` contains the complete runtime workflow and output contract
- `references/`, `scripts/`, and `assets/` are intentionally absent until a repeated lookup or deterministic extraction need appears

## Validation

- Lightweight validation: Agent Skill structural validator
- Deeper validation: run in an isolated subagent against an API with known overlap and payload inconsistencies
- Acceptance gates: identifies verified overlap, distinguishes overlap classes, compares each overlapping group by functional scope, filters/sorting, and pagination, adds auth only when it differs, evaluates every REST rubric rule as Pass/Issue/N/A/Unverified, detects incompatible pagination envelopes, and does not exclude unmarked routes as deprecated

## Known Limitations

- Route discovery depends on repository conventions and available specifications.
- Semantic replacement safety may remain unverified without consumer evidence.
- Rule 8's recommendation to avoid `404` for entity absence is opinionated and may conflict with established HTTP or project conventions; reviews must state that context.

## Maintenance Notes

- Update `SKILL.md` when review dimensions or output requirements change.
- Update `SOURCES.md` when evidence, decisions, or validation outcomes change.
