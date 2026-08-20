# Deep Build

`deep-build` implements a substantial approved change only after a written Plan passes independent review. Its portable contract is:

```text
Plan document → Plan Review PASS → incremental implementation → Code Review PASS → user acceptance
```

It is host-neutral. An OpenCode/OMO workflow can use separate agents and models; another host can use an external Agent or human reviewer. A same-context self-review never satisfies the Plan Review gate. Git delivery, deployment, and remote PR/MR review are outside this skill.

```text
Use deep-build to implement the approved tenant-scoped export feature across the API and worker.
```

## Recommended external skills

The workflow remains usable without these skills because its mandatory gates and concise fallback criteria are included locally. Installing them provides their deeper specialist guidance. Each dependency, trigger, source URL, and fallback is also declared in [external-dependencies.json](external-dependencies.json).

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
