#!/usr/bin/env python3
"""Keep declared external-Skill integration explicit and independently reviewable."""

from __future__ import annotations

import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "requirements-clarification"
MANIFEST = SKILL / "external-dependencies.json"
SOURCES_LOCK = ROOT / "docs" / "external-sources.lock.json"


def main() -> None:
    sources_lock = json.loads(SOURCES_LOCK.read_text(encoding="utf-8"))
    assert sources_lock["schema_version"] == 1
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", sources_lock["reviewed_on"])
    sources = {item["id"]: item for item in sources_lock["sources"]}
    assert set(sources) == {"obra-superpowers", "mattpocock-skills"}
    expected_sources = {
        "obra-superpowers": ("https://github.com/obra/superpowers", "b36e0829c6d0140e93cfef2ca599b1b07d4a7797"),
        "mattpocock-skills": ("https://github.com/mattpocock/skills", "84fdeffd12f2ee307994d1eb6feb48173b6e0502"),
    }
    for source_id, (repository, revision) in expected_sources.items():
        assert sources[source_id]["repository"] == repository
        assert sources[source_id]["revision"] == revision
        assert re.fullmatch(r"[0-9a-f]{40}", sources[source_id]["revision"])
        assert sources[source_id]["reviewed_paths"]

    document = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert document["schema_version"] == 1
    assert document["skill_name"] == "requirements-clarification"
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", document["reviewed_on"])

    dependencies = {item["id"]: item for item in document["dependencies"]}
    assert set(dependencies) == {"brainstorming", "grill-me", "grilling"}
    expected = {
        "brainstorming": {
            "upstream_skill": "obra/superpowers:brainstorming",
            "upstream_repository": "obra/superpowers",
            "upstream_path": "skills/brainstorming",
            "required_for_modes": {"brainstorming", "brainstorming_then_grill_me"},
            "invocation": "agent_or_user",
        },
        "grill-me": {
            "upstream_skill": "mattpocock/skills:grill-me",
            "upstream_repository": "mattpocock/skills",
            "upstream_path": "skills/productivity/grill-me",
            "required_for_modes": {"grill_me", "brainstorming_then_grill_me"},
            "invocation": "user_only_wrapper",
        },
        "grilling": {
            "upstream_skill": "mattpocock/skills:grilling",
            "upstream_repository": "mattpocock/skills",
            "upstream_path": "skills/productivity/grilling",
            "required_for_modes": {"grill_me", "brainstorming_then_grill_me"},
            "invocation": "model_invokable_primitive",
        },
    }
    for dependency_id, required in expected.items():
        dependency = dependencies[dependency_id]
        for field, value in required.items():
            if field == "required_for_modes":
                assert set(dependency[field]) == value
            else:
                assert dependency[field] == value
        for field in ("install", "success_handoff", "failure_action"):
            assert isinstance(dependency[field], str) and dependency[field].strip()
        assert dependency["install"].startswith("npx skills@1.5.20 add ")
        assert dependency["source_lock"] in sources
        assert dependency["upstream_repository"] == sources[dependency["source_lock"]]["repository"].removeprefix("https://github.com/")

    assert dependencies["grill-me"]["requires"] == ["grilling"]
    config = (SKILL / "config.example.yaml").read_text(encoding="utf-8")
    for dependency in dependencies.values():
        assert dependency["upstream_skill"] in config
    for document_path in (
        SKILL / "SKILL.md",
        SKILL / "README.md",
        SKILL / "references" / "external-skills.md",
    ):
        content = document_path.read_text(encoding="utf-8")
        assert "external-dependencies.json" in content
        for dependency in dependencies.values():
            assert dependency["upstream_skill"] in content

    benchmark = (ROOT / "docs" / "design-benchmarks.md").read_text(encoding="utf-8")
    assert "external-sources.lock.json" in benchmark
    for source in sources.values():
        assert source["revision"] in benchmark

    print("PASS: external-Skill dependency contract and source locks are complete")


if __name__ == "__main__":
    main()
