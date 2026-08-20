#!/usr/bin/env python3
"""Offline structural validation for engineering-agent-skills."""

from __future__ import annotations

import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
REQUIRED_ROOT_FILES = (
    "README.md",
    "README.zh-CN.md",
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "AGENTS.md",
    "docs/skill-quality-standard.md",
    "docs/skill-quality-standard.zh-CN.md",
    "docs/design-benchmarks.md",
    "docs/compatibility.md",
    "docs/compatibility.json",
    "docs/configuration-contract.md",
    "docs/configuration-contract.json",
    "docs/evaluation.md",
    "docs/evaluation-result-format.md",
    "docs/external-sources.lock.json",
    "docs/privacy-review.md",
    "evals/README.md",
)
REQUIRED_SKILL_FILES = (
    "SKILL.md",
    "README.md",
    "config.example.yaml",
    "agents/openai.yaml",
    "examples/input-output.md",
    "evals/evals.json",
    "evals/triggers.json",
    "evals/cases.md",
    "evals/rubric.md",
)

PORTABLE_FRONT_MATTER_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}


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
    license_name = re.search(r"^license:\s*(.+?)\s*$", metadata, re.MULTILINE)
    compatibility = re.search(
        r"^compatibility:\s*(.+?)\s*$", metadata, re.MULTILINE
    )
    parsed_name = name.group(1).strip(" '\"") if name else ""
    parsed_description = description.group(1).strip(" '\"") if description else ""
    if parsed_name != expected_name:
        fail(f"{skill_file.relative_to(ROOT)} name must match '{expected_name}'")
    if len(parsed_name) > 64 or not re.fullmatch(
        r"[a-z0-9]+(?:-[a-z0-9]+)*", parsed_name
    ):
        fail(f"{skill_file.relative_to(ROOT)} has an invalid Agent Skills name")
    if not parsed_description:
        fail(f"{skill_file.relative_to(ROOT)} needs a non-empty description")
    if len(parsed_description) > 1024:
        fail(f"{skill_file.relative_to(ROOT)} description exceeds 1024 characters")
    if not parsed_description.startswith("Use when "):
        fail(f"{skill_file.relative_to(ROOT)} description must start with 'Use when '")
    if not license_name or license_name.group(1).strip(" '\"") != "Apache-2.0":
        fail(f"{skill_file.relative_to(ROOT)} must declare license: Apache-2.0")
    if compatibility and len(compatibility.group(1).strip(" '\"")) > 500:
        fail(f"{skill_file.relative_to(ROOT)} compatibility exceeds 500 characters")

    top_level_fields = {
        field.group(1)
        for field in re.finditer(r"^([a-z][a-z0-9-]*):", metadata, re.MULTILINE)
    }
    unsupported_fields = top_level_fields - PORTABLE_FRONT_MATTER_FIELDS
    if unsupported_fields:
        fail(
            f"{skill_file.relative_to(ROOT)} has runtime-specific front matter: "
            f"{', '.join(sorted(unsupported_fields))}"
        )
    if len(content.splitlines()) > 500:
        fail(f"{skill_file.relative_to(ROOT)} exceeds 500 lines")
    if len(content.split()) > 500:
        fail(f"{skill_file.relative_to(ROOT)} exceeds the 500-word context budget")
    if "config.example.yaml" not in content:
        fail(f"{skill_file.relative_to(ROOT)} must reference config.example.yaml")
    if not re.search(r"\b(read-only|confirm|confirmation)\b", content, re.IGNORECASE):
        fail(f"{skill_file.relative_to(ROOT)} must define a safety boundary")


def validate_config(config_file: Path) -> None:
    content = config_file.read_text(encoding="utf-8")
    if not re.search(r"^schema_version:\s*1\s*$", content, re.MULTILINE):
        fail(f"{config_file.relative_to(ROOT)} must declare schema_version: 1")


def validate_agent_metadata(metadata_file: Path, expected_name: str) -> None:
    content = metadata_file.read_text(encoding="utf-8")
    for field in ("display_name", "short_description", "default_prompt"):
        if not re.search(rf"^\s+{field}:\s*.+$", content, re.MULTILINE):
            fail(f"{metadata_file.relative_to(ROOT)} is missing {field}")
    if f"${expected_name}" not in content:
        fail(
            f"{metadata_file.relative_to(ROOT)} default_prompt must invoke "
            f"${expected_name}"
        )


def validate_evaluations(cases_file: Path, rubric_file: Path) -> None:
    cases = cases_file.read_text(encoding="utf-8")
    case_count = len(re.findall(r"^##\s+\S", cases, re.MULTILINE))
    if case_count < 3:
        fail(f"{cases_file.relative_to(ROOT)} needs at least three cases")

    rubric = rubric_file.read_text(encoding="utf-8")
    criterion_count = len(
        re.findall(r"^\|\s*[^-|][^|]*\|\s*[^|]+\|\s*$", rubric, re.MULTILINE)
    )
    if criterion_count < 3:
        fail(f"{rubric_file.relative_to(ROOT)} needs at least three criteria")


def validate_machine_evals(evals_file: Path, expected_name: str) -> None:
    try:
        document = json.loads(evals_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        fail(f"{evals_file.relative_to(ROOT)} is invalid JSON: {error}")

    if document.get("skill_name") != expected_name:
        fail(f"{evals_file.relative_to(ROOT)} skill_name must match {expected_name}")
    fixture_backed = document.get("fixture_backed", False)
    if not isinstance(fixture_backed, bool):
        fail(f"{evals_file.relative_to(ROOT)} fixture_backed must be boolean")
    evaluations = document.get("evals")
    if not isinstance(evaluations, list) or len(evaluations) < 3:
        fail(f"{evals_file.relative_to(ROOT)} needs at least three evaluations")

    ids: set[int] = set()
    for evaluation in evaluations:
        if not isinstance(evaluation, dict):
            fail(f"{evals_file.relative_to(ROOT)} evaluations must be objects")
        eval_id = evaluation.get("id")
        if not isinstance(eval_id, int) or eval_id in ids:
            fail(f"{evals_file.relative_to(ROOT)} evaluation IDs must be unique integers")
        ids.add(eval_id)
        for field in ("prompt", "expected_output"):
            if not isinstance(evaluation.get(field), str) or not evaluation[field].strip():
                fail(f"{evals_file.relative_to(ROOT)} evaluation {eval_id} needs {field}")
        files = evaluation.get("files", [])
        if not isinstance(files, list) or not all(isinstance(path, str) for path in files):
            fail(f"{evals_file.relative_to(ROOT)} evaluation {eval_id} has invalid files")
        if any(Path(path).is_absolute() or ".." in Path(path).parts for path in files):
            fail(f"{evals_file.relative_to(ROOT)} evaluation {eval_id} has unsafe paths")
        if any(not (evals_file.parent.parent / path).is_file() for path in files):
            fail(f"{evals_file.relative_to(ROOT)} evaluation {eval_id} references a missing fixture")
        if fixture_backed and not files:
            fail(f"{evals_file.relative_to(ROOT)} fixture-backed evaluation {eval_id} needs files")
        expectations = evaluation.get("expectations")
        if not isinstance(expectations, list) or len(expectations) < 2:
            fail(
                f"{evals_file.relative_to(ROOT)} evaluation {eval_id} needs at "
                "least two expectations"
            )
        if not all(isinstance(item, dict) for item in expectations):
            fail(
                f"{evals_file.relative_to(ROOT)} evaluation {eval_id} must use "
                "structured expectations"
            )


def validate_fictional_example(example_file: Path) -> None:
    content = example_file.read_text(encoding="utf-8")
    if not re.search(r"\b(fictional|invented)\b", content, re.IGNORECASE):
        fail(f"{example_file.relative_to(ROOT)} must state that its data is fictional")


def validate_trigger_cases(trigger_file: Path, expected_name: str) -> None:
    try:
        document = json.loads(trigger_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        fail(f"{trigger_file.relative_to(ROOT)} is invalid JSON: {error}")

    if document.get("schema_version") != 1:
        fail(f"{trigger_file.relative_to(ROOT)} must declare schema_version 1")
    if document.get("skill_name") != expected_name:
        fail(f"{trigger_file.relative_to(ROOT)} skill_name must match {expected_name}")
    fixture_notice = document.get("fixture_notice")
    if not isinstance(fixture_notice, str) or not re.search(
        r"\b(fictional|invented)\b", fixture_notice, re.IGNORECASE
    ):
        fail(f"{trigger_file.relative_to(ROOT)} needs a fictional-data notice")

    cases = document.get("cases")
    if not isinstance(cases, list) or len(cases) < 20:
        fail(f"{trigger_file.relative_to(ROOT)} needs at least 20 trigger cases")

    ids: set[int] = set()
    queries: set[str] = set()
    outcomes: list[bool] = []
    for case in cases:
        if not isinstance(case, dict):
            fail(f"{trigger_file.relative_to(ROOT)} cases must be objects")
        case_id = case.get("id")
        if not isinstance(case_id, int) or case_id in ids:
            fail(f"{trigger_file.relative_to(ROOT)} case IDs must be unique integers")
        ids.add(case_id)
        if not all(
            isinstance(case.get(field), str) and case[field].strip()
            for field in ("query", "reason")
        ):
            fail(f"{trigger_file.relative_to(ROOT)} case {case_id} is incomplete")
        normalized_query = case["query"].strip().casefold()
        if normalized_query in queries:
            fail(f"{trigger_file.relative_to(ROOT)} repeats a trigger query")
        queries.add(normalized_query)
        if not isinstance(case.get("should_trigger"), bool):
            fail(f"{trigger_file.relative_to(ROOT)} case {case_id} needs should_trigger")
        outcomes.append(case["should_trigger"])

    if outcomes.count(True) < 8 or outcomes.count(False) < 8:
        fail(f"{trigger_file.relative_to(ROOT)} needs eight positive and eight negative cases")
    expected_ids = set(range(1, len(cases) + 1))
    if ids != expected_ids:
        fail(f"{trigger_file.relative_to(ROOT)} case IDs must be consecutive from 1")
    for expected_outcome, label in ((True, "positive"), (False, "negative")):
        matching_queries = [
            case["query"]
            for case in cases
            if case["should_trigger"] is expected_outcome
        ]
        if not any(re.search(r"[\u3400-\u9fff]", query) for query in matching_queries):
            fail(f"{trigger_file.relative_to(ROOT)} needs a Chinese {label} case")


def validate_progressive_resources(skill_directory: Path) -> None:
    skill_content = (skill_directory / "SKILL.md").read_text(encoding="utf-8")
    for directory_name in ("references", "assets", "scripts"):
        resource_directory = skill_directory / directory_name
        if not resource_directory.is_dir():
            continue
        for resource in resource_directory.rglob("*"):
            if not resource.is_file():
                continue
            relative_resource = resource.relative_to(skill_directory).as_posix()
            if relative_resource not in skill_content:
                fail(
                    f"{relative_resource} is not referenced directly from "
                    f"{skill_directory.name}/SKILL.md"
                )


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
    expected_skill_files = {(path / "SKILL.md").resolve() for path in skill_directories}
    discovered_skill_files = {
        path.resolve()
        for path in ROOT.rglob("SKILL.md")
        if ".git" not in path.parts
    }
    if discovered_skill_files != expected_skill_files:
        extras = discovered_skill_files - expected_skill_files
        missing = expected_skill_files - discovered_skill_files
        fail(
            "discoverable SKILL.md files do not match the public catalog; "
            f"extras={[str(path.relative_to(ROOT)) for path in sorted(extras)]}, "
            f"missing={[str(path.relative_to(ROOT)) for path in sorted(missing)]}"
        )
    root_readmes = tuple(
        (ROOT / relative_path).read_text(encoding="utf-8")
        for relative_path in ("README.md", "README.zh-CN.md")
    )

    for skill_directory in skill_directories:
        for relative_path in REQUIRED_SKILL_FILES:
            if not (skill_directory / relative_path).is_file():
                fail(f"{skill_directory.name} is missing {relative_path}")
        validate_front_matter(skill_directory / "SKILL.md", skill_directory.name)
        validate_config(skill_directory / "config.example.yaml")
        validate_agent_metadata(
            skill_directory / "agents/openai.yaml", skill_directory.name
        )
        validate_progressive_resources(skill_directory)
        validate_fictional_example(skill_directory / "examples/input-output.md")
        validate_machine_evals(skill_directory / "evals/evals.json", skill_directory.name)
        validate_trigger_cases(
            skill_directory / "evals/triggers.json", skill_directory.name
        )
        skill_readme = (skill_directory / "README.md").read_text(encoding="utf-8")
        if "evals/evals.json" not in skill_readme:
            fail(f"{skill_directory.name}/README.md must link evals/evals.json")
        if "evals/triggers.json" not in skill_readme:
            fail(f"{skill_directory.name}/README.md must link evals/triggers.json")
        validate_evaluations(
            skill_directory / "evals/cases.md",
            skill_directory / "evals/rubric.md",
        )
        catalog_link = f"skills/{skill_directory.name}/"
        for index, readme in enumerate(root_readmes):
            if catalog_link not in readme:
                readme_name = ("README.md", "README.zh-CN.md")[index]
                fail(f"{readme_name} does not list {skill_directory.name}")

    for markdown_file in ROOT.rglob("*.md"):
        if ".git" not in markdown_file.parts:
            validate_relative_links(markdown_file)

    print(f"PASS: validated {len(skill_directories)} skill(s) in {ROOT}")


if __name__ == "__main__":
    main()
