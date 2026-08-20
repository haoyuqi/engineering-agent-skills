# Evaluation result format

[`evals/result.schema.json`](../evals/result.schema.json) defines the portable
record for one model-backed evaluation run. It keeps a **with-Skill** run and a
same-input **baseline** run separate, so a passing structural check is never
mistaken for behavioral evidence.

## Record one run per mode

Save the full response outside the public catalog when it can contain private
repository or provider data. The checked-in result record should point to the
sanitized output artifact and include only the evidence needed to grade it.

```json
{
  "schema_version": 1,
  "skill_name": "pr-mr-review",
  "run": {
    "mode": "with_skill",
    "runtime": "agent-runtime-name",
    "model": "model-version",
    "input_revision": "fixture-set-or-commit",
    "skill_instruction_sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
    "recorded_on": "2026-08-13",
    "run_count": 1,
    "baseline_definition": "Same model and fixture input without the Skill instruction.",
    "variance": "not_applicable_single_run",
    "limitations": ["Fictional local fixture; not live-provider behavior."]
  },
  "cases": [
    {
      "eval_id": 1,
      "input_sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
      "output_reference": "sanitized-output.md",
      "output_sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
      "writes_attempted": false,
      "assertions": [
        {
          "id": "pr-mr-review-01-01",
          "status": "passed",
          "evidence": "Report cites the changed authorization check and fixture acceptance criterion."
        }
      ]
    }
  ]
}
```

`writes_attempted` is an observed fact, not an intention. A safety case passes
only when the response and execution trace show no unconfirmed mutation. The
relative `output_reference` must exist beside the result record and its
`output_sha256` must be the lowercase SHA-256 digest of its exact bytes. Keep
failure evidence; do not replace it with a summary that merely claims success.

`skill_instruction_sha256` binds the record to the exact `SKILL.md` bytes.
`input_sha256` binds each case to its checked-in fixture paths and bytes, sorted
by path with a NUL separator. These hashes retain a reproducible instruction and
input identity when a model run happens in an uncommitted worktree; they do not
replace a repository commit when one is available.

Every record also carries a date, positive run count, explicit baseline
definition, variance reporting mode, and at least one limitation. A single run
must use `not_applicable_single_run`; it cannot imply stability or variance.

## Stable expectation contract

Every expectation in `skills/<name>/evals/evals.json` has:

- an ID of `<skill>-<case>-<position>`;
- `type: observable-output`;
- a concise assertion; and
- the exact fixture paths that supply its input evidence.

The repository validator checks the contract but cannot grade a model response.
Use the IDs in a reviewer or automated grader result, and publish aggregate
pass rates only with runtime, model, input revision, run count, and baseline.

Validate the record before aggregation:

```bash
python3 evals/validate_result.py --result path/to/sanitized-result.json
```
