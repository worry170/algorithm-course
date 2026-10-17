def top_k_similar(
    items: Sequence[Equipment],
    target: Equipment,
    k: int,
    recorder: EventRecorder | None = None,
) -> list[Equipment]:
    """Return the ``k`` nearest equipment to ``target``, nearest first.
    Rules (lesson 10 / D5):
    * exclude any candidate with the same ``item_id`` as ``target``;
    * ``k <= 0`` raises ``ValueError``;
    * if ``k`` exceeds the candidate count, return every candidate;
    * equal distance → smaller ``item_id`` wins (stable, unique order);
    * size-K max-heap of distances via ``heapq`` + negated distance.
    """
    if k <= 0:
        raise ValueError("k must be positive")
    recorder = recorder or EventRecorder()
    heap: list[tuple[float, str, Equipment]] = []
    target_id = target.item_id

    for item in items:
        if item.item_id == target_id:
            recorder.emit("skip", SOURCE_SIMILAR, item_id=item.item_id, reason="self")
            continue
        dist = distance(target, item)
        entry = (-dist, item.item_id, item)

        if len(heap) < k:
            heapq.heappush(heap, entry)
            recorder.emit(
                "push", SOURCE_SIMILAR, item_id=item.item_id, distance=dist, heap_size=len(heap)
            )
        else:
            # heap[0][0] 是负的最大距离
            current_worst_neg_dist, _, _ = heap[0]
            current_worst_dist = -current_worst_neg_dist
            if dist < current_worst_dist:
                evicted_entry = heapq.heapreplace(heap, entry)
                evicted_id = evicted_entry[1]
                recorder.emit(
                    "replace",
                    SOURCE_SIMILAR,
                    item_id=item.item_id,
                    distance=dist,
                    evicted=evicted_id
                )
            else:
                recorder.emit("skip", SOURCE_SIMILAR, item_id=item.item_id, distance=dist)

    # 取出堆内容，恢复真实距离；排序：距离升序，距离相等 item_id小优先
    unpacked = [(-neg_d, iid, equip) for neg_d, iid, equip in heap]
    unpacked.sort(key=lambda t: (t[0], t[1]))
    result = [equip for (d, iid, equip) in unpacked]
    recorder.emit("final", SOURCE_SIMILAR, top_k=[e.item_id for e in result])
    return result
