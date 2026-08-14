#!/usr/bin/env python3
"""Normalize Composer or npm audit JSON with versions from a lockfile."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


def load_json(path_value: str) -> dict[str, Any]:
    try:
        if path_value == "-":
            value = json.load(sys.stdin)
        else:
            value = json.loads(Path(path_value).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read valid JSON from {path_value}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object in {path_value}")
    return value


def composer_versions(lockfile: dict[str, Any]) -> dict[str, dict[str, str]]:
    versions: dict[str, dict[str, str]] = {}
    for key, dependency_kind in (("packages", "production"), ("packages-dev", "dev")):
        packages = lockfile.get(key, [])
        if not isinstance(packages, list):
            raise ValueError(f"composer.lock field {key} must be a list")
        for package in packages:
            if not isinstance(package, dict):
                continue
            name = package.get("name")
            version = package.get("version")
            if isinstance(name, str) and isinstance(version, str):
                versions[name] = {
                    "version": version,
                    "dependency_kind": dependency_kind,
                }
    return versions


def normalize_composer(
    lockfile: dict[str, Any], audit: dict[str, Any], project: str
) -> dict[str, Any]:
    versions = composer_versions(lockfile)
    findings: list[dict[str, Any]] = []
    warnings: list[str] = []

    for audit_key, ignored in (("advisories", False), ("ignored-advisories", True)):
        advisories = audit.get(audit_key, {})
        if advisories is None:
            advisories = {}
        if not isinstance(advisories, dict):
            raise ValueError(f"Composer audit field {audit_key} must be an object")
        for package_name, package_advisories in advisories.items():
            if not isinstance(package_advisories, list):
                raise ValueError(f"Composer advisories for {package_name} must be a list")
            installed = versions.get(package_name, {})
            if not installed:
                warnings.append(f"no lockfile version for advisory package {package_name}")
            for advisory in package_advisories:
                if not isinstance(advisory, dict):
                    continue
                identifiers = [
                    value
                    for value in (advisory.get("advisoryId"), advisory.get("cve"))
                    if isinstance(value, str) and value
                ]
                sources = advisory.get("sources", [])
                if isinstance(sources, list):
                    identifiers.extend(
                        source["remoteId"]
                        for source in sources
                        if isinstance(source, dict)
                        and isinstance(source.get("remoteId"), str)
                    )
                findings.append(
                    {
                        "project_path": project,
                        "ecosystem": "composer",
                        "package": package_name,
                        "installed_versions": [installed["version"]]
                        if installed.get("version")
                        else [],
                        "dependency_kind": installed.get("dependency_kind", "unknown"),
                        "severity": advisory.get("severity"),
                        "identifiers": list(dict.fromkeys(identifiers)),
                        "affected_range": advisory.get("affectedVersions"),
                        "title": advisory.get("title"),
                        "advisory_url": advisory.get("link"),
                        "reported_at": advisory.get("reportedAt"),
                        "ignored_by_policy": ignored,
                        "source_tool": "composer-audit",
                    }
                )

    extra_categories = {
        key: audit[key]
        for key in ("abandoned", "malware", "policy-violations")
        if key in audit and audit[key]
    }
    return {
        "schema_version": 1,
        "ecosystem": "composer",
        "project_path": project,
        "findings": findings,
        "non_vulnerability_categories": extra_categories,
        "warnings": sorted(set(warnings)),
    }


def npm_versions(lockfile: dict[str, Any]) -> tuple[dict[str, str], dict[str, set[str]]]:
    node_versions: dict[str, str] = {}
    package_versions: dict[str, set[str]] = {}

    packages = lockfile.get("packages", {})
    if packages is not None and not isinstance(packages, dict):
        raise ValueError("package-lock.json field packages must be an object")
    if isinstance(packages, dict):
        for node, metadata in packages.items():
            if not node or not isinstance(metadata, dict):
                continue
            version = metadata.get("version")
            if not isinstance(version, str):
                continue
            name = metadata.get("name")
            if not isinstance(name, str):
                marker = "node_modules/"
                name = node.rsplit(marker, 1)[-1] if marker in node else ""
            if name:
                node_versions[node] = version
                package_versions.setdefault(name, set()).add(version)

    def visit_dependencies(dependencies: Any) -> None:
        if not isinstance(dependencies, dict):
            return
        for name, metadata in dependencies.items():
            if not isinstance(metadata, dict):
                continue
            version = metadata.get("version")
            if isinstance(name, str) and isinstance(version, str):
                package_versions.setdefault(name, set()).add(version)
            visit_dependencies(metadata.get("dependencies"))

    visit_dependencies(lockfile.get("dependencies"))
    return node_versions, package_versions


def normalize_npm(
    lockfile: dict[str, Any], audit: dict[str, Any], project: str
) -> dict[str, Any]:
    node_versions, package_versions = npm_versions(lockfile)
    vulnerabilities = audit.get("vulnerabilities", {})
    if not isinstance(vulnerabilities, dict):
        raise ValueError("npm audit field vulnerabilities must be an object")

    findings: list[dict[str, Any]] = []
    warnings: list[str] = []
    for package_name, vulnerability in vulnerabilities.items():
        if not isinstance(vulnerability, dict):
            continue
        nodes = [node for node in vulnerability.get("nodes", []) if isinstance(node, str)]
        node_installed_versions = {
            node_versions[node] for node in nodes if node in node_versions
        }
        installed_versions = node_installed_versions or package_versions.get(
            package_name, set()
        )
        if not installed_versions:
            warnings.append(f"no lockfile version for vulnerability package {package_name}")

        advisory_entries = [
            item for item in vulnerability.get("via", []) if isinstance(item, dict)
        ]
        meta_dependencies = [
            item for item in vulnerability.get("via", []) if isinstance(item, str)
        ]
        if not advisory_entries:
            advisory_entries = [{}]
        for advisory in advisory_entries:
            source_id = advisory.get("source")
            identifiers = [str(source_id)] if source_id is not None else []
            findings.append(
                {
                    "project_path": project,
                    "ecosystem": "npm",
                    "package": package_name,
                    "installed_versions": sorted(installed_versions),
                    "dependency_kind": "direct"
                    if vulnerability.get("isDirect") is True
                    else "transitive",
                    "severity": advisory.get("severity", vulnerability.get("severity")),
                    "identifiers": identifiers,
                    "affected_range": advisory.get("range", vulnerability.get("range")),
                    "title": advisory.get("title"),
                    "advisory_url": advisory.get("url"),
                    "nodes": nodes,
                    "version_resolution": "audit-nodes"
                    if node_installed_versions
                    else "package-name-fallback",
                    "via_dependencies": meta_dependencies,
                    "fix_available": vulnerability.get("fixAvailable"),
                    "source_tool": "npm-audit",
                }
            )

    report_version = audit.get("auditReportVersion")
    if report_version not in (None, 2):
        warnings.append(f"unrecognized npm auditReportVersion: {report_version}")
    return {
        "schema_version": 1,
        "ecosystem": "npm",
        "project_path": project,
        "findings": findings,
        "audit_metadata": audit.get("metadata", {}),
        "warnings": sorted(set(warnings)),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize read-only Composer/npm audit JSON with lockfile versions."
    )
    parser.add_argument("--ecosystem", required=True, choices=("composer", "npm"))
    parser.add_argument("--lockfile", required=True)
    parser.add_argument("--audit-json", required=True, help="Path or - for stdin")
    parser.add_argument("--project", default=".", help="Project path for output evidence")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        lockfile = load_json(args.lockfile)
        audit = load_json(args.audit_json)
        if args.ecosystem == "composer":
            result = normalize_composer(lockfile, audit, args.project)
        else:
            result = normalize_npm(lockfile, audit, args.project)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
