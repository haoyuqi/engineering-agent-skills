#!/usr/bin/env python3
"""Offline regression tests; all credential-shaped inputs are synthetic."""

from __future__ import annotations

from contextlib import redirect_stdout
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import test_public_content as scanner  # noqa: E402


def synthetic_token() -> str:
    return "gh" + "p_" + "a" * 24


class ContentTests(unittest.TestCase):
    def test_multiple_findings_without_values(self):
        token = synthetic_token()
        output = io.StringIO()
        scan = scanner.Scan()
        with redirect_stdout(output):
            scan.inspect("fixture.txt", (token + "\n" + token).encode())
            self.assertEqual(scan.finish(), 1)
        self.assertEqual(scan.blocked, 2)
        self.assertNotIn(token, output.getvalue())
        self.assertIn(":2", output.getvalue())

    def test_public_links_and_example_email(self):
        self.assertEqual(scanner.findings("https://www.python.org/docs user@example.org"), [])

    def test_review_warnings_do_not_block(self):
        value = "/" + "home/" + "fictional/file"
        scan = scanner.Scan()
        with redirect_stdout(io.StringIO()):
            scan.inspect("example.toml", value.encode())
            self.assertEqual(scan.finish(), 0)
        self.assertEqual(scan.reviews, 1)

    def test_rules(self):
        values = [
            "-" * 5 + "BEGIN PRIVATE KEY" + "-" * 5,
            "github_" + "pat_" + "a" * 30,
            "gl" + "pat-" + "a" * 24,
            "npm" + "_" + "a" * 35,
            "xox" + "b-" + "a" * 24,
            "AK" + "IA" + "A" * 16,
            "Bearer " + "a" * 24,
            "https://" + "user:password@" + "example.org",
        ]
        for value in values:
            self.assertTrue(any(level == "BLOCK" for level, _, _ in scanner.findings(value)))

    def test_incomplete_is_not_pass(self):
        for raw in (b"\0binary", b"\xff", b"x" * (scanner.MAX_TEXT_BYTES + 1),
                    b"version https://git-lfs.github.com/spec/v1\n"):
            scan = scanner.Scan()
            with redirect_stdout(io.StringIO()):
                scan.inspect("fixture.bin", raw)
                self.assertEqual(scan.finish(), 2)

    def test_label_redaction(self):
        self.assertNotIn(synthetic_token(), scanner.safe_label(synthetic_token()))


class HistoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repository"
        self.root.mkdir()
        self.patch = patch.object(scanner, "ROOT", self.root)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.git("init", "-q")
        self.git("config", "user.name", "Fictional Test")
        self.git("config", "user.email", "test@example.org")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.hooksPath", str(self.root / "no-hooks"))
        self.commit("baseline", "safe")

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args],
                                       stderr=subprocess.DEVNULL).decode().strip()

    def commit(self, message, content):
        (self.root / "fixture.lock").write_text(content)
        self.git("add", "fixture.lock")
        self.git("commit", "--allow-empty", "-qm", message)
        return self.git("rev-parse", "HEAD")

    def test_intermediate_commit_cannot_hide_deleted_token(self):
        base = self.git("rev-parse", "HEAD")
        self.commit("synthetic addition", synthetic_token())
        self.commit("remove synthetic data", "safe")
        scan = scanner.Scan()
        with redirect_stdout(io.StringIO()):
            scanner.scan_history(scan, base)
        self.assertEqual(scan.blocked, 1)

    def test_dedup_and_empty_range_final_snapshot(self):
        tip = self.commit("another message", "safe")
        scan = scanner.Scan()
        with redirect_stdout(io.StringIO()):
            scanner.scan_history(scan)
        self.assertEqual(len(scan.seen), 1)
        self.assertEqual(scan.checked, 3)  # Two messages plus one unique blob.
        scan = scanner.Scan()
        with redirect_stdout(io.StringIO()):
            scanner.scan_history(scan, tip, tip)
        self.assertEqual(scan.checked, 2)

    def test_commit_message_scanned(self):
        self.commit(synthetic_token(), "safe")
        scan = scanner.Scan()
        with redirect_stdout(io.StringIO()):
            scanner.scan_history(scan)
        self.assertEqual(scan.blocked, 1)

    def test_shallow_clone_rejected(self):
        clone = Path(self.temp.name) / "shallow"
        self.git("clone", "-q", "--depth=1", self.root.as_uri(), str(clone))
        with patch.object(scanner, "ROOT", clone):
            with self.assertRaises(ValueError):
                scanner.scan_history(scanner.Scan())

    def test_missing_ref_rejected(self):
        with self.assertRaises(subprocess.CalledProcessError):
            scanner.scan_history(scanner.Scan(), "missing-ref")

    def test_all_text_extensions_and_no_file_exemptions(self):
        for name in ("LICENSE", "example.toml", "test_public_content.py"):
            (self.root / name).write_text(synthetic_token())
        scan = scanner.Scan()
        with redirect_stdout(io.StringIO()):
            scanner.scan_worktree(scan)
        self.assertEqual(scan.blocked, 3)

    def test_symlink_does_not_read_destination(self):
        external = Path(self.temp.name) / "outside.txt"
        external.write_text(synthetic_token())
        (self.root / "link").symlink_to(external)
        scan = scanner.Scan()
        with redirect_stdout(io.StringIO()):
            scanner.scan_worktree(scan)
        self.assertEqual(scan.blocked, 0)

    def test_final_snapshot_includes_merge_resolution(self):
        base = self.git("rev-parse", "HEAD")
        self.git("checkout", "-qb", "side")
        self.commit("side change", "side")
        self.git("checkout", "-qb", "target", base)
        (self.root / "target.txt").write_text("target")
        self.git("add", "target.txt")
        self.git("commit", "-qm", "target change")
        self.git("merge", "--no-ff", "--no-commit", "side")
        (self.root / "fixture.lock").write_text(synthetic_token())
        self.git("add", "fixture.lock")
        self.git("commit", "-qm", "synthetic merge result")
        scan = scanner.Scan()
        with redirect_stdout(io.StringIO()):
            scanner.scan_history(scan, "HEAD", "HEAD")
        self.assertEqual(scan.blocked, 1)


class WorkflowTests(unittest.TestCase):
    def test_complete_history_and_explicit_pr_range(self):
        workflow = (ROOT / ".github/workflows/validate.yml").read_text()
        self.assertIn("fetch-depth: 0", workflow)
        self.assertIn("persist-credentials: false", workflow)
        self.assertIn("github.event.pull_request.base.sha", workflow)
        self.assertIn("github.event.pull_request.head.sha", workflow)
        self.assertIn('--base "$BASE_SHA" --head "$HEAD_SHA"', workflow)
        self.assertIn('--base HEAD --head HEAD', workflow)
        self.assertIn('--base "$BEFORE_SHA" --head HEAD', workflow)


if __name__ == "__main__":
    unittest.main()
