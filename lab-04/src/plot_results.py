# plot_results.py
"""Модуль для визуализации результатов тестирования."""

import matplotlib.pyplot as plt
from typing import Dict

import performance_test


def plot_size_vs_time(results: Dict[str, Dict[str, Dict[int, float]]]) -> None:
    """Строит графики зависимости времени от размера массива.

    Args:
        results: Результаты тестов производительности.
    """
    sizes = [100, 500, 1000, 2000, 5000]  # O(1)
    data_types = ['random', 'sorted', 'reversed', 'almost_sorted']  # O(1)

    for data_type in data_types:  # O(p)
        plt.figure(figsize=(12, 8))  # O(1)

        for algo_name, algo_results in results.items():  # O(m)
            times = [algo_results.get(data_type, {}).get(size, 0)  # O(k)
                     for size in sizes]  # O(k)
            plt.plot(sizes, times, 'o-', label=algo_name, linewidth=2)  # O(k)

        plt.xlabel('Размер массива')  # O(1)
        plt.ylabel('Время выполнения (мс)')  # O(1)
        plt.title(f'Зависимость времени выполнения от размера массива\n'
                  # O(1)
                  f'Тип данных: {data_type}')  # O(1)
        plt.grid(True, linestyle='--', alpha=0.7)  # O(1)
        plt.legend()  # O(1)
        plt.xscale('log')  # O(1)
        plt.yscale('log')  # O(1)

        filename = f'sorting_performance_{data_type}.png'  # O(1)
        plt.savefig(filename, dpi=300, bbox_inches='tight')  # O(1)
        print(f'Сохранен график: {filename}')  # O(1)
        plt.close()  # O(1)


def plot_data_type_comparison(results: Dict[str, Dict[str, Dict[int, float]]],
                              size: int = 1000) -> None:
    """Строит график сравнения алгоритмов по типам данных
    для фиксированного размера.

    Args:
        results: Результаты тестов производительности.
        size: Фиксированный размер массива для сравнения.
    """
    data_types = ['random', 'sorted', 'reversed', 'almost_sorted']  # O(1)

    plt.figure(figsize=(12, 8))  # O(1)

    for algo_name, algo_results in results.items():  # O(m)
        times = [algo_results.get(data_type, {}).get(size, 0)  # O(p)
                 for data_type in data_types]  # O(p)
        plt.plot(data_types, times, 's-', label=algo_name,  # O(p)
                 linewidth=2, markersize=8)  # O(p)

    plt.xlabel('Тип данных')  # O(1)
    plt.ylabel('Время выполнения (мс)')  # O(1)
    plt.title(f'Сравнение алгоритмов по типам данных\n'  # O(1)
              f'Размер массива: {size}')  # O(1)
    plt.grid(True, linestyle='--', alpha=0.7)  # O(1)
    plt.legend()  # O(1)

    filename = f'algorithm_comparison_size_{size}.png'  # O(1)
    plt.savefig(filename, dpi=300, bbox_inches='tight')  # O(1)
    print(f'Сохранен график: {filename}')  # O(1)
    plt.close()  # O(1)


if __name__ == '__main__':
    # Запускаем тесты и строим графики
    results = performance_test.run_performance_tests()  # O(n²)

    print('\nПостроение графиков...')  # O(1)
    plot_size_vs_time(results)  # O(m*k*p)
    plot_data_type_comparison(results, 1000)  # O(m*p)
    plot_data_type_comparison(results, 5000)  # O(m*p)

    print('\nВизуализация завершена!')  # O(1)
