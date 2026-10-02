# Review checklist

Load after pinning the target, before exploring surrounding code. Apply only relevant categories; findings require concrete evidence and user impact.

## Revision-matched evidence

- For remote reviews, read finding-critical files from the pinned Git objects
  (for example, `git show <head-sha>:<path>`) or a provider response addressed by
  that commit. Verify base-side evidence at the pinned base/diff range too.
- Matching local `HEAD` is insufficient if the working tree is dirty. A stale
  or dirty checkout may suggest callers or design context, but neither a defect
  nor a dismissal of a defect may rely on it without revision verification.
- If the required revision or surrounding file is unavailable, name the missing
  evidence and its consequence. Do not invent it, automatically fetch, switch
  branches, or treat an old implementation as current.

## Snapshot and freshness

- For local worktree reviews, record selected paths, change layers (index,
  worktree, untracked), exclusions, `HEAD`, and a reproducible fingerprint of
  contents, statuses, and relevant modes. Status or filenames alone cannot
  detect same-path edits. Include finding-critical local context in the snapshot.
  Do not read ignored/private files or follow links outside the selected scope.
- For base-ref comparisons, resolve both commits and record the actual diff
  range/semantics. Dirty worktree changes are excluded unless separately selected.
- Use the same scope and fingerprint method at the end; detect additions,
  removals, same-path edits, and index changes. If evidence changed during
  collection and no coherent snapshot is available, report cannot complete.
- For remote targets, re-read head/base and the provider diff identity (including
  merge-base/start revision where applicable). Head equality alone is insufficient
  when the base moved. Record retrieval/check timestamps and check commit SHAs.
- On target drift, preserve findings tied to the original snapshot and identify
  the newer target as unreviewed. Offer a new review; do not restart indefinitely.
  If rechecking fails, report freshness unknown. A finding must still be supported
  by retained original evidence; otherwise downgrade it to a verification gap.

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
