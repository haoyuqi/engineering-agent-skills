# Repository evaluation suite

This directory covers behavior that cannot be proven by file layout alone.

- Each `skills/<name>/evals/triggers.json` contains at least 20 positive and near-neighbor negative cases that travel with that independently installed Skill.
- Each `skills/<name>/evals/evals.json` tests successful execution, missing evidence or tool failure, and safety pressure.
- Each `skills/<name>/evals/cases.md` and `rubric.md` provides a human-readable review path.

Each expectation is an evidence-linked object with a stable ID, rather than an
unaddressable text bullet. Use the ID when grading the response against the
same fixture input. Published output artifacts are bound to their result record
with a SHA-256 digest, so a later artifact edit invalidates the record.

The offline checks validate schemas and coverage. They do not claim that a model passed a behavioral evaluation. For model testing, run the cases in fresh contexts, record the runtime and model, compare the Skill-enabled result with a baseline, and grade only observable output. Store each run using the [result format](../docs/evaluation-result-format.md). See [Evaluation guide](../docs/evaluation.md).

Validate a sanitized result without third-party Python packages:

```bash
python3 evals/validate_result.py --result path/to/result.json
```
