"""M2 lesson 10: binary search and lower-bound over already-sorted equipment.
The input must already be sorted by ``key``. Ascending ``binary_search_by``
should be implemented via ``lower_bound_by`` so duplicate keys return the
*first* match. Do not scan from left to right.
"""
from __future__ import annotations
from typing import Any, Callable, Sequence, TypeVar
from herodungeon.core.events import EventRecorder
T = TypeVar("T")
SOURCE = "m2.binary_search"
SOURCE_LOWER = "m2.lower_bound"


def lower_bound_by(
    sorted_items: Sequence[T],
    target_key: Any,
    key: Callable[[T], Any],
    recorder: EventRecorder | None = None,
) -> int:
    """Return the first index whose key is ``>= target_key`` (ascending only).
    Returns ``0..n``. Use a closed interval ``lo..hi`` and an ``ans`` slot
    (same as lesson 8). Emit ``probe`` (with ``go_left``) and a final ``bound``.
    """
    recorder = recorder or EventRecorder()
    n = len(sorted_items)
    lo = 0
    hi = n - 1
    ans = n  # 初值n，全部元素都小于target时返回n

    while lo <= hi:
        mid = (lo + hi) // 2
        mid_val = key(sorted_items[mid])
        if mid_val >= target_key:
            ans = mid
            # 往左找更靠前满足条件的
            hi = mid - 1
            go_left = True
        else:
            lo = mid + 1
            go_left = False
        recorder.emit("probe", SOURCE_LOWER, mid=mid, go_left=go_left)

    recorder.emit("bound", SOURCE_LOWER, index=ans)
    return ans


def binary_search_by(
    sorted_items: Sequence[T],
    target_key: Any,
    key: Callable[[T], Any],
    recorder: EventRecorder | None = None,
    descending: bool = False,
) -> int:
    """Return the index of the first item whose key equals ``target_key``.
    Ascending (default): call ``lower_bound_by``, then check that cell.
    Return ``-1`` when no match exists. ``descending=True`` is optional.
    """
    recorder = recorder or EventRecorder()
    n = len(sorted_items)
    if not descending:
        # 升序：依赖lower_bound_by
        i = lower_bound_by(sorted_items, target_key, key, recorder)
        if i < n and key(sorted_items[i]) == target_key:
            return i
        else:
            return -1
    else:
        # 选做：降序闭区间二分
        lo = 0
        hi = n - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            mid_k = key(sorted_items[mid])
            if mid_k == target_key:
                return mid
            elif mid_k > target_key:
                # 降序，目标更小 → 向右
                lo = mid + 1
            else:
                hi = mid - 1
        return -1
