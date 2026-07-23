"""Production-readiness audit certifications (permanent).

Locks in governance fixes discovered during the ACM/Aria 1.0 platform audit:
read-only write spine, identity assent via encode, snapshot retention.
"""

from __future__ import annotations

from pathlib import Path

from acm import CognitiveEngine
from acm.authority.mode import read_only
from acm.persistence.sqlite import SqliteDurableStore
from acm.provenance import TRUSTED_USER_STATEMENT


def test_audit_encode_blocked_under_read_only() -> None:
    eng = CognitiveEngine(agent_id="audit-ro")
    with read_only():
        out = eng.encode("My name is Jeff.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    assert out.get("encoded") is False
    assert out.get("reason") == "read_only_blocked"
    assert len(eng.store.experiences) == 0


def test_audit_cool_and_reactivate_blocked_under_read_only() -> None:
    eng = CognitiveEngine(agent_id="audit-cool")
    eng.encode("I prefer pizza.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    cid = next(iter(eng.store.concepts))
    with read_only():
        cool = eng.cool_memory(cid)
        react = eng.reactivate_memory(cid)
    assert cool.get("cooled") is False
    assert cool.get("reason") == "read_only_blocked"
    assert react.get("reactivated") is False
    assert react.get("reason") == "read_only_blocked"


def test_audit_assent_identity_births_experience() -> None:
    eng = CognitiveEngine(agent_id="audit-assent")
    eng.encode("My name is Jeff.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    before = len(eng.store.experiences)
    prop = eng.propose_identity_change(key="name", value="Jeffrey", who="user")
    out = eng.assent_identity(prop["proposal"]["id"])
    assert out.get("assented") is True
    assert out.get("experience_id")
    assert len(eng.store.experiences) > before
    assert "jeffrey" in eng.cognitive_respond("Who am I?")["memory"].lower()


def test_audit_sqlite_snapshot_prunes(tmp_path: Path) -> None:
    path = tmp_path / "acm_audit_prune.db"
    store = SqliteDurableStore(path, max_snapshots=3)
    from acm.core.store import CognitiveStore

    for i in range(8):
        s = CognitiveStore()
        # Minimal save cycle — payload is empty store each time
        out = store.save(s, kind=f"c{i}")
        assert out["ok"] is True
    count = store._conn.execute("SELECT COUNT(*) FROM snapshots").fetchone()[0]
    assert count == 3
    store.close()
