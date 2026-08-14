#!/usr/bin/env python3
"""Discover and read-only audit Composer/npm projects below one repository root.

The script intentionally requires both --run-audits and an allow-list for every
registry host before it contacts a package registry.  Without --run-audits it
prints a deterministic discovery and audit plan only.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any
from urllib.parse import urlsplit

from discover_projects import DEFAULT_EXCLUDES, ECOSYSTEMS, discover
from normalize_audit import normalize_composer, normalize_npm


DEFAULT_REGISTRY_ORIGINS = {
    "composer": {"https://repo.packagist.org"},
    "npm": {"https://registry.npmjs.org"},
}
MAX_STDERR_SUMMARY = 500


def registry_origin(value: object) -> str | None:
    """Return a credential-free canonical origin; reject paths, queries, and fragments."""
    if not isinstance(value, str) or not value.strip():
        return None
    candidate = value.strip()
    parsed = urlsplit(candidate if "://" in candidate else "https:" + "//" + candidate)
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.path not in {"", "/"}
        or parsed.query
        or parsed.fragment
    ):
        return None
    port = parsed.port
    default_port = 443 if parsed.scheme == "https" else 80
    authority = parsed.hostname.lower()
    if port and port != default_port:
        authority = f"{authority}:{port}"
    return f"{parsed.scheme}://{authority}"


def load_json_file(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def npm_registry_destinations(project: Path, root: Path) -> tuple[list[dict[str, str]], list[str], bool]:
    """Inspect project-controlled npmrc files without reading user/global config."""
    default_origin = next(iter(DEFAULT_REGISTRY_ORIGINS["npm"]))
    scoped_origins: set[str] = set()
    sources: list[str] = []
    dynamic = False
    candidates = [root / ".npmrc"]
    if project != root:
        candidates.append(project / ".npmrc")
    for candidate in candidates:
        if not candidate.is_file():
            continue
        sources.append(candidate.relative_to(root).as_posix())
        try:
            lines = candidate.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for line in lines:
            line = re.split(r"[;#]", line, maxsplit=1)[0].strip()
            if "=" not in line:
                continue
            key, value = (piece.strip() for piece in line.split("=", 1))
            if key == "registry" or re.fullmatch(r"@[^:]+:registry", key):
                if "${" in value:
                    dynamic = True
                    continue
                configured_origin = registry_origin(value)
                if key == "registry" and configured_origin:
                    default_origin = configured_origin
                elif re.fullmatch(r"@[^:]+:registry", key) and configured_origin:
                    scoped_origins.add(configured_origin)
                else:
                    dynamic = True
    return (
        [{"origin": value, "kind": "static"} for value in sorted({default_origin, *scoped_origins})],
        sources,
        dynamic,
    )


def composer_registry_destinations(project: Path, root: Path) -> tuple[list[dict[str, str]], list[str], bool]:
    """Inspect composer.json repositories without reading Composer home/auth files."""
    origins = set(DEFAULT_REGISTRY_ORIGINS["composer"])
    manifest = project / "composer.json"
    document = load_json_file(manifest)
    if not document:
        return ([{"origin": value, "kind": "static"} for value in sorted(origins)], [], False)

    repositories = document.get("repositories", [])
    entries: list[object]
    if isinstance(repositories, dict):
        entries = list(repositories.values())
    elif isinstance(repositories, list):
        entries = repositories
    else:
        entries = []
    dynamic = False
    for entry in entries:
        if isinstance(entry, dict):
            configured_origin = registry_origin(entry.get("url"))
            if configured_origin:
                origins.add(configured_origin)
            elif entry.get("url") is not None:
                dynamic = True
    return (
        [{"origin": value, "kind": "static"} for value in sorted(origins)],
        [manifest.relative_to(root).as_posix()],
        dynamic,
    )


def project_credential_sources(project: Path, root: Path, ecosystem: str) -> list[str]:
    """Return locations of project credential configuration without reading values."""
    candidates: list[Path] = []
    if ecosystem == "npm":
        for npmrc in (root / ".npmrc", project / ".npmrc"):
            if not npmrc.is_file():
                continue
            try:
                lines = npmrc.read_text(encoding="utf-8").splitlines()
            except OSError:
                continue
            if any(
                re.search(r"(?i)(?:_auth(?:token)?|_password|username|certfile|keyfile)\s*=", line)
                for line in lines
            ):
                candidates.append(npmrc)
    elif (project / "auth.json").is_file():
        candidates.append(project / "auth.json")
    return sorted({path.relative_to(root).as_posix() for path in candidates})


def registry_plan(project: dict[str, str], root: Path) -> dict[str, Any]:
    project_directory = root / project["project_path"]
    if project["ecosystem"] == "npm":
        destinations, sources, dynamic = npm_registry_destinations(project_directory, root)
    else:
        destinations, sources, dynamic = composer_registry_destinations(project_directory, root)
    return {
        "project_path": project["project_path"],
        "ecosystem": project["ecosystem"],
        "destinations": destinations,
        "dynamic_destination_detected": dynamic,
        "project_credential_sources": project_credential_sources(
            project_directory, root, project["ecosystem"]
        ),
        "project_controlled_sources": sources,
        "configuration_limit": (
            "Only project-controlled configuration was inspected; user, global, "
            "and environment configuration can still change the effective registry."
        ),
    }


def npm_workspace_patterns(manifest: Path) -> list[str]:
    """Return declared npm workspace patterns without interpreting package scripts."""
    document = load_json_file(manifest)
    if not document:
        return []
    workspaces = document.get("workspaces", [])
    if isinstance(workspaces, dict):
        workspaces = workspaces.get("packages", [])
    return [item for item in workspaces if isinstance(item, str) and item.strip()]


def matches_workspace(path: str, patterns: list[str]) -> bool:
    """Apply npm workspace include/exclude patterns in declaration order."""
    included = False
    for raw_pattern in patterns:
        negated = raw_pattern.startswith("!")
        pattern = raw_pattern[1:] if negated else raw_pattern
        if pattern and fnmatch.fnmatchcase(path, pattern):
            included = not negated
    return included


def workspace_lockfile_coverage(discovery: dict[str, Any], root: Path) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Link incomplete npm workspace manifests to a discovered parent lockfile."""
    parents = [
        project
        for project in discovery["projects"]
        if project["ecosystem"] == "npm"
        and npm_workspace_patterns(root / project["manifest_path"])
    ]
    covered: list[dict[str, str]] = []
    gaps: list[dict[str, str]] = []
    for incomplete in discovery["incomplete"]:
        if incomplete["ecosystem"] != "npm" or incomplete["present"] != "package.json":
            continue
        candidate_directory = root / incomplete["project_path"]
        for parent in parents:
            parent_directory = root / parent["project_path"]
            try:
                relative_candidate = candidate_directory.relative_to(parent_directory).as_posix()
            except ValueError:
                continue
            patterns = npm_workspace_patterns(root / parent["manifest_path"])
            if matches_workspace(relative_candidate, patterns):
                lockfile = load_json_file(root / parent["lockfile_path"])
                package_entries = lockfile.get("packages", {}) if lockfile else {}
                workspace_key = relative_candidate
                if isinstance(package_entries, dict) and workspace_key in package_entries:
                    covered.append(
                        {
                            "project_path": incomplete["project_path"],
                            "covered_by_project": parent["project_path"],
                            "covered_by_lockfile": parent["lockfile_path"],
                        }
                    )
                else:
                    gaps.append(
                        {
                            "project_path": incomplete["project_path"],
                            "reason": "workspace declaration exists but lockfile does not prove inclusion",
                        }
                    )
                break
    return covered, gaps


def command_for(ecosystem: str) -> list[str]:
    if ecosystem == "composer":
        return ["composer", "--no-plugins", "--no-scripts", "audit", "--locked", "--format=json"]
    return ["npm", "audit", "--json", "--package-lock-only", "--ignore-scripts"]


def redact_summary(value: str | bytes) -> str:
    """Keep diagnostics useful without leaking URL credentials or common token forms."""
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="replace")
    value = re.sub(r"(https?://)[^/@\s:]+:[^/@\s]*@", r"\1<redacted>@", value)
    value = re.sub(r"(?i)(token|password|authorization)\s*[=:]\s*\S+", r"\1=<redacted>", value)
    return value.strip()[:MAX_STDERR_SUMMARY]


def isolated_audit_environment(directory: Path) -> dict[str, str]:
    """Prevent user/global package-manager configuration from changing audit scope."""
    environment = os.environ.copy()
    for key in list(environment):
        normalized = key.upper()
        if normalized.startswith("NPM_CONFIG_") or normalized.startswith("COMPOSER_"):
            environment.pop(key, None)
    environment.pop("NPM_TOKEN", None)
    environment.pop("NODE_AUTH_TOKEN", None)
    for key in list(environment):
        if key.lower() in {"http_proxy", "https_proxy", "all_proxy", "no_proxy"}:
            environment.pop(key, None)

    npm_userconfig = directory / "npm-userconfig"
    npm_globalconfig = directory / "npm-globalconfig"
    npm_userconfig.touch()
    npm_globalconfig.touch()
    environment.update(
        {
            "COMPOSER_HOME": str(directory / "composer-home"),
            "COMPOSER_CACHE_DIR": str(directory / "composer-cache"),
            "COMPOSER_NO_INTERACTION": "1",
            "npm_config_cache": str(directory / "npm-cache"),
            "npm_config_userconfig": str(npm_userconfig),
            "npm_config_globalconfig": str(npm_globalconfig),
            "npm_config_ignore_scripts": "true",
        }
    )
    return environment


def execute_audit(project: dict[str, str], root: Path, timeout: int) -> dict[str, Any]:
    ecosystem = project["ecosystem"]
    command = command_for(ecosystem)
    project_directory = root / project["project_path"]
    result: dict[str, Any] = {
        "project_path": project["project_path"],
        "ecosystem": ecosystem,
        "command": command,
    }
    if shutil.which(command[0]) is None:
        result.update({"status": "tool_missing", "stdout_parse_state": "not-run"})
        return result
    with tempfile.TemporaryDirectory(prefix="repository-vulnerability-audit-") as temporary:
        try:
            completed = subprocess.run(
                command,
                cwd=project_directory,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=isolated_audit_environment(Path(temporary)),
            )
        except subprocess.TimeoutExpired as error:
            result.update(
                {
                    "status": "timed_out",
                    "stdout_parse_state": "not-parseable",
                    "stderr_summary": redact_summary(error.stderr or "timed out"),
                }
            )
            return result
        except OSError as error:
            result.update(
                {
                    "status": "execution_error",
                    "stdout_parse_state": "not-parseable",
                    "stderr_summary": redact_summary(str(error)),
                }
            )
            return result

    result["exit_code"] = completed.returncode
    if completed.stderr:
        result["stderr_summary"] = redact_summary(completed.stderr)
    try:
        audit_json = json.loads(completed.stdout)
        if not isinstance(audit_json, dict):
            raise ValueError("expected a JSON object")
        lockfile = load_json_file(root / project["lockfile_path"])
        if lockfile is None:
            raise ValueError("cannot read a valid lockfile JSON object")
        normalized = (
            normalize_composer(lockfile, audit_json, project["project_path"])
            if ecosystem == "composer"
            else normalize_npm(lockfile, audit_json, project["project_path"])
        )
    except (json.JSONDecodeError, ValueError) as error:
        result.update(
            {
                "status": "execution_error" if completed.returncode else "malformed_output",
                "stdout_parse_state": "not-parseable",
                "parse_error": str(error),
            }
        )
        return result

    result.update(
        {
            "status": "completed",
            "stdout_parse_state": "parseable",
            "normalized": normalized,
        }
    )
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Discover Composer/npm projects and run approved read-only audits."
    )
    parser.add_argument("--root", default=".", help="Approved repository root")
    parser.add_argument("--exclude", action="append", default=[], metavar="NAME")
    parser.add_argument(
        "--ecosystem", action="append", choices=sorted(ECOSYSTEMS), default=[]
    )
    parser.add_argument(
        "--run-audits",
        action="store_true",
        help="Run read-only audit commands after registry-host approval",
    )
    parser.add_argument(
        "--allow-registry-origin",
        action="append",
        default=[],
        metavar="ORIGIN",
        help="Explicitly approved static registry origin, such as https://registry.npmjs.org",
    )
    parser.add_argument(
        "--timeout-seconds", type=int, default=120, help="Per-project audit timeout"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print(json.dumps({"error": "root is not a directory"}), file=sys.stderr)
        return 2
    if args.timeout_seconds < 1:
        print(json.dumps({"error": "timeout-seconds must be positive"}), file=sys.stderr)
        return 2

    ecosystems = set(args.ecosystem) or set(ECOSYSTEMS)
    discovery = discover(root, DEFAULT_EXCLUDES | set(args.exclude), ecosystems)
    allowed_origins = {
        origin
        for value in args.allow_registry_origin
        if (origin := registry_origin(value))
    }
    registry_destinations = [registry_plan(project, root) for project in discovery["projects"]]
    workspace_coverage, workspace_coverage_gaps = workspace_lockfile_coverage(discovery, root)
    audits: list[dict[str, Any]] = []
    for project, destination in zip(discovery["projects"], registry_destinations):
        required_origins = [item["origin"] for item in destination["destinations"]]
        unapproved_origins = sorted(set(required_origins) - allowed_origins)
        if not args.run_audits:
            audits.append(
                {
                    "project_path": project["project_path"],
                    "ecosystem": project["ecosystem"],
                    "status": "awaiting_run_confirmation",
                    "required_registry_origins": required_origins,
                }
            )
        elif destination["dynamic_destination_detected"]:
            audits.append(
                {
                    "project_path": project["project_path"],
                    "ecosystem": project["ecosystem"],
                    "status": "dynamic_registry_configuration_unsupported",
                }
            )
        elif destination["project_credential_sources"]:
            audits.append(
                {
                    "project_path": project["project_path"],
                    "ecosystem": project["ecosystem"],
                    "status": "project_credential_configuration_detected",
                    "credential_sources": destination["project_credential_sources"],
                }
            )
        elif unapproved_origins:
            audits.append(
                {
                    "project_path": project["project_path"],
                    "ecosystem": project["ecosystem"],
                    "status": "registry_approval_required",
                    "unapproved_registry_origins": unapproved_origins,
                }
            )
        else:
            audits.append(execute_audit(project, root, args.timeout_seconds))

    completed = [item for item in audits if item["status"] == "completed"]
    completed_projects = {
        (item["project_path"], item["ecosystem"]) for item in completed
    }
    covered_workspaces = [
        item
        for item in workspace_coverage
        if (item["covered_by_project"], "npm") in completed_projects
    ]
    workspace_covered_paths = {item["project_path"] for item in covered_workspaces}
    unverified_incomplete = [
        item
        for item in discovery["incomplete"]
        if item["project_path"] not in workspace_covered_paths
    ]
    findings = sum(
        len(item["normalized"]["findings"])
        for item in completed
        if isinstance(item.get("normalized"), dict)
    )
    result = {
        "schema_version": 1,
        "root": ".",
        "read_only": True,
        "discovery": discovery,
        "registry_destinations": registry_destinations,
        "workspace_lockfile_coverage": workspace_coverage,
        "workspace_lockfile_coverage_gaps": workspace_coverage_gaps,
        "audits": audits,
        "counts": {
            "discovered_projects": len(discovery["projects"]),
            "incomplete_projects": len(discovery["incomplete"]),
            "workspace_covered_projects": len(covered_workspaces),
            "workspace_coverage_gaps": len(workspace_coverage_gaps),
            "completed_audits": len(completed),
            "normalized_findings": findings,
            "unverified_projects": len(audits) - len(completed) + len(unverified_incomplete),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
