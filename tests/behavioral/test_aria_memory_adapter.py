from __future__ import annotations

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
    remembered = ad.remember("Coffee is bitter.")
    assert remembered["authoritative"] == "legacy"
    assert remembered["user_visible_changed"] is False
    assert remembered["acm_shadow"] is not None
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
