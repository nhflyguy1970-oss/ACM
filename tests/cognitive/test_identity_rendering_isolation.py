"""Identity rendering isolation — no cross-identity blending (D044)."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.authority.result import MemoryStatus
from acm.identity.rendering import IdentityRenderTarget, isolate_identity_text


def _speech(eng: CognitiveEngine, q: str) -> tuple[str, str, str]:
    result = eng.cognitive_respond(q)
    speech = eng.speak_cognitive_result(result)
    return str(result["status"]), str(result.get("memory") or ""), speech


def test_isolate_strips_known_as_user_blend() -> None:
    blended = "I am ARIA. I am known as Jeff. And you know me as Jeff."
    out = isolate_identity_text(
        blended,
        target=IdentityRenderTarget.ASSISTANT,
        forbidden_values={"Jeff"},
    )
    assert out is not None
    assert "jeff" not in out.lower()
    assert "know me" not in out.lower()
    assert "aria" in out.lower()


def test_who_are_you_never_mentions_user() -> None:
    eng = CognitiveEngine(
        agent_id="aria",
        assistant_identity={"name": "ARIA", "role": "assistant"},
    )
    eng.encode("My name is Jeff.")
    st, mem, speech = _speech(eng, "Who are you?")
    assert st == MemoryStatus.KNOWN.value
    low = speech.lower()
    assert "aria" in low
    assert "jeff" not in low
    assert "know me" not in low
    assert "known as" not in low
    assert "your name" not in low


def test_who_am_i_never_mentions_assistant() -> None:
    eng = CognitiveEngine(
        agent_id="aria",
        assistant_identity={"name": "ARIA", "role": "assistant"},
    )
    eng.encode("My name is Jeff.")
    st, mem, speech = _speech(eng, "Who am I?")
    assert st == MemoryStatus.KNOWN.value
    low = speech.lower()
    assert "jeff" in low
    assert "aria" not in low
    assert "my name is" not in low  # first-person assistant form


def test_call_me_jeffrey_leaves_assistant() -> None:
    eng = CognitiveEngine(agent_id="aria", assistant_identity={"name": "ARIA"})
    eng.encode("My name is Jeff.")
    eng.encode("Call me Jeffrey.")
    user_speech = _speech(eng, "Who am I?")[2].lower()
    assert "jeffrey" in user_speech or "jeff" in user_speech
    asst = _speech(eng, "Who are you?")[2].lower()
    assert "aria" in asst
    assert "jeffrey" not in asst
    assert "jeff" not in asst


def test_your_name_is_aria_leaves_user() -> None:
    eng = CognitiveEngine(agent_id="aria", assistant_identity={"name": "ARIA"})
    eng.encode("My name is Jeff.")
    eng.encode("Your name is ARIA.", assent=True)
    assert "jeff" in _speech(eng, "Who am I?")[2].lower()
    assert "aria" not in _speech(eng, "Who am I?")[2].lower()
    asst = _speech(eng, "Who are you?")[2].lower()
    assert "aria" in asst
    assert "jeff" not in asst


def test_forced_blend_memory_is_isolated_by_filter() -> None:
    """Even if memory text were contaminated, isolation must scrub it."""
    cleaned = isolate_identity_text(
        "I'm ARIA, and you know me as Jeff.",
        target=IdentityRenderTarget.ASSISTANT,
        forbidden_values={"Jeff"},
    )
    assert cleaned is None or "jeff" not in cleaned.lower()
    assert cleaned is None or "know me" not in cleaned.lower()


def test_host_independence_render_isolation() -> None:
    eng = CognitiveEngine(agent_id="solo", assistant_identity={"name": "Solo"})
    eng.encode("My name is Pat.")
    assert "pat" in _speech(eng, "Who am I?")[2].lower()
    assert "solo" in _speech(eng, "Who are you?")[2].lower()
    assert "pat" not in _speech(eng, "Who are you?")[2].lower()
