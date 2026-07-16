from __future__ import annotations

from acm import CognitiveEngine


def test_identity_emerges_from_experience_not_manual_fields() -> None:
    engine = CognitiveEngine(agent_id="guide")
    # Assistant self-encode requires explicit speaker (D043)
    engine.encode("I am a research assistant.", kind="identity", speaker="assistant")
    engine.encode("I can organize long-term memory.", kind="identity", speaker="assistant")
    engine.open_goal("Support lifelong learning", importance=0.8)

    who = engine.who_am_i()
    assert "research assistant" in who["answer"].lower()
    assert who["confidence"] > 0.4
    assert who["evolution"]["growth_events"] >= 1

    remembered = engine.remember("Who are you?")
    assert "research assistant" in remembered.answer.lower()
    assert remembered.confidence > 0.0


def test_identity_persists_and_strengthens() -> None:
    engine = CognitiveEngine(agent_id="guide")
    engine.encode("I am a coding helper.", kind="identity", speaker="assistant")
    engine.encode("I am a coding helper.", kind="identity", speaker="assistant")
    second = engine.identity_snapshot()
    role = next(
        a
        for a in second["schemas"]["agent"]["attributes"]
        if a["key"] == "role" and a["value"].lower().startswith("coding")
    )
    assert role["confidence"] >= 0.55
    assert second["evolution"]["stability_hits"] >= 1


def test_identity_adaptation_requires_assent() -> None:
    engine = CognitiveEngine(agent_id="guide")
    engine.encode("I am a librarian.", kind="identity", speaker="assistant")
    conflict = engine.encode("I am a navigator.", kind="identity", speaker="assistant")
    assert conflict["identity"]["status"] == "proposed"
    proposal_id = conflict["identity"]["proposal_id"]

    # Without assent, role remains librarian
    snap = engine.identity_snapshot()
    attrs = snap["schemas"]["agent"]["attributes"]
    roles = [a["value"].lower() for a in attrs if a["key"] == "role"]
    assert "librarian" in roles
    assert "navigator" not in roles

    assented = engine.assent_identity(proposal_id)
    assert assented["assented"] is True
    snap2 = engine.identity_snapshot()
    active_roles = [
        a["value"].lower() for a in snap2["schemas"]["agent"]["attributes"] if a["key"] == "role"
    ]
    assert "navigator" in active_roles
    assert any(e["kind"] == "supersede" for e in snap2["lineage_tail"])


def test_identity_influence_on_attention_and_goals() -> None:
    engine = CognitiveEngine(agent_id="guide")
    engine.open_goal("Become a reliable memory engine")
    out = engine.encode("I can remember user preferences over years.")
    assert out["encoded"] is True
    assert out["identity"]["identity"] is True
    # Preference becomes adjacent to identity
    pref = engine.encode("My favorite coffee is dark roast.", kind="preference")
    assert pref["identity"]["status"] == "adjacent"
    snap = engine.identity_snapshot()
    assert "Become a reliable memory engine" in snap["active_goals"]
