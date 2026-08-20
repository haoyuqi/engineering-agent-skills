# Design benchmarks

Reviewed on 2026-08-13. Commit identifiers make this comparison reproducible without claiming that upstream projects will remain unchanged. The two upstream repositories used as runtime dependencies are pinned in [external-sources.lock.json](external-sources.lock.json); the lock is an audit record, not an installer constraint.

| Source | Inspected revision | What this repository adopts |
| --- | --- | --- |
| [Agent Skills specification](https://agentskills.io/specification) | `69ef37e9424c0a7ea9dd2293b559e43ec8176379` | Portable frontmatter, official naming limits, compatibility metadata, one-level file references, and progressive disclosure. |
| [Vercel skills CLI](https://github.com/vercel-labs/skills) | npm `1.5.20` (reviewed 2026-08-13) | Cross-Agent repository discovery and independently selectable Skill installation. |
| [GitHub Copilot Agent Skills docs](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) and [Awesome Copilot](https://github.com/github/awesome-copilot) | Documentation accessed 2026-08-13; Awesome Copilot `main` | One portable Skill directory, runtime-selected installation location, and bundled scripts/resources rather than Copilot-only prompt copies. |
| [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) | `b8caa260a420a73042e35521de4b5c8baf6446cc` | JSON-producing deterministic scripts, stderr/status separation, direct one-level resources, troubleshooting, and public installation guidance. |
| [Anthropic Skills](https://github.com/anthropics/skills) | `f17010c9bb483898c1d9c9f42dde2b3a98889434` | Realistic machine-readable evals, with-skill versus baseline comparison, evidence-backed grading, reusable scripts, and output templates. |
| [obra/superpowers](https://github.com/obra/superpowers) | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | Behavior and pressure testing, explicit gates, visible rationalization failures, checkable workflow state, and evidence before completion claims. |
| [mattpocock/skills](https://github.com/mattpocock/skills) | `84fdeffd12f2ee307994d1eb6feb48173b6e0502` | Small composable capabilities, descriptions as invocation pointers, completion criteria for each step, purposeful splitting by branch, and thin user-facing wrappers over reusable primitives. |
| [Trail of Bits Skills](https://github.com/trailofbits/skills) | `304c81a8cefb6e3c029ebd0d12940ccf0713eccb` | Risk-proportional prescriptiveness, security-specific rationalizations to reject, value-add over reference dumps, and explicit anti-pattern reasoning. |

## Deliberate differences

The goal is not to copy a framework wholesale.

- We do not require a global bootstrap Skill, plugin runtime, issue tracker, sub-agent implementation, or a specific model.
- We do not inherit upstream defaults that commit files, publish issues, or mutate external systems. This repository's explicit-confirmation boundary remains authoritative.
- We retain one flat `skills/` catalog so every directory is independently installable even when the README groups related capabilities conceptually.
- Runtime-specific metadata lives outside portable `SKILL.md` fields.
- Configuration remains optional and provider-neutral; no setup Skill is required for the rest of the catalog.

## External dependency lesson

`mattpocock/skills:grill-me` is a user-facing wrapper whose implementation delegates to `mattpocock/skills:grilling`. Installing or invoking only the wrapper is therefore not a complete integration on runtimes that do not resolve Skill dependencies automatically. `requirements-clarification` documents both names, stops when either is unavailable, and never substitutes an improvised interview.

External Skill behavior can change. Integration expectations are tested at the boundary we rely on—approved design from `brainstorming`, resolved decision tree from `grill-me`/`grilling`—instead of copying their internal prompts.

## Follow-up adoption — 2026-08-13

A follow-up review of [Superpowers' skill-testing guidance](https://github.com/obra/superpowers/blob/main/skills/writing-skills/testing-skills-with-subagents.md) reinforced an important distinction: a fixture alone is not behavioral proof. High-risk instructions need an observable baseline failure, a with-Skill pressure run, and a record of the exact assertion being graded.

This repository adopts that principle without coupling to Claude Code or a paid model runner:

- every one of the 51 machine-evaluation expectations has a stable ID, an observable-output type, and explicit fictional fixture source(s);
- [`evals/result.schema.json`](../evals/result.schema.json) defines separate with-Skill and baseline records; and
- [`evals/validate_result.py`](../evals/validate_result.py) cross-checks a sanitized record against the installed Skill contract before aggregation.

The contract makes larger, repeated pressure campaigns reproducible; it does not convert a schema check into a model-quality claim.
