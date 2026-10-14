"""Exercise the handoff gate against real, isolated Git indexes and history."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CHECKER = Path(__file__).resolve().parents[1] / "tools" / "check_repository.py"
HANDOFF = """# Handoff

Updated: 2026-10-14

## 当前状态
Repository preparation; game checks NOT_RUN.

## 本轮变更
Initial repository workflow.

## 已执行的验证
No game execution.

## 未验证与阻塞
Windows game installation is not connected.

## 下一步
Connect Windows and run E0.

## 跨 clone 接续
Commit, synchronize, then clone.
"""


class RepositoryChecksTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="strategic-mind-checks-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Repository Test")
        self.git("config", "user.email", "repository-test@example.invalid")
        self.git("config", "core.hooksPath", ".disabled-test-hooks")
        self.git("config", "core.autocrlf", "false")
        self.git("config", "commit.gpgsign", "false")
        self.write("README.md", "# Test\n\n[Rules](RULES.md)\n")
        self.write("RULES.md", "# Rules\n\nUpdate HANDOFF.md in every change.\n")
        self.write("HANDOFF.md", HANDOFF)
        for entry in ("AGENTS.md", "CLAUDE.md", ".github/copilot-instructions.md",
                      ".cursor/rules/project.mdc"):
            self.write(entry, "Read RULES.md and HANDOFF.md first.\n")
        self.git("add", ".")
        self.git("commit", "-qm", "initial workflow")
        self.base = self.git("rev-parse", "HEAD").stdout.strip()

    def git(self, *args):
        return subprocess.run(
            ["git", *args], cwd=self.root, capture_output=True,
            text=True, encoding="utf-8", check=True,
        )

    def write(self, name, content):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def run_check(self, *args, extra_env=None):
        env = os.environ.copy()
        env.update(extra_env or {})
        return subprocess.run(
            [sys.executable, str(CHECKER), *args], cwd=self.root,
            capture_output=True, text=True, encoding="utf-8", env=env,
        )

    def assert_ok(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def assert_error(self, result, expected):
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(expected, result.stdout + result.stderr)

    def change_readme(self):
        self.write("README.md", "# Updated\n\n[Rules](RULES.md)\n")
        self.git("add", "README.md")

    def update_handoff(self):
        self.write("HANDOFF.md", HANDOFF.replace(
            "Initial repository workflow.", "Added the next documented experiment."))
        self.git("add", "HANDOFF.md")

    def test_clean_working_tree_passes(self):
        self.assert_ok(self.run_check())

    def test_missing_handoff_is_rejected(self):
        (self.root / "HANDOFF.md").unlink()
        self.assert_error(self.run_check(), "HANDOFF.md")

    def test_empty_handoff_section_is_rejected(self):
        self.write("HANDOFF.md", HANDOFF.replace("Connect Windows and run E0.", ""))
        self.assert_error(self.run_check(), "下一步")

    def test_broken_link_is_rejected(self):
        self.write("README.md", "# Test\n\n[Missing](docs/missing.md)\n")
        self.assert_error(self.run_check(), "docs/missing.md")

    def test_link_with_space_unicode_and_fenced_example(self):
        self.write("docs/中文 notes.md", "# Notes\n")
        self.write("README.md", '# Test\n\n[Notes](<docs/中文 notes.md>)\n\n'
                   '```text\n[Example](not-created.md)\n```\n')
        self.assert_ok(self.run_check())

    def test_entry_must_route_to_both_rules_and_handoff(self):
        self.write("CLAUDE.md", "Read RULES.md.\n")
        self.assert_error(self.run_check(), "CLAUDE.md")

    def test_staged_change_requires_handoff(self):
        self.change_readme()
        self.assert_error(self.run_check("--staged"), "HANDOFF.md")

    def test_unstaged_handoff_does_not_satisfy_gate(self):
        self.change_readme()
        self.write("HANDOFF.md", HANDOFF.replace("Initial", "Updated"))
        self.assert_error(self.run_check("--staged"), "HANDOFF.md")

    def test_whitespace_only_handoff_is_rejected(self):
        self.change_readme()
        self.write("HANDOFF.md", HANDOFF + "\n")
        self.git("add", "HANDOFF.md")
        self.assert_error(self.run_check("--staged"), "HANDOFF.md")

    def test_meaningful_staged_handoff_passes(self):
        self.change_readme()
        self.update_handoff()
        self.assert_ok(self.run_check("--staged"))

    def test_date_only_handoff_is_rejected(self):
        self.change_readme()
        self.write("HANDOFF.md", HANDOFF.replace("2026-10-14", "2026-10-15"))
        self.git("add", "HANDOFF.md")
        self.assert_error(self.run_check("--staged"), "HANDOFF.md")

    def test_unicode_diagnostics_work_with_ascii_process_default(self):
        self.write("HANDOFF.md", HANDOFF.replace("Connect Windows and run E0.", ""))
        self.assert_error(self.run_check(extra_env={"PYTHONIOENCODING": "ascii"}), "下一步")

    def test_handoff_only_commit_passes(self):
        self.update_handoff()
        self.assert_ok(self.run_check("--staged"))

    def test_staged_snapshot_ignores_unstaged_repairs(self):
        self.write("README.md", "# Broken\n\n[Missing](missing.md)\n")
        self.git("add", "README.md")
        self.update_handoff()
        self.write("README.md", "# Repaired only in worktree\n")
        self.assert_error(self.run_check("--staged"), "missing.md")

    def test_deleting_a_tracked_file_requires_handoff(self):
        self.write("note.txt", "temporary fixture\n")
        self.update_handoff()
        self.git("add", "note.txt")
        self.git("commit", "-qm", "add note")
        self.git("rm", "-q", "note.txt")
        self.assert_error(self.run_check("--staged"), "HANDOFF.md")

    def test_valid_commit_range_passes(self):
        self.change_readme()
        self.update_handoff()
        self.git("commit", "-qm", "document experiment")
        self.assert_ok(self.run_check("--base", self.base))

    def test_later_handoff_does_not_hide_earlier_missing_update(self):
        self.change_readme()
        self.git("commit", "-qm", "forgot handoff")
        self.update_handoff()
        self.git("commit", "-qm", "later handoff")
        self.assert_error(self.run_check("--base", self.base), "HANDOFF.md")

    def test_legacy_commit_before_rules_is_not_retroactively_blocked(self):
        self.git("rm", "-q", "RULES.md", "HANDOFF.md")
        self.git("commit", "-qm", "legacy state without workflow")
        legacy = self.git("rev-parse", "HEAD").stdout.strip()
        self.write("RULES.md", "# Rules\n")
        self.write("HANDOFF.md", HANDOFF.replace("Initial", "Restored"))
        self.git("add", ".")
        self.git("commit", "-qm", "introduce workflow")
        self.assert_ok(self.run_check("--base", legacy))

    def test_invalid_base_fails_with_actionable_message(self):
        self.assert_error(self.run_check("--base", "missing-ref"), "missing-ref")

    def test_removing_rules_cannot_disable_handoff_gate(self):
        self.git("rm", "-q", "RULES.md")
        self.git("commit", "-qm", "remove rules without handoff")
        self.write("RULES.md", "# Restored rules\n")
        self.update_handoff()
        self.git("add", "RULES.md")
        self.git("commit", "-qm", "restore rules later")
        self.assert_error(self.run_check("--base", self.base), "HANDOFF.md")

    def test_ci_new_branch_checks_available_history(self):
        self.assert_ok(self.run_check("--ci", extra_env={"REPOSITORY_BASE": "0" * 40}))


if __name__ == "__main__":
    unittest.main()
