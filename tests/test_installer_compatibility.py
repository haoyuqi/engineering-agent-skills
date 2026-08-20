#!/usr/bin/env python3
"""Install one Skill into representative Agent layouts and compare resources."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parent.parent
SKILLS_CLI_VERSION = "1.5.20"
INSTALL_TIMEOUT_SECONDS = 180


def project_skill_layouts() -> dict[str, Path]:
    contract = json.loads((ROOT / "docs" / "compatibility.json").read_text(encoding="utf-8"))
    assert contract["schema_version"] == 1
    agents = contract["verified_project_agents"]
    layouts = {item["id"]: Path(item["project_skill_root"]) for item in agents}
    assert layouts == {
        "codex": Path(".agents/skills"),
        "claude-code": Path(".claude/skills"),
        "opencode": Path(".agents/skills"),
        "github-copilot": Path(".agents/skills"),
    }
    return layouts


def file_digests(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


def main() -> None:
    environment = os.environ.copy()
    environment.update({"CI": "1", "DISABLE_TELEMETRY": "1", "NO_COLOR": "1"})
    source_skills = sorted(
        path for path in (ROOT / "skills").iterdir() if (path / "SKILL.md").is_file()
    )
    assert source_skills
    layouts = project_skill_layouts()
    with tempfile.TemporaryDirectory(prefix="skill-installer-") as temp:
        destination = Path(temp)
        command = [
            "npx",
            "--yes",
            f"skills@{SKILLS_CLI_VERSION}",
            "add",
            str(ROOT),
            "--skill",
            "*",
        ]
        for agent in layouts:
            command.extend(["--agent", agent])
        command.extend(["--copy", "--yes"])
        try:
            subprocess.run(
                command,
                cwd=destination,
                env=environment,
                check=True,
                timeout=INSTALL_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired as error:
            raise AssertionError(
                f"skills CLI exceeded {INSTALL_TIMEOUT_SECONDS}s; check npm access and pinned version"
            ) from error

        expected_names = {path.name for path in source_skills}
        layout_roots = {
            agent: destination / layout for agent, layout in layouts.items()
        }
        for agent, layout_root in layout_roots.items():
            assert layout_root.is_dir(), f"{agent} project layout was not created: {layout_root}"
            assert {path.name for path in layout_root.iterdir()} == expected_names
            for source in source_skills:
                assert file_digests(layout_root / source.name) == file_digests(source)

        vulnerability_copy = layout_roots["codex"] / "repository-vulnerabilities"
        assert (vulnerability_copy / "evals" / "fixtures" / "composer.lock").is_file()
        assert (vulnerability_copy / "scripts" / "normalize_audit.py").is_file()

    print("PASS: all target Agent project layouts receive identical complete resources for every Skill")


if __name__ == "__main__":
    main()
