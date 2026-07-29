# Sources And Decisions

## Source inventory

| Source | Trust | Contribution | Constraints |
|---|---|---|---|
| User requests in this session | Primary | Required checks: endpoint overlap, response consistency, deprecated-route exclusion, difference tables, functional scope, full REST rubric evaluation, exact rule names in references, and no final coverage table | Private session; store only generalized requirements |
| [How to (and how not to) design REST APIs](https://github.com/stickfigure/blog/wiki/How-to-%28and-how-not-to%29-design-REST-APIs) | Secondary, opinionated | Rules 0–12 covering pragmatism, resources, URLs, payloads, IDs, not-found behavior, consistency, errors, idempotency, and timestamps | Adapted into a compact rubric; fetched 2026-07-28; retain attribution and flag 8. Distinguishable not-found as non-universal |
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
- **Adopted:** all upstream Rules 0–12 as an every-run internal review rubric, transformed from narrative into checks.
- **Adopted:** findings cite every applicable rule by number and exact rubric name; the final output omits a separate rule coverage table.
- **Adapted:** 8. Distinguishable not-found retains the warning about ambiguous `404` responses but must be presented as opinionated when established HTTP or project conventions differ.
- **Deferred:** performance and implementation-quality review unrelated to the API contract.

## Source adaptation

- **Source intent:** promote pragmatic, evolvable REST APIs that are predictable for clients.
- **Local target:** turn every numbered rule into an evidence-backed review check without replacing the existing overlap analysis.
- **Fidelity boundary:** preserve Rules 0–12 and their important exceptions, especially simple metadata maps, compound paths, mutation applicability, and UTC timestamps.
- **Local replacements:** narrative examples became concise internal checks and rule references attached directly to findings.
- **Omitted material:** anecdotes, vendor criticism, and extended distributed-systems explanation do not change review decisions.
- **Rights and attribution:** no license was identified on the fetched wiki page; retain the source link and paraphrase rather than reproducing substantial prose.

## Coverage

| Dimension | Status |
|---|---|
| Preconditions and revision selection | Covered |
| Endpoint discovery | Covered |
| Scope overlap | Covered |
| Success payload consistency | Covered |
| Deprecation handling | Covered |
| Missing-evidence behavior | Covered |
| REST rules 0–12 | Covered |
| Applicability and opinionated-rule handling | Covered |
| Output contract | Covered |
| Provider portability | Covered; no provider-specific mechanics |

## Retrieval stopping rationale

The requested upstream article was fetched in full and every numbered rule was mapped into the runtime rubric. Additional REST guidance would introduce criteria outside the requested source rather than improve source coverage.

## Iteration evidence

- Human-verified fix: when functionality overlaps, compare the affected endpoints in a table rather than describing differences only in prose.
- Human-verified correction: `Scope` means functional scope, not authentication or authorization scope.
- Skill delta: require `Endpoint`, `Functional scope`, `Filters and sorting`, and `Pagination`; append `Auth` only when auth differs.
- Human-verified expansion: add all rules from the fetched REST design article.
- Skill delta: broadened the internal review to evaluate Rules 0–12.
- Subagent weakness found: mutation findings could escape a user-specified read-endpoint review boundary.
- Skill delta: require an explicit boundary; supporting code may provide evidence but cannot expand the endpoints under review.
- Human-verified positive example: a single priority-ordered finding list was clearer than separate REST issue and detailed finding sections.
- Skill delta: consolidate rubric and non-rubric issues by root cause and include applicable REST rule numbers and exact names on each finding.
- Human-verified correction: omit the final REST rule coverage table; keep full rubric evaluation as working evidence only.

## Validation history

- Structural validation after this iteration: passed with no warnings.
- Subagent replay against the five execution collection endpoints: passed; every overlap group was compared using the required four columns, including pagination parameter location, limits, and response envelope.
- Functional-scope replay: passed; auth was excluded from functional scope and the optional `Auth` column was correctly omitted because all compared routes used the same policy.
- Consolidated-output replay: passed against three overlapping execution-query endpoints; every issue appeared once in a priority-tagged list and applicable REST rules were attached to findings.

## Gaps

- No cross-framework route extractor; add one only after repeated discovery failures justify a script.
- No persistent holdout suite; add examples after real false-positive or false-negative feedback.
