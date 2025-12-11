# heap.py


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class Heap:
    """Куча, реализованная на массиве.

    is_min = True  -> min-heap (по умолчанию)
    is_min = False -> max-heap
    """

    is_min: bool = True  # ПО УМОЛЧАНИЮ: min-heap
    _data: List[Any] = field(default_factory=list)

    def _compare(self, a: Any, b: Any) -> bool:
        """Сравнение двух ключей с учетом типа кучи.

        Для min-heap: a < b (меньший "лучше").
        Для max-heap: a > b (больший "лучше").

        Время: O(1).
        """
        if self.is_min:
            return a < b
        return a > b

    def _sift_up(self, index: int) -> None:
        """Всплытие элемента вверх по куче. O(log n)."""
        i = index
        # Пока не корень. O(h)
        while i > 0:
            parent = (i - 1) // 2  # O(1)
            # Если ребенок "лучше" родителя — меняем. O(1)
            if self._compare(self._data[i], self._data[parent]):
                self._data[i], self._data[parent] = (
                    self._data[parent],
                    self._data[i],
                )
                i = parent  # O(1)
            else:
                break  # O(1)

    def _sift_down(self, index: int) -> None:
        """Погружение элемента вниз по куче. O(log n)."""
        n = len(self._data)  # O(1)
        i = index  # O(1)

        while True:  # O(h)
            left = 2 * i + 1  # O(1)
            right = 2 * i + 2  # O(1)
            best = i  # текущий кандидат. O(1)

            if left < n and self._compare(self._data[left], self._data[best]):
                best = left  # O(1)
            if right < n and self._compare(self._data[right],
                                           self._data[best]):
                best = right  # O(1)

            if best == i:  # свойство кучи выполнено. O(1)
                break  # O(1)

            self._data[i], self._data[best] = self._data[best], self._data[i]
            i = best  # O(1)

    def insert(self, value: Any) -> None:
        """Вставка нового элемента в кучу.

        1) Добавляем в конец массива.
        2) Всплываем вверх (_sift_up).

        Время: O(log n).
        """
        self._data.append(value)  # амортизированно O(1)
        self._sift_up(len(self._data) - 1)  # O(log n)

    def peek(self) -> Any:
        """Возвращает значение корня без удаления. O(1)."""
        if not self._data:  # O(1)
            raise IndexError("peek from empty heap")
        return self._data[0]  # O(1)

    def extract(self) -> Any:
        """Извлекает корень (min или max) из кучи. O(log n)."""
        if not self._data:  # O(1)
            raise IndexError("extract from empty heap")

        root_value = self._data[0]  # O(1)
        last_value = self._data.pop()  # O(1)

        if self._data:  # если не опустели. O(1)
            self._data[0] = last_value  # O(1)
            self._sift_down(0)  # O(log n)

        return root_value  # O(1)

    def build_heap(self, array: List[Any]) -> None:
        """Построение кучи из массива (метод Флойда). O(n)."""
        self._data = list(array)  # O(n)
        # Погружаем все внутренние узлы снизу вверх. O(n)
        for i in range(len(self._data) // 2 - 1, -1, -1):  # O(n)
            self._sift_down(i)  # суммарно O(n)

    def to_list(self) -> List[Any]:
        """Возвращает копию внутреннего массива. O(n)."""
        return list(self._data)  # O(n)

    def __len__(self) -> int:
        """Количество элементов в куче. O(1)."""
        return len(self._data)

    def is_empty(self) -> bool:
        """Пуста ли куча. O(1)."""
        return not self._data
