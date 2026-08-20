#!/usr/bin/env python3
"""Validate portable, evidence-linked contracts for every machine evaluation."""

from __future__ import annotations

import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
EXPECTATION_TYPES = {"observable-output"}


def main() -> None:
    result_schema = json.loads((ROOT / "evals" / "result.schema.json").read_text(encoding="utf-8"))
    assert result_schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert result_schema["properties"]["run"]["properties"]["mode"]["enum"] == [
        "with_skill",
        "baseline",
    ]

    expected_ids: set[str] = set()
    evaluation_count = 0
    for eval_path in sorted((ROOT / "skills").glob("*/evals/evals.json")):
        document = json.loads(eval_path.read_text(encoding="utf-8"))
        skill_name = document["skill_name"]
        for evaluation in document["evals"]:
            evaluation_count += 1
            files = evaluation["files"]
            assert files
            for position, expectation in enumerate(evaluation["expectations"], start=1):
                assert set(expectation) == {
                    "id",
                    "type",
                    "assertion",
                    "evidence_sources",
                }
                expected_id = f"{skill_name}-{evaluation['id']:02d}-{position:02d}"
                assert expectation["id"] == expected_id
                assert expectation["id"] not in expected_ids
                expected_ids.add(expectation["id"])
                assert expectation["type"] in EXPECTATION_TYPES
                assert isinstance(expectation["assertion"], str) and expectation["assertion"].strip()
                assert expectation["evidence_sources"] == files
                assert all(
                    isinstance(path, str)
                    and not Path(path).is_absolute()
                    and ".." not in Path(path).parts
                    for path in expectation["evidence_sources"]
                )

    assert evaluation_count >= 3
    assert re.fullmatch(r"[a-z0-9-]+-\d{2}-\d{2}", next(iter(expected_ids)))
    print(
        "PASS: validated "
        f"{len(expected_ids)} stable, evidence-linked evaluation expectations"
    )


if __name__ == "__main__":
    main()
