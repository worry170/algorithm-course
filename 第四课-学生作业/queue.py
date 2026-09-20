"""M1 lesson 4: implement a FIFO action queue.

Do not use ``list.pop(0)`` as your dequeue. Keep an explicit head index and
compact the consumed prefix when it wastes at least half of the buffer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterator

from herodungeon.core.events import AlgorithmEvent, EventRecorder

SOURCE = "m1.queue"


class QueueEmptyError(IndexError):
    """Raised when dequeuing or peeking an empty queue."""


@dataclass(slots=True)
class ActionQueue:
    recorder: EventRecorder = field(default_factory=EventRecorder)
    _buffer: list[Any] = field(default_factory=list, init=False, repr=False)
    _head: int = field(default=0, init=False, repr=False)

    def __len__(self) -> int:
        return len(self._buffer) - self._head

    def __iter__(self) -> Iterator[Any]:
        return iter(self._buffer[self._head :])

    @property
    def is_empty(self) -> bool:
        return len(self) == 0

    @property
    def items(self) -> tuple[Any, ...]:
        return tuple(self._buffer[self._head :])

    def enqueue(self, action: Any) -> AlgorithmEvent:
        """Append to the tail and emit enqueue."""
        self._buffer.append(action)
        tail_index = len(self._buffer) - 1
        return self.recorder.emit("enqueue", source=SOURCE, size=len(self), tail_index=tail_index)

    def dequeue(self) -> Any:
        """Remove the front item in O(1) amortized time."""
        if self.is_empty:
            self.recorder.emit("underflow", source=SOURCE)
            raise QueueEmptyError("dequeue from empty queue")
        action = self._buffer[self._head]
        self._head += 1
        self.recorder.emit("dequeue", source=SOURCE)
        self._compact_if_needed()
        return action

    def peek(self) -> Any:
        """Return the front item without removing it."""
        if self.is_empty:
            self.recorder.emit("underflow", source=SOURCE)
            raise QueueEmptyError("peek from empty queue")
        self.recorder.emit("peek", source=SOURCE)
        return self._buffer[self._head]

    def drain(self) -> list[Any]:
        """Dequeue everything in FIFO order."""
        result = []
        for _ in range(len(self)):
            result.append(self.dequeue())
        return result

    def _compact_if_needed(self) -> None:
        """Drop the consumed prefix when it is at least half of the buffer."""
        if self._head > 0 and self._head * 2 >= len(self._buffer):
            reclaimed = self._head
            self._buffer = self._buffer[self._head :]
            self._head = 0
            self.recorder.emit("compact", source=SOURCE, reclaimed=reclaimed, size=len(self))