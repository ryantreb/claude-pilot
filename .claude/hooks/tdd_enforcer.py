#!/usr/bin/env python3
"""TDD enforcer - warns when implementation code is modified without failing tests.

This is a SOFT warning system (PostToolUse hook) - edits complete first,
then a warning is shown to encourage TDD practices. Returns exit code 2
for visibility alongside other quality hooks.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

YELLOW = "\033[0;33m"
NC = "\033[0m"

EXCLUDED_EXTENSIONS = [
    ".md",
    ".rst",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".lock",
    ".sum",
    ".env",
    ".env.example",
    ".sql",
    ".tsx",
]

EXCLUDED_DIRS = [
    "/cdk/",
    "/infra/",
    "/infrastructure/",
    "/terraform/",
    "/pulumi/",
    "/stacks/",
    "/cloudformation/",
    "/aws/",
    "/deploy/",
    "/migrations/",
    "/alembic/",
    "/generated/",
    "/proto/",
    "/__generated__/",
    "/dist/",
    "/build/",
    "/node_modules/",
    "/.venv/",
    "/venv/",
    "/__pycache__/",
]


def should_skip(file_path: str) -> bool:
    """Check if file should be skipped based on extension or directory."""
    path = Path(file_path)

    if path.suffix in EXCLUDED_EXTENSIONS:
        return True

    if path.name in EXCLUDED_EXTENSIONS:
        return True

    for excluded_dir in EXCLUDED_DIRS:
        if excluded_dir in file_path:
            return True

    return False


def is_test_file(file_path: str) -> bool:
    """Check if file is a test file."""
    path = Path(file_path)
    name = path.name

    if name.endswith(".py"):
        stem = path.stem
        if stem.startswith("test_") or stem.endswith("_test"):
            return True

    if name.endswith((".test.ts", ".spec.ts", ".test.tsx", ".spec.tsx")):
        return True

    return False


def get_corresponding_test_file(impl_path: str) -> Path | None:
    """Get the corresponding test file for a Python implementation file."""
    path = Path(impl_path)

    parts = path.parts
    stem = path.stem

    test_patterns = [
        path.parent / f"test_{stem}.py",
        path.parent / f"{stem}_test.py",
        path.parent / "tests" / f"test_{stem}.py",
        path.parent / "tests" / "unit" / f"test_{stem}.py",
    ]

    if "steps" in parts:
        steps_idx = parts.index("steps")
        if steps_idx > 0:
            base = Path(*parts[:steps_idx])
            test_patterns.append(base / "tests" / "unit" / "steps" / f"test_{stem}.py")

    for i, part in enumerate(parts):
        if part in ("ccp", "installer", "src"):
            base = Path(*parts[: i + 1])
            test_patterns.append(base / "tests" / "unit" / f"test_{stem}.py")
            break

    for test_path in test_patterns:
        if test_path.exists():
            return test_path

    return None


def has_typescript_test_file(impl_path: str) -> bool:
    """Check if corresponding TypeScript test file exists."""
    path = Path(impl_path)
    directory = path.parent

    if path.name.endswith(".tsx"):
        base_name = path.name[:-4]
        extensions = [".test.tsx", ".spec.tsx", ".test.ts", ".spec.ts"]
    elif path.name.endswith(".ts"):
        base_name = path.name[:-3]
        extensions = [".test.ts", ".spec.ts"]
    else:
        return False

    for ext in extensions:
        test_file = directory / f"{base_name}{ext}"
        if test_file.exists():
            return True

    return False


def warn(message: str, suggestion: str) -> int:
    """Show warning and return exit code 2 for visibility."""
    print("", file=sys.stderr)
    print(f"{YELLOW}TDD: {message}{NC}", file=sys.stderr)
    print(f"{YELLOW}    {suggestion}{NC}", file=sys.stderr)
    return 2


def run_tdd_enforcer() -> int:
    """Run TDD enforcement and return exit code."""
    try:
        hook_data = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return 0

    tool_name = hook_data.get("tool_name", "")
    if tool_name not in ("Write", "Edit"):
        return 0

    tool_input = hook_data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    if not file_path:
        return 0

    if should_skip(file_path):
        return 0

    if is_test_file(file_path):
        return 0

    if file_path.endswith(".py"):
        test_file = get_corresponding_test_file(file_path)

        if test_file is None:
            stem = Path(file_path).stem
            return warn(
                f"No test file found for {stem}.py",
                f"Consider creating test_{stem}.py first.",
            )

        return 0

    if file_path.endswith((".ts", ".tsx")):
        if has_typescript_test_file(file_path):
            return 0

        base_name = Path(file_path).stem
        return warn(
            "No test file found for this module",
            f"Consider creating {base_name}.test.ts first.",
        )

    return 0


if __name__ == "__main__":
    sys.exit(run_tdd_enforcer())
