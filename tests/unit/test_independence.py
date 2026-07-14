from __future__ import annotations

import ast
from pathlib import Path

FORBIDDEN = (
    "aiplatform",
    "mission_control",
    "capability_bus",
    "jarvis",
    "aria.",
)


def test_no_host_imports() -> None:
    root = Path(__file__).resolve().parents[2]
    offenders: list[str] = []
    for path in (root / "acm").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            mod = ""
            if isinstance(node, ast.Import):
                for alias in node.names:
                    mod = alias.name
            elif isinstance(node, ast.ImportFrom) and node.module:
                mod = node.module
            else:
                continue
            lowered = mod.lower()
            if any(tok in lowered for tok in FORBIDDEN):
                offenders.append(f"{path}:{mod}")
    assert not offenders, offenders
