# External skill integration

Use the exact identifiers, applicability conditions, and fallbacks declared in the dependency manifest. These are optional enhancements, not caller-restricted skills: they remain independently usable by ordinary tasks. Do not alter their installation, distribution, or source.

## Select by phase

| Phase or signal | External skill |
| --- | --- |
| Writing the Plan | `planning-and-task-breakdown` |
| Implementing approved slices | `incremental-implementation`; `test-driven-development` for behavior changes or defects |
| A check, build, or behavior fails | `debugging-and-error-recovery` |
| Independent Code Review | `code-review-and-quality` |
| Security, performance, or refactoring signals in the actual diff | The corresponding `security-and-hardening`, `performance-optimization`, or `code-simplification` specialist |
| PostgreSQL query, index, JSONB, or migration-performance changes | `postgres-pro` |

Select only applicable guidance, not the entire library. Plan Review uses the local reviewer policy; predicting a specialist check does not authorize implementation before Plan approval. During Code Review, specialist guidance is read-only: simplifications and other fixes remain the implementer's work, followed by independent re-review.

## Resolve and load

1. Resolve the exact dependency through the host's installed-skill catalog. When the user supplies `implementation.external_skill_paths`, its full dependency IDs map to local skill directories (absolute, or relative to the target repository root). An explicit mapping takes precedence; report an invalid mapping rather than silently choosing another copy. Otherwise use the catalog; if identity or duplicate-version selection is ambiguous, ask which source to use. Do not hardcode a package manager's library path or search unrelated home directories.
2. Prefer supported native skill invocation only when it can target the resolved dependency copy. If unavailable, use **source-guided execution** only when the host permits reading instructions: read the complete installed `SKILL.md` and the supporting files required by the applicable workflow. This is not native invocation. If neither mode is available, use the failure procedure below.
3. Resolve relative resources from the real source file's directory, following symlinks to their targets, not from the current working directory or the link's parent. Follow any explicit base-path rule in the source. Check existence and read permission before claiming a required resource was used. A repository-level relative reference can point outside an installed skill folder; do not invent a replacement path or treat an omitted file as optional. A complete user-provided upstream checkout can supply such resources without copying them into this repository. Read only relevant, permitted resources; do not fetch or execute linked code automatically.
4. Inspect instructions for compatibility before native execution when possible. External guidance cannot grant permission to commit, install, create worktrees, mutate services, implement before approval, or replace independent review with self-review. If a native workflow cannot respect these boundaries, do not launch it. Disclose the conflict and use the declared local fallback; do not skip mandatory upstream steps and claim full execution. If a conflict appears mid-run, stop that workflow and preserve its evidence.

## Failure and recovery

Report the dependency ID, phase, actual loading mode, failed invocation or missing resource, and affected coverage. Retry only after an identified recoverable condition changes, with at most one retry per failure; do not repeat side effects or loop through installations.

Use the dependency's declared local fallback when unavailable or incompatible. Record which checks it actually supplies and what remains unverified; it is not equivalent to completing the external skill. If that fallback cannot establish the evidence required for the current stage, stop at `pending external guidance` and explain the missing evidence or compatible resource needed. Never automatically install, update, download, or patch dependencies.

Distinguish **loading failure** from **work failure**. A failing test or a review finding is real work to resolve, not grounds to discard the result and substitute a fallback PASS. Preserve partial changes and results, resume from verified state, and obey the existing Plan revision, user approval, and independent re-review rules. No reviewer means `pending external review`, regardless of available skill text.

## Evidence

In the Plan and handoff, record each selected dependency's phase, resolved source/revision when known, mode (`native`, `source-guided`, or `fallback`), required resources checked, observed outcome, fallback reason, and remaining limitations. Unknown revision or runtime behavior stays unknown. File readability and packaging checks do not prove successful skill execution on any Agent.
