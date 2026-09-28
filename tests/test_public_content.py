#!/usr/bin/env python3
"""Flag obvious disclosure hazards; not a substitute for provenance review."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
MAX_TEXT_BYTES = 2 * 1024 * 1024
# Only credential shapes block CI. Never print matched values.
BLOCKING = {
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    "GitLab token": re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b"),
    "npm token": re.compile(r"\bnpm_[A-Za-z0-9]{30,}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    "bearer credential": re.compile(r"\bBearer\s+[A-Za-z0-9._~-]{20,}\b", re.I),
    "credential in URL": re.compile(r"https?://[^\s/:@]+:[^\s/@]+@", re.I),
}
REVIEW = {
    "workstation path": re.compile(
        r"(?:/" r"Users/[^/\s]+|/" r"home/[^/\s]+|/" r"var/www(?:/|\b)|[A-Za-z]:\\Users\\[^\\\s]+)"
    ),
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "private domain": re.compile(r"\b(?:[a-z0-9-]+\.)+(?:corp|internal|intranet|local)\b", re.I),
    "private IPv4 address": re.compile(r"\b(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})\b"),
    "tracker custom field": re.compile(r"\bcustomfield_\d+\b", re.I),
}


def safe_label(label: str) -> str:
    for pattern in (*BLOCKING.values(), *REVIEW.values()):
        label = pattern.sub("<redacted>", label)
    return json.dumps(label, ensure_ascii=True)


def findings(content: str) -> list[tuple[str, str, int]]:
    result = []
    for level, rules in (("BLOCK", BLOCKING), ("REVIEW", REVIEW)):
        for rule, pattern in rules.items():
            for match in pattern.finditer(content):
                if rule == "email address":
                    domain = match.group().rsplit("@", 1)[1].lower()
                    if domain in {"example.com", "example.org", "example.net", "example.invalid"}:
                        continue
                result.append((level, rule, content.count("\n", 0, match.start()) + 1))
    return result


@dataclass
class Scan:
    checked: int = 0
    blocked: int = 0
    reviews: int = 0
    skipped: Counter = field(default_factory=Counter)
    seen: set[str] = field(default_factory=set)

    def skip(self, label: str, reason: str) -> None:
        self.skipped[reason] += 1
        print(f"SKIP: {safe_label(label)} ({reason})")

    def inspect(self, label: str, raw: bytes) -> None:
        if len(raw) > MAX_TEXT_BYTES:
            self.skip(label, "over size limit")
            return
        if b"\0" in raw:
            self.skip(label, "binary content")
            return
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            self.skip(label, "non-UTF-8 content")
            return
        if content.startswith("version https://git-lfs.github.com/spec/v1\n"):
            self.skip(label, "Git LFS payload unavailable")
            return
        self.checked += 1
        for level, rule, line in findings(content):
            self.blocked += level == "BLOCK"
            self.reviews += level == "REVIEW"
            print(f"{level}: {rule} at {safe_label(label)}:{line}")

    def finish(self) -> int:
        print(f"SUMMARY: {self.checked} text items; {self.blocked} blocking findings; "
              f"{self.reviews} review warnings; {sum(self.skipped.values())} skipped items")
        if self.blocked:
            return 1
        if self.skipped:
            print("INCOMPLETE: skipped items require separate inspection")
            return 2
        print("PASS: no blocking patterns found; not a provenance or secrecy guarantee")
        return 0


def git(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True).stdout


def scan_worktree(scan: Scan) -> None:
    # Tracked plus untracked, non-ignored files; never traverse caches or .git.
    paths = git("ls-files", "--cached", "--others", "--exclude-standard", "-z").split(b"\0")
    for name in sorted(set(paths) - {b""}):
        path = ROOT / os.fsdecode(name)
        label = os.fsdecode(name)
        try:
            if path.is_symlink():
                scan.inspect(label, os.fsencode(os.readlink(path)))
            elif not path.exists():
                continue  # Tracked deletion: history mode covers earlier content.
            elif path.is_dir():
                scan.skip(label, "submodule/directory not traversed")
            else:
                with path.open("rb") as stream:
                    scan.inspect(label, stream.read(MAX_TEXT_BYTES + 1))
        except OSError:
            scan.skip(label, "unreadable file")


def resolve_commit(ref: str) -> str:
    return git("rev-parse", "--verify", "--end-of-options", ref + "^{commit}").decode().strip()


def scan_history(scan: Scan, base: str | None = None, head: str = "HEAD") -> None:
    if git("rev-parse", "--is-shallow-repository").strip() != b"false":
        raise ValueError("history scanning requires a complete checkout (fetch-depth: 0)")
    if base is not None:
        base_sha, head_sha = resolve_commit(base), resolve_commit(head)
        commits = git("rev-list", f"{base_sha}..{head_sha}").decode().splitlines()
        commits = list(dict.fromkeys([*commits, head_sha]))
    else:
        commits = git("rev-list", "--all").decode().splitlines()
    if not commits:
        raise ValueError("no commits available to scan")
    print(f"SCOPE: {len(commits)} commit snapshots; identical blobs scanned once")
    for commit in commits:
        scan.inspect(f"{commit[:12]}:commit-message", git("show", "-s", "--format=%B", commit))
        for entry in git("ls-tree", "-r", "-z", commit).split(b"\0"):
            if not entry:
                continue
            metadata, name = entry.split(b"\t", 1)
            mode, kind, oid = metadata.decode().split()
            label = f"{commit[:12]}:{os.fsdecode(name)}"
            if kind != "blob":
                scan.skip(label, "submodule not traversed")
                continue
            if oid in scan.seen:
                continue
            scan.seen.add(oid)
            if int(git("cat-file", "-s", oid)) > MAX_TEXT_BYTES:
                scan.skip(label, "over size limit")
                continue
            scan.inspect(label, git("cat-file", "blob", oid))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--history", action="store_true", help="scan all locally reachable history")
    scope.add_argument("--base", help="scan every commit in BASE..HEAD and the final snapshot")
    parser.add_argument("--head", default="HEAD", help="range tip; requires --base")
    args = parser.parse_args()
    if args.head != "HEAD" and args.base is None:
        parser.error("--head requires --base")
    scan = Scan()
    try:
        if args.history or args.base is not None:
            scan_history(scan, args.base, args.head)
        else:
            scan_worktree(scan)
    except (subprocess.CalledProcessError, OSError, ValueError):
        print("ERROR: scope unavailable; check refs, Git access, and full checkout depth")
        return 2
    return scan.finish()


if __name__ == "__main__":
    raise SystemExit(main())
