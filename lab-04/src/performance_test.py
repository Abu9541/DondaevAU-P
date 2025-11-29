# performance_test.py
"""Модуль для тестирования производительности алгоритмов сортировки."""

from sorts import (bubble_sort, selection_sort, insertion_sort,  # O(1)
                   merge_sort, quick_sort, is_sorted)  # O(1)
from generate_data import generate_test_datasets  # O(1)

import timeit
import sys
import os
from typing import List, Dict, Any, Callable
# Добавляем путь для импорта модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # O(1)


# Характеристики ПК для тестирования
PC_INFO = """
Характеристики ПК для тестирования:
- Процессор: Intel Core i7-13620H @ 2.40GHz
- Оперативная память: 32 GB DDR5
- ОС: Windows 11
- Python: 3.13.3
"""


def measure_sorting_time(sort_func: Callable[[List[Any]], List[Any]],
                         data: List[Any], number: int = 1) -> float:
    """Измеряет время выполнения функции сортировки.

    Args:
        sort_func: Функция сортировки.
        data: Данные для сортировки.
        number: Количество запусков для усреднения.

    Returns:
        Время выполнения в миллисекундах.
    """
    def wrapper():  # O(1)
        return sort_func(data)  # O(?) - зависит от алгоритма

    time_seconds = timeit.timeit(wrapper, number=number)  # O(?)
    return (time_seconds * 1000) / number  # Конвертация в миллисекунды O(1)


def run_performance_tests() -> Dict[str, Dict[str, Dict[int, float]]]:
    """Запускает тесты производительности для всех алгоритмов и типов данных.

    Returns:
        Словарь с результатами тестов.
    """
    sizes = [100, 500, 1000, 2000, 5000]  # O(1)
    datasets = generate_test_datasets(sizes)  # O(n)

    algorithms = [  # O(1)
        ('bubble_sort', bubble_sort),  # O(1)
        ('selection_sort', selection_sort),  # O(1)
        ('insertion_sort', insertion_sort),  # O(1)
        ('merge_sort', merge_sort),  # O(1)
        ('quick_sort', quick_sort)  # O(1)
    ]

    results = {}  # O(1)

    print('Запуск тестов производительности...')  # O(1)
    print(PC_INFO)  # O(1)

    for algo_name, algo_func in algorithms:  # O(m)
        results[algo_name] = {}  # O(1)
        print(f'\nТестирование {algo_name}:')  # O(1)

        for data_type, size_data in datasets.items():  # O(p)
            results[algo_name][data_type] = {}  # O(1)
            print(f'  {data_type}: ', end='')  # O(1)

            for size, data in size_data.items():  # O(k)
                # Определяем количество запусков
                # в зависимости от размера и алгоритма
                number_runs = 1  # O(1)
                if size > 1000 and algo_name in ['bubble_sort',
                                                 'selection_sort']:  # O(1)
                    number_runs = 1  # O(1)
                elif size <= 1000:  # O(1)
                    number_runs = 3  # O(1)

                # Проверяем корректность сортировки
                sorted_data = algo_func(data)  # O(?)
                if not is_sorted(sorted_data):  # O(n)
                    print(f'Ошибка: {algo_name} некорректно отсортировал!')
                    # O(1)
                    continue  # O(1)

                # Замеряем время
                time_ms = measure_sorting_time(algo_func, data, number_runs)
                # O(?)
                results[algo_name][data_type][size] = time_ms  # O(1)
                print(f'{size}({time_ms:.2f}мс) ', end='')  # O(1)

            print()  # O(1)

    return results  # O(1)


def print_results_table(results: Dict[str, Dict[str, Dict[int,
                                                          float]]]) -> None:
    """Выводит результаты тестов в виде таблицы.

    Args:
        results: Результаты тестов производительности.
    """
    sizes = [100, 500, 1000, 2000, 5000]  # O(1)
    data_types = ['random', 'sorted', 'reversed', 'almost_sorted']  # O(1)

    print('\n' + '='*80)  # O(1)
    print('СВОДНАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ (время в миллисекундах)')  # O(1)
    print('='*80)  # O(1)

    for data_type in data_types:  # O(p)
        print(f'\nТип данных: {data_type.upper()}')  # O(1)
        print('Algorithm    ', end='')  # O(1)
        for size in sizes:  # O(k)
            print(f'| {size:>8} ', end='')  # O(1)
        print()  # O(1)
        print('-' * (13 + 10 * len(sizes)))  # O(1)

        for algo_name in results.keys():  # O(m)
            print(f'{algo_name:12} ', end='')  # O(1)
            for size in sizes:  # O(k)
                time_val = results[algo_name].get(data_type, {}).get(size, 0)
                # O(1)
                print(f'| {time_val:8.2f} ', end='')  # O(1)
            print()  # O(1)


if __name__ == '__main__':
    results = run_performance_tests()  # O(n²) для квадратичных алгоритмов
    print_results_table(results)  # O(m*k*p)
