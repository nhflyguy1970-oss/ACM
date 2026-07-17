from __future__ import annotations

from acm.provenance import TRUSTED_USER_STATEMENT
from aria_memory_adapter import AcmMemoryAdapter, FeatureFlags


class _Legacy:
    def remember(self, text: str, **kwargs):  # noqa: ANN001
        return {"ok": True, "text": text, "id": "L1", "confidence": 0.8}

    def recall(self, query: str, **kwargs):  # noqa: ANN001
        return {"ok": True, "answer": "legacy coffee facts", "confidence": 0.85}

    def health(self):
        return {"ok": True, "backend": "test"}


def test_shadow_legacy_authoritative() -> None:
    ad = AcmMemoryAdapter(legacy=_Legacy(), flags=FeatureFlags())
    remembered = ad.remember(
        "Coffee is bitter.",
        ingestion_provenance=TRUSTED_USER_STATEMENT,
    )
    assert remembered["authoritative"] == "legacy"
    assert remembered["user_visible_changed"] is False
    assert remembered["acm_shadow"] is not None
    assert remembered["acm_shadow"]["encoded"] is True
    recalled = ad.recall("coffee")
    assert recalled["authoritative"] == "legacy"
    assert recalled["result"]["answer"] == "legacy coffee facts"
    assert recalled["user_visible_changed"] is False
    assert "comparison" in recalled
    assert recalled["trace"]["fallbacks"]["authoritative"] == "legacy"


def test_adapter_capabilities_and_health() -> None:
    ad = AcmMemoryAdapter(legacy=_Legacy())
    caps = ad.capabilities()
    assert caps["shadow"] is True
    assert caps["aria_import"] is False
    assert caps["acm_read_primary"] is False
    health = ad.health()
    assert health["authoritative"] == "legacy"
    assert health["ok"] is True
    report = ad.shadow_report()
    assert report["certified"] is False
    assert "mission_control" in report


def test_adapter_does_not_invent_trusted_provenance() -> None:
    ad = AcmMemoryAdapter(legacy=_Legacy(), flags=FeatureFlags())
    remembered = ad.remember("My favorite color is adapter-blue.")
    assert remembered["legacy"]["ok"] is True
    assert remembered["acm_shadow"]["encoded"] is False
    assert remembered["acm_shadow"]["reason"] == "memory_trust"
    assert len(ad.engine.store.experiences) == 0
