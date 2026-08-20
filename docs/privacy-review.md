# Public-content privacy review

This repository contains generalized public workflows and fully fictional examples. It must not contain employer, customer, or production material. Automated checks reduce accidental disclosure but are not a legal guarantee; a human provenance review remains required before publication.

## Automated gate

`python3 tests/test_public_content.py` checks the current worktree, while `python3 tests/test_public_content.py --history` checks every committed file revision. They inspect every reasonably sized UTF-8 text file, regardless of extension, and reject common workstation paths, email addresses, private network addresses and domains, Jira numeric custom-field identifiers, private-key markers, credential-shaped values, and credential-bearing URLs. Every HTTP(S) hostname must be an explicitly reviewed public documentation host or a reserved example domain. `python3 tests/test_public_content_coverage.py` keeps lockfile and non-Markdown text coverage from regressing.

The allowlist is deliberately small. Adding a real provider documentation host requires an explicit code review; adding an organization, customer, repository, or environment host is forbidden.

## Human provenance checklist

Review every changed example, fixture, prompt, template, configuration key, and output before release:

- Organization, product, project, service, repository, environment, team, and person names are invented or refer to a public upstream project.
- Issue prefixes, field names, labels, status vocabularies, Agent role names, directory layouts, API schemas, and report formats do not reproduce a workplace convention.
- Source excerpts, commit messages, incident details, vulnerability records, metrics, logs, URLs, paths, and identifiers are invented or taken from a cited public source.
- Examples do not preserve a distinctive combination of real architecture, business behavior, infrastructure, or failure symptoms.
- Credentials, cookies, tokens, authorization headers, personal data, customer data, and private attachment content are absent rather than merely visually hidden.
- Git history and generated artifacts are reviewed in addition to the current files.

When provenance is uncertain, replace the material with a newly invented scenario or remove it. Do not publish first and investigate later.
