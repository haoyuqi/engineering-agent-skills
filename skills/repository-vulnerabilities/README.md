# Repository Vulnerabilities

Scan the current repository's Composer and npm lockfiles, run their read-only audit commands, and verify affected versions against authoritative advisories before recommending action.

## Quick start

```text
Use repository-vulnerabilities to scan the current codebase for Composer and npm vulnerabilities. Report affected versions and false positives; do not apply fixes.
```

The current directory is scanned by default. [config.example.yaml](config.example.yaml) is an Agent policy template, not an executable runner configuration: explicitly translate approved roots, exclusions, ecosystems, and Registry origins into the runner's CLI arguments. Do not place credentials in the file.

Project discovery uses the dependency-free, read-only [`scripts/discover_projects.py`](scripts/discover_projects.py), so monorepo coverage and exclusions can be tested independently of a model or package registry.

Captured Composer/npm JSON is normalized by the dependency-free [`scripts/normalize_audit.py`](scripts/normalize_audit.py), which joins findings to actual production, development, direct, transitive, and nested lockfile versions without classifying an advisory by itself.

## Prerequisites

- **Python 3.9+** to run the bundled discovery, audit-orchestration, and result-normalization scripts.
- **Composer** for each Composer project you want to audit, and/or **npm** for each npm project. Discovery still works when either package manager is unavailable; that ecosystem is reported as unverified instead of being skipped silently.
- **User approval for network access** before an audit runs. Discovery is local and offline; `composer audit` and `npm audit` send dependency metadata only to the exact registry origins disclosed for approval.

## Run against the current repository

First generate a local, no-network discovery and registry-destination plan. It searches the current repository and its subprojects for complete `composer.json`/`composer.lock` and `package.json`/`package-lock.json` pairs.

```bash
python3 <installed-skill>/scripts/audit_current_repository.py --root .
```

Review the `registry_destinations` output. The script reports credential-free origins, never credential values. It rejects dynamic project Registry values and detected project credential configuration; it also removes user/global configuration and proxy environment from child audit processes.

After the user approves the exact origins, run the audits explicitly. This example permits only the two public defaults:

```bash
python3 <installed-skill>/scripts/audit_current_repository.py \
  --root . \
  --run-audits \
  --allow-registry-origin https://repo.packagist.org \
  --allow-registry-origin https://registry.npmjs.org
```

The runner uses temporary package-manager homes and caches, ignores user/global package-manager configuration and proxies, and suppresses lifecycle scripts. This prevents an unseen local registry override or cached credential from changing the approved destination. A private registry that depends on user/global credentials therefore becomes an explicit unverified result rather than silently using them.

The JSON result reconciles discovered, incomplete, completed, blocked, and unverified projects. It also identifies child npm workspace manifests covered by a completed parent `package-lock.json`; a workspace remains unverified if that parent audit is blocked or fails. A parseable non-zero audit result remains `completed`; it is a vulnerability finding, not automatically a tool failure. The script never runs `install`, `update`, `require`, or `audit fix`.

Before writing a report, create a local evidence summary from that JSON:

```bash
python3 <installed-skill>/scripts/summarize_findings.py \
  --audit-result <audit-result.json>
```

This keeps scanner advisory records, affected lockfile package/version occurrences, and npm propagation-only markers separate. The summary is local and does not contact a registry. Use its lockfile versions and totals verbatim; do not substitute `composer show`, `npm view`, `node_modules`, or a live registry response.

## Advisory verification

Registry approval permits only the Composer/npm audits. It does **not** permit requests to GitHub Advisory Database, vendor bulletins, or any other external advisory source. If authoritative verification is wanted, first disclose those additional origins and obtain a separate confirmation. Until then, scanner findings remain `Cannot verify`, rather than being described as confirmed, already fixed, or false positive.

## What it distinguishes

- confirmed affected dependencies;
- already-fixed or false-positive findings;
- compatibility-sensitive upgrades;
- Composer and npm projects that were cleanly audited;
- findings that cannot be verified with available evidence.

## Safety

`composer audit` and `npm audit` do not modify dependency files, but they may send package metadata to configured registries. The Skill discloses redacted registry hosts and stops before an unclear or unsafe metadata destination. Installation, updates, `npm audit fix`, dependency-file edits, branches, commits, pushes, and PR/MR creation require explicit confirmation after the exact action is shown.

## Evaluation

- [Fictional example](examples/input-output.md)
- [Machine-readable evaluations](evals/evals.json)
- [Trigger evaluations](evals/triggers.json)
- [Evaluation cases](evals/cases.md)
- [Rubric](evals/rubric.md)
