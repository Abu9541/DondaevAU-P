# generate_data.py
"""Модуль для генерации тестовых данных."""

import random
from typing import List, Dict


def generate_random_array(size: int, min_val: int = 1,
                          max_val: int = 10000) -> List[int]:
    """Генерирует массив случайных чисел.

    Args:
        size: Размер массива.
        min_val: Минимальное значение.
        max_val: Максимальное значение.

    Returns:
        Массив случайных чисел.
    """
    return [random.randint(min_val, max_val) for _ in range(size)]  # O(n)


def generate_sorted_array(size: int, min_val: int = 1,
                          max_val: int = 10000) -> List[int]:
    """Генерирует отсортированный массив.

    Args:
        size: Размер массива.
        min_val: Минимальное значение.
        max_val: Максимальное значение.

    Returns:
        Отсортированный массив.
    """
    arr = generate_random_array(size, min_val, max_val)  # O(n)
    arr.sort()  # O(n log n)
    return arr  # O(1)


def generate_reversed_array(size: int, min_val: int = 1,
                            max_val: int = 10000) -> List[int]:
    """Генерирует обратно отсортированный массив.

    Args:
        size: Размер массива.
        min_val: Минимальное значение.
        max_val: Максимальное значение.

    Returns:
        Обратно отсортированный массив.
    """
    arr = generate_sorted_array(size, min_val, max_val)  # O(n log n)
    arr.reverse()  # O(n)
    return arr  # O(1)


def generate_almost_sorted_array(size: int, swap_percent: float = 0.05,
                                 min_val: int = 1,
                                 max_val: int = 10000) -> List[int]:
    """Генерирует почти отсортированный массив.

    Args:
        size: Размер массива.
        swap_percent: Процент элементов для перемешивания.
        min_val: Минимальное значение.
        max_val: Максимальное значение.

    Returns:
        Почти отсортированный массив.
    """
    arr = generate_sorted_array(size, min_val, max_val)  # O(n log n)
    num_swaps = int(size * swap_percent)  # O(1)

    for _ in range(num_swaps):  # O(k)
        i = random.randint(0, size - 1)  # O(1)
        j = random.randint(0, size - 1)  # O(1)
        arr[i], arr[j] = arr[j], arr[i]  # O(1)

    return arr  # O(1)


def generate_test_datasets(sizes: List[int]) -> Dict[str, Dict[int,
                                                               List[int]]]:
    """Генерирует тестовые данные всех типов для заданных размеров.

    Args:
        sizes: Список размеров массивов.

    Returns:
        Словарь с тестовыми данными.
    """
    datasets = {}  # O(1)
    data_types = [  # O(1)
        ('random', generate_random_array),  # O(1)
        ('sorted', generate_sorted_array),  # O(1)
        ('reversed', generate_reversed_array),  # O(1)
        ('almost_sorted', generate_almost_sorted_array)  # O(1)
    ]

    for data_type, generator in data_types:  # O(m)
        datasets[data_type] = {}  # O(1)
        for size in sizes:  # O(k)
            datasets[data_type][size] = generator(size)  # O(n)

    return datasets  # O(1)


if __name__ == '__main__':
    # Демонстрация генерации данных
    test_sizes = [10, 20, 50]  # O(1)
    datasets = generate_test_datasets(test_sizes)  # O(n)

    for data_type, size_data in datasets.items():  # O(m)
        print(f'\n{data_type}:')  # O(1)
        for size, array in size_data.items():  # O(k)
            print(f'  Размер {size}: {array[:5]}...')  # O(1)
