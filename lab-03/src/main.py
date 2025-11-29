# main.py
"""Анализ производительности рекурсивных алгоритмов."""


import timeit

import matplotlib.pyplot as plt
from typing import List, Tuple
from recursion import fibonacci_naive
from memoization import fibonacci_memoized


# Характеристики ПК для тестирования
pc_info = """
Характеристики ПК для тестирования:
- Процессор: Intel Core i7-13620H @ 2.40GHz
- Оперативная память: 32 GB DDR5
- ОС: Windows 11
- Python: 3.13.3
"""


def measure_fibonacci_performance() -> Tuple[List[int],
                                             List[float],
                                             List[float]]:
    """Измеряет время выполнения наивной и мемоизированной версий Фибоначчи."""

    # Используем одинаковые размеры для обеих версий
    sizes = list(range(20, 36, 2))  # [20, 22, 24, 26, 28, 30, 32, 34]

    times_naive = []
    times_memoized = []

    print('Замеры времени выполнения для алгоритма Фибоначчи:')
    print('{:>10} {:>15} {:>20}'.format('Размер (N)', 'Время наивной (мс)',
                                        'Время мемоизир. (мс)'))

    for size in sizes:
        # Замер для наивной версии (1 запуск из-за медленной скорости)
        time_naive = timeit.timeit(
            lambda: fibonacci_naive(size),
            number=1
        ) * 1000

        # Замер для мемоизированной версии (100 запусков для точности)
        time_memoized = timeit.timeit(
            lambda: fibonacci_memoized(size),
            number=100
        ) * 1000 / 100  # Усреднение

        times_naive.append(time_naive)
        times_memoized.append(time_memoized)

        print('{:>10} {:>15.4f} {:>20.4f}'.format(
            size, time_naive, time_memoized
        ))

    return sizes, times_naive, times_memoized


def plot_performance_comparison(sizes: List[int], times_naive: List[float],
                                times_memoized: List[float]) -> None:
    """Строит график сравнения производительности."""
    plt.figure(figsize=(12, 8))  # O(1)

    # Фильтруем ненулевые значения для построения графиков
    naive_sizes = [sizes[i] for i in range(len(sizes)) if times_naive[i] > 0]
    # O(n)
    naive_times = [t for t in times_naive if t > 0]  # O(n)

    memo_sizes = [sizes[i] for i in range(len(sizes)) if times_memoized[i] > 0]
    # O(n)
    memo_times = [t for t in times_memoized if t > 0]  # O(n)

    plt.plot(naive_sizes, naive_times, 'ro-', label='Наивная рекурсия O(2^n)',
             linewidth=2, markersize=6)  # O(n)
    plt.plot(memo_sizes, memo_times, 'go-', label='Мемоизация O(n)',
             linewidth=2, markersize=6)  # O(n)

    plt.xlabel('Размер входных данных (N)')  # O(1)
    plt.ylabel('Время выполнения (мс)')  # O(1)
    plt.title('Сравнение производительности: наивная рекурсия vs мемоизация\n'
              # O(1)
              'Алгоритм вычисления чисел Фибоначчи')  # O(1)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)  # O(1)
    plt.legend()  # O(1)
    plt.yscale('log')  # O(1) - логарифмическая шкала для наглядности

    plt.savefig('img_1.png', dpi=300,  # O(1)
                bbox_inches='tight')  # O(1)
    plt.show()  # O(1)


def analyze_results() -> None:
    """Проводит анализ результатов экспериментов."""
    print('\nАнализ результатов:')  # O(1)
    print('1. Теоретическая сложность наивного алгоритма Фибоначчи: O(2^n)')
    # O(1)
    print('2. Теоретическая сложность алгоритма с мемоизацией: O(n)')  # O(1)
    print('3. Практические замеры подтверждают экспоненциальный рост времени '
          # O(1)
          'для наивной версии')  # O(1)
    print('4. Мемоизация уменьшает сложность до линейной, что кардинально '
          # O(1)
          'улучшает производительность')  # O(1)
    print('5. Для больших n наивный алгоритм становится практически '  # O(1)
          'неприменимым')  # O(1)


if __name__ == '__main__':
    print(pc_info)  # O(1)

    sizes, times_naive, times_memoized = measure_fibonacci_performance()
    # O(2^n + n)
    plot_performance_comparison(sizes, times_naive, times_memoized)  # O(n)
    analyze_results()  # O(1)
