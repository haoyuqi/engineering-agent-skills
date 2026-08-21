# Engineering Agent Skills

Portable, provider-neutral Agent Skills for software-engineering investigation, planning, review, security, operations, and delivery workflows.

This repository is a collection of independently installable skills that follow the open Agent Skills specification and work with compatible coding agents. Each Skill owns its workflow, configuration template, fictional example, machine-readable evaluations, adversarial cases, rubric, and runtime-optional Agent UI metadata.

## Install and quick start

Install one Skill from GitHub with a compatible Skill installer:

```bash
npx skills@1.5.20 add haoyuqi/engineering-agent-skills --skill pr-mr-review
```

Replace `pr-mr-review` with any name from the catalog below. Select the target Agent through the installer's supported options when needed. After installation, explicitly invoke it with a request such as:

```text
Use pr-mr-review to review this pull request without posting comments or approvals.
```

For GitHub Copilot, install the same portable directory into its supported Agent location:

```bash
npx skills@1.5.20 add haoyuqi/engineering-agent-skills --skill pr-mr-review --agent github-copilot
```

The repository does not maintain Copilot-only copies. The installer selects the runtime location while the portable `SKILL.md` stays the source of truth.

See [compatibility and installation](docs/compatibility.md) for the verified Codex, Claude Code, OpenCode, and GitHub Copilot packaging layouts, manual-copy guidance, and the limits of that verification.

Configuration templates are explicit Agent policy inputs, never credential
stores or implicit write permission. See the checked
[configuration contract](docs/configuration-contract.md) before adapting a
template.

`requirements-clarification` relies on two externally installed skills for its three modes. They are not bundled by this repository:

- `obra/superpowers:brainstorming` — install with `npx skills@1.5.20 add obra/superpowers --skill brainstorming`
- `mattpocock/skills:grill-me` — this upstream wrapper delegates to `mattpocock/skills:grilling`; install both with `npx skills@1.5.20 add mattpocock/skills --skill grill-me --skill grilling`

It does not replace or impose an additional lifecycle on either external skill. A missing selected dependency stops this skill's workflow without writing its requirement document.

The commands above use the exact installer version verified by this repository.
Using a newer installer is possible, but it is outside the recorded packaging
evidence until the compatibility check is rerun and its version is updated.

## Development disclosure

This repository is developed with AI assistance. Coding Agents help research,
draft, review, test, and maintain its Skills and documentation. The maintainer
retains responsibility for scope, source provenance, security, tests, and every
publication decision. AI output is not treated as evidence until it has been
reviewed and verified.

Published content must pass the same public-content and provenance review
described in [docs/privacy-review.md](docs/privacy-review.md), whether it was
written with AI assistance or not.

## Validate a checkout

The repository includes offline structural and public-content checks. They verify official metadata constraints, each selected Skill's resources, workflow and trigger-boundary cases, links, and common privacy hazards; they neither install dependencies nor invoke external skills.

```bash
python3 tests/test_repository_structure.py
python3 tests/test_workflow_supply_chain.py
python3 tests/test_compatibility_contract.py
python3 tests/test_configuration_contract.py
python3 tests/test_public_content.py
python3 tests/test_public_content_coverage.py
python3 tests/test_public_content.py --history
python3 tests/test_repository_vulnerability_discovery.py
python3 tests/test_repository_vulnerability_normalization.py
python3 tests/test_repository_vulnerability_audit_runner.py
python3 tests/test_core_eval_fixtures.py
python3 tests/test_evaluation_contract.py
python3 tests/test_evaluation_result_validator.py
python3 tests/test_external_dependency_contract.py
python3 tests/test_template_quality.py
```

CI also runs a networked packaging check against pinned `skills` CLI version `1.5.20`, installing every Skill into representative Codex, Claude Code, OpenCode, and GitHub Copilot project layouts and comparing every bundled file. The test has a bounded timeout, so unavailable npm access fails clearly instead of hanging. Run it locally only when npm access is available:

```bash
python3 tests/test_installer_compatibility.py
```

## Principles

- **Independent within this repository** — each skill is self-contained and does not require another skill from this repository. External dependencies, if any, are declared in that skill's documentation.
- **Provider-neutral** — GitHub, GitLab, local Git, issue trackers, and security scanners are optional inputs rather than hard dependencies.
- **Read-only by default** — comments, approvals, commits, pushes, and external updates require explicit user confirmation.
- **Evidence first** — findings must link to a diff, file location, requirement, dependency version, or tool output. Unknowns remain unknown.
- **Verifiable** — each skill includes sanitized examples and offline evaluation cases.

The repository's definition of a high-quality Skill is documented in [docs/skill-quality-standard.md](docs/skill-quality-standard.md). [docs/design-benchmarks.md](docs/design-benchmarks.md) records adopted upstream patterns and deliberate differences. [docs/privacy-review.md](docs/privacy-review.md) defines the automated and human provenance gate for public content.

See [docs/evaluation.md](docs/evaluation.md) for trigger tests, fixture-backed
workflow evaluation, repeated-run reporting, and the distinction between
offline validation and model-backed evidence. Model-run evidence is publishable
only when reproduced from the committed Skill revision and validated with the
[result format](docs/evaluation-result-format.md).

See [README.zh-CN.md](README.zh-CN.md) for Chinese documentation.

## Available skills

| Skill | Purpose |
| --- | --- |
| [deep-build](skills/deep-build/) | Plan, implement, verify, and independently review a substantial change; stop before Git delivery. |
| [git-change-delivery](skills/git-change-delivery/) | Stage, commit, push, and open a GitHub PR or GitLab MR with confirmation gates. |
| [pr-mr-review](skills/pr-mr-review/) | Review GitHub PRs, GitLab MRs, or local patches against requirements and code. |
| [repository-vulnerabilities](skills/repository-vulnerabilities/) | Discover and audit Composer/npm lockfiles in the current repository. |
| [requirements-clarification](skills/requirements-clarification/) | Turn current discussion into a testable requirements draft through external exploration and challenge workflows. |

## License

Licensed under the [Apache License 2.0](LICENSE).
