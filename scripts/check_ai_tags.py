#!/usr/bin/env python3
"""
check_ai_tags.py — Enforce AI attribution tags on every new Python function and Java method.

Every newly added function/method in a PR must declare authorship with one of:

  Python / Go:        # generated: copilot — reviewed by: <name>
                      # human-authored

  Java / JS / TS:     // generated: copilot — reviewed by: <name>
                      // human-authored

Exits 0 if all new functions are tagged. Exits 1 if any are missing a tag.

Usage:
  python scripts/check_ai_tags.py [base_ref]
  base_ref defaults to 'origin/main'
"""

import ast
import re
import subprocess
import sys
from pathlib import Path

# Matches either attribution form for Python/Go
TAG_PATTERN_PY = re.compile(r"#\s*(generated:\s*copilot|human-authored)")

# Matches either attribution form for Java/JS/TS
TAG_PATTERN_JAVA = re.compile(r"//\s*(generated:\s*copilot|human-authored)")

# Matches a Java/TS method-like signature line:
# optional modifiers, return type, method name, parameter list, then { or throws
JAVA_METHOD_RE = re.compile(
    r"^\s*(?:(?:public|private|protected|static|final|synchronized|abstract|"
    r"native|default|override|async)\s+)+"
    r"[\w<>\[\],\s]+\s+\w+\s*\([^)]*\)\s*(?:\{|throws\b)"
)


def get_changed_hunks(base_ref: str) -> dict[str, list[int]]:
    """
    Run git diff and return a dict mapping each changed file path to the list
    of line numbers (1-indexed) that were *added* in this diff.
    Only includes .py and .java files.
    """
    result = subprocess.run(
        [
            "git", "diff", f"{base_ref}...HEAD",
            "--unified=0",
            "--diff-filter=AM",
            "--", "*.py", "*.java",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    added_lines: dict[str, list[int]] = {}
    current_file: str | None = None

    for line in result.stdout.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:]
            added_lines.setdefault(current_file, [])
        elif line.startswith("@@") and current_file is not None:
            # @@ -old +new_start[,new_count] @@
            m = re.search(r"\+(\d+)(?:,(\d+))?", line)
            if m:
                start = int(m.group(1))
                count = int(m.group(2)) if m.group(2) is not None else 1
                added_lines[current_file].extend(range(start, start + count))

    return added_lines


def check_python_file(path: Path, added_lines: list[int]) -> list[str]:
    """
    Use the AST to find every function definition whose first line appears in
    added_lines. For each such function, check that its body contains the
    attribution tag. Return a list of violation messages.
    """
    violations: list[str] = []
    added_set = set(added_lines)

    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, OSError) as exc:
        return [f"{path}: could not parse — {exc}"]

    file_lines = source.splitlines()

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.lineno not in added_set:
            continue  # function not newly added in this diff

        # Slice the function body text
        body_start = node.body[0].lineno - 1  # 0-indexed
        body_end = node.end_lineno             # 1-indexed, inclusive
        body_text = "\n".join(file_lines[body_start:body_end])

        if not TAG_PATTERN_PY.search(body_text):
            violations.append(
                f"  {path}:{node.lineno}: '{node.name}()' — missing attribution.\n"
                f"    Add one of:\n"
                f"      # generated: copilot — reviewed by: <name>\n"
                f"      # human-authored"
            )

    return violations


def check_java_file(path: Path, added_lines: list[int]) -> list[str]:
    """
    Scan added lines for Java/TS method signatures using a regex. For each
    matched signature, check the following 30 lines for the attribution tag.
    Return a list of violation messages.
    """
    violations: list[str] = []
    added_set = set(added_lines)

    try:
        file_lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return [f"{path}: could not read — {exc}"]

    for lineno, line in enumerate(file_lines, start=1):
        if lineno not in added_set:
            continue
        if not JAVA_METHOD_RE.match(line):
            continue

        # Check the method header + first 30 lines of body for the tag
        window_end = min(lineno + 30, len(file_lines))
        window_text = "\n".join(file_lines[lineno - 1: window_end])

        if not TAG_PATTERN_JAVA.search(window_text):
            method_name = re.search(r"\b(\w+)\s*\(", line)
            name = method_name.group(1) if method_name else "?"
            violations.append(
                f"  {path}:{lineno}: '{name}()' — missing attribution.\n"
                f"    Add one of:\n"
                f"      // generated: copilot — reviewed by: <name>\n"
                f"      // human-authored"
            )

    return violations


def main() -> int:
    base_ref = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    print(f"Checking AI attribution tags (base: {base_ref})")

    try:
        changed = get_changed_hunks(base_ref)
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git diff failed: {exc}")
        return 1

    if not changed:
        print("No Python or Java files changed — nothing to check.")
        return 0

    all_violations: list[str] = []

    for file_path, added_lines in changed.items():
        if not added_lines:
            continue
        path = Path(file_path)
        if not path.exists():
            continue

        if path.suffix == ".py":
            all_violations.extend(check_python_file(path, added_lines))
        elif path.suffix == ".java":
            all_violations.extend(check_java_file(path, added_lines))

    if all_violations:
        print(f"\nERROR: {len(all_violations)} function(s) missing attribution tags:\n")
        for v in all_violations:
            print(v)
        print(
            "\nEvery new function/method must declare authorship.\n"
            "See CLAUDE.md and AGENTS.md §7 for the required format."
        )
        return 1

    print(f"OK: All new functions/methods in the diff carry attribution tags.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
