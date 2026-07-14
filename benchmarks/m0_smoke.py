#!/usr/bin/env python3
"""M0 smoke benchmark — informative latency only."""

from __future__ import annotations

from time import perf_counter

from acm import CognitiveEngine


def main() -> None:
    engine = CognitiveEngine(agent_id="bench")
    t0 = perf_counter()
    for i in range(50):
        engine.encode(f"My favorite item{i} is value{i}.", kind="preference")
    for i in range(50):
        engine.remember(f"What is my favorite item{i}?")
    elapsed = perf_counter() - t0
    print(f"50 encode + 50 remember: {elapsed:.3f}s")
    print(engine.metacognitive_sketch())


if __name__ == "__main__":
    main()
