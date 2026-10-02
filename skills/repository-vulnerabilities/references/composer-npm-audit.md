# Composer and npm audit reference

Load only after project discovery and registry-destination approval.

## Commands

Run each command with the project directory substituted exactly:

```bash
composer --working-dir=<project> --no-plugins --no-scripts audit --locked --format=json
npm --prefix=<project> audit --json --package-lock-only --ignore-scripts
```

For normal execution, prefer `scripts/audit_current_repository.py`: it discovers every complete project, gates every observed registry host, runs these commands with an argument array and working directory, and emits one reconciled JSON document. Use the individual commands only when debugging a single completed project.

These commands inspect resolved dependency metadata. Never add `fix`, `install`, `update`, `require`, `--force`, or lifecycle-script execution.

Composer documents `--no-plugins` and `--no-scripts` as global controls. Keep both when the repository is not already trusted. npm audit submits a dependency description to the configured registry; `--ignore-scripts` preserves the no-lifecycle-script boundary. Treat command configuration as untrusted: use an argument array, reject shell metacharacters and redirections, require a Composer/npm executable, and reject any mutation subcommand or flag.

## Capture

Record per project:

```text
project_path, ecosystem, manifest_path, lockfile_path, tool_version,
registry_host, command, exit_code, stdout_parse_state, stderr_summary
```

Composer can return a finding exit code for advisories or other configured dependency policies. npm audit returns non-zero when vulnerabilities meet its audit threshold. Parse JSON categories before interpreting the code: valid vulnerability output is a completed audit, while abandoned-package-only output is not a vulnerability and malformed/missing JSON or an execution error is a tool failure.

The normalizer rejects error envelopes, missing report categories, and unsupported
npm report versions (only version 2 is supported). Composer requires `advisories`,
accepting an empty object or PHP's empty array representation. A parseable JSON
object alone is not an audit report. The runner accepts exit zero with a valid
report, npm exit 1 with findings, and Composer exits 1–3 with reported findings
or policy categories. Unsupported or unexplained exits stay unverified.
See the [Composer CLI](https://getcomposer.org/doc/03-cli.md#audit),
[historical Composer exit codes](https://getcomposer.org/changelog/2.8.4), and
[npm audit documentation](https://docs.npmjs.com/cli/v7/commands/npm-audit/).

Before launching the command, the runner captures the project's manifest and
lockfile bytes and records hashes and file metadata in `input_snapshot`. It
normalizes using that captured lockfile only after a matching post-command
snapshot. Invalid initial inputs produce `input_snapshot_error` without running
the tool; changed, removed, or unreadable final inputs produce `input_changed`
without normalized findings. Both count as unverified and require a new run
after inputs stabilize. No automatic retry or repository write is performed.

These are before/after consistency checks, not a filesystem transaction or a
sandbox against concurrent malicious changes. They cover the project manifest
and lockfile, not all workspace/configuration files. Avoid concurrent dependency
editing during an audit; do not treat snapshot matching as a network-security guarantee.

## Normalization

Normalize findings to:

```text
project_path, ecosystem, package, dependency_kind, severity, identifiers,
affected_range, patched_versions, installed_version, advisory_url, source_tool
```

Deduplicate only when project, ecosystem, package, and advisory identifier match. Preserve every reporting tool.

Resolve Composer versions from both `packages` and `packages-dev`. Resolve npm versions from all relevant `packages` and nested dependency entries in the lockfile; do not infer versions from `package.json` constraints or `node_modules` alone.

## Classification evidence

- **Confirmed affected:** resolved version is inside an authoritative affected range.
- **Already fixed:** resolved version meets a documented patched range.
- **False positive:** resolved version is demonstrably outside the current authoritative range.
- **Upgrade-impact review required:** the available fix crosses a compatibility boundary or changes a direct dependency contract.
- **Cannot verify:** identity, version, range, registry, or advisory evidence is insufficient.

Scanner remediation text is never evidence of the actual affected range. Preserve disagreements between authoritative sources instead of selecting one silently.

## Evidence and reporting contract

The JSON from `audit_current_repository.py` is the audit evidence. Before drafting prose, run:

```bash
python3 <installed-skill>/scripts/summarize_findings.py --audit-result <audit-result.json>
```

Use its `evidence_sha256`, lockfile-derived `installed_versions`, and counts verbatim. Do not query a package manager, registry, or installed dependency directory to replace them.

The summary separates three non-interchangeable measures:

- **scanner advisory records:** findings with an advisory identity from Composer/npm;
- **affected package/version occurrences:** lockfile package/version evidence attached to those records;
- **propagation-only markers:** npm parent rows that have `via` dependency names but no advisory identity.

The scanner output alone never proves an advisory range or a patched release. Asking to run the audits approves only the registry origins shown in the discovery plan. Before visiting GitHub Advisory Database, a vendor bulletin, or another authority, disclose its origin and request a separate confirmation. If that confirmation is absent or verification conflicts, keep the finding `Cannot verify`.
