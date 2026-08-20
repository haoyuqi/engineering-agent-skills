#!/usr/bin/env python3
"""Reject common secrets, private infrastructure, and workstation identifiers."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent.parent
SKIP_PARTS = {".git", "__pycache__"}
TEXT_SUFFIXES = {"", ".md", ".json", ".py", ".yaml", ".yml", ".txt"}
MAX_TEXT_BYTES = 2 * 1024 * 1024
APPROVED_PUBLIC_HOSTS = {
    "agentskills.io",
    "docs.github.com",
    "docs.npmjs.com",
    "example.com",
    "example.invalid",
    "example.net",
    "example.org",
    "getcomposer.org",
    "github.com",
    "gitlab.com",
    "json-schema.org",
    "registry.npmjs.org",
    "repo.packagist.org",
    "skills.sh",
    "www.apache.org",
}
URL_PATTERN = re.compile(r"https?://[^\s)\]}>\"`]+", re.IGNORECASE)

FORBIDDEN_PATTERNS = {
    "private workstation path": re.compile(
        r"(?:/Users/[^/\s]+|/home/[^/\s]+|/var/www(?:/|\b)|[A-Za-z]:\\Users\\[^\\\s]+)"
    ),
    "email address": re.compile(
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE
    ),
    "private domain": re.compile(
        r"\b(?:[a-z0-9-]+\.)+(?:corp|internal|intranet|local)\b", re.IGNORECASE
    ),
    "private IPv4 address": re.compile(
        r"\b(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})\b"
    ),
    "Jira custom field identifier": re.compile(r"\bcustomfield_\d+\b", re.IGNORECASE),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "GitLab token": re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b"),
    "npm token": re.compile(r"\bnpm_[A-Za-z0-9]{30,}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "bearer credential": re.compile(r"\bBearer\s+[A-Za-z0-9._~-]{20,}\b", re.IGNORECASE),
    "credential in URL": re.compile(
        r"https?://[^\s/:@]+:[^\s/@]+@", re.IGNORECASE
    ),
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def should_scan(relative_path: Path) -> bool:
    return (
        not SKIP_PARTS.intersection(relative_path.parts)
        and relative_path.as_posix() != "tests/test_public_content.py"
        and relative_path.name != "LICENSE"
    )


def read_text_if_safe(path: Path, content: bytes | None = None) -> str | None:
    """Scan every reasonably-sized UTF-8 text file, regardless of extension."""
    try:
        raw = content if content is not None else path.read_bytes()
    except OSError:
        return None
    if len(raw) > MAX_TEXT_BYTES or b"\0" in raw:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


def scan_content(label: str, content: str) -> None:
    for url in URL_PATTERN.findall(content):
        hostname = (urlsplit(url).hostname or "").lower()
        if hostname not in APPROVED_PUBLIC_HOSTS:
            line = content.count("\n", 0, content.find(url)) + 1
            fail(f"unreviewed URL host in {label}:{line}")
    for pattern_label, pattern in FORBIDDEN_PATTERNS.items():
        match = pattern.search(content)
        if match:
            line = content.count("\n", 0, match.start()) + 1
            fail(f"{pattern_label} in {label}:{line}")


def scan_worktree() -> int:
    checked = 0
    for path in sorted(ROOT.rglob("*")):
        if path.is_symlink() or not path.is_file():
            continue
        relative_path = path.relative_to(ROOT)
        if not should_scan(relative_path):
            continue
        content = read_text_if_safe(path)
        if content is None:
            continue
        checked += 1
        scan_content(relative_path.as_posix(), content)
    return checked


def scan_history() -> int:
    checked = 0
    commits = subprocess.run(
        ["git", "rev-list", "--all"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    for commit in commits:
        paths = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", "-z", commit],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout.split(b"\0")
        for raw_path in paths:
            if not raw_path:
                continue
            try:
                relative_path = Path(raw_path.decode("utf-8"))
            except UnicodeDecodeError:
                continue
            if not should_scan(relative_path):
                continue
            blob = subprocess.run(
                ["git", "show", f"{commit}:{relative_path.as_posix()}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
            ).stdout
            content = read_text_if_safe(relative_path, blob)
            if content is None:
                continue
            checked += 1
            scan_content(f"{commit[:12]}:{relative_path.as_posix()}", content)
    return checked


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--history",
        action="store_true",
        help="scan every committed file revision instead of the current worktree",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.history:
        files_checked = scan_history()
        scope = "committed file revision(s)"
    else:
        files_checked = scan_worktree()
        scope = "worktree text file(s)"
    print(f"PASS: public-content scan checked {files_checked} {scope}")


if __name__ == "__main__":
    main()
