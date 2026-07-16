"""Identity pipeline debug — encode My name is Jeff → Who am I? → Your name is Jeff."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.identity.pipeline_trace import trace_identity_pipeline


def test_my_name_is_jeff_stored_and_retrieved() -> None:
    eng = CognitiveEngine(agent_id="aria")
    before = eng.cognitive_respond("Who am I?")
    assert before["status"] in ("low_confidence", "unknown", "insufficient_evidence")
    speech = eng.speak_cognitive_result(before).lower()
    assert "jeff" not in speech
    assert "don't" in speech or "not confident" in speech or "enough" in speech

    out = eng.encode("My name is Jeff.", pin=True)
    assert out["encoded"] is True
    user = eng.identity.schema_concept("user")
    names = [a for a in user.attributes if a.key == "name" and a.active]
    assert len(names) == 1
    assert names[0].value == "Jeff"
    assert names[0].confidence >= 0.85
    # No concept-token pollution on identity schema
    assert not any(a.key == "mentioned" and a.active for a in user.attributes)
    agent = eng.identity.schema_concept("agent")
    assert not any(a.key == "name" and a.value == "Jeff" and a.active for a in agent.attributes)

    result = eng.cognitive_respond("Who am I?")
    assert result["status"] == "known"
    assert result["confidence"] >= 0.85
    assert (result.get("memory") or "").strip() == "Your name is Jeff."
    speech = eng.speak_cognitive_result(result)
    assert speech.strip() == "Your name is Jeff."
    assert "mentioned" not in speech.lower()


def test_im_jeff_and_call_me() -> None:
    eng = CognitiveEngine(agent_id="aria")
    eng.encode("I'm Jeff.", pin=True)
    r = eng.cognitive_respond("Who am I?")
    assert "jeff" in (r.get("memory") or "").lower()
    eng2 = CognitiveEngine(agent_id="aria2")
    eng2.encode("Call me Jeff.", pin=True)
    user = eng2.identity.schema_concept("user")
    prefs = [a.value for a in user.attributes if a.key == "preferred_name" and a.active]
    assert prefs == ["Jeff"]


def test_name_update_jeffrey_no_duplicate() -> None:
    eng = CognitiveEngine(agent_id="aria")
    eng.encode("My name is Jeff.", pin=True)
    eng.encode("My name is Jeffrey.", pin=True)
    user = eng.identity.schema_concept("user")
    active = [a.value for a in user.attributes if a.key == "name" and a.active]
    assert active == ["Jeffrey"]
    r = eng.cognitive_respond("Who am I?")
    assert "jeffrey" in (r.get("memory") or "").lower()
    assert "jeff." not in (r.get("memory") or "").lower().replace("jeffrey", "")


def test_no_assistant_user_confusion() -> None:
    eng = CognitiveEngine(agent_id="aria")
    eng.encode("My name is Jeff.", pin=True)
    eng.encode("You are ARIA.", pin=True)
    user = eng.identity.schema_concept("user")
    agent = eng.identity.schema_concept("agent")
    assert any(a.key == "name" and a.value == "Jeff" and a.active for a in user.attributes)
    assert any(a.key == "name" and a.value.upper() == "ARIA" and a.active for a in agent.attributes)
    who_user = eng.cognitive_respond("Who am I?")
    assert "jeff" in (who_user.get("memory") or "").lower()
    assert "aria" not in (who_user.get("memory") or "").lower()


def test_pipeline_trace_evidence() -> None:
    eng = CognitiveEngine(agent_id="trace")
    report = trace_identity_pipeline(eng)
    assert report["ok"] is True
    stages = {s["stage"]: s for s in report["stages"]}
    assert stages["semantic_extraction"]["arrived"]
    assert stages["identity_organ_storage"]["stored"]
    assert stages["identity_structured_record"]["arrived"]
    assert stages["cognitive_memory_result"]["value"]["memory"] == "Your name is Jeff."
    assert stages["faithful_language_rendering"]["value"].strip() == "Your name is Jeff."
    assert stages["confidence_calculation"]["value"]["confidence"] >= 0.85
