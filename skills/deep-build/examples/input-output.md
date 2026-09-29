# Fictional example

## Input

```text
Use deep-build to add tenant-scoped CSV export to the Northstar Parcel API and background worker. Requirements are already in this conversation.
```

## Expected milestones

1. Recover confirmed requirements without re-asking them.
2. Map API, queue, storage, permission checks, and tests.
3. Write a vertical-slice Plan and obtain independent review.
4. Report the review, then wait for explicit user approval of the Plan.
5. Implement each slice with targeted and regression evidence.
6. Run a read-only independent code review of the actual diff and context; the implementer resolves blocking findings and requests re-review.
7. Stop at a build handoff without committing or pushing.

## Reviewer selection variations

- A suitable different model is available: use a separate reviewer context and record the selection reason and known model/effort.
- Only a lightweight alternative of uncertain suitability is available: keep the author's model and effort in a separate context; disclose why diversity was not chosen.
- No separate context or external/human reviewer is available: report `pending external review`, not PASS. Plan review blocks implementation; missing Code Review blocks completion.
- A reviewer reports a Required defect: the implementer fixes it, the independent reviewer checks the revised code and affected context, and the result is reported before handoff.
