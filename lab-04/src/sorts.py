# sorts.py
"""Модуль с реализацией алгоритмов сортировки."""

from typing import List, Any


def bubble_sort(arr: List[Any]) -> List[Any]:
    """Сортировка пузырьком.

    Args:
        arr: Исходный массив для сортировки.

    Returns:
        Отсортированный массив.

    Сложность:
        Временная:
            - Худший случай: O(n²)
            - Средний случай: O(n²)
            - Лучший случай: O(n) - для уже отсортированного массива
        Пространственная: O(1) - сортировка на месте
    """
    n = len(arr)  # O(1) - получение длины массива
    arr_copy = arr.copy()  # O(n) - создание копии массива

    for i in range(n):  # O(n) - внешний цикл
        swapped = False  # O(1) - флаг обмена
        for j in range(0, n - i - 1):  # O(n) - внутренний цикл
            if arr_copy[j] > arr_copy[j + 1]:  # O(1) - сравнение
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                # O(1)
                swapped = True  # O(1)
        if not swapped:  # O(1) - проверка на отсортированность
            break  # O(1)
    return arr_copy  # O(1)
    # Общая сложность: O(n²)


def selection_sort(arr: List[Any]) -> List[Any]:
    """Сортировка выбором.

    Args:
        arr: Исходный массив для сортировки.

    Returns:
        Отсортированный массив.

    Сложность:
        Временная:
            - Худший случай: O(n²)
            - Средний случай: O(n²)
            - Лучший случай: O(n²)
        Пространственная: O(1) - сортировка на месте
    """
    n = len(arr)  # O(1)
    arr_copy = arr.copy()  # O(n)

    for i in range(n):  # O(n)
        min_idx = i  # O(1)
        for j in range(i + 1, n):  # O(n)
            if arr_copy[j] < arr_copy[min_idx]:  # O(1)
                min_idx = j  # O(1)
        arr_copy[i], arr_copy[min_idx] = arr_copy[min_idx], arr_copy[i]  # O(1)
    return arr_copy  # O(1)
    # Общая сложность: O(n²)


def insertion_sort(arr: List[Any]) -> List[Any]:
    """Сортировка вставками.

    Args:
        arr: Исходный массив для сортировки.

    Returns:
        Отсортированный массив.

    Сложность:
        Временная:
            - Худший случай: O(n²) - обратно отсортированный массив
            - Средний случай: O(n²)
            - Лучший случай: O(n) - уже отсортированный массив
        Пространственная: O(1) - сортировка на месте
    """
    arr_copy = arr.copy()  # O(n)

    for i in range(1, len(arr_copy)):  # O(n)
        key = arr_copy[i]  # O(1)
        j = i - 1  # O(1)
        while j >= 0 and arr_copy[j] > key:  # O(n) в худшем случае
            arr_copy[j + 1] = arr_copy[j]  # O(1)
            j -= 1  # O(1)
        arr_copy[j + 1] = key  # O(1)
    return arr_copy  # O(1)
    # Общая сложность: O(n²) в худшем случае, O(n) в лучшем


def merge_sort(arr: List[Any]) -> List[Any]:
    """Сортировка слиянием.

    Args:
        arr: Исходный массив для сортировки.

    Returns:
        Отсортированный массив.

    Сложность:
        Временная:
            - Худший случай: O(n log n)
            - Средний случай: O(n log n)
            - Лучший случай: O(n log n)
        Пространственная: O(n) - требуется дополнительная память
    """

    def merge(left: List[Any], right: List[Any]) -> List[Any]:
        """Слияние двух отсортированных массивов."""
        result = []  # O(1)
        i = j = 0  # O(1)

        while i < len(left) and j < len(right):  # O(n)
            if left[i] <= right[j]:  # O(1)
                result.append(left[i])  # O(1)
                i += 1  # O(1)
            else:  # O(1)
                result.append(right[j])  # O(1)
                j += 1  # O(1)

        result.extend(left[i:])  # O(n)
        result.extend(right[j:])  # O(n)
        return result  # O(1)

    def recursive_merge_sort(array: List[Any]) -> List[Any]:
        """Рекурсивная часть сортировки слиянием."""
        if len(array) <= 1:  # O(1) - базовый случай
            return array  # O(1)

        mid = len(array) // 2  # O(1)
        left = recursive_merge_sort(array[:mid])  # O(n log n)
        right = recursive_merge_sort(array[mid:])  # O(n log n)

        return merge(left, right)  # O(n)

    return recursive_merge_sort(arr.copy())  # O(n log n)
    # Общая сложность: O(n log n)


def quick_sort(arr: List[Any]) -> List[Any]:
    """Быстрая сортировка.

    Args:
        arr: Исходный массив для сортировки.

    Returns:
        Отсортированный массив.

    Сложность:
        Временная:
            - Худший случай: O(n²) - плохой выбор опорного элемента
            - Средний случай: O(n log n)
            - Лучший случай: O(n log n)
        Пространственная: O(log n) - глубина рекурсии
    """

    def recursive_quick_sort(array: List[Any]) -> List[Any]:
        """Рекурсивная часть быстрой сортировки."""
        if len(array) <= 1:  # O(1) - базовый случай
            return array  # O(1)

        pivot = array[len(array) // 2]
        # O(1) - выбор среднего элемента как опорного
        left = [x for x in array if x < pivot]  # O(n)
        middle = [x for x in array if x == pivot]  # O(n)
        right = [x for x in array if x > pivot]  # O(n)

        return (recursive_quick_sort(left) + middle +  # O(n log n)
                recursive_quick_sort(right))  # O(n log n)

    return recursive_quick_sort(arr.copy())  # O(n log n) в среднем случае
    # Общая сложность: O(n log n) в среднем, O(n²) в худшем случае


def is_sorted(arr: List[Any]) -> bool:
    """Проверяет, отсортирован ли массив.

    Args:
        arr: Массив для проверки.

    Returns:
        True если массив отсортирован, иначе False.
    """
    for i in range(len(arr) - 1):  # O(n)
        if arr[i] > arr[i + 1]:  # O(1)
            return False  # O(1)
    return True  # O(1)
    # Общая сложность: O(n)


if __name__ == '__main__':
    # Демонстрация работы сортировок
    test_array = [64, 34, 25, 12, 22, 11, 90]  # O(1)
    print(f'Исходный массив: {test_array}')  # O(1)

    algorithms = [  # O(1)
        ('Сортировка пузырьком', bubble_sort),  # O(1)
        ('Сортировка выбором', selection_sort),  # O(1)
        ('Сортировка вставками', insertion_sort),  # O(1)
        ('Сортировка слиянием', merge_sort),  # O(1)
        ('Быстрая сортировка', quick_sort)  # O(1)
    ]

    for name, algorithm in algorithms:  # O(k)
        sorted_array = algorithm(test_array)  # O(?) - зависит от алгоритма
        print(f'{name}: {sorted_array}')  # O(1)
        print(f'Корректность: {is_sorted(sorted_array)}')  # O(n)
