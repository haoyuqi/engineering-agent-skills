---
name: git-change-delivery
description: Use when the user explicitly asks to stage, commit, push, publish a branch, or open a GitHub pull request or GitLab merge request from local changes.
license: Apache-2.0
compatibility: Requires Git; opening a PR or MR also requires an authenticated GitHub or GitLab integration.
---

# Git Change Delivery

Deliver within user authorization, without redundant confirmation.

## Configuration

Use [config.example.yaml](config.example.yaml). Explicit user choices and repository rules win. Configuration never grants permission. Resolve provider and conventions from repository evidence; do not invent issue keys or metadata.

## Authorization

Record authorized operations, scope, exclusions, target, and stopping point. An explicit commit/push/PR request authorizes that sequence. Commit requests include necessary scoped staging unless limited to already staged changes. Show the resolved plan and proceed without asking again while scope and risk remain unchanged.

Partial authorization stays partial: stage-only cannot commit; commit-only cannot push; preparing a PR proposal cannot publish it. A PR-only request uses an existing published branch unless the conversation clearly authorizes delivering the current changes too. Ambiguous “ship it” is not blanket permission. Ask only about material ambiguity or missing authority.

Honor explicit requests for step-by-step approval or exact-message approval. Broad delivery authorization does not cover force push, hook bypass, history rewriting, target changes, or scope expansion: disclose the exact risk/action and obtain specific approval. An existing specific approval remains valid only for unchanged scope and conditions.

## Workflow

1. **Inspect.** Read instructions, branch/remotes/upstream, status, staged/unstaged diffs, untracked files, and hooks. Classify intended, excluded, unrelated, and uncertain changes. Resolve the authorized scope; preserve unrelated pre-staged work. If the index would include uncertain/unrelated content, stop before commit and ask how to isolate it; never silently unstage it.
2. **Stage.** Show paths, purpose, and fingerprint; recheck before staging. Use explicit paths or selected hunks, never blanket staging in mixed worktrees. Unexpected drift requires inspection; material scope changes need approval. Verify the staged diff matches the authorized change.
3. **Commit.** Run applicable checks and normal hooks. Derive a message from the staged diff and recent repository history; show it and commit when authorized. Offer alternatives only when requested or convention is materially ambiguous. Hook failure stops delivery; never bypass automatically.
4. **Push.** Show exact remote/branch and upstream action; push only within authorization. No automatic force mode or target substitution. Stop dependent steps on failure.
5. **PR/MR.** Check for an existing request; avoid duplicates and report its URL. Use the repository template. Show base/head, title, body, draft state, and requested metadata; create when authorized. Validate labels/reviewers; creating missing labels, adding unrequested reviewers, or modifying an existing request requires separate authority.
6. **Verify.** Read back commit, remote ref, request URL/state, and worktree. Report completed operations, remaining work, and blockers using [assets/delivery-report-template.md](assets/delivery-report-template.md).

## Failure behavior

Preserve evidence and state. Never treat a failed or uncertain write as success; inspect remote state before retrying. Do not rewrite history, alter hooks/remotes, or merge automatically. If provider integration fails after push, report the branch and safe manual compare URL.
