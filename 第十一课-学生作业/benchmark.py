"""M2 lesson 11: reproducible comparison-count benchmark (quick vs bubble vs selection).

Count ``compare`` events, never wall-clock time: clocks differ across machines
and make CI flaky.

* ``quicksort_by`` is your lesson-9 quicksort (paste it into ``quicksort.py``);
* ``bubble_sort_by`` / ``selection_sort_by`` are teacher-provided contrast
  baselines in ``baseline_sorts.py`` (not graded, do not modify).
"""

from __future__ import annotations

from typing import Any, Callable, Sequence

from herodungeon.core.events import EventRecorder

from .baseline_sorts import bubble_sort_by, selection_sort_by
from .equipment import Equipment, generate_equipment
from .quicksort import quicksort_by

#: Lesson-11 deck sizes. 1600 is an optional extra row (docs only; ~6 s).
DEFAULT_SIZES: tuple[int, ...] = (100, 200, 400, 800)


def count_comparisons(sort: Callable[..., list[Any]], items: Sequence[Equipment]) -> int:
    """Run ``sort(items, key=power, recorder=...)`` and count its ``compare`` events."""
    recorder = EventRecorder()
    # 拷贝一份，避免某个排序原地修改输入影响后续调用
    sort(list(items), key=lambda eq: eq.power, recorder=recorder)
    return sum(1 for event in recorder.events if event.type == "compare")


def run_sort_benchmark(
    sizes: Sequence[int] = DEFAULT_SIZES, seed: int = 42
) -> list[dict[str, Any]]:
    """Return one row per ``n``: comparison counts and the bubble/quick ratio.

    Row fields: ``n``, ``quick_comparisons``, ``bubble_comparisons``,
    ``selection_comparisons``, ``bubble_over_quick`` (rounded to 2 decimals).
    """
    # 注意：rows 的初始化必须在 for 循环【外面】，且只初始化一次
    rows: list[dict[str, Any]] = []

    for n in sizes:
        items = generate_equipment(n, seed=seed)

        quick = count_comparisons(quicksort_by, items)
        bubble = count_comparisons(bubble_sort_by, items)
        selection = count_comparisons(selection_sort_by, items)

        denom = quick if quick else 1  # quick 为 0 时按 1 算
        rows.append(
            {
                "n": n,
                "quick_comparisons": quick,
                "bubble_comparisons": bubble,
                "selection_comparisons": selection,
                "bubble_over_quick": round(bubble / denom, 2),
            }
        )

    # 注意：return rows 必须与 for 循环【同级】，不能缩进进循环体内
    return rows