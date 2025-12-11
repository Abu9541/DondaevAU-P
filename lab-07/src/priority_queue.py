# priority_queue.py


from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Tuple

from heap import Heap


@dataclass
class PriorityQueue:
    """Приоритетная очередь на min-куче.

    Внутренне хранит пары (priority, item) в Heap(is_min=True).
    """

    _heap: Heap

    def __init__(self) -> None:
        """Создает пустую приоритетную очередь. O(1)."""
        self._heap = Heap(is_min=True)  # MIN-heap

    def push(self, priority: int, item: Any) -> None:
        """Добавляет элемент с заданным приоритетом. O(log n)."""
        # Кортежи сравниваются сначала по priority → min-heap отдаст
        # наименьший приоритет первым.
        self._heap.insert((priority, item))

    def pop(self) -> Tuple[int, Any]:
        """Извлекает элемент с наивысшим приоритетом (наименьший priority).

        Время: O(log n).
        """
        if self._heap.is_empty():
            raise IndexError("pop from empty priority queue")
        return self._heap.extract()

    def peek(self) -> Tuple[int, Any]:
        """Просмотр элемента с наивысшим приоритетом без удаления. O(1)."""
        if self._heap.is_empty():
            raise IndexError("peek from empty priority queue")
        return self._heap.peek()

    def is_empty(self) -> bool:
        """Пуста ли очередь. O(1)."""
        return self._heap.is_empty()

    def __len__(self) -> int:
        """Количество элементов в очереди. O(1)."""
        return len(self._heap)
