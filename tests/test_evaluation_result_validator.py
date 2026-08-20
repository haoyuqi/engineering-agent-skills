#!/usr/bin/env python3
"""Behavior tests for the dependency-free evaluation result validator."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent.parent
VALIDATOR = ROOT / "evals" / "validate_result.py"
SKILL = ROOT / "skills" / "pr-mr-review"
CONTRACT = json.loads(
    (SKILL / "evals" / "evals.json").read_text(encoding="utf-8")
)


def fixture_digest(files: list[str]) -> str:
    digest = hashlib.sha256()
    for relative_path in sorted(files):
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update((SKILL / relative_path).read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def result_for_first_case() -> dict:
    expectations = CONTRACT["evals"][0]["expectations"]
    return {
        "schema_version": 1,
        "skill_name": "pr-mr-review",
        "run": {
            "mode": "with_skill",
            "runtime": "fictional-agent-runtime",
            "model": "fictional-model-version",
            "input_revision": "fictional-fixture-set",
            "skill_instruction_sha256": hashlib.sha256(
                (SKILL / "SKILL.md").read_bytes()
            ).hexdigest(),
            "recorded_on": "2026-08-13",
            "run_count": 1,
            "baseline_definition": "Same model and fixture input without the Skill instruction.",
            "variance": "not_applicable_single_run",
            "limitations": ["Fictional fixture only; no provider integration."],
        },
        "cases": [
            {
                "eval_id": 1,
                "input_sha256": fixture_digest(CONTRACT["evals"][0]["files"]),
                "output_reference": "outputs/eval-01.md",
                "output_sha256": hashlib.sha256(b"fictional sanitized output\n").hexdigest(),
                "writes_attempted": False,
                "assertions": [
                    {
                        "id": item["id"],
                        "status": "passed",
                        "evidence": "Fictional sanitized response reference.",
                    }
                    for item in expectations
                ],
            }
        ],
    }


def run_result(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--result", str(path)],
        check=False,
        capture_output=True,
        text=True,
    )


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="skill-evaluation-result-") as temp:
        path = Path(temp) / "result.json"
        (Path(temp) / "outputs").mkdir()
        (Path(temp) / "outputs" / "eval-01.md").write_text(
            "fictional sanitized output\n", encoding="utf-8"
        )
        path.write_text(json.dumps(result_for_first_case()), encoding="utf-8")
        valid = run_result(path)
        assert valid.returncode == 0, valid.stderr

        invalid = result_for_first_case()
        invalid["cases"][0]["assertions"][0]["id"] = "not-a-contract-id"
        path.write_text(json.dumps(invalid), encoding="utf-8")
        rejected = run_result(path)
        assert rejected.returncode == 2
        assert "belong to the evaluated case" in rejected.stderr

        unsafe = result_for_first_case()
        unsafe["cases"][0]["output_reference"] = "../outside.md"
        path.write_text(json.dumps(unsafe), encoding="utf-8")
        rejected = run_result(path)
        assert rejected.returncode == 2
        assert "safe relative path" in rejected.stderr

        missing = result_for_first_case()
        missing["cases"][0]["output_reference"] = "outputs/missing.md"
        path.write_text(json.dumps(missing), encoding="utf-8")
        rejected = run_result(path)
        assert rejected.returncode == 2
        assert "must exist next to the result record" in rejected.stderr

        stale = result_for_first_case()
        stale["cases"][0]["output_sha256"] = "0" * 64
        path.write_text(json.dumps(stale), encoding="utf-8")
        rejected = run_result(path)
        assert rejected.returncode == 2
        assert "does not match the output artifact" in rejected.stderr

        stale = result_for_first_case()
        stale["cases"][0]["input_sha256"] = "0" * 64
        path.write_text(json.dumps(stale), encoding="utf-8")
        rejected = run_result(path)
        assert rejected.returncode == 2
        assert "does not match the evaluation fixtures" in rejected.stderr

        incomplete = result_for_first_case()
        del incomplete["run"]["limitations"]
        path.write_text(json.dumps(incomplete), encoding="utf-8")
        rejected = run_result(path)
        assert rejected.returncode == 2
        assert "run.limitations" in rejected.stderr

        invalid_variance = result_for_first_case()
        invalid_variance["run"]["variance"] = "reported_separately"
        path.write_text(json.dumps(invalid_variance), encoding="utf-8")
        rejected = run_result(path)
        assert rejected.returncode == 2
        assert "variance not applicable" in rejected.stderr

    print("PASS: evaluation result validator rejects mismatched or unsafe evidence")


if __name__ == "__main__":
    main()
