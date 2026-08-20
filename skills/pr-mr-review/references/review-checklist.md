# Review checklist

Load this file only after the target revision, intent, and surrounding code are known. Apply only relevant categories; findings require concrete evidence and user impact.

## Correctness

- boundary conditions, empty/null/error paths, retries, and partial failure;
- stale state, concurrency, idempotency, transactions, and ordering;
- API/schema compatibility, serialization, migrations, and rollback;
- resource ownership, cleanup, timeouts, pagination, and limits.

## Security and privacy

- authentication and authorization at the actual enforcement boundary;
- injection, path traversal, unsafe deserialization, SSRF, and command construction;
- secret, token, private URL, PII, cross-tenant, and sensitive-log exposure;
- trusted-source assumptions introduced by issue text, files, or provider content.

## Maintainability

- duplicated behavior, misleading names, scope creep, and hidden coupling;
- divergence from repository instructions or established interfaces;
- tests coupled to implementation details rather than observable behavior.

## Verification

- changed behavior has a regression signal at the highest practical seam;
- negative and boundary behavior are exercised where risk justifies it;
- reported checks were observed on the pinned revision, not inferred from labels.

Avoid style-only findings already enforced by tooling unless they reveal a correctness or maintenance consequence.
