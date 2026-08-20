# Fictional example

Everything below is invented.

## Input

```text
Review GitHub PR #42 in acme-example/parcel-api. Issue ACME-81 requires tenant-scoped CSV exports and a 10,000-row limit.
```

## Illustrative output

```markdown
# Change Review: GitHub PR #42 — Add shipment export

## Verdict
Changes required: the export query is not tenant-scoped.

## Findings
### P1 — Export can include another tenant's records
- Location: `src/exports.py:48`
- Evidence: the query filters by status but never by the authenticated tenant ID.
- Impact: one customer can receive another customer's shipment data.
- Recommendation: require tenant ID in the query and add a cross-tenant regression test.

## Acceptance Criteria Coverage
| ID | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| AC-001 | Export contains only the active tenant's data | Not covered | Tenant predicate is absent. |
| AC-002 | Export stops at 10,000 rows | Covered | Limit and boundary test are present. |
```
