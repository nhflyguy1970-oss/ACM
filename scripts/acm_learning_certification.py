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
        "tests/cognitive/test_m5_learning_explainability_cert.py",
        "tests/cognitive/test_m5_learning_stability_cert.py",
        "tests/cognitive/test_diagnostic_safety_learning_cert.py",
        "tests/cognitive/test_conversation_safe_debug_learning_cert.py",
        "tests/cognitive/test_preference_editing_learning_cert.py",
        "tests/cognitive/test_preference_correction_learning_cert.py",
        "tests/cognitive/test_conflict_resolution_learning_cert.py",
        "tests/cognitive/test_identity_correction_learning_cert.py",
        "tests/cognitive/test_relationship_presentation_learning_cert.py",
        "tests/cognitive/test_erase_governance_learning_cert.py",
        "tests/cognitive/test_possession_recall_learning_cert.py",
        "tests/cognitive/test_production_audit_learning_cert.py",
        "tests/behavioral/test_production_audit_conversation.py",
        "tests/behavioral/test_m5_concept_hierarchies.py",
        "tests/behavioral/test_m5_evidence_weighting.py",
        "tests/behavioral/test_m5_prediction_audit.py",
        "tests/behavioral/test_m5_multi_level_abstraction.py",
        "tests/behavioral/test_m5_temporal_patterns.py",
        "tests/behavioral/test_m5_learning_explainability.py",
        "tests/behavioral/test_m5_learning_stability.py",
        "tests/behavioral/test_diagnostic_safety_conversation.py",
        "tests/behavioral/test_conversation_safe_debug_conversation.py",
        "tests/behavioral/test_preference_editing_conversation.py",
        "tests/behavioral/test_preference_correction_conversation.py",
        "tests/behavioral/test_conflict_resolution_conversation.py",
        "tests/behavioral/test_identity_correction_conversation.py",
        "tests/behavioral/test_relationship_presentation_conversation.py",
        "tests/behavioral/test_erase_governance_conversation.py",
        "tests/behavioral/test_possession_recall_conversation.py",
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
