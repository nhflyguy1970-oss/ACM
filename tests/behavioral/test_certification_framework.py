from __future__ import annotations

from pathlib import Path

from acm.certification import CertificationFramework


def test_certification_framework_builds_report_not_certified(tmp_path: Path) -> None:
    fw = CertificationFramework(workdir=tmp_path / "cert")
    report = fw.run_all()
    assert report["schema"] == "acm.certification/0.13"
    assert report["certified"] is False
    assert report["total"] >= 1
    assert Path(report["report_path"]).exists()
    # Phase 2 builds gates; may be all green, but never claims certification
    assert "Formal certification requires explicit approval" in report["note"]
