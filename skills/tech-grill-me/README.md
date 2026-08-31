# Tech Grill Me

`tech-grill-me` runs an adaptive technical interview practice session. It can
use a topic, a readable technical document, a selected codebase area, or a
previous weak-points record.

```text
Use tech-grill-me to quiz me on database transaction isolation.
```

It asks one question at a time, gives one non-revealing hint for an incomplete
answer, records gaps during the session, and ends with a focused study summary.
It is an interviewer, not a general tutor, code reviewer, or implementation
workflow.

## Input and safety

Paths are read only after the user confirms the exact document or codebase area
to inspect. The Skill never executes supplied code, installs dependencies, or
widens a codebase scan on its own. A weak-points file is written only after the
user approves its exact target and content.

Optional session policy is documented in [config.example.yaml](config.example.yaml).
Unknown settings are reported rather than assumed.

## Resources and validation

- [Fictional input/output example](examples/input-output.md)
- [Machine-readable evaluations](evals/evals.json)
- [Trigger evaluations](evals/triggers.json)
- [Manual cases](evals/cases.md) and [rubric](evals/rubric.md)
