#!/usr/bin/env python3
"""Validate a model-evaluation result against a Skill's checked-in contract."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
VALID_MODES = {"with_skill", "baseline"}
VALID_STATUSES = {"passed", "failed", "not_applicable"}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(2)


def read_object(path: Path) -> dict[str, Any]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot read JSON object: {error}")
    if not isinstance(document, dict):
        fail("result must be a JSON object")
    return document


def safe_reference(value: object) -> bool:
    return isinstance(value, str) and value.strip() and not Path(value).is_absolute() and ".." not in Path(value).parts


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_sha256(skill_directory: Path, files: list[str]) -> str:
    """Hash the exact, ordered fixture set without requiring a Git revision."""
    digest = hashlib.sha256()
    for relative_path in sorted(files):
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update((skill_directory / relative_path).read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def validate(result: dict[str, Any], root: Path, result_path: Path) -> str:
    if result.get("schema_version") != 1:
        fail("schema_version must be 1")
    skill_name = result.get("skill_name")
    if not isinstance(skill_name, str):
        fail("skill_name must be a string")
    contract_path = root / "skills" / skill_name / "evals" / "evals.json"
    skill_directory = contract_path.parent.parent
    contract = read_object(contract_path)
    if contract.get("skill_name") != skill_name:
        fail("skill contract does not match result skill_name")

    run = result.get("run")
    if not isinstance(run, dict):
        fail("run must be an object")
    if run.get("mode") not in VALID_MODES:
        fail("run.mode must be with_skill or baseline")
    for field in ("runtime", "model", "input_revision", "baseline_definition"):
        if not isinstance(run.get(field), str) or not run[field].strip():
            fail(f"run.{field} must be a non-empty string")
    if not isinstance(run.get("recorded_on"), str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}", run["recorded_on"]
    ):
        fail("run.recorded_on must use YYYY-MM-DD")
    if not isinstance(run.get("run_count"), int) or run["run_count"] < 1:
        fail("run.run_count must be a positive integer")
    if run.get("variance") not in {"not_applicable_single_run", "reported_separately"}:
        fail("run.variance must declare a supported reporting mode")
    if run["run_count"] == 1 and run["variance"] != "not_applicable_single_run":
        fail("a one-run result must declare variance not applicable")
    limitations = run.get("limitations")
    if not isinstance(limitations, list) or not limitations or not all(
        isinstance(item, str) and item.strip() for item in limitations
    ):
        fail("run.limitations must contain at least one non-empty limitation")
    instruction_digest = run.get("skill_instruction_sha256")
    if not isinstance(instruction_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", instruction_digest):
        fail("run.skill_instruction_sha256 must be a lowercase SHA-256 digest")
    if instruction_digest != sha256_file(skill_directory / "SKILL.md"):
        fail("run.skill_instruction_sha256 does not match SKILL.md")

    expected = {item["id"]: item for item in contract["evals"]}
    cases = result.get("cases")
    if not isinstance(cases, list) or not cases:
        fail("cases must be a non-empty list")
    seen_evaluations: set[int] = set()
    for case in cases:
        if not isinstance(case, dict):
            fail("every case must be an object")
        eval_id = case.get("eval_id")
        if not isinstance(eval_id, int) or eval_id not in expected or eval_id in seen_evaluations:
            fail("case eval_id must be a unique evaluation from the Skill contract")
        seen_evaluations.add(eval_id)
        fixture_digest = case.get("input_sha256")
        if not isinstance(fixture_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", fixture_digest):
            fail("case input_sha256 must be a lowercase SHA-256 digest")
        if fixture_digest != input_sha256(skill_directory, expected[eval_id]["files"]):
            fail("case input_sha256 does not match the evaluation fixtures")
        if not safe_reference(case.get("output_reference")):
            fail("case output_reference must be a safe relative path")
        output_path = result_path.parent / case["output_reference"]
        if not output_path.is_file():
            fail("case output_reference must exist next to the result record")
        output_sha256 = case.get("output_sha256")
        if not isinstance(output_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", output_sha256):
            fail("case output_sha256 must be a lowercase SHA-256 digest")
        if output_sha256 != sha256_file(output_path):
            fail("case output_sha256 does not match the output artifact")
        if not isinstance(case.get("writes_attempted"), bool):
            fail("case writes_attempted must be boolean")
        assertions = case.get("assertions")
        if not isinstance(assertions, list):
            fail("case assertions must be a list")
        expected_ids = {item["id"] for item in expected[eval_id]["expectations"]}
        observed_ids = set()
        for assertion in assertions:
            if not isinstance(assertion, dict):
                fail("every assertion result must be an object")
            assertion_id = assertion.get("id")
            if assertion_id not in expected_ids or assertion_id in observed_ids:
                fail("assertion IDs must be unique and belong to the evaluated case")
            observed_ids.add(assertion_id)
            if assertion.get("status") not in VALID_STATUSES:
                fail("assertion status is invalid")
            if not isinstance(assertion.get("evidence"), str) or not assertion["evidence"].strip():
                fail("assertion evidence must be a non-empty string")
        if observed_ids != expected_ids:
            fail("every contracted assertion must have one result")
    return skill_name


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result", required=True, help="Sanitized evaluation-result JSON")
    parser.add_argument("--catalog-root", default=str(ROOT), help="Repository root containing skills/")
    args = parser.parse_args()
    result_path = Path(args.result)
    skill_name = validate(read_object(result_path), Path(args.catalog_root), result_path)
    print(f"PASS: evaluation result matches {skill_name} contract")


if __name__ == "__main__":
    main()
