#!/usr/bin/env python3
"""Discover Composer and npm projects without executing package-manager commands."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil


DEFAULT_EXCLUDES = {
    ".git",
    ".agents",
    ".claude",
    ".codex",
    ".hg",
    ".svn",
    "node_modules",
    "vendor",
}

ECOSYSTEMS = {
    "composer": ("composer.json", "composer.lock", "composer"),
    "npm": ("package.json", "package-lock.json", "npm"),
}


def relative(directory: Path, root: Path) -> str:
    value = directory.relative_to(root).as_posix()
    return value or "."


def discover(root: Path, excludes: set[str], ecosystems: set[str]) -> dict:
    projects: list[dict[str, str]] = []
    incomplete: list[dict[str, str]] = []
    excluded_directories: list[dict[str, str]] = []
    traversal_errors: list[dict[str, str]] = []

    def record_traversal_error(error: OSError) -> None:
        error_path = Path(error.filename or root)
        try:
            displayed_path = error_path.resolve().relative_to(root).as_posix() or "."
        except ValueError:
            displayed_path = "[outside approved root]"
        traversal_errors.append(
            {
                "path": displayed_path,
                "error": error.strerror or error.__class__.__name__,
            }
        )

    for current, directory_names, file_names in os.walk(
        root, topdown=True, onerror=record_traversal_error
    ):
        current_path = Path(current)
        retained_directories: list[str] = []
        for name in sorted(directory_names):
            candidate = current_path / name
            if name in excludes:
                excluded_directories.append(
                    {
                        "path": candidate.relative_to(root).as_posix(),
                        "reason": "excluded directory name",
                    }
                )
            elif candidate.is_symlink():
                excluded_directories.append(
                    {
                        "path": candidate.relative_to(root).as_posix(),
                        "reason": "directory symlink not followed",
                    }
                )
            else:
                retained_directories.append(name)
        directory_names[:] = retained_directories
        files = set(file_names)

        for ecosystem in sorted(ecosystems):
            manifest, lockfile, _ = ECOSYSTEMS[ecosystem]
            has_manifest = manifest in files
            has_lockfile = lockfile in files
            project_path = relative(current_path, root)
            if has_manifest and has_lockfile:
                projects.append(
                    {
                        "project_path": project_path,
                        "ecosystem": ecosystem,
                        "manifest_path": (current_path / manifest)
                        .relative_to(root)
                        .as_posix(),
                        "lockfile_path": (current_path / lockfile)
                        .relative_to(root)
                        .as_posix(),
                    }
                )
            elif has_manifest or has_lockfile:
                incomplete.append(
                    {
                        "project_path": project_path,
                        "ecosystem": ecosystem,
                        "present": manifest if has_manifest else lockfile,
                        "missing": lockfile if has_manifest else manifest,
                    }
                )

    return {
        "schema_version": 1,
        "root": ".",
        "projects": projects,
        "incomplete": incomplete,
        "excluded_directories": excluded_directories,
        "traversal_errors": traversal_errors,
        "counts": {
            "projects": len(projects),
            "incomplete": len(incomplete),
            "excluded_directories": len(excluded_directories),
            "traversal_errors": len(traversal_errors),
        },
        "tool_availability": {
            ecosystem: shutil.which(command) is not None
            for ecosystem, (_, _, command) in ECOSYSTEMS.items()
            if ecosystem in ecosystems
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Discover Composer/npm manifest-lockfile pairs read-only."
    )
    parser.add_argument("--root", default=".", help="Approved repository root")
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="NAME",
        help="Additional directory name to exclude; repeat as needed",
    )
    parser.add_argument(
        "--ecosystem",
        action="append",
        choices=sorted(ECOSYSTEMS),
        default=[],
        help="Ecosystem to discover; defaults to composer and npm",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit("error: root is not a directory")

    ecosystems = set(args.ecosystem) or set(ECOSYSTEMS)
    result = discover(root, DEFAULT_EXCLUDES | set(args.exclude), ecosystems)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
