#!/usr/bin/env python3
"""Structural deep-build contract checks, not a model-behavior evaluation."""

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills/deep-build"


def read(name):
    return (SKILL / name).read_text(encoding="utf-8")


def main():
    config = read("config.example.yaml")
    for key in ("require_written_plan", "require_plan_review_pass",
                "require_user_plan_approval", "require_code_review_pass",
                "require_independent_plan_review", "require_independent_code_review",
                "record_known_model_and_selection_reason"):
        assert re.search(rf"^\s+{key}: true$", config, re.M), key
    for key in ("allow_model_downgrade_for_diversity", "reviewer_writes",
                "allow_git_writes", "allow_external_writes"):
        assert re.search(rf"^\s+{key}: false$", config, re.M), key
    assert re.search(r"unknown_alternative_fallback:\s*same_model_and_effort_separate_context", config)

    # Check ordered workflow sections and reference wiring, not entire prose sentences.
    skill = read("SKILL.md")
    steps = re.findall(r"^\d+\.\s+\*\*([^*]+)\*\*(.*)", skill, re.M)
    assert len(steps) == 6
    plan_step = next(i for i, (title, _) in enumerate(steps) if "Plan Review" in title)
    build_step = next(i for i, (title, _) in enumerate(steps) if "Implement" in title)
    code_step = next(i for i, (title, _) in enumerate(steps) if "Code Review" in title)
    assert plan_step < build_step < code_step
    for index in (plan_step, code_step):
        assert "references/review-criteria.md" in steps[index][1]
    for state in ("pending user plan decision", "pending user plan approval", "pending external review"):
        assert state in skill

    manifest = json.loads(read("external-dependencies.json"))
    integration = manifest["integration"]
    assert integration["preferred_mode"] == "native"
    assert integration["permitted_reading_mode"] == "source-guided"
    assert integration["unavailable_behavior"] == "declared_fallback_then_stop_if_insufficient"
    assert integration["automatic_installation"] is False
    assert integration["caller_exclusive"] is False
    assert integration["path_override"] == "implementation.external_skill_paths"
    assert "external_skill_paths: {}" in config
    assert integration["instructions"] in skill
    assert (SKILL / integration["instructions"]).is_file()
    dependencies = manifest["dependencies"]
    assert len({item["id"] for item in dependencies}) == len(dependencies)
    for item in dependencies:
        assert item["fallback"] and item["when"]
        assert item["id"].split(":", 1)[1] in item["install"]
    criteria = read("references/review-criteria.md")
    for specialist in ("security-and-hardening", "performance-optimization",
                       "code-simplification", "postgres-pro"):
        assert specialist in criteria

    evaluations = json.loads(read("evals/evals.json"))["evals"]
    ids = [item["id"] for item in evaluations]
    assert len(ids) == len(set(ids))
    assert {1, 2, 3, 4, 5, 6, 7}.issubset(ids)  # Existing IDs remain stable.
    for evaluation in evaluations:
        for source in evaluation["files"]:
            assert (SKILL / source).is_file()
        assert len(evaluation["expectations"]) >= 2
    scenarios = json.loads(read("evals/fixtures/review-routing.json"))["reviewer_scenarios"]
    by_id = {item["id"]: item for item in scenarios}
    assert len(by_id) == len(scenarios)
    assert by_id["capable-alternative"]["alternative_suitability"] == "established"
    assert by_id["unknown-lightweight"]["alternative_suitability"] == "unknown"
    assert by_id["self-review-only"]["separate_context_available"] is False
    assert by_id["self-review-only"]["external_or_human_reviewer_available"] is False
    assert by_id["repair-round"]["reviewer_authored_version"] is False
    assert by_id["repair-round"]["version"] != by_id["repair-round"]["next_version"]
    assert by_id["unknown-metadata"]["model"] is None
    # Validate the evaluation inputs, not simulated Agent decisions.
    dependency_cases = json.loads(read("evals/fixtures/review-routing.json"))["dependency_scenarios"]
    cases = {item["id"]: item for item in dependency_cases}
    assert len(cases) == len(dependency_cases) == 8
    assert all(item["dependency"] in {dep["id"] for dep in dependencies} for item in dependency_cases)
    relative = cases["source-relative"]
    assert relative["native_available"] is False and relative["file_reading_permitted"] is True
    assert Path(relative["real_source"]).parent != Path(relative["discovered_link"])
    assert cases["missing-reference"]["resource_exists"] is False
    assert cases["insufficient-fallback"]["performance_acceptance_verified"] is False
    assert cases["incompatible-native"]["commit_authorized"] is False
    assert cases["work-failure"]["loading_result"] == "success"
    assert cases["work-failure"]["test_result"].startswith("FAIL")
    assert cases["no-approval"]["user_plan_approval"] is False
    assert cases["invalid-override"]["directory_exists"] is False
    assert 8 in ids
    print("PASS: deep-build policy, ordered gates, and evaluation fixtures are consistent; model behavior not proved")


if __name__ == "__main__":
    main()
