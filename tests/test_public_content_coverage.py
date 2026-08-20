#!/usr/bin/env python3
"""Regression tests for extension-independent public-content scanning."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import test_public_content as public_content  # noqa: E402


def main() -> None:
    assert public_content.should_scan(Path("fixtures/example.composer.lock"))
    assert public_content.should_scan(Path("fixtures/example.toml"))
    assert public_content.read_text_if_safe(Path("unused"), b"plain UTF-8") == "plain UTF-8"
    assert public_content.read_text_if_safe(Path("unused"), b"\0binary") is None
    assert public_content.read_text_if_safe(
        Path("unused"), b"x" * (public_content.MAX_TEXT_BYTES + 1)
    ) is None
    print("PASS: public-content scanning covers UTF-8 lockfiles and other text files")


if __name__ == "__main__":
    main()
