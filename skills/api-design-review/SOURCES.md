# Sources And Decisions

## Source inventory

| Source | Trust | Contribution | Constraints |
|---|---|---|---|
| User request in this session | Primary | Required checks: endpoint scope overlap, response payload consistency, deprecated-route exclusion | Private session; store only generalized requirements |
| Agent Skills format and local `skill-writer` guidance | Primary | Skill structure, trigger description, inline shape, specification, validation | None |

## Decisions

- **Adopted:** `workflow-process` class because the skill runs a fixed evidence-gathering and comparison review.
- **Adopted:** `inline-guidance` execution shape because one checklist and output contract handle the task.
- **Rejected:** scripts; route frameworks vary and deterministic extraction is not yet justified.
- **Rejected:** references; every runtime rule is short and universal.
- **Adopted:** explicit overlap classifications to prevent treating every intersection as redundancy.
- **Adopted:** explicit deprecation evidence; age and newer alternatives are insufficient.
- **Adopted:** every overlap group gets a compact difference table covering endpoint, functional scope, filters/sorting, and pagination.
- **Adopted:** auth is not part of functional scope; add an optional auth column only when requirements differ within the group.
- **Deferred:** review of errors, naming, authentication, and performance until requested.

## Coverage

| Dimension | Status |
|---|---|
| Preconditions and revision selection | Covered |
| Endpoint discovery | Covered |
| Scope overlap | Covered |
| Success payload consistency | Covered |
| Deprecation handling | Covered |
| Missing-evidence behavior | Covered |
| Output contract | Covered |
| Provider portability | Covered; no provider-specific mechanics |

## Retrieval stopping rationale

The user supplied narrow review dimensions, the target repository provides a representative test case, and the portable Agent Skills requirements are known. Further API-design research would broaden the skill beyond the requested checks.

## Iteration evidence

- Human-verified fix: when functionality overlaps, compare the affected endpoints in a table rather than describing differences only in prose.
- Human-verified correction: `Scope` means functional scope, not authentication or authorization scope.
- Skill delta: require `Endpoint`, `Functional scope`, `Filters and sorting`, and `Pagination`; append `Auth` only when auth differs.

## Validation history

- Structural validation after this iteration: passed with no warnings.
- Subagent replay against the five execution collection endpoints: passed; every overlap group was compared using the required four columns, including pagination parameter location, limits, and response envelope.
- Functional-scope replay: passed; auth was excluded from functional scope and the optional `Auth` column was correctly omitted because all compared routes used the same policy.

## Gaps

- No cross-framework route extractor; add one only after repeated discovery failures justify a script.
- No persistent holdout suite; add examples after real false-positive or false-negative feedback.
