# Git Change Delivery

An explicit, provider-neutral workflow for staging, committing, pushing, and opening a GitHub PR or GitLab MR. Each stage is independently confirmable and stoppable.

## Quick start

```text
Use git-change-delivery to review these changes, commit them, push the current branch, and prepare a draft PR.
```

The Skill auto-detects GitHub or GitLab from the remote. Use [config.example.yaml](config.example.yaml) for project conventions, never for credentials.

## Safety

No mutation is implied by inspection. The exact files, commit, push target, and PR/MR proposal are each shown before execution. Hooks are never bypassed automatically, force pushes are disabled by default, and labels are never created implicitly.

## Evaluation

- [Fictional example](examples/input-output.md)
- [Machine-readable evaluations](evals/evals.json)
- [Trigger evaluations](evals/triggers.json)
- [Evaluation cases](evals/cases.md)
- [Rubric](evals/rubric.md)
