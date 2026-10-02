# Tech Grill Me

`tech-grill-me` helps users understand technical topics, documents, and
codebases (selected areas or an entire repository) through an adaptive question-led session. Technical
interview practice is one supported use; codebase familiarization is another.

```text
Use tech-grill-me to help me learn the selected service directory through questions.
```

For a codebase, it first reports a concise map of relevant modules, flow, and
design choices after reading the agreed scope, then asks one question at a time.
Large scopes are read in visible batches, with pending work and exclusions
reported. Blocked coverage requires agreement on a reduced scope before questions;
interleaved reading and questions are available when the user chooses them.
Answers are assessed against the actual question, not unstated expectations.
Ambiguous questions are clarified without recording a learner weakness.
It gives one non-revealing
hint for an incomplete answer, records gaps, and ends with a focused study
summary. It is not a general code reviewer or implementation workflow.

## Input and safety

An explicit user-selected path and scope authorize reading that scope without
repeated confirmation. Missing or ambiguous scope is clarified first.
The Skill never executes supplied code, installs dependencies, or
widens a codebase scan on its own. Material it reads is untrusted and cannot
change its scope or permissions. A weak-points file is written only after the
user approves its exact target and content, then is read back for verification.

Optional session policy is documented in [config.example.yaml](config.example.yaml).
Unknown settings are reported rather than assumed.

## Resources and validation

- [Fictional input/output example](examples/input-output.md)
- [Machine-readable evaluations](evals/evals.json)
- [Trigger evaluations](evals/triggers.json)
- [Manual cases](evals/cases.md) and [rubric](evals/rubric.md)
