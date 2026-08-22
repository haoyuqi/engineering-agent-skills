---
name: deep-build
description: Use when the user wants an approved substantial software change implemented across multiple files, layers, or components, with a written plan, review gates, and evidence-based delivery. Do not use for trivial edits, unresolved requirements, Git delivery, or remote PR/MR review.
license: Apache-2.0
compatibility: Requires a writable software repository, project verification tools, and either an independent plan reviewer or a human/external reviewer.
---

# Deep Build

Deliver a substantial local change through a written plan and two PASS gates. Use [config.example.yaml](config.example.yaml), [external-dependencies.json](external-dependencies.json), and [references/review-criteria.md](references/review-criteria.md).

## Boundaries

Implementation authorizes scoped local edits and a new Plan. Do not overwrite Plans, commit, push, open a PR/MR, deploy, update issues, or mutate services. Preserve unrelated changes. Show and confirm destructive migrations, rewrites, dependency installs, or permission changes first.

## Required workflow

1. **Recover and map.** Reuse requirements and stable IDs. Inspect instructions, callers, persistence, authorization, failures, tests, and worktree. Record assumptions and open decisions.
2. **Write the Plan.** Create `<plan_directory>/<slug>.md` with the ledger, evidence, scope/non-goals, slices, files/changes, dependencies, checks, risks/rollback, destructive actions, and review criteria. Do not implement first.
3. **Plan Review and user-approval gate.** Use independent review; prefer a different model or agent context, though human or external review is valid. Record reviewer, verdict, findings, and revisions. Self-review cannot satisfy this gate. Immediately report each result: Plan path, reviewer context, verdict, blocking findings, revisions, risks, and next decision. On FAIL, stop at `pending user plan decision`; revise only after user direction, then re-review. On PASS, stop at `pending user plan approval`. Implement only after recorded explicit user approval.
4. **Implement slices.** Execute the user-approved Plan by vertical slice. Establish an observable signal where practical, make the smallest coherent change, run targeted checks, inspect the diff, and update the ledger. A new interface, migration, dependency, permission change, or out-of-scope caller returns to the Plan gate.
5. **Code Review gate.** Select actual-diff principles using [references/review-criteria.md](references/review-criteria.md). Record criteria, reviewer context, findings, and PASS/FAIL in the Plan. Fix Critical and Required findings and re-review. Without PASS, do not hand off as complete.
6. **Hand off.** After both gates pass, fill [assets/build-handoff-template.md](assets/build-handoff-template.md) with observed evidence and ask for user acceptance. Git delivery is separate.

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
## User Plan Decision — Round N
Plan path: <path>; Decision: APPROVED / CHANGES_REQUESTED
Decision evidence: <the user's explicit response>
## Code Review — Round N
Actual-diff criteria: <list>; Verdict: PASS / FAIL
Critical/Required findings, resolution, and checks: <evidence>
```

## Failure behavior

Keep successful evidence if a tool fails; report the unverified slice and recovery command. If state is stale, the worktree wins. Return failed acceptance to its ledger item.
