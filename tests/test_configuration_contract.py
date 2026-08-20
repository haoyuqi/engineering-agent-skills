#!/usr/bin/env python3
"""Validate that public configuration templates stay explicit and auditable."""

from __future__ import annotations

import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
CONTRACT = ROOT / "docs" / "configuration-contract.json"
TOP_LEVEL_KEY = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):", re.MULTILINE)
FORBIDDEN_KEY = re.compile(r"(?i)(?:^|[_-])(token|secret|password|api[_-]?key|credential)(?:$|[_-])")


def template_keys(path: Path) -> list[str]:
    content = path.read_text(encoding="utf-8")
    return TOP_LEVEL_KEY.findall(content)


def main() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert contract["schema_version"] == 1
    semantics = contract["semantics"]
    assert semantics == {
        "delivery": "explicit_user_input",
        "automatic_loading": False,
        "unknown_key_behavior": "report_as_unsupported_and_do_not_assume_effect",
        "secret_policy": "never_store_credentials_or_tokens_in_tracked_configuration",
        "write_authorization": "configuration_never_replaces_exact_user_confirmation",
    }

    contracts = {item["skill_name"]: item for item in contract["skill_contracts"]}
    skill_names = {
        path.name for path in (ROOT / "skills").iterdir() if (path / "SKILL.md").is_file()
    }
    assert set(contracts) == skill_names
    assert len(contracts) == len(contract["skill_contracts"])
    for skill_name, item in contracts.items():
        assert item["configuration_role"] in {"agent_workflow_policy", "agent_policy_only"}
        configured_keys = template_keys(ROOT / "skills" / skill_name / "config.example.yaml")
        assert configured_keys == item["top_level_keys"], skill_name
        assert configured_keys[0] == "schema_version"
        assert all(not FORBIDDEN_KEY.search(key) for key in configured_keys)

    documentation = (ROOT / "docs" / "configuration-contract.md").read_text(encoding="utf-8")
    for required_phrase in ("explicit", "unknown key", "secrets", "confirmation"):
        assert required_phrase in documentation
    for skill_name in skill_names:
        assert "config.example.yaml" in (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
    print(f"PASS: configuration contract accounts for {len(contracts)} Skill template(s)")


if __name__ == "__main__":
    main()
