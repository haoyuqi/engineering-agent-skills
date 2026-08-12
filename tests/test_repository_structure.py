#!/usr/bin/env python3
"""Offline structural validation for engineering-agent-skills."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
REQUIRED_ROOT_FILES = (
    "README.md",
    "README.zh-CN.md",
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
)
REQUIRED_SKILL_FILES = (
    "SKILL.md",
    "README.md",
    "examples/input-output.md",
    "evals/cases.md",
    "evals/rubric.md",
)


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def validate_front_matter(skill_file: Path, expected_name: str) -> None:
    content = skill_file.read_text(encoding="utf-8")
    match = re.match(r"^---\n(?P<meta>.*?)\n---\n", content, re.DOTALL)
    if not match:
        fail(f"{skill_file.relative_to(ROOT)} has no YAML front matter")

    metadata = match.group("meta")
    name = re.search(r"^name:\s*(.+?)\s*$", metadata, re.MULTILINE)
    description = re.search(r"^description:\s*(.+?)\s*$", metadata, re.MULTILINE)
    if not name or name.group(1).strip(" '\"") != expected_name:
        fail(f"{skill_file.relative_to(ROOT)} name must match '{expected_name}'")
    if not description or not description.group(1).strip():
        fail(f"{skill_file.relative_to(ROOT)} needs a non-empty description")


def validate_relative_links(markdown_file: Path) -> None:
    content = markdown_file.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
        target = target.strip("<>")
        target_path = target.split("#", 1)[0]
        if not target_path or "://" in target_path or target_path.startswith("mailto:"):
            continue
        if not (markdown_file.parent / target_path).exists():
            fail(
                f"broken relative link in {markdown_file.relative_to(ROOT)}: {target}"
            )


def main() -> None:
    for relative_path in REQUIRED_ROOT_FILES:
        if not (ROOT / relative_path).is_file():
            fail(f"missing required root file: {relative_path}")

    skills_root = ROOT / "skills"
    skill_directories = sorted(path for path in skills_root.iterdir() if path.is_dir())
    if not skill_directories:
        fail("no skill directories found")

    for skill_directory in skill_directories:
        for relative_path in REQUIRED_SKILL_FILES:
            if not (skill_directory / relative_path).is_file():
                fail(f"{skill_directory.name} is missing {relative_path}")
        validate_front_matter(skill_directory / "SKILL.md", skill_directory.name)

    for markdown_file in ROOT.rglob("*.md"):
        if ".git" not in markdown_file.parts:
            validate_relative_links(markdown_file)

    print(f"PASS: validated {len(skill_directories)} skill(s) in {ROOT}")


if __name__ == "__main__":
    main()
