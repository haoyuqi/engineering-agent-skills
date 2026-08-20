#!/usr/bin/env python3
"""Reject mutable third-party GitHub Action references in checked-in workflows."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS = ROOT / ".github" / "workflows"
USES_REFERENCE = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)", re.MULTILINE)
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")


def main() -> None:
    workflow_files = sorted((*WORKFLOWS.glob("*.yml"), *WORKFLOWS.glob("*.yaml")))
    assert workflow_files, "expected at least one GitHub Actions workflow"
    references: list[str] = []
    for workflow in workflow_files:
        for reference in USES_REFERENCE.findall(workflow.read_text(encoding="utf-8")):
            if reference.startswith(("./", "docker://")):
                continue
            owner_repository, separator, revision = reference.partition("@")
            assert separator and "/" in owner_repository, (
                f"invalid action reference in {workflow.relative_to(ROOT)}: {reference}"
            )
            assert FULL_SHA.fullmatch(revision), (
                f"third-party action must use a full immutable SHA in "
                f"{workflow.relative_to(ROOT)}: {reference}"
            )
            references.append(reference)
    assert references, "expected at least one third-party action reference"
    print(f"PASS: validated {len(references)} immutable GitHub Action pin(s)")


if __name__ == "__main__":
    main()
