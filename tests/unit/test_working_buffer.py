from __future__ import annotations

from acm.working.buffer import BufferItem, WorkingBuffer


def test_capacity_displaces() -> None:
    buf = WorkingBuffer(capacity=3)
    displaced_total = 0
    for i in range(5):
        displaced = buf.push(
            BufferItem(kind="concept", ref_id=f"c{i}", label=str(i), attention=0.2, importance=0.2)
        )
        displaced_total += len(displaced)
    assert len(buf) == 3
    assert displaced_total >= 2


def test_same_ref_replaces_without_extra_slot() -> None:
    buf = WorkingBuffer(capacity=2)
    buf.push(BufferItem(kind="concept", ref_id="a", label="a", attention=1.0, importance=1.0))
    buf.push(BufferItem(kind="concept", ref_id="a", label="a2", attention=1.0, importance=1.0))
    assert len(buf) == 1
    assert buf.items()[0].label == "a2"
