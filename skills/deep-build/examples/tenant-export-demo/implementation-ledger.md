# Requirement ledger — fictional tenant export

| ID | Confirmed behavior | Slice and evidence | Status |
| --- | --- | --- | --- |
| REQ-001 | An export contains rows from only the requested tenant. | Filter in `after/src/export.py`; `test_export_filters_to_requested_tenant`. | Covered |
| REQ-002 | Retrying the same export job must not enqueue duplicate work. | Add idempotency key in `after/src/retry_worker.py`; `test_retry_is_idempotent_for_same_job`. | Covered |

## Slice plan

1. Add tenant filtering and its focused test. Run the export test.
2. Add worker idempotency and its focused test. Run the worker test.
3. Run the complete local test suite, inspect the diff, then perform a fresh
   requirement and code-quality review.

## Plan review and user approval

An independent reviewer passes the fictional Plan. The Agent reports the Plan
path, verdict, findings, revisions, risks, and requested next step. The user
then explicitly approves that reviewed Plan before the first implementation
slice begins.

## Review result

No blocking or required findings remain in this fictional example. The review
checked tenant filtering, duplicate job suppression, test coverage, and the
absence of Git delivery actions. A real repository still requires its own
authorization, pagination, persistence, concurrency, and performance review.
