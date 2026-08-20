---
name: deep-build
description: Use when the user wants an approved substantial software change implemented across multiple files, layers, or components, with a written plan, review gates, and evidence-based delivery. Do not use for trivial edits, unresolved requirements, Git delivery, or remote PR/MR review.
license: Apache-2.0
compatibility: Requires a writable software repository, project verification tools, and either an independent plan reviewer or a human/external reviewer.
---

# Deep Build

Deliver a substantial local change through a written plan and two PASS gates. Use [config.example.yaml](config.example.yaml), [external-dependencies.json](external-dependencies.json), and [references/review-criteria.md](references/review-criteria.md).

## Boundaries

Implementation authorizes scoped local edits and a new Plan in the configured directory. Do not overwrite Plans, commit, push, open a PR/MR, deploy, update issues, or mutate services. Preserve unrelated changes. Show and confirm destructive migrations, data rewrites, dependency installation, or permission changes first.

## Required workflow

1. **Recover and map.** Reuse requirements; assign stable IDs; inspect instructions, callers, persistence, authorization, failures, tests, and worktree. Record assumptions and open decisions separately.
2. **Write the Plan.** Create `<plan_directory>/<slug>.md` with the ledger, evidence, scope/non-goals, vertical slices, files/changes, dependencies, checks, risks/rollback, destructive actions, and predicted review criteria. No implementation before it exists.
3. **Plan Review gate.** Have an independent reviewer examine the Plan. Prefer a different model or independent agent context; human or external review is valid. Record reviewer type, verdict, findings, and revisions. A same-context self-review can improve the Plan but cannot satisfy this gate. On FAIL, revise and re-review. Without recorded PASS, stop at `pending external review`.
4. **Implement slices.** Execute the approved Plan one vertical slice at a time. Establish an observable signal where practical, make the smallest coherent change, run targeted checks, inspect the diff, and update the ledger. A new interface, migration, dependency, permission change, or out-of-scope caller returns to the Plan gate.
5. **Code Review gate.** Select principles from the actual diff using [references/review-criteria.md](references/review-criteria.md). Record principles, reviewer context, findings, and PASS/FAIL in the Plan. Fix Critical and Required findings and re-review. Without recorded PASS, do not hand off as complete.
6. **Hand off.** Only after both gates pass, fill [assets/build-handoff-template.md](assets/build-handoff-template.md) with observed evidence and ask for user acceptance. Git delivery remains a separate workflow.

## Plan record format

```markdown
# Build Plan: <change>
## Requirement ledger
| ID | Requirement | Acceptance evidence | Status |
## Codebase evidence and scope
## Slices and verification
| Slice | Requirement IDs | Files/change | Checks | Risk/rollback |
## Predicted review criteria
## Plan Review — Round N
Reviewer: <independent agent/model | human | external>; Verdict: PASS / FAIL
Findings and revisions: <evidence>
## Code Review — Round N
Actual-diff criteria: <list>; Verdict: PASS / FAIL
Critical/Required findings, resolution, and checks: <evidence>
```

## Failure behavior

Keep successful evidence if a tool fails; report the unverified slice and recovery command. If state is stale, the worktree wins. If acceptance fails, return to the ledger item.
