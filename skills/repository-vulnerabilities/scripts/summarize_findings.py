#!/usr/bin/env python3
"""Summarize normalized audit evidence without network or package-manager access."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


def load_result(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_bytes()
    try:
        parsed = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("audit result must be valid UTF-8 JSON") from error
    if not isinstance(parsed, dict):
        raise ValueError("audit result must be a JSON object")
    return parsed, hashlib.sha256(raw).hexdigest()


def is_propagation_marker(finding: dict[str, Any]) -> bool:
    identifiers = finding.get("identifiers")
    via = finding.get("via_dependencies")
    return identifiers == [] and isinstance(via, list) and bool(via)


def summarize(result: dict[str, Any], digest: str) -> dict[str, Any]:
    if result.get("read_only") is not True:
        raise ValueError("audit result does not declare read_only: true")
    audits = result.get("audits")
    counts = result.get("counts")
    if not isinstance(audits, list) or not isinstance(counts, dict):
        raise ValueError("audit result is missing audits or counts")

    advisory_records = 0
    propagation_markers = 0
    package_version_occurrences = 0
    by_ecosystem: dict[str, dict[str, int]] = {}
    for audit in audits:
        if not isinstance(audit, dict) or audit.get("status") != "completed":
            continue
        normalized = audit.get("normalized")
        if not isinstance(normalized, dict):
            raise ValueError("completed audit is missing normalized evidence")
        ecosystem = str(audit.get("ecosystem", "unknown"))
        bucket = by_ecosystem.setdefault(
            ecosystem,
            {"scanner_advisory_records": 0, "affected_package_version_occurrences": 0, "propagation_only_markers": 0},
        )
        findings = normalized.get("findings")
        if not isinstance(findings, list):
            raise ValueError("normalized findings must be a list")
        for finding in findings:
            if not isinstance(finding, dict):
                raise ValueError("normalized finding must be an object")
            if is_propagation_marker(finding):
                propagation_markers += 1
                bucket["propagation_only_markers"] += 1
                continue
            identifiers = finding.get("identifiers")
            if not isinstance(identifiers, list) or not identifiers:
                raise ValueError("finding without an identifier is not a valid propagation marker")
            installed = finding.get("installed_versions")
            if not isinstance(installed, list):
                raise ValueError("finding installed_versions must be a list")
            advisory_records += 1
            occurrences = len(installed)
            package_version_occurrences += occurrences
            bucket["scanner_advisory_records"] += 1
            bucket["affected_package_version_occurrences"] += occurrences

    if counts.get("normalized_findings") != advisory_records + propagation_markers:
        raise ValueError("normalized_findings does not reconcile with normalized evidence")
    return {
        "schema_version": 1,
        "read_only": True,
        "evidence_sha256": digest,
        "scan_counts": {
            "discovered_projects": counts.get("discovered_projects"),
            "completed_audits": counts.get("completed_audits"),
            "unverified_projects": counts.get("unverified_projects"),
            "normalized_findings": counts.get("normalized_findings"),
        },
        "finding_counts": {
            "scanner_advisory_records": advisory_records,
            "affected_package_version_occurrences": package_version_occurrences,
            "propagation_only_markers": propagation_markers,
        },
        "by_ecosystem": by_ecosystem,
        "classification_constraint": "Scanner evidence only: classify every record Cannot verify until separately approved authoritative sources are checked.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize normalized audit JSON without external access.")
    parser.add_argument("--audit-result", required=True)
    args = parser.parse_args()
    try:
        result, digest = load_result(Path(args.audit_result))
        summary = summarize(result, digest)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
