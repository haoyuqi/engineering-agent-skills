# PR/MR Review

Provider-neutral review of GitHub pull requests, GitLab merge requests, and local patches. It combines requirement coverage with evidence-based code analysis while remaining read-only.

## Quick start

Install this Skill directory with a compatible installer, then ask:

```text
Use pr-mr-review to review https://github.com/acme-example/parcel-api/pull/42.
```

The Skill can use GitHub or GitLab integrations, their CLIs, or a local `git diff`. A GitHub PR or GitLab MR URL on its own selects the remote review target; before analysis, the Skill searches the execution directory and its immediate child Git worktrees for a matching `origin` remote, then uses that local checkout to understand the codebase. If no unique checkout exists, it asks for a path or approval for limited remote-only review. If you provide a directory instead, it derives the local change set from that directory's `git status`, staged/unstaged diffs, and relevant untracked files. Requirements may come from Jira, GitHub/GitLab Issues, a document, or the current conversation.

## Configuration

Copy or adapt [config.example.yaml](config.example.yaml) only when auto-detection is insufficient. Keep tokens and private URLs out of tracked configuration.

## Output

The report contains a verdict, severity-ranked findings, acceptance-criteria coverage, verification gaps, and evidence locations. It never posts comments or approvals.

## Safety

All providers are read-only by default. Any later request to comment, approve, or modify external state requires a separate confirmation containing the exact target and proposed action.

## Evaluation

- [Fictional example](examples/input-output.md)
- [Machine-readable evaluations](evals/evals.json)
- [Trigger evaluations](evals/triggers.json)
- [Evaluation cases](evals/cases.md)
- [Rubric](evals/rubric.md)
