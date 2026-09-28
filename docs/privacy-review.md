# Public-content privacy review

This repository contains generalized public workflows and fully fictional examples. It must not contain employer, customer, or production material. Automated checks reduce accidental disclosure but are not a legal guarantee; a human provenance review remains required before publication.

## Automated gate

This is a lightweight disclosure check, not automatic sanitization. It does not rewrite content or establish that a workflow is safe to publish.

- Credential-shaped values, private-key markers, and credential-bearing URLs block the check. Matches are never printed; reports contain only rule, location, and line.
- Workstation paths, non-example email addresses, private addresses/domains, and tracker field identifiers produce non-blocking `REVIEW` warnings. These may be legitimate examples; review their provenance rather than assuming they are leaks. Reserved example-domain emails are accepted.
- Public URLs do not need a domain allowlist. A public host is not proof that a link or its path is appropriate for publication.
- All findings are collected. Binary, non-UTF-8, oversized, unreadable, submodule, and unavailable LFS content is reported as incomplete coverage, not a clean result. Exit codes: `0` no blocking patterns (warnings may remain), `1` blocking findings, `2` incomplete/error.
- No scanner or license file is exempt. Symlink targets are inspected as text; their destinations are not read. No files or dependencies are installed.

### Scope and commands

```bash
# Tracked files plus non-ignored untracked files; excludes Git metadata.
python3 tests/test_public_content.py
# One-time baseline or explicit periodic review of all locally reachable refs.
python3 tests/test_public_content.py --history
# Every introduced commit snapshot, including content later deleted, and final tip.
python3 tests/test_public_content.py --base origin/main --head HEAD
python3 tests/test_public_content_coverage.py
```

History modes require a non-shallow checkout and deduplicate identical Git blobs. They also scan commit messages, but not author identities, reflogs, unreachable objects, remote-only refs, issues, PR bodies, artifacts, or ignored local files. The baseline therefore covers available Git history, not everything ever published.

CI fetches complete history, scans all PR commits, and separately scans the generated merge result. Main pushes scan the introduced range; new-branch pushes fall back to full history. CI runs **after upload** and cannot prevent initial disclosure. Run the worktree and range checks locally before pushing. No local hook is installed automatically. A passing check never replaces the human review below; if a real credential is found in published history, treat it as exposed and rotate it. History rewriting requires separate approval.

## Human provenance checklist

Review every changed example, fixture, prompt, template, configuration key, and output before release:

- Organization, product, project, service, repository, environment, team, and person names are invented or refer to a public upstream project.
- Issue prefixes, field names, labels, status vocabularies, Agent role names, directory layouts, API schemas, and report formats do not reproduce a workplace convention.
- Source excerpts, commit messages, incident details, vulnerability records, metrics, logs, URLs, paths, and identifiers are invented or taken from a cited public source.
- Examples do not preserve a distinctive combination of real architecture, business behavior, infrastructure, or failure symptoms.
- Credentials, cookies, tokens, authorization headers, personal data, customer data, and private attachment content are absent rather than merely visually hidden.
- Git history and generated artifacts are reviewed in addition to the current files.

When provenance is uncertain, replace the material with a newly invented scenario or remove it. Do not publish first and investigate later.
