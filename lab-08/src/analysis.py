# analysis.py

from __future__ import annotations

import random
import timeit
from typing import Callable,  List, Tuple

import matplotlib.pyplot as plt  # type: ignore
from greedy_algorithms import (  # noqa: WPS235
    Interval,
    Item,
)


def measure_time(func: Callable, *args, repeats: int = 5, **kwargs) -> float:
    """
    Замерить среднее время работы функции в миллисекундах.
    """
    def wrapped() -> None:
        func(*args, **kwargs)

    timer = timeit.Timer(wrapped)
    total_seconds = timer.timeit(number=repeats)
    return (total_seconds / repeats) * 1000.0


PC_INFO = """
Характеристики ПК для тестирования:
- Процессор: Intel Core i7-13620H @ 2.40GHz
- Оперативная память: 32 GB DDR5
- ОС: Windows 11
- Python: 3.13.3
"""


def generate_random_intervals(
    n: int,
    max_time: int = 10_000,
    max_length: int = 1_000,
) -> List[Interval]:
    """
    Сгенерировать список случайных интервалов.
    """
    intervals: List[Interval] = []
    for _ in range(n):  # O(n)
        start = random.randint(0, max_time)
        end = start + random.randint(1, max_length)
        intervals.append(Interval(start=start, end=end))
    return intervals


def generate_random_items(
    n: int,
    max_weight: int = 100,
    max_value: int = 100,
) -> List[Item]:
    """
    Генерация случайных предметов для задачи о рюкзаке.
    """
    items: List[Item] = []
    for i in range(n):  # O(n)
        weight = random.randint(1, max_weight)
        value = random.randint(0, max_value)
        items.append(Item(weight=weight, value=value, name=f"item_{i}"))
    return items


def generate_random_graph(
    num_vertices: int,
    edge_probability: float = 0.3,
    max_weight: int = 100,
) -> List[Tuple[int, int, float]]:
    """
    Генерация случайного неориентированного взвешенного графа.
    """
    edges: List[Tuple[int, int, float]] = []
    for u in range(num_vertices):  # O(n^2)
        for v in range(u + 1, num_vertices):
            if random.random() < edge_probability:
                weight = random.randint(1, max_weight)
                edges.append((u, v, float(weight)))
    return edges


# Точный 0-1 рюкзак и жадный 0-1 рюкзак


def knapsack_01_dp(items: List[Item], capacity: int) -> float:
    """
    Точный алгоритм 0-1 рюкзака (динамическое программирование, bottom-up).
    """
    n = len(items)
    if capacity < 0:
        raise ValueError("Capacity must be non-negative.")

    # dp[i][w] — максимальная стоимость, используя первые i предметов
    # при вместимости w.
    dp: List[List[float]] = [
        [0.0] * (capacity + 1) for _ in range(n + 1)
    ]  # O(n * capacity)

    for i in range(1, n + 1):  # O(n)
        item = items[i - 1]
        w_i = int(item.weight)
        v_i = item.value
        for w in range(capacity + 1):  # O(capacity)
            if w_i <= w:
                dp[i][w] = max(
                    dp[i - 1][w],               # не берём предмет
                    dp[i - 1][w - w_i] + v_i,   # берём предмет
                )
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]


def greedy_knapsack_01(items: List[Item], capacity: int) -> float:
    """
    Жадный 0-1 алгоритм рюкзака (НЕ оптимальный в общем случае).
    """
    items_sorted = sorted(
        items,
        key=lambda it: it.value_density,
        reverse=True,
    )  # O(n log n)

    remaining = capacity
    total_value = 0.0

    for item in items_sorted:  # O(n)
        w_i = int(item.weight)
        if w_i <= remaining:
            total_value += item.value
            remaining -= w_i

    return total_value


# Сравнение жадного и точного подходов (рюкзак)


def compare_knapsack_greedy_vs_dp() -> None:
    """
    Сравнить жадный 0-1 рюкзак и динамическое программирование.
    """
    random.seed(42)

    n_list = [5, 8, 10, 12]
    capacity_factor = 5

    sizes: List[int] = []
    times_greedy: List[float] = []
    times_dp: List[float] = []
    quality_ratios: List[float] = []

    print("Сравнение жадного и DP-подхода для 0-1 рюкзака:")
    print("{:>6} {:>10} {:>10} {:>12} {:>10}".format(
        "n",
        "Greedy",
        "DP",
        "Ratio(G/DP)",
        "Time(ms)",
    ))

    for n in n_list:
        items = generate_random_items(n)
        capacity = capacity_factor * n

        value_greedy = greedy_knapsack_01(items, capacity)
        value_dp = knapsack_01_dp(items, capacity)

        t_greedy = measure_time(greedy_knapsack_01, items, capacity)
        t_dp = measure_time(knapsack_01_dp, items, capacity)

        ratio = (value_greedy / value_dp) if value_dp > 0 else 1.0

        sizes.append(n)
        times_greedy.append(t_greedy)
        times_dp.append(t_dp)
        quality_ratios.append(ratio)

        print("{:>6} {:>10.2f} {:>10.2f} {:>12.3f} {:>10.3f}".format(
            n,
            value_greedy,
            value_dp,
            ratio,
            t_dp,
        ))

    # График времени
    plt.figure()
    plt.plot(sizes, times_greedy, marker="o", label="Greedy 0-1")
    plt.plot(sizes, times_dp, marker="o", label="DP 0-1")
    plt.xlabel("Число предметов n")
    plt.ylabel("Время, мс")
    plt.title("Время работы: жадный vs DP (0-1 рюкзак)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("greedy.png", dpi=300)

    # График качества решения
    plt.figure()
    plt.plot(sizes, quality_ratios, marker="o")
    plt.xlabel("Число предметов n")
    plt.ylabel("Отношение value_greedy / value_dp")
    plt.title("Качество жадного решения (0-1 рюкзак)")
    plt.grid(True)
    plt.tight_layout()
    plt.ylim(0, 1.05)
    plt.savefig("knapsack_quality_ratio.png", dpi=300)


def main() -> None:
    """
    Точка входа для ручного запуска экспериментов.

    Запускает:
    * вывод информации о ПК,
    * сравнение жадного и DP-подхода для 0-1 рюкзака,
    * примерные бенчмарки интервалов и MST.
    """
    print(PC_INFO)

    compare_knapsack_greedy_vs_dp()


if __name__ == "__main__":
    main()
