# tests.py


from __future__ import annotations

import unittest

from heap import Heap
from heapsort import heapsort_with_heap, heapsort_inplace
from priority_queue import PriorityQueue


class TestHeap(unittest.TestCase):
    """Тесты для структуры данных Heap."""

    def test_min_heap_insert_extract_sorted(self) -> None:
        """Min-heap должен извлекать элементы по возрастанию. O(n log n)."""
        values = [5, 3, 8, 1, 4]
        heap = Heap(is_min=True)
        for v in values:
            heap.insert(v)

        extracted = [heap.extract() for _ in range(len(values))]
        self.assertEqual(extracted, sorted(values))

    def test_max_heap_insert_extract_sorted(self) -> None:
        """Max-heap должен извлекать элементы по убыванию. O(n log n)."""
        values = [5, 3, 8, 1, 4]
        heap = Heap(is_min=False)
        for v in values:
            heap.insert(v)
        extracted = [heap.extract() for _ in range(len(values))]
        self.assertEqual(extracted, sorted(values, reverse=True))

    def test_build_heap_preserves_heap_property(self) -> None:
        """build_heap должен корректно формировать кучу. O(n)."""
        values = [9, 1, 7, 3, 2, 8]
        heap = Heap(is_min=True)
        heap.build_heap(values)

        # Проверяем, что каждый родитель не больше потомков.
        data = heap.to_list()
        n = len(data)
        for i in range(n // 2):
            left = 2 * i + 1
            right = 2 * i + 2
            if left < n:
                self.assertLessEqual(data[i], data[left])
            if right < n:
                self.assertLessEqual(data[i], data[right])

    def test_peek_and_len(self) -> None:
        """peek возвращает корень, len — количество элементов."""
        heap = Heap(is_min=True)
        heap.insert(10)
        heap.insert(5)
        self.assertEqual(len(heap), 2)
        self.assertEqual(heap.peek(), 5)


class TestHeapsort(unittest.TestCase):
    """Тесты для алгоритмов Heapsort."""

    def test_heapsort_with_heap(self) -> None:
        """heapsort_with_heap должен сортировать список."""
        data = [3, 1, 4, 1, 5, 9]
        sorted_data = heapsort_with_heap(data)
        self.assertEqual(sorted_data, sorted(data))

    def test_heapsort_inplace(self) -> None:
        """heapsort_inplace сортирует массив на месте."""
        data = [3, 1, 4, 1, 5, 9]
        heapsort_inplace(data)
        self.assertEqual(data, sorted([3, 1, 4, 1, 5, 9]))


class TestPriorityQueue(unittest.TestCase):
    """Тесты для PriorityQueue на основе кучи."""

    def test_priority_queue_push_pop(self) -> None:
        """Элементы должны выходить по возрастанию приоритета."""
        pq = PriorityQueue()
        pq.push(5, "low")
        pq.push(1, "high")
        pq.push(3, "medium")

        p1, v1 = pq.pop()
        p2, v2 = pq.pop()
        p3, v3 = pq.pop()

        self.assertEqual((p1, v1), (1, "high"))
        self.assertEqual((p2, v2), (3, "medium"))
        self.assertEqual((p3, v3), (5, "low"))
        self.assertTrue(pq.is_empty())

    def test_priority_queue_peek(self) -> None:
        """peek не должен удалять элемент из очереди."""
        pq = PriorityQueue()
        pq.push(2, "task")
        self.assertEqual(pq.peek(), (2, "task"))
        self.assertFalse(pq.is_empty())
        self.assertEqual(len(pq), 1)


if __name__ == "__main__":
    unittest.main()
