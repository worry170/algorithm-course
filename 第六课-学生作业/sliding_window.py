"""M1 lesson 6: sliding window over the recent combat damage log.

Do not recompute each window from scratch. Slide by subtracting the leaving
value and adding the entering value so the whole scan is O(n).
"""

from __future__ import annotations

from typing import Any, Sequence

from herodungeon.core.events import EventRecorder

SOURCE = "m1.sliding_window"


def _validate(damage_log: Sequence[int], size: int) -> None:
    if size <= 0:
        raise ValueError("window size must be positive")
    if size > len(damage_log):
        raise ValueError(
            f"window size {size} exceeds damage log length {len(damage_log)}"
        )


def max_damage_window(
    damage_log: Sequence[int],
    size: int,
    recorder: EventRecorder | None = None,
) -> tuple[int, int]:
    """Return (start_index, window_sum) of the highest-damage window.

    Ties must keep the earliest window.
    """
    _validate(damage_log, size)
    recorder = recorder or EventRecorder()

    n = len(damage_log)
    log = list(damage_log)

    # 1. 计算第一个窗口的和
    window_sum = sum(log[0:size])
    best_start = 0
    best_sum = window_sum

    # emit window_init
    recorder.emit(
        "window_init", SOURCE,
        start=0,
        end=size - 1,
        values=tuple(log[0:size]),
        window_sum=window_sum,
    )

    # 2. 窗口右移：减去离开的数，加上进入的数
    for i in range(1, n - size + 1):
        leaving = log[i - 1]
        entering = log[i + size - 1]
        window_sum = window_sum - leaving + entering
        start = i
        end = i + size - 1

        # emit window_slide
        recorder.emit(
            "window_slide", SOURCE,
            start=start,
            end=end,
            values=tuple(log[start:end + 1]),
            window_sum=window_sum,
        )

        # 3. 只有严格更大时才更新最优（平局保留更早的）
        if window_sum > best_sum:
            best_sum = window_sum
            best_start = start

    # 4. emit window_best
    recorder.emit(
        "window_best", SOURCE,
        start=best_start,
        end=best_start + size - 1,
        values=tuple(log[best_start:best_start + size]),
        window_sum=best_sum,
    )

    return (best_start, best_sum)


def window_states(
    damage_log: Sequence[int], size: int
) -> list[dict[str, Any]]:
    """Return every window as {start, end, values, window_sum}."""
    _validate(damage_log, size)
    log = list(damage_log)
    n = len(log)
    states = []

    for i in range(n - size + 1):
        start = i
        end = i + size - 1
        values = list(log[start:end + 1])
        window_sum = sum(values)
        states.append({
            "start": start,
            "end": end,
            "values": values,
            "window_sum": window_sum,
        })

    return states
