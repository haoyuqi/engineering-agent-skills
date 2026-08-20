---
name: git-change-delivery
description: Use when the user explicitly asks to stage, commit, push, publish a branch, or open a GitHub pull request or GitLab merge request from local changes.
license: Apache-2.0
compatibility: Requires Git; opening a PR or MR also requires an authenticated GitHub or GitLab integration.
---

# Git Change Delivery

Deliver only intended change. Staging, committing, pushing, and opening a PR/MR are separate gates with different targets and recovery costs.

## Configuration

Use [config.example.yaml](config.example.yaml). Repository instructions and explicit user choices win. Never assume issue keys, labels, reviewers, branch conventions, or provider.

## Confirmation gates

After showing exact scope, get fresh confirmation for each mutation:

1. paths to stage; 2. commit message/hook behavior; 3. remote/branch, upstream or force mode; 4. full PR/MR proposal.

Confirmation of one gate never authorizes the next.

## Workflow

1. **Inspect.** Read instructions, branch/remotes/upstream, status, diffs, untracked files, and hooks. Classify every path intended, excluded, unrelated, or uncertain.
2. **Propose staging.** Show paths, purpose, fingerprint. Never default to `git add .`/`-A` in mixed worktrees. Recheck before staging; changed content needs new diff and confirmation. Stage unchanged paths only; show staged diff/status and stop on scope drift.
3. **Verify and commit.** Run approved checks. Never bypass a failed hook automatically. Offer 2–3 messages from staged diff; commit only after exact message/scope confirmation.
4. **Push.** Show exact remote ref. Force mode needs separate branch/mode confirmation. Stop before PR/MR if push fails.
5. **Prepare request.** Detect GitHub/GitLab unless configured; reuse template when present. Propose target, title, body, draft state, labels, reviewers, assignees. Validate labels; never create missing labels implicitly. Create only after full confirmation.
6. **Verify.** Read back commit SHA, branch, PR/MR reference/state. Load [assets/delivery-report-template.md](assets/delivery-report-template.md) only for final response.

## Rationalizations to reject

- “Ship it authorizes everything.” Staging, commit, push, and PR/MR creation remain separate gates.
- “`git add .` is faster.” Mixed worktrees require explicit paths.
- “The hook is unrelated.” Never bypass it automatically.
- “Force push is the recovery.” Explain ref state before proposing force-with-lease.
- “Create the missing label.” Provider metadata is a separate mutation.

## Failure behavior

Preserve state and stop at failed gate. Do not restage unrelated work, rewrite commits, change remotes, create duplicates, or switch provider automatically. If provider integration is missing after push, report branch and safe manual compare URL.
