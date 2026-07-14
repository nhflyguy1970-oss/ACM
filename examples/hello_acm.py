#!/usr/bin/env python3
"""Minimal ACM integration example — no host framework required."""

from __future__ import annotations

from acm import CognitiveEngine


def main() -> None:
    engine = CognitiveEngine(agent_id="demo-agent")
    engine.open_goal("Learn user preferences", importance=0.7)
    engine.encode("My favorite coffee is dark roast.", kind="preference")
    result = engine.remember("What is my favorite coffee?")
    print(result.answer)
    print(result.explanation)
    print("confidence:", round(result.confidence, 3))
    sketch = engine.metacognitive_sketch()
    print("know_count:", sketch["what_i_know_count"])
    snap = engine.validation.snapshot()
    print("activations:", snap["counts"]["activations"])
    sleep = engine.sleep()
    print("sleep:", sleep)


if __name__ == "__main__":
    main()
