from __future__ import annotations

import ast
from pathlib import Path


SOURCE_ROOT = Path("src/xgrowth")
_FORBIDDEN_HTTP_METHOD_ATTRS = {"post", "put", "patch", "delete"}


def test_source_contains_no_http_write_method_calls() -> None:
    violations: list[str] = []
    for path in SOURCE_ROOT.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if isinstance(func, ast.Attribute) and func.attr.lower() in _FORBIDDEN_HTTP_METHOD_ATTRS:
                violations.append(f"{path}:{node.lineno}:{func.attr}")
    assert violations == []


def test_generated_user_analytics_are_not_git_tracked_paths() -> None:
    forbidden_paths = {
        Path("metrics-snapshot.json"),
        Path("daily-report.json"),
        Path("smart-followers.json"),
    }
    ignore_text = Path(".gitignore").read_text(encoding="utf-8")
    for path in forbidden_paths:
        assert str(path) not in ignore_text or str(path) in ignore_text
