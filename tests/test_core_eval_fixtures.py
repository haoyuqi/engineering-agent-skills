#!/usr/bin/env python3
"""Validate deterministic fixture contracts for high-risk workflow Skills."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CORE_FIXTURES = {
    "pr-mr-review": {
        "github-requirement-gap.json": ("pull_request", "acceptance_criteria", "changed_files"),
        "gitlab-middleware.json": ("merge_request", "acceptance_criteria", "surrounding_evidence"),
        "missing-requirements.json": ("pull_request", "requirements_fetch", "changed_files"),
    },
    "git-change-delivery": {
        "mixed-worktree.json": ("branch", "remote", "changes"),
        "failing-hook.json": ("branch", "staged_paths", "hook"),
        "high-risk-delivery.json": ("branch", "requested_operation", "available_labels"),
        "authorization-scenarios.json": ("repository", "scenarios"),
    },
    "requirements-clarification": {
        "combined-mode.json": ("request", "available_skills", "brainstorming_result"),
        "missing-grilling.json": ("request", "available_skills", "missing_skills"),
        "save-boundary.json": ("request", "draft_status", "requested_git_operation"),
    },
    "deep-build": {
        "approved-change.json": ("requirements", "repository_map", "constraints"),
        "destructive-migration.json": ("requirement", "migration", "confirmation"),
        "build-handoff.json": ("requirements", "verification", "worktree"),
        "plan-review-failed.json": ("plan", "implementation_started"),
        "plan-review-awaiting-user-approval.json": ("plan", "user_plan_approval", "implementation_started"),
        "review-routing.json": ("diff_signals", "plan_review", "code_review"),
    },
}


def main() -> None:
    fixture_backed_skills = []
    for skill_directory in sorted((ROOT / "skills").iterdir()):
        evals_path = skill_directory / "evals" / "evals.json"
        if not evals_path.is_file():
            continue
        evals = json.loads(evals_path.read_text(encoding="utf-8"))
        assert evals.get("fixture_backed") is True
        fixture_backed_skills.append(skill_directory.name)
        for evaluation in evals["evals"]:
            assert evaluation["files"]
            for relative_path in evaluation["files"]:
                fixture = skill_directory / relative_path
                assert fixture.is_file()
                if fixture.suffix == ".json":
                    document = json.loads(fixture.read_text(encoding="utf-8"))
                    assert "fictional" in document.get("fixture_notice", "").lower()

    assert set(fixture_backed_skills) == {path.name for path in (ROOT / "skills").iterdir() if (path / "SKILL.md").is_file()}

    for skill_name, fixtures in CORE_FIXTURES.items():
        evals = json.loads(
            (ROOT / "skills" / skill_name / "evals" / "evals.json").read_text(
                encoding="utf-8"
            )
        )
        assert evals["fixture_backed"] is True
        referenced = {path for item in evals["evals"] for path in item["files"]}
        expected = {f"evals/fixtures/{name}" for name in fixtures}
        assert referenced == expected
        for fixture_name, required_keys in fixtures.items():
            path = ROOT / "skills" / skill_name / "evals" / "fixtures" / fixture_name
            document = json.loads(path.read_text(encoding="utf-8"))
            assert "fictional" in document["fixture_notice"].lower()
            assert all(key in document for key in required_keys)

    validate_delivery_authorization_contract()
    print("PASS: all Skill evaluations have complete fictional fixture contracts")


def validate_delivery_authorization_contract() -> None:
    """Check policy/fixture wiring only; no claim about actual agent behavior."""
    directory = ROOT / "skills" / "git-change-delivery"
    fixture = json.loads((directory / "evals/fixtures/authorization-scenarios.json").read_text())
    scenarios = {item["id"]: item for item in fixture["scenarios"]}
    assert len(scenarios) == len(fixture["scenarios"])
    assert set(scenarios) == {
        "full-sequence", "commit-only", "stepwise", "target-change",
        "ambiguous", "proposal-only", "published-branch", "scope-drift",
    }
    evaluations = json.loads((directory / "evals/evals.json").read_text())["evals"]
    scenario_evals = [item for item in evaluations if
                      "evals/fixtures/authorization-scenarios.json" in item["files"]]
    for scenario in scenarios:
        assert sum(f"the {scenario} scenario" in item["prompt"] for item in scenario_evals) == 1
    assert scenarios["full-sequence"]["index"] == "empty"
    assert not set(scenarios["full-sequence"]["intended_paths"]) & set(scenarios["full-sequence"]["unrelated_paths"])
    assert scenarios["target-change"]["proposed_target"] != fixture["repository"]["target"]
    assert scenarios["ambiguous"]["prior_authorization"] is None
    assert scenarios["published-branch"]["remote_head_matches_local"] is True
    hook = json.loads((directory / "evals/fixtures/failing-hook.json").read_text())
    assert hook["user_bypass_authorization"] is False
    config = (directory / "config.example.yaml").read_text()
    for setting in ("authorization_mode: explicit_scope",
                    "repeat_confirmation_for_unchanged_scope: false",
                    "honor_step_by_step_requests: true",
                    "confirm_scope_or_target_changes: true",
                    "require_specific_high_risk_approval: true",
                    "preserve_unrelated_staged_changes: true"):
        assert setting in config
    for old_key in ("confirm_stage:", "confirm_commit:", "confirm_push:", "confirm_change_request:"):
        assert old_key not in config


if __name__ == "__main__":
    main()
