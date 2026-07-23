#!/usr/bin/env python3
"""Standalone M4 Learning Certification runner."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    cmd = [
        str(ROOT / ".venv/bin/pytest"),
        "tests/cognitive/test_m4_learning_certification.py",
        "tests/cognitive/test_m4_aml_capabilities.py",
        "tests/cognitive/test_m5_hierarchy_learning_cert.py",
        "tests/cognitive/test_m5_evidence_decay_learning_cert.py",
        "tests/cognitive/test_m5_prediction_audit_learning_cert.py",
        "tests/cognitive/test_m5_abstraction_learning_cert.py",
        "tests/cognitive/test_m5_temporal_pattern_learning_cert.py",
        "tests/behavioral/test_m5_concept_hierarchies.py",
        "tests/behavioral/test_m5_evidence_weighting.py",
        "tests/behavioral/test_m5_prediction_audit.py",
        "tests/behavioral/test_m5_multi_level_abstraction.py",
        "tests/behavioral/test_m5_temporal_patterns.py",
        "tests/behavioral/test_learning_assent_apply.py",
        "tests/behavioral/test_goal_learning.py",
        "tests/behavioral/test_lifecycle_learning.py",
        "tests/cognitive/test_privacy_redaction.py",
        "-q",
    ]
    print("Running:", " ".join(cmd), flush=True)
    proc = subprocess.run(cmd, cwd=ROOT)
    report = {
        "suite": "learning_certification",
        "exit_code": proc.returncode,
        "doc": "docs/LEARNING_CERTIFICATION.md",
    }
    out = Path("/tmp/acm_learning_cert.json")
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report), flush=True)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
