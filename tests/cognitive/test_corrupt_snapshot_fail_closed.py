"""Corrupt durable load must fail closed (never empty-overwrite)."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from acm.core.store import CognitiveStore
from acm.persistence import DurableCognitiveStore
from acm.persistence.sqlite import SqliteDurableStore


def test_corrupt_snapshot_refuses_empty_store(tmp_path: Path) -> None:
    path = tmp_path / "corrupt.db"
    store = SqliteDurableStore(path, max_snapshots=8)
    store.save(CognitiveStore(), kind="good")
    # Corrupt latest payload checksum/body
    with store._lock:
        store._conn.execute(
            "UPDATE snapshots SET payload=? WHERE id=(SELECT MAX(id) FROM snapshots)",
            (json.dumps({"schema_version": 1, "checksum": "dead", "store": {}}),),
        )
        store._conn.commit()
    store.close()

    with pytest.raises(RuntimeError, match="durable load failed"):
        DurableCognitiveStore(path)
