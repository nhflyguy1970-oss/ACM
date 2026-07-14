#!/usr/bin/env python3
"""Fail if ACM imports forbidden host stacks."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

FORBIDDEN = ("aiplatform", "mission_control", "capability_bus", "jarvis")
ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    offenders: list[str] = []
    for path in (ROOT / "acm").rglob("*.py"):
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
            if any(tok in mod.lower() for tok in FORBIDDEN):
                offenders.append(f"{path.relative_to(ROOT)}:{mod}")
    if offenders:
        print("Forbidden host imports:\n" + "\n".join(offenders))
        return 1
    print("Independence OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
