# Fictional example

Everything below is invented.

## Input

```text
Review GitHub PR #42 in acme-example/parcel-api. Issue ACME-81 requires tenant-scoped CSV exports and a 10,000-row limit.
```

## Illustrative output

```markdown
# Change Review: GitHub PR #42 — Add shipment export

## Review target
Remote: acme-example/parcel-api PR #42; base `base-A`, head `head-A`, diff `base-A..head-A`.
Local context: parcel-api/ at `older-L`; used for orientation only.
Finding-critical export query and caller were read from pinned `head-A`.

## Target freshness
Initial: base-A/head-A. Final read: base-A/head-A, unchanged at 10:05 UTC.
Conclusion covers this snapshot only. Checks were not run.

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

Revision labels above are fictional placeholders, not actual commit SHAs.
If the final observation is head-B instead, the report retains the head-A
finding but marks head-B unreviewed. If the final read fails, it reports
freshness unknown. A stale local query alone cannot support the finding.

## Local target variation

For a directory-only request, use local metadata instead of fabricated PR fields:

```text
Directory: example-service/; HEAD: local-A; mode: worktree snapshot.
Selected: staged src/a.py; unstaged src/b.py; untracked tests/new_case.py.
Excluded: ignored/private files.
Fingerprint: content-C, digest of selected paths/status/modes/contents across
index, worktree, untracked files, and inspected context.
Captured at 10:00 UTC; rechecked at 10:05 UTC: content-D (changed).
Applicability: original content-C only; current content-D is unreviewed.
Checks: not run.
```

Fingerprint labels are fictional. Identical path/status listings do not make
content-C and content-D the same snapshot; do not claim the current worktree passed.
