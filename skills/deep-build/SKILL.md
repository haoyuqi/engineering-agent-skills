---
name: deep-build
description: Use when implementing an approved substantial change across files or components with written planning and review gates. Excludes trivial edits, unresolved requirements, Git delivery, and remote PR/MR review.
license: Apache-2.0
compatibility: Requires a writable repository, verification tools, and independent Plan and Code reviewers (agent, external session, or human).
---

# Deep Build

Require a Plan and two independent PASS gates. Use [config.example.yaml](config.example.yaml) and optional [external-dependencies.json](external-dependencies.json).

## Boundaries

Implementation authorizes scoped local edits and a new Plan. Do not overwrite Plans, commit, push, open a PR/MR, deploy, update issues, or mutate services. Preserve unrelated changes. Show and confirm destructive migrations, rewrites, dependency installs, or permission changes first.

## Workflow

1. **Recover and map.** Reuse requirements/IDs. Inspect instructions, callers, persistence, authorization, failures, tests, and worktree. Record assumptions and decisions.
2. **Write the Plan.** Create `<plan_directory>/<slug>.md` with the ledger, evidence, scope/non-goals, slices, files/changes, dependencies, checks, risks/rollback, destructive actions, and review criteria. Do not implement first.
3. **Plan Review and user-approval gate.** Read [references/review-criteria.md](references/review-criteria.md) for independence and model selection. Self-review cannot satisfy either gate. Immediately report each result: Plan path, reviewer context, verdict, blocking findings, revisions, risks, and next decision. On FAIL, stop at `pending user plan decision`; revise only after user direction, then re-review. On PASS, stop at `pending user plan approval`. Implement only after recorded explicit user approval.
4. **Implement slices.** Follow the approved Plan. Establish observable signals, make small coherent changes, run checks, inspect diffs, and update the ledger. A new interface, migration, dependency, permission change, or out-of-scope caller returns to the Plan gate.
5. **Code Review gate.** Obtain independent review of the actual diff, surrounding code, and tests using [references/review-criteria.md](references/review-criteria.md). Record criteria, reviewer/model selection, findings, and PASS/FAIL in the Plan; report the result to the user. The implementer fixes Critical/Required findings, then requests independent re-review. Without PASS, do not hand off as complete.
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
Reviewer/context: <agent | human | external>; Model/effort: <known value | unknown | N/A>
Selection rationale and reviewed version: <evidence>; Verdict: PASS / FAIL
Findings and revisions: <evidence>
## User Plan Decision — Round N
Plan path: <path>; Decision: APPROVED / CHANGES_REQUESTED
Decision evidence: <the user's explicit response>
## Code Review — Round N
Reviewer/context, model/effort, selection rationale, reviewed version: <evidence>
Actual-diff criteria: <list>; Verdict: PASS / FAIL
Critical/Required findings, resolution, and checks: <evidence>
```

## Failure behavior

Without an independent reviewer, report `pending external review`; neither implementation nor final completion may bypass its gate. Preserve evidence on tool failure; report unverified work and recovery. If state is stale, the worktree wins. Return failed acceptance to its ledger item.
