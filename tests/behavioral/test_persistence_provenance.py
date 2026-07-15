from __future__ import annotations

from pathlib import Path

from acm import CognitiveEngine
from acm.persistence import DurableCognitiveStore, export_store, verify_snapshot


def test_sqlite_persist_roundtrip(tmp_path: Path) -> None:
    db = tmp_path / "acm.sqlite"
    eng = CognitiveEngine(agent_id="p", persist_path=str(db), auto_persist=True)
    eng.encode("Harbor lights guide ships.", pin=True)
    eng.flush()
    assert eng.verify_persistence()["ok"] is True
    eng2 = CognitiveEngine(agent_id="p", persist_path=str(db))
    assert len(eng2.store.experiences) >= 1
    assert len(eng2.store.provenance) >= 1


def test_export_import_checksum(tmp_path: Path) -> None:
    eng = CognitiveEngine(agent_id="p")
    eng.encode("Tea is warm.", pin=True)
    dest = tmp_path / "snap.json"
    out = eng.export_snapshot(str(dest))
    assert out["ok"] is True
    snap = export_store(eng.store)
    assert verify_snapshot(snap) == []
    eng2 = CognitiveEngine(agent_id="p2")
    eng2.import_snapshot(str(dest))
    assert len(eng2.store.experiences) >= 1


def test_backup_restore(tmp_path: Path) -> None:
    db = tmp_path / "acm.sqlite"
    bak = tmp_path / "acm.bak"
    durable = DurableCognitiveStore(db)
    eng = CognitiveEngine(agent_id="p")
    eng.encode("Backup subject.", pin=True)
    durable.store = eng.store
    durable.flush()
    durable.backup(bak)
    n = len(durable.store.experiences)
    eng.encode("After backup.", pin=True)
    durable.flush()
    durable.restore(bak)
    assert len(durable.store.experiences) == n
    durable.close()


def test_provenance_not_fabricated() -> None:
    eng = CognitiveEngine(agent_id="prov")
    payload = eng.encode("Source provenance sample.", pin=True)
    rows = eng.provenance_of(payload["experience_id"])
    assert rows
    assert all(r["fabricated"] is False for r in rows)
    assert rows[0]["origin"] == "encode"
