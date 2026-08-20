#!/usr/bin/env python3
"""Ensure the public new-Skill template demonstrates current quality gates."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "template"


def main() -> None:
    skill = (TEMPLATE / "SKILL.template.md").read_text(encoding="utf-8")
    readme = (TEMPLATE / "README.md").read_text(encoding="utf-8")
    assert "config.example.yaml" in skill
    assert "unknown settings" in skill
    assert "external-dependencies.json" in readme
    for contract in (
        "docs/configuration-contract.json",
        "evals/evaluation-status.json",
        "docs/compatibility.json",
    ):
        assert contract in readme

    fixture = TEMPLATE / "evals" / "fixtures" / "scenario.json"
    fixture_document = json.loads(fixture.read_text(encoding="utf-8"))
    assert "fictional" in fixture_document["fixture_notice"].lower()

    evals = json.loads((TEMPLATE / "evals" / "evals.json").read_text(encoding="utf-8"))
    assert evals["skill_name"] == "replace-me"
    assert evals["fixture_backed"] is True
    for evaluation in evals["evals"]:
        assert evaluation["files"] == ["evals/fixtures/scenario.json"]
        for position, expectation in enumerate(evaluation["expectations"], start=1):
            assert expectation["id"] == f"replace-me-{evaluation['id']:02d}-{position:02d}"
            assert expectation["type"] == "observable-output"
            assert expectation["evidence_sources"] == evaluation["files"]
            assert expectation["assertion"]

    print("PASS: new-Skill template demonstrates fixture-backed evaluation contracts")


if __name__ == "__main__":
    main()
