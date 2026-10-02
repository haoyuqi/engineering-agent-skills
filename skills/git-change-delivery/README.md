# Git Change Delivery

An explicit, provider-neutral workflow for staging, committing, pushing, and opening a GitHub PR or GitLab MR. Authorization covers the requested sequence, not an automatic question before every command.

## Quick start

```text
Use git-change-delivery to commit the export fix, push the current branch, and open a draft PR. Exclude notes.txt.
```

The Skill auto-detects GitHub or GitLab from the remote. Use [config.example.yaml](config.example.yaml) for project conventions, never for credentials.

## Safety

No mutation is implied by inspection or configuration. Show the resolved files, message, push target, and PR/MR proposal before executing the authorized operations; this disclosure does not require another yes when the user already authorized that bounded sequence.

- Commit + push + open PR/MR: carry out all three, including scoped staging, without repetitive questions.
- Commit only: commit and stop. Stage only: stage and stop.
- Prepare a PR proposal: draft it in conversation without publishing. PR-only on an already published branch: create the request without new commits.
- If the user's intent or target is unclear, ask only the missing question. Honor explicit step-by-step approval requests.
- If unrelated or uncertain content is already staged, stop before commit; do not include it or silently unstage it.
- New scope, changed target, force push, hook bypass, and history rewrites need specific risk-aware authorization. A failed hook never causes an automatic bypass.

The configuration is declarative guidance, not executable authorization. The previous per-operation `confirm_stage`, `confirm_commit`, `confirm_push`, and `confirm_change_request` switches are replaced by scope-based authorization guidance; an explicitly supplied old policy requesting per-step approval must be clarified rather than silently ignored. No automatic configuration migration occurs.

## Evaluation

- [Fictional example](examples/input-output.md)
- [Machine-readable evaluations](evals/evals.json)
- [Trigger evaluations](evals/triggers.json)
- [Evaluation cases](evals/cases.md)
- [Rubric](evals/rubric.md)
