# Engineering Agent Skills

Portable, provider-neutral Agent Skills for software-engineering planning and delivery workflows.

This repository is a collection of independently installable skills that follow the open `SKILL.md` convention and work with compatible coding agents. Its current focus is turning ambiguous product or engineering discussion into a reviewable requirements draft.

## Install and quick start

Install one skill from a local checkout with a compatible skill installer:

```bash
npx skills add ./engineering-agent-skills --skill requirements-clarification -a codex
```

Replace `codex` with the target agent supported by your installer. After installation, explicitly invoke it with a request such as:

```text
Use requirements-clarification to turn our discussion into a testable requirements draft.
```

`requirements-clarification` relies on two externally installed skills for its three modes. They are not bundled by this repository:

- `obra/superpowers:brainstorming` — install with `npx skills add https://github.com/obra/superpowers --skill brainstorming`
- `mattpocock/skills:grill-me` — install with `npx skills add https://github.com/mattpocock/skills --skill grill-me`

It does not replace or impose an additional lifecycle on either external skill. A missing selected dependency stops this skill's workflow without writing its requirement document.

## Validate a checkout

The repository includes an offline structural check. It verifies required documentation, per-skill resources, and `SKILL.md` metadata; it neither installs dependencies nor invokes external skills.

```bash
python3 tests/test_repository_structure.py
```

## Principles

- **Independent within this repository** — each skill is self-contained and does not require another skill from this repository. External dependencies, if any, are declared in that skill's documentation.
- **Provider-neutral** — GitHub, GitLab, local Git, issue trackers, and security scanners are optional inputs rather than hard dependencies.
- **Read-only by default** — comments, approvals, commits, pushes, and external updates require explicit user confirmation.
- **Evidence first** — findings must link to a diff, file location, requirement, dependency version, or tool output. Unknowns remain unknown.
- **Verifiable** — each skill includes sanitized examples and offline evaluation cases.

See [README.zh-CN.md](README.zh-CN.md) for Chinese documentation.

## Available skills

| Skill | Purpose |
| --- | --- |
| [requirements-clarification](skills/requirements-clarification/) | Turn current discussion into a testable requirements draft through external exploration and challenge workflows. Includes [a fictional input/output example](skills/requirements-clarification/examples/input-output.md) and offline evaluation cases. |
| [repository-vulnerabilities](skills/repository-vulnerabilities/) | Audit Composer/npm lockfiles with registry approval gates, deterministic evidence summaries, and separately approved advisory verification. |

## License

Licensed under the [Apache License 2.0](LICENSE).
