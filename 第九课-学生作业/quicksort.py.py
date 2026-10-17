"""M2 lesson 9: quicksort for equipment.

Implement quicksort_by yourself. Do not call sorted(), list.sort()
or any library sort.

Requirements:

* return a **new** list; never modify items;
* ascending by key(item); descending=True gives the reverse order;
* pick the pivot with a rule that does **not** degrade on already-sorted input
  (median-of-three recommended: the median of low / mid / high),
  and write your pivot rule in this docstring;
* quicksort is not stable; equal keys may come out in any order.

Events (source=SOURCE), one round of partitioning emits, in this order:

* partition    the range being split (e.g. low, high, depth)
* pivot        the chosen pivot (e.g. pivot_index, pivot_key)
* compare      every element compared against the pivot
* swap         every exchange of two different positions
* place_pivot  where the pivot finally lands

Pivot rule: median-of-three (median of items[low], items[mid], items[high])
"""

from __future__ import annotations

from typing import Any, Callable, Sequence, TypeVar

from herodungeon.core.events import EventRecorder

T = TypeVar("T")
SOURCE = "m2.quicksort"


def quicksort_by(
    items: Sequence[T],
    key: Callable[[T], Any],
    recorder: EventRecorder | None = None,
    descending: bool = False,
) -> list[T]:
    """Return a new list sorted by key using quicksort."""
    if recorder is None:
        recorder = EventRecorder()

    arr = list(items)
    n = len(arr)

    if n <= 1:
        return arr

    # Precompute keys so we don't call key() repeatedly
    keys = [key(arr[i]) for i in range(n)]

    def _quicksort(low: int, high: int, depth: int) -> None:
        if low >= high:
            return

        # Emit partition event
        recorder.emit("partition", SOURCE, low=low, high=high, depth=depth)

        # --- Median-of-three pivot selection ---
        mid = (low + high) // 2
        # Sort the three candidate indices by their key values
        three = [(keys[low], low), (keys[mid], mid), (keys[high], high)]
        three.sort(key=lambda x: x[0])
        pivot_idx = three[1][1]  # index of the median value

        # Swap pivot element to the high position (for Lomuto scheme)
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        keys[pivot_idx], keys[high] = keys[high], keys[pivot_idx]

        pivot_key = keys[high]

        # Emit pivot event
        recorder.emit("pivot", SOURCE, pivot_index=high, pivot_key=pivot_key)

        # --- Lomuto partition ---
        i = low  # boundary: arr[low..i-1] are "before" pivot
        for j in range(low, high):
            # Emit compare event for every element compared against pivot
            recorder.emit("compare", SOURCE, index=j, pivot_key=pivot_key)

            # Determine if arr[j] should come before the pivot
            if descending:
                before = keys[j] > pivot_key
            else:
                before = keys[j] < pivot_key

            if before:
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    keys[i], keys[j] = keys[j], keys[i]
                    recorder.emit("swap", SOURCE, i=i, j=j)
                i += 1

        # Place pivot in its final sorted position
        arr[i], arr[high] = arr[high], arr[i]
        keys[i], keys[high] = keys[high], keys[i]

        # Emit place_pivot event
        recorder.emit("place_pivot", SOURCE, index=i)

        # Recurse on left and right partitions
        _quicksort(low, i - 1, depth + 1)
        _quicksort(i + 1, high, depth + 1)

    _quicksort(0, n - 1, depth=0)
    return arr
