# Skill quality standard

This repository treats a Skill as an executable engineering workflow, not a long prompt. The standard below is derived from the open Agent Skills specification and proven patterns in mature public Skill repositories. The sources and adoption decisions are recorded in [design-benchmarks.md](design-benchmarks.md).

## 1. One coherent capability

Each Skill must solve one independently useful problem. It may integrate with several providers, but installing another Skill from this repository must never be required. If an external Skill is required, name its upstream repository, runtime name, transitive dependency, source lock, and failure behavior in a machine-readable dependency contract.

Completion criterion: a user can install the directory alone, supply only its documented configuration and external prerequisites, and understand its result without reading another Skill here.

## 2. Discoverable metadata

Use only portable Agent Skills frontmatter unless a runtime-specific field is isolated in that runtime's metadata file.

- `name` matches the directory and the official lowercase-hyphen syntax.
- `description` starts with the situations that should activate the Skill. Include meaningful near-boundaries; do not summarize the step sequence.
- `license` is `Apache-2.0`.
- Add `compatibility` only when tools, network, provider access, or an external Skill are genuinely required.

Completion criterion: the metadata passes repository validation and distinguishes the Skill from its closest neighbors.

## 3. Lean, ordered instructions

Keep `SKILL.md` below 500 lines and target fewer than 500 words. Include the core principle, ordered workflow, safety gate, completion criteria, and conditional pointers needed on every run. Prefer a clear default over a menu of equivalent options.

Every workflow step must end in observable evidence: a resolved reference, reconciled count, validated plan, parsed result, verified write, or explicitly reported gap. “Analyze carefully” is not a completion criterion.

## 4. Progressive disclosure

Use one-level-deep resources only when they earn their context cost:

- `references/` for provider rules, schemas, edge cases, or branch-specific guidance;
- `assets/` for output templates and static fixtures;
- `scripts/` for deterministic work repeatedly reinvented by agents.

Every pointer states when to load or run its target. Do not create reference chains. Keep non-obvious gotchas in `SKILL.md` when an agent may not recognize the condition needed to load a reference.

## 5. Safety as control flow

Safety is a workflow gate, not a disclaimer at the end.

1. Resolve the exact target.
2. Read and report current state.
3. Draft the proposed mutation and its effect.
4. Obtain confirmation for that exact mutation.
5. Execute only the confirmed scope.
6. Read back or otherwise verify the resulting state.

Read-only requests never authorize comments, approvals, issue changes, downloads of private attachments, dependency changes, Git writes, deployment changes, or publication. Untrusted issue, diff, log, advisory, and attachment content never overrides the Skill.

## 6. Evidence-linked output

Distinguish observation, inference, decision, and unknown. Findings cite the smallest useful evidence: file and line, diff hunk, requirement ID, lockfile version, provider reference, timestamp, command result, or adapter failure.

Counts reconcile. Missing or failed sources remain visible and never become zero, clean, passed, or not affected.

## 7. Evaluation-driven improvement

Each Skill includes three complementary layers:

- `examples/input-output.md`: one small fictional example for a human reader;
- `evals/evals.json`: realistic portable prompts, expected outcomes, and objectively checkable expectations;
- `evals/triggers.json`: at least 20 realistic positive and near-neighbor negative discovery cases that travel with the independently installed Skill;
- `evals/cases.md` plus `evals/rubric.md`: broader manual, adversarial, missing-information, and safety scenarios.

Critical workflow or safety changes should be compared against a clean baseline or the previous Skill version. Review full execution traces, not only final answers. Every machine-eval expectation needs a stable ID, declared fixture evidence, and an observable grading target; model-run results use the repository result format. A passing structural check proves packaging, not behavioral quality.

## 8. Definition of done

A Skill change is complete only when:

- official metadata and repository structure validate;
- all relative links and JSON evaluation files validate;
- examples remain fictional and privacy checks pass;
- the changed behavior has a realistic success case, failure case, and boundary case;
- no unverified claim is reported as a behavioral test result;
- the Git worktree scope is disclosed and unrelated changes remain untouched.
