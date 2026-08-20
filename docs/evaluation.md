# Evaluation guide

The repository separates three questions: is a Skill valid, does it trigger for the right request, and does it produce a safe, useful result?

## 1. Offline validation

Run the checks that require no model or external service:

```bash
python3 tests/test_repository_structure.py
python3 tests/test_public_content.py
python3 tests/test_public_content_coverage.py
python3 tests/test_public_content.py --history
python3 tests/test_repository_vulnerability_discovery.py
python3 tests/test_repository_vulnerability_normalization.py
python3 tests/test_repository_vulnerability_audit_runner.py
python3 tests/test_core_eval_fixtures.py
python3 tests/test_evaluation_contract.py
python3 tests/test_evaluation_result_validator.py
python3 tests/test_external_dependency_contract.py
python3 tests/test_template_quality.py
```

These checks validate portable metadata, required resources, evaluation schemas, links, context budgets, fictional examples, and generic privacy patterns. The vulnerability runner test additionally proves origin-level registry gating, lockfile-proven workspace coverage, isolated package-manager configuration, parseable non-zero audit handling, and malformed-output recovery without contacting a registry. They do not prove model behavior.

Every Skill declares `fixture_backed: true`. Their portable JSON fixtures supply pinned provider/repository/dependency states, and `test_core_eval_fixtures.py` verifies that every machine evaluation references a complete fictional fixture contract. The high-risk workflow fixtures additionally validate the key state fields needed for their safety boundaries. These fixtures make model runs repeatable; they are not a claim that a model has passed them.

`python3 tests/test_installer_compatibility.py` is a separate networked packaging check. It uses a pinned installer version and disposable directories to verify that Codex/OpenCode/GitHub Copilot's shared layout and Claude Code's distinct layout receive byte-identical complete resources for every Skill.

`python3 tests/test_external_dependency_contract.py` checks the explicit upstream integration contract and its source locks. `python3 tests/test_template_quality.py` prevents new Skills from starting with an obsolete evaluation format. Publish model-run comparisons only after rerunning them against the committed Skill version and validating their paired records with `evals/validate_result.py`.

## 2. Trigger evaluation

Use each independently installed Skill's `evals/triggers.json` in a fresh runtime context. Every file includes at least 20 intended and near-neighbor requests, with at least eight positive and eight negative cases. Cases include multilingual, informal, degraded-evidence, and safety-pressure requests where relevant.

For every supported Agent runtime:

1. Install the repository without manually invoking a Skill.
2. Run every prompt in a clean context at least three times.
3. Record the runtime, model, model version, Skill selected, and run timestamp.
4. Score positive recall and negative precision separately.
5. Review any unstable or neighbor-confusion cases before changing a description.

## 3. Workflow evaluation

Each `skills/<name>/evals/evals.json` contains realistic success, degraded-evidence, and safety-pressure cases. Run each case both with the Skill and against a baseline without it, using the same model and inputs.

Grade only observable behavior against the stable, evidence-linked `expectations`. Save the output, duration, token usage when available, passed expectations, and reviewer notes using the [evaluation result format](evaluation-result-format.md). Do not count a persuasive explanation as proof that a command, provider query, or verification actually ran.

Mutation cases must use a disposable fixture or mocked provider. A passing result performs no write before the case supplies explicit confirmation. Tool failure cases must name missing evidence and narrow the conclusion instead of inventing a result.

## 4. Reporting

Publish a result only when it identifies:

- repository revision, or (for an uncommitted evaluation workspace) verified Skill-instruction and fixture SHA-256 hashes;
- runtime and model revision;
- case set revision;
- number of runs;
- baseline definition;
- pass rate and repeated-run variance;
- known limitations and untested integrations.

Model-backed runs can consume paid API or local compute resources, so they are intentionally not part of the default CI workflow.
