# Security Policy

## Design baseline

Skills in this repository are read-only by default. They must not perform external writes, including comments, approvals, commits, pushes, pull/merge-request creation, issue changes, or dependency updates, without explicit user confirmation after presenting the exact proposed action.

Skills must not expose credentials, tokens, cookies, private repository content, personally identifiable information, or unredacted production logs in reports, examples, fixtures, or tests.

GitHub Actions workflows use least-privilege permissions and full immutable
commit SHAs for third-party Actions. Update a pin only after reviewing the
upstream release and source; the offline workflow supply-chain test rejects
mutable tags or branches.

## Reporting a vulnerability

Please do not open a public issue for a security vulnerability. Until a dedicated contact is published, report it privately to the repository maintainer through the hosting platform's private security-advisory feature.
