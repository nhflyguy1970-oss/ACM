"""Assistant vs User identity separation (D043)."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.authority.result import MemoryStatus
from acm.provenance import (
    TRUSTED_USER_STATEMENT,
    HostOperation,
    IngestionActor,
    IngestionProvenance,
    MessageRole,
)


def _speech(eng: CognitiveEngine, q: str) -> tuple[str, str, str]:
    result = eng.cognitive_respond(q)
    speech = eng.speak_cognitive_result(result)
    return str(result["status"]), str(result.get("memory") or ""), speech


def test_who_am_i_vs_who_are_you_independent() -> None:
    eng = CognitiveEngine(
        agent_id="aria",
        assistant_identity={"name": "Aria", "role": "cognitive assistant"},
    )
    st, mem, speech = _speech(eng, "Who am I?")
    assert st in (
        MemoryStatus.UNKNOWN.value,
        MemoryStatus.LOW_CONFIDENCE.value,
        MemoryStatus.INSUFFICIENT_EVIDENCE.value,
    )
    assert "jeff" not in speech.lower()
    assert "aria" not in speech.lower()

    st2, mem2, speech2 = _speech(eng, "Who are you?")
    assert st2 == MemoryStatus.KNOWN.value
    assert "aria" in speech2.lower()
    assert "jeff" not in speech2.lower()


def test_user_teach_does_not_change_assistant() -> None:
    eng = CognitiveEngine(
        agent_id="aria",
        assistant_identity={"name": "Aria"},
    )
    before = _speech(eng, "Who are you?")
    eng.encode("My name is Jeff.", provenance=TRUSTED_USER_STATEMENT)
    st_u, mem_u, speech_u = _speech(eng, "Who am I?")
    assert st_u == MemoryStatus.KNOWN.value
    assert "your name is jeff" in speech_u.lower()

    st_a, mem_a, speech_a = _speech(eng, "Who are you?")
    assert st_a == MemoryStatus.KNOWN.value
    assert "aria" in speech_a.lower()
    assert "jeff" not in speech_a.lower()
    assert before[2].split(".")[0] in speech_a or "aria" in speech_a.lower()

    agent = eng.identity.schema_concept("agent")
    assert not any(a.key == "name" and a.value == "Jeff" and a.active for a in agent.attributes)


def test_user_rename_leaves_assistant() -> None:
    eng = CognitiveEngine(agent_id="aria", assistant_identity={"name": "Aria"})
    eng.encode("My name is Jeff.", provenance=TRUSTED_USER_STATEMENT)
    eng.encode("My name is Bob.", provenance=TRUSTED_USER_STATEMENT)
    assert "bob" in _speech(eng, "Who am I?")[2].lower()
    assert "jeff" not in _speech(eng, "Who am I?")[2].lower()
    assert "aria" in _speech(eng, "Who are you?")[2].lower()
    assert "bob" not in _speech(eng, "Who are you?")[2].lower()


def test_tool_outcome_kind_identity_no_assistant_user_name() -> None:
    eng = CognitiveEngine(agent_id="aria", assistant_identity={"name": "Aria"})
    eng.encode("My name is Jeff.", provenance=TRUSTED_USER_STATEMENT)
    rejected = eng.encode(
        "Tool `memory_search` worked for: My name is Jeff.",
        kind="identity",
        provenance=IngestionProvenance(
            actor=IngestionActor.TOOL,
            host_operation=HostOperation.MEMORY_SEARCH,
            message_role=MessageRole.TOOL_RESULT,
        ),
    )
    assert rejected["encoded"] is False
    assert rejected["reason"] == "memory_trust"
    speech = _speech(eng, "Who are you?")[2].lower()
    assert "aria" in speech
    assert "jeff" not in speech


def test_your_name_jeff_rejected_when_user_is_jeff() -> None:
    eng = CognitiveEngine(agent_id="aria", assistant_identity={"name": "Aria"})
    eng.encode("My name is Jeff.", provenance=TRUSTED_USER_STATEMENT)
    eng.encode(
        "Your name is Jeff.", provenance=TRUSTED_USER_STATEMENT
    )  # would map to assistant without collision guard
    speech = _speech(eng, "Who are you?")[2].lower()
    assert "jeff" not in speech
    assert "aria" in speech


def test_no_duplicate_active_user_and_assistant_names() -> None:
    eng = CognitiveEngine(agent_id="aria", assistant_identity={"name": "Aria"})
    eng.encode("My name is Jeff.", provenance=TRUSTED_USER_STATEMENT)
    user_names = {
        a.value
        for a in eng.identity.schema_concept("user").attributes
        if a.key == "name" and a.active
    }
    agent_names = {
        a.value
        for a in eng.identity.schema_concept("agent").attributes
        if a.key == "name" and a.active
    }
    assert user_names == {"Jeff"}
    assert agent_names == {"Aria"}
    assert user_names.isdisjoint(agent_names)


def test_host_independence_default_agent_id() -> None:
    eng = CognitiveEngine(agent_id="solo-bot")
    speech = _speech(eng, "Who are you?")[2].lower()
    assert "solo-bot" in speech
    eng.encode("My name is Pat.", provenance=TRUSTED_USER_STATEMENT)
    assert "pat" in _speech(eng, "Who am I?")[2].lower()
    assert "pat" not in _speech(eng, "Who are you?")[2].lower()
