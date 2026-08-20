# Contributing

Read [docs/skill-quality-standard.md](docs/skill-quality-standard.md) before proposing a change. Each Skill must be independently installable and include `SKILL.md`, a standalone README, `config.example.yaml`, a fictional input/output example, machine-readable `evals/evals.json`, adversarial cases, a rubric, runtime-optional Agent UI metadata, provider fallback behavior, and a read-only safety boundary.

When changing a trigger description or workflow, follow [docs/evaluation.md](docs/evaluation.md). Add or update the nearest-neighbor cases in that Skill's `evals/triggers.json`, and do not describe a model behavior as tested unless the result records its runtime, model, case revision, baseline, and repeated runs.

Start from a realistic task and add evaluation coverage for success, missing information or tool failure, and safety pressure. Keep the main workflow lean; move branch-specific reference and long templates behind explicit one-level pointers.

For a new Skill, start with [`template/`](template/). Update the
configuration contract in addition to the Skill directory; do not add
Agent-specific copies unless the compatibility contract and its packaging test
are intentionally expanded.

Before proposing a Skill, run:

```bash
python3 tests/test_repository_structure.py
python3 tests/test_workflow_supply_chain.py
python3 tests/test_compatibility_contract.py
python3 tests/test_configuration_contract.py
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
git diff --check
```

When npm access is available, also run `python3 tests/test_installer_compatibility.py` and `npx --yes skills@1.5.20 add . --list`. CI runs both checks to protect independently selectable, cross-Agent installation.

Do not add credentials, internal URLs, employee information, customer data, proprietary source code, or production logs. External write workflows must show the exact target/action, require confirmation, and verify resulting state.
