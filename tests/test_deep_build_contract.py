#!/usr/bin/env python3
"""Focused offline contract checks for the deep-build workflow."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "deep-build"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
for text in (
    "Plan Review gate",
    "Without recorded PASS, stop at `pending external review`",
    "same-context self-review can improve the Plan but cannot satisfy this gate",
    "Code Review gate",
    "actual diff",
    "assets/build-handoff-template.md",
    "references/review-criteria.md",
):
    require(text in skill, f"SKILL.md must contain: {text}")

criteria = (SKILL / "references" / "review-criteria.md").read_text(encoding="utf-8")
for text in (
    "five-axis review",
    "security-and-hardening",
    "performance-optimization",
    "code-simplification",
    "postgres-pro",
):
    require(text in criteria, f"review criteria must contain: {text}")

dependencies = json.loads((SKILL / "external-dependencies.json").read_text(encoding="utf-8"))
expected_ids = {
    "addyosmani/agent-skills:planning-and-task-breakdown",
    "addyosmani/agent-skills:incremental-implementation",
    "addyosmani/agent-skills:test-driven-development",
    "addyosmani/agent-skills:debugging-and-error-recovery",
    "addyosmani/agent-skills:code-review-and-quality",
    "addyosmani/agent-skills:security-and-hardening",
    "addyosmani/agent-skills:performance-optimization",
    "addyosmani/agent-skills:code-simplification",
    "Jeffallan/claude-skills:postgres-pro",
}
actual_ids = {item["id"] for item in dependencies["dependencies"]}
require(actual_ids == expected_ids, "external dependency IDs must be complete")
for item in dependencies["dependencies"]:
    require(item["install"].startswith("npx skills add "), f"missing install command: {item['id']}")
    require(item["source_url"].startswith("https://github.com/"), f"missing source URL: {item['id']}")
    require(item["fallback"], f"missing fallback: {item['id']}")

evals = json.loads((SKILL / "evals" / "evals.json").read_text(encoding="utf-8"))
require({item["id"] for item in evals["evals"]} == {1, 2, 3, 4, 5}, "expected five deep-build evaluations")
for fixture in ("plan-review-failed.json", "review-routing.json"):
    require((SKILL / "evals" / "fixtures" / fixture).is_file(), f"missing fixture: {fixture}")

print("PASS: deep-build Plan, review, and external dependency contract is complete")
