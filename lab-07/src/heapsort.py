# heapsort.py


from __future__ import annotations

from typing import List

from heap import Heap


def heapsort_with_heap(array: List[int]) -> List[int]:
    """Сортирует массив, используя вспомогательную кучу Heap.

    Алгоритм:
        1. Построить max-heap из массива (build_heap).
        2. Повторять:
            - извлечь максимум extract();
            - добавить его в результат.

    Время:
        - Построение кучи: O(n).
        - n извлечений по O(log n): O(n log n).
        - Итого: O(n log n).
    Память:
        - O(n) дополнительной памяти под кучу и под результат.
    """
    if not array:  # O(1)
        return []  # O(1)

    heap = Heap(is_min=False)  # max-heap. O(1)
    heap.build_heap(array)  # O(n)

    result: List[int] = []  # O(1)
    while not heap.is_empty():  # O(n)
        result.append(heap.extract())  # O(log n)

    # Так как это max-heap, result сейчас по убыванию. Разворачиваем. O(n)
    result.reverse()  # O(n)
    return result  # O(1)


def heapsort_inplace(array: List[int]) -> None:
    """Классический in-place Heapsort.

    Модифицирует исходный массив, сортируя его по возрастанию.

    Алгоритм:
        1. Построить max-heap "на месте" в массиве.
        2. Повторять:
            - поменять местами корень (максимум) и последний элемент;
            - уменьшить "эффективный" размер кучи;
            - восстановить свойство кучи погружением корня.

    Время: O(n log n).
    Память: O(1) дополнительной.
    """

    n = len(array)  # O(1)

    def sift_down(i: int, heap_size: int) -> None:
        """Погружение узла i в массиве как в max-heap. O(log n)."""
        while True:  # O(h)
            left = 2 * i + 1  # O(1)
            right = 2 * i + 2  # O(1)
            largest = i  # O(1)

            if left < heap_size and array[left] > array[largest]:  # O(1)
                largest = left  # O(1)
            if right < heap_size and array[right] > array[largest]:  # O(1)
                largest = right  # O(1)

            if largest == i:  # O(1)
                break  # O(1)

            array[i], array[largest] = array[largest], array[i]  # O(1)
            i = largest  # O(1)

    # 1. Построение max-heap за O(n).
    for i in range(n // 2 - 1, -1, -1):  # O(n)
        sift_down(i, n)  # суммарно O(n)

    # 2. Извлечение максимумов и восстановление кучи. O(n log n)
    for end in range(n - 1, 0, -1):  # O(n)
        array[0], array[end] = array[end], array[0]  # O(1)
        sift_down(0, end)  # O(log n)
