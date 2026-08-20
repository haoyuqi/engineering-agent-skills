#!/usr/bin/env python3
"""Keep cross-Agent installation claims tied to one readable data contract."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    contract = json.loads((ROOT / "docs" / "compatibility.json").read_text(encoding="utf-8"))
    assert contract["schema_version"] == 1
    agents = contract["verified_project_agents"]
    expected = {
        "codex": ".agents/skills",
        "claude-code": ".claude/skills",
        "opencode": ".agents/skills",
        "github-copilot": ".agents/skills",
    }
    assert {item["id"]: item["project_skill_root"] for item in agents} == expected
    for item in agents:
        assert isinstance(item["display_name"], str) and item["display_name"].strip()

    document = (ROOT / "docs" / "compatibility.md").read_text(encoding="utf-8")
    assert "compatibility.json" in document
    for agent, location in expected.items():
        assert f"`{agent}`" in document
        assert f"`{location}/<skill-name>/`" in document
    for readme_name in ("README.md", "README.zh-CN.md"):
        assert "docs/compatibility.md" in (ROOT / readme_name).read_text(encoding="utf-8")
    print(f"PASS: compatibility contract documents {len(agents)} verified Agent layout(s)")


if __name__ == "__main__":
    main()
