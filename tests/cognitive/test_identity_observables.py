from __future__ import annotations

from acm import CognitiveEngine
from acm.plugins import BaseExtension


class ProbeExtension(BaseExtension):
    name = "test.probe"
    version = "0.1.0"

    def __init__(self) -> None:
        self.encodes = 0

    def after_encode(self, event: dict) -> None:
        self.encodes += 1


def test_harness_identity_metrics() -> None:
    engine = CognitiveEngine(agent_id="obs")
    engine.encode("I am an experimenter.", kind="identity")
    engine.encode("I am an experimenter.", kind="identity")
    engine.encode("I am a cartographer.", kind="identity")
    engine.who_am_i()
    snap = engine.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.13"
    assert snap["identity"]["growth"] >= 1
    assert snap["identity"]["stability"] >= 1
    assert snap["identity"]["change"] >= 1
    assert snap["identity"]["lineage"] >= 1
    assert snap["counts"]["identity_touches"] >= 3


def test_identity_reconstruction_and_confidence() -> None:
    engine = CognitiveEngine(agent_id="obs")
    engine.encode("My name is ACM-Guide.", kind="identity")
    engine.encode("I can form identity from experience.", kind="identity")
    snap = engine.identity_snapshot()
    assert snap["schemas"]["agent"]["attributes"]
    assert snap["lineage_tail"]
    assert 0.0 <= snap["confidence"] <= 1.0
    obs = engine.identity.observables()
    assert obs["growth"] >= 1
    assert "evolution" in obs


def test_extension_registry_hook() -> None:
    engine = CognitiveEngine(agent_id="obs")
    probe = ProbeExtension()
    engine.extensions.register(probe)
    engine.encode("I am a plugin host.", kind="identity")
    assert probe.encodes == 1
    assert "test.probe" in engine.metacognitive_sketch()["extensions"]


def test_reject_preserves_prior_identity() -> None:
    engine = CognitiveEngine(agent_id="obs")
    engine.encode("I am stable.", kind="identity")
    conflict = engine.encode("I am volatile.", kind="identity")
    engine.reject_identity(conflict["identity"]["proposal_id"])
    who = engine.who_am_i()
    assert "stable" in who["answer"].lower()
    assert "volatile" not in who["answer"].lower()
