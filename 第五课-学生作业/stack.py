"""M1 lesson 5: implement a LIFO undo stack.

Push/pop the newest operation. If max_depth is set, evict the oldest entry
before pushing a new one that would overflow.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterator

from herodungeon.core.events import AlgorithmEvent, EventRecorder

SOURCE = "m1.stack"


class StackEmptyError(IndexError):
    """Raised when popping or peeking an empty stack."""


@dataclass(slots=True)
class UndoStack:
    max_depth: int | None = None
    recorder: EventRecorder = field(default_factory=EventRecorder)
    _buffer: list[Any] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.max_depth is not None and self.max_depth <= 0:
            raise ValueError("max_depth must be positive when provided")

    def __len__(self) -> int:
        return len(self._buffer)

    def __iter__(self) -> Iterator[Any]:
        return reversed(self._buffer)

    @property
    def is_empty(self) -> bool:
        return not self._buffer

    @property
    def items(self) -> tuple[Any, ...]:
        return tuple(self._buffer)

    def push(self, operation: Any) -> AlgorithmEvent:
        """Push to the top; evict the oldest item if max_depth is exceeded."""
        evicted = None
        if self.max_depth is not None and len(self._buffer) >= self.max_depth:
            evicted = self._buffer.pop(0)
            self.recorder.emit("evict", SOURCE, evicted=evicted)
        self._buffer.append(operation)
        return self.recorder.emit(
            "push", SOURCE, depth=len(self._buffer), evicted=evicted
        )

    def pop(self) -> Any:
        """Remove and return the top operation."""
        if self.is_empty:
            self.recorder.emit("underflow", SOURCE)
            raise StackEmptyError("pop from empty stack")
        operation = self._buffer.pop()
        self.recorder.emit("pop", SOURCE)
        return operation

    def peek(self) -> Any:
        """Return the top operation without removing it."""
        if self.is_empty:
            self.recorder.emit("underflow", SOURCE)
            raise StackEmptyError("peek from empty stack")
        self.recorder.emit("peek", SOURCE)
        return self._buffer[-1]