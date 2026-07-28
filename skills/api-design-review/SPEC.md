# API Design Review Specification

## Intent

Identify active API routes whose scopes overlap and success responses whose shapes are inconsistent, with evidence sufficient for an API owner to choose a compatible simplification.

## Scope

In scope:
- endpoint discovery and inventory
- duplicate, superset, and partial functional-scope overlap
- authorization comparison when requirements differ across overlapping endpoints
- collection and pagination success-response consistency
- explicit deprecation evidence

Out of scope:
- general REST style, naming, authentication, error design, or performance unless requested
- automatic endpoint removal or compatibility migration

## Users And Trigger Context

- Primary users: API designers, maintainers, and reviewers
- Common requests: review routes, compare endpoints, find overlap, review response or pagination consistency
- Should not trigger for: implementing one endpoint, debugging a handler, or reviewing unrelated code quality

## Runtime Contract

- Required first actions: select a revision, discover routes, and verify contracts in implementation or generated specifications
- Required outputs: endpoint inventory, a difference table for each overlapping endpoint group, an optional auth column when auth differs, evidence-backed findings, minimal compatible recommendations, and excluded deprecated routes
- Non-negotiable constraints: functional scope excludes auth; compare differing auth separately; do not infer deprecation; distinguish overlap from redundancy; label missing evidence
- Expected bundled files loaded at runtime: `SKILL.md` only

## Source And Evidence Model

Authoritative sources:
- route registrations and handlers
- generated OpenAPI or equivalent API specifications
- request and response models
- endpoint tests and migration documentation

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
- Acceptance gates: identifies verified overlap, distinguishes overlap classes, compares each overlapping group by functional scope, filters/sorting, and pagination, adds auth only when it differs, detects incompatible pagination envelopes, and does not exclude unmarked routes as deprecated

## Known Limitations

- Route discovery depends on repository conventions and available specifications.
- Semantic replacement safety may remain unverified without consumer evidence.

## Maintenance Notes

- Update `SKILL.md` when review dimensions or output requirements change.
- Update `SOURCES.md` when evidence, decisions, or validation outcomes change.
