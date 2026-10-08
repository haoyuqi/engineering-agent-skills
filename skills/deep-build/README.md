# Deep Build

`deep-build` implements a substantial approved change only after a written Plan passes independent review and the user approves that reviewed Plan. Its portable contract is:

```text
Plan document → independent Plan Review → report to user → user approves Plan → incremental implementation → independent Code Review PASS → report to user → user acceptance
```

It is host-neutral. Both review gates require a reviewer who did not author the reviewed version. A separate agent context, another session, an external reviewer, or a human can satisfy this; same-context self-review cannot. Reviewers inspect artifacts read-only; the author makes fixes and requests re-review. Without a reviewer, report `pending external review` rather than claiming PASS.

Prefer a different model only when suitable for the task, never a capability downgrade just for diversity. If alternative capability is unknown, retain the author's model and reasoning effort in a separate context. Record the actual known model/effort and selection reason; do not invent missing metadata. No specific runtime or model is required. The full policy is in [review-criteria.md](references/review-criteria.md).

Report every review result with the Plan path, reviewer context, findings, revisions, risks, and next decision; after Plan PASS, request Plan approval and stop until the user responds. Git delivery, deployment, and remote PR/MR review are outside this skill. Configuration is host guidance only: independence is mandatory, while model diversity is a preference.

```text
Use deep-build to implement the approved tenant-scoped export feature across the API and worker.
```

## Recommended external skills

The workflow remains usable without these skills because its mandatory gates and concise fallback criteria are included locally. Installing them provides their deeper specialist guidance. Each dependency, trigger, source URL, and fallback is also declared in [external-dependencies.json](external-dependencies.json).

They remain independently discoverable; deep-build does not restrict their callers or manage their distribution. At each applicable phase, use native invocation where supported, or explicitly identified source-guided execution where the host permits it. Read the complete skill and required resources using their real source-relative paths. Reading instructions is not native invocation and does not establish cross-Agent behavior. The [integration policy](references/external-skills.md) defines phase routing, incompatible workflows, partial results, and failure handling.

Supply `implementation.external_skill_paths` in the explicit configuration input to override a dependency's local directory, keyed by its full ID (for example, `addyosmani/agent-skills:code-review-and-quality`). Absolute paths or paths relative to the target repository root are accepted. Otherwise use the host catalog. No package-manager-specific location is required. Keep machine-specific paths out of published configuration.

If invocation or a required resource fails, report it and use the declared local fallback. Stop when that fallback cannot establish the stage's evidence; never silently claim full external execution or automatically install anything. Some upstream references may require files outside the skill subdirectory: an installer that copies only that subdirectory may omit them. A user-provided complete checkout can be used, but deep-build neither repairs the installer nor vendors upstream files. Test failures and review findings still require resolution; fallback cannot manufacture PASS or waive user approval and reviewer independence.

The following are from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills):

```bash
npx skills add addyosmani/agent-skills --skill planning-and-task-breakdown
npx skills add addyosmani/agent-skills --skill incremental-implementation
npx skills add addyosmani/agent-skills --skill test-driven-development
npx skills add addyosmani/agent-skills --skill debugging-and-error-recovery
npx skills add addyosmani/agent-skills --skill code-review-and-quality
npx skills add addyosmani/agent-skills --skill security-and-hardening
npx skills add addyosmani/agent-skills --skill performance-optimization
npx skills add addyosmani/agent-skills --skill code-simplification
```

For PostgreSQL query, index, JSONB, or migration-performance work, optionally install [Jeffallan/claude-skills:postgres-pro](https://github.com/Jeffallan/claude-skills):

```bash
npx skills add Jeffallan/claude-skills --skill postgres-pro
```

## Resources and validation

- [Configuration example](config.example.yaml)
- [Review criteria](references/review-criteria.md)
- [Fictional example](examples/input-output.md)
- [Runnable multi-file demo](examples/tenant-export-demo/)
- [Machine-readable evaluations](evals/evals.json)
- [Trigger evaluations](evals/triggers.json)
- [Evaluation cases](evals/cases.md)
- [Rubric](evals/rubric.md)
