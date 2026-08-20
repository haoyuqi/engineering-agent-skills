# Repository guidance for coding agents

This repository contains independently installable Agent Skills. Preserve that independence: a Skill may declare an external dependency, but it must not silently depend on another Skill in this repository.

Before editing, read [docs/skill-quality-standard.md](docs/skill-quality-standard.md). Keep the main `SKILL.md` focused on the path every run needs; move branch-specific reference material and long output templates into one-level-deep `references/` or `assets/` files with an explicit condition for loading them.

Every change must preserve the default read-only boundary. A state-changing operation must show its exact target and effect, receive user confirmation, and be verified afterward. Never add real organization names, private endpoints, employee or customer data, production logs, credentials, or workstation paths.

Run these checks before claiming completion:

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

When npm access is available, also run `python3 tests/test_installer_compatibility.py` and `npx --yes skills@1.5.20 add . --list`.

Do not stage, commit, push, publish, or open a PR/MR unless the user explicitly requests that separate delivery action.
