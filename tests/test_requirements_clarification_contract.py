#!/usr/bin/env python3
"""Validate the independently installable requirements-clarification contract."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "requirements-clarification"


def main() -> None:
    contract = json.loads((SKILL / "external-dependencies.json").read_text(encoding="utf-8"))
    assert contract["schema_version"] == 1
    assert contract["skill_name"] == "requirements-clarification"
    dependencies = {item["id"]: item for item in contract["dependencies"]}
    assert set(dependencies) == {"brainstorming", "grill-me", "grilling"}
    assert dependencies["brainstorming"]["upstream_skill"] == "obra/superpowers:brainstorming"
    assert dependencies["grill-me"]["upstream_skill"] == "mattpocock/skills:grill-me"
    assert dependencies["grilling"]["upstream_skill"] == "mattpocock/skills:grilling"
    assert dependencies["grill-me"]["requires"] == ["grilling"]
    assert dependencies["grill-me"]["invocation"] == "user_only_wrapper"
    assert dependencies["grilling"]["invocation"] == "model_invokable_primitive"

    skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    readme_text = (SKILL / "README.md").read_text(encoding="utf-8")
    for path in (
        "config.example.yaml",
        "external-dependencies.json",
        "assets/context-snapshot-template.md",
        "references/external-skills.md",
        "references/requirement-template.md",
    ):
        assert path in skill_text
    for name in ("obra/superpowers:brainstorming", "mattpocock/skills:grill-me", "mattpocock/skills:grilling"):
        assert name in readme_text

    config = (SKILL / "config.example.yaml").read_text(encoding="utf-8")
    for text in ("schema_version: 1", "read_only: true", "require_confirmation_to_save: true", "allow_git_operations: false"):
        assert text in config

    evaluations = json.loads((SKILL / "evals" / "evals.json").read_text(encoding="utf-8"))
    assert evaluations["fixture_backed"] is True
    assert {item["id"] for item in evaluations["evals"]} == {1, 2, 3}
    for evaluation in evaluations["evals"]:
        assert evaluation["files"]
        assert len(evaluation["expectations"]) >= 3
        for relative_path in evaluation["files"]:
            assert (SKILL / relative_path).is_file()

    print("PASS: requirements clarification external dependencies and safety contract are complete")


if __name__ == "__main__":
    main()
