---
name: api-design-review
description: Reviews REST API design by inventorying routes, finding overlapping functionality, comparing payloads and pagination, and checking resource naming, URL structure, identifiers, errors, idempotency, and timestamps. Use when asked to review API routes, compare endpoints, find redundant or superseding operations, assess contract consistency, or run a REST API design review.
---

# API Design Review

Review the implemented API contract, not route names alone.

## Workflow

1. Establish the target version or revision and review boundary: named endpoints, one resource family, or the whole API. If the working copy and default branch differ, state which one is reviewed.
2. Discover endpoints from route registrations and the generated API specification. Confirm behavior in handlers, request/response models, and tests where needed.
3. Build an endpoint inventory with:
   - method and normalized path
   - active or deprecated status
   - resource and operation
   - functional scope dimensions such as tenant, agent, target organisation, or cross-tenant
   - filters and sorting
   - authorization requirements when they differ between compared endpoints
   - success response type and pagination contract
4. Ignore an endpoint only when code, specification, or migration documentation explicitly marks it deprecated. Do not infer deprecation from words such as `legacy`, an older payload shape, or the presence of a newer endpoint.
5. Compare active endpoints pairwise for scope overlap:
   - **duplicate**: same resource, scope, and capability
   - **superset**: one endpoint can perform every material query of another
   - **partial**: scopes or capabilities intersect but each retains distinct behavior
   - **none**: shared resource names without intersecting use cases
6. Compare success payloads among endpoints returning the same resource or serving overlapping use cases. Check:
   - top-level array versus object
   - collection field names
   - pagination metadata, token names, and token location
   - `hasMore` or link semantics
   - field naming and nullability when response models differ
7. Evaluate every item in the REST design rubric below against the inventoried review boundary. Mark non-applicable rules rather than silently skipping them.
8. Verify each finding against implementation evidence. Do not report a difference as an inconsistency when it follows from a materially different operation and does not burden the same consumers.

## REST Design Rubric

| Rule | Check |
|---|---|
| 0. Be pragmatic | Judge client usefulness and consistency, not semantic arguments about whether an API is strictly RESTful. |
| 1. Plural collections | Use plural nouns for collection resources. |
| 2. Minimal paths | Remove path segments that do not identify or scope the resource. Keep parent segments for genuine compound keys or containment. |
| 3. No representation extensions | Do not put `.json` or other representation formats in resource URLs; use HTTP content negotiation. |
| 4. Object top level | Return a top-level object, not an array, so metadata and pagination can be added compatibly. |
| 5. Arrays, not object maps | Represent collections as arrays of objects rather than maps keyed by dynamic identifiers. Allow simple string key/value metadata maps. |
| 6. String identifiers | Serialize identifiers as strings even when storage uses numeric IDs. |
| 7. Prefixed identifiers | Use stable, visually distinct type prefixes where clients handle multiple identifier types. Mark `N/A` when the API has only one unambiguous identifier type or an established incompatible convention. |
| 8. Distinguishable not-found | Flag entity-absence responses that clients cannot distinguish from routing or infrastructure failures. The source recommends avoiding `404` and suggests `410`; record contrary project or HTTP conventions rather than presenting this opinionated rule as universal. |
| 9. Consistent models | Keep names, types, nullability, envelopes, and semantics consistent for fields and objects with the same meaning. |
| 10. Structured errors | Use one machine-readable error format across endpoints; preserve nested causes or stable error types when clients need them. |
| 11. Idempotent mutations | Give retried non-idempotent operations an idempotency key, client-selected ID, or equivalent mechanism. Verify conflict or replay behavior. Mark read-only operations and naturally idempotent mutations `N/A`. |
| 12. ISO 8601 time values | Encode timestamps and other date/time values as ISO 8601 strings; timestamps use UTC with `Z`. Verify serialization rather than trusting platform defaults. |

## Review Rules

- Treat functional scope as the result-set boundary and capabilities across tenancy, ownership, target, filters, and sorting—not just the URL hierarchy.
- Do not include authentication or authorization in functional scope or use an authorization difference to dismiss functional overlap. Compare authorization separately when it differs.
- Distinguish overlap from redundancy. Overlap is a finding; removal requires evidence that one endpoint is a safe replacement.
- Call out silent limits on unpaged collections because they affect whether a paged endpoint is truly equivalent.
- Prefer one pagination contract for overlapping collection endpoints unless compatibility requirements justify otherwise.
- Inspect supporting code outside the review boundary for evidence, but do not add unrelated endpoints or findings. For an endpoint subset with no mutations, mark idempotency `N/A`; for a full-API review, inspect all applicable mutations.
- Separate compatibility findings from style guidance. Label a change as breaking when existing clients must change.
- Recommend the smallest compatible correction; do not implement or redesign the API unless asked.
- If evidence is missing, label the conclusion `unverified` rather than guessing.

## Output

### Endpoint inventory

| Endpoint | Functional scope | Capabilities | Success payload | Status |
|---|---|---|---|---|

Append an `Auth` column only when authentication or authorization differs across inventoried endpoints.

### Overlap comparison

For every duplicate, superset, or partial-overlap group, show how the endpoints differ before the detailed finding:

| Endpoint | Functional scope | Filters and sorting | Pagination |
|---|---|---|---|

If authentication or authorization differs within the overlap group, append an `Auth` column. Omit it when requirements are the same or auth evidence is unavailable.

Use exact methods and paths. Describe parameter location, page limit, and response envelope in the pagination column. Keep auth details out of `Functional scope`. Include only endpoints in that overlap group; reuse one table when a group supports multiple findings.

### REST rule check

Report every rubric item, including passes and non-applicable rules:

| Rule | Status | Evidence |
|---|---|---|

Use only `Pass`, `Issue`, `N/A`, or `Unverified` as status values. A rule may produce more than one detailed finding.

### Findings

Order findings by consumer impact. For each finding provide:

1. **Issue** — violated rule, overlap classification, or payload inconsistency.
2. **Endpoints** — exact methods and paths.
3. **Evidence** — implementation or specification locations and relevant behavior.
4. **Impact** — concrete client or maintenance cost.
5. **Recommendation** — smallest compatible change; preserve an existing endpoint when removal would be breaking.

If no issue survives verification, say so. End with a short list of deprecated endpoints excluded from the comparison, or `None`.
