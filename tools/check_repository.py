"""Dependency-free repository and handoff checks (Python 3.10+ and Git)."""

import argparse
from datetime import date
import os
from pathlib import Path
import posixpath
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit


ROUTES = ("AGENTS.md", "CLAUDE.md", ".github/copilot-instructions.md",
          ".cursor/rules/project.mdc")
REQUIRED = ("README.md", "RULES.md", "HANDOFF.md", *ROUTES)
HANDOFF_SECTIONS = ("当前状态", "本轮变更", "已执行的验证", "未验证与阻塞",
                    "下一步", "跨 clone 接续")
LINK = re.compile(r"\[[^\]]*\]\((<[^>]+>|[^\s)]+)(?:\s+[\"'].*?[\"'])?\)")


class CheckError(Exception):
    pass


def git(root, *args, optional=False):
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True,
        text=True, encoding="utf-8",
    )
    if result.returncode:
        if optional:
            return None
        raise CheckError(f"git {' '.join(args)}: {result.stderr.strip()}")
    return result.stdout


class Snapshot:
    def __init__(self, root, revision=None, staged=False):
        self.root, self.revision, self.staged = root, revision, staged
        if staged:
            listing = git(root, "ls-files", "--cached", "-z")
        elif revision:
            listing = git(root, "ls-tree", "-rz", "--name-only", revision)
        else:
            listing = git(root, "ls-files", "--cached", "--others",
                          "--exclude-standard", "-z")
        self.paths = set(filter(None, listing.split("\0")))
        if not staged and not revision:
            self.paths = {p for p in self.paths if (root / p).is_file()}

    def read(self, name):
        if name not in self.paths:
            return None
        if self.staged:
            return git(self.root, "show", f":{name}")
        if self.revision:
            return git(self.root, "show", f"{self.revision}:{name}")
        return (self.root / name).read_text(encoding="utf-8")


def validate_snapshot(snapshot):
    errors = []
    for required in REQUIRED:
        if required not in snapshot.paths:
            errors.append(f"Missing required file: {required}")
    for route in ROUTES:
        content = snapshot.read(route) or ""
        if not all(name in content for name in ("RULES.md", "HANDOFF.md")):
            errors.append(f"{route}: must point to RULES.md and HANDOFF.md")

    handoff = snapshot.read("HANDOFF.md") or ""
    updated = re.search(r"^Updated: (\d{4}-\d{2}-\d{2})$", handoff, re.MULTILINE)
    try:
        if not updated:
            raise ValueError()
        date.fromisoformat(updated[1])
    except ValueError:
        errors.append("HANDOFF.md: expected valid Updated: YYYY-MM-DD")
    sections = dict(re.findall(r"^## ([^\n]+)\n(.*?)(?=^## |\Z)", handoff,
                               re.MULTILINE | re.DOTALL))
    for name in HANDOFF_SECTIONS:
        if not sections.get(name, "").strip():
            errors.append(f"HANDOFF.md: missing or empty section: {name}")

    for name in sorted(snapshot.paths):
        if not name.endswith((".md", ".mdc")):
            continue
        content = snapshot.read(name)
        if not content.endswith("\n"):
            errors.append(f"{name}: missing final newline")
        fence = None
        for number, line in enumerate(content.splitlines(), 1):
            marker = re.match(r"^\s*(`{3,}|~{3,})", line)
            if marker:
                if fence is None:
                    fence = marker[1]
                elif marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                    fence = None
                continue
            if fence:
                continue
            if line.rstrip() != line:
                errors.append(f"{name}:{number}: trailing whitespace")
            for match in LINK.finditer(line):
                href = match[1].strip("<>")
                parsed = urlsplit(href)
                if parsed.scheme or not parsed.path:
                    continue
                target = unquote(parsed.path)
                if target.startswith("/"):
                    resolved = posixpath.normpath(target.lstrip("/"))
                else:
                    resolved = posixpath.normpath(posixpath.join(
                        posixpath.dirname(name), target))
                if resolved == ".." or resolved.startswith("../"):
                    errors.append(f"{name}:{number}: link escapes repository: {href}")
                elif resolved not in snapshot.paths and not any(
                        p.startswith(resolved.rstrip("/") + "/") for p in snapshot.paths):
                    errors.append(f"{name}:{number}: missing link target: {href}")
        if fence:
            errors.append(f"{name}: unclosed code fence")
    return errors


def meaningful(text):
    body = re.sub(r"^Updated:.*$", "", text or "", flags=re.MULTILINE)
    return re.sub(r"\s+", "", body)


def validate_change(root, before, after, *, staged=False, label="staged changes"):
    args = ["diff", "--name-only", "-z", "--no-renames"]
    if staged:
        args.append("--cached")
        if before:
            args.append(before)
    elif before:
        args.extend([before, after])
    else:
        args = ["diff-tree", "--root", "--no-commit-id", "--name-only", "-r", "-z",
                "--no-renames", after]
    args.append("--")
    changed = set(filter(None, git(root, *args).split("\0")))
    if not (changed - {"HANDOFF.md"}):
        return []
    current = Snapshot(root, revision=after, staged=staged)
    # Commits predating the rule are historical evidence, not violations.
    previous_rules = git(root, "show", f"{before}:RULES.md", optional=True) if before else None
    if not staged and "RULES.md" not in current.paths and previous_rules is None:
        return []
    previous = git(root, "show", f"{before}:HANDOFF.md", optional=True) if before else ""
    if "HANDOFF.md" not in changed or meaningful(previous) == meaningful(current.read("HANDOFF.md")):
        return [f"{label}: update and stage a substantive HANDOFF.md change in the same commit"]
    return []


def validate_history(root, base):
    if base:
        resolved = git(root, "rev-parse", "--verify", f"{base}^{{commit}}", optional=True)
        if not resolved:
            raise CheckError(f"Invalid or unavailable base: {base}; fetch complete Git history")
        revision_range = f"{resolved.strip()}..HEAD"
    else:
        revision_range = "HEAD"
    commits = git(root, "rev-list", "--reverse", revision_range).splitlines()
    errors = []
    for commit in commits:
        parents = git(root, "show", "-s", "--format=%P", commit).split()
        errors.extend(validate_change(root, parents[0] if parents else None, commit,
                                      label=f"commit {commit[:12]}"))
    return errors


def main():
    # Keep diagnostics readable through Windows pipes as well as terminals.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--staged", action="store_true", help="validate the Git index before commit")
    mode.add_argument("--base", help="validate HEAD and each commit after this ref")
    mode.add_argument("--ci", action="store_true", help="use REPOSITORY_BASE from CI")
    args = parser.parse_args()
    try:
        root = Path(git(Path.cwd(), "rev-parse", "--show-toplevel").strip())
        committed = bool(args.base or args.ci)
        snapshot = Snapshot(root, revision="HEAD" if committed else None, staged=args.staged)
        errors = validate_snapshot(snapshot)
        if args.staged:
            head = git(root, "rev-parse", "--verify", "HEAD", optional=True)
            errors.extend(validate_change(root, head.strip() if head else None, None, staged=True))
        elif committed:
            base = args.base if args.base else os.environ.get("REPOSITORY_BASE", "")
            # GitHub uses all-zero before SHA for an initial push or new branch.
            if base and set(base) == {"0"}:
                base = None
            errors.extend(validate_history(root, base))
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print(f"Repository checks passed ({len(snapshot.paths)} files; "
              f"{'index' if args.staged else 'HEAD/history' if committed else 'working tree'}).")
        return 0
    except (CheckError, OSError, UnicodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
