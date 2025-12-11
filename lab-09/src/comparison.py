# comparison.py


from __future__ import annotations

import random
import timeit
from typing import Callable, List

import matplotlib.pyplot as plt  # type: ignore
from dynamic_programming import (  # noqa: WPS235
    KnapsackItem,
    coin_change_min_coins,
    fibonacci_bottom_up,
    fibonacci_memo,
    fibonacci_naive,
    knapsack_01_bottom_up,
    lis_dp,
    lcs_bottom_up,
    levenshtein_distance,
    print_coin_change_table,
    print_knapsack_table,
    print_lcs_table,
    print_lis_table,
    print_levenshtein_table,
)

PC_INFO = """
Характеристики ПК для тестирования:
- Процессор: Intel Core i7-13620H @ 2.40GHz
- Оперативная память: 32 GB DDR5
- ОС: Windows 11
- Python: 3.13.3
"""


def measure_time(
    func: Callable,
    *args,
    repeats: int = 5,
    **kwargs,
) -> float:
    """
    Замерить среднее время работы функции в миллисекундах.
    """
    def wrapped() -> None:
        func(*args, **kwargs)

    timer = timeit.Timer(wrapped)
    total_seconds = timer.timeit(number=repeats)
    return total_seconds * 1000.0 / repeats


# 1. Сравнение для чисел Фибоначчи


def compare_fibonacci() -> None:
    """
    Сравнить наивный, memo и bottom-up подходы для чисел Фибоначчи.
    Замеряем время работы для набора значений n.
    Также строим графики зависимости времени от n.
    """
    print("=== Сравнение алгоритмов Фибоначчи ===")

    n_values_naive = [5, 10, 20, 25, 30]
    n_values_dp = [100, 500, 1_000, 5_000, 10_000]

    # Сравнение для наивного, memo и bottom-up на малых n
    print("\nНаивный vs memo vs bottom-up (малые n):")
    print("{:>6} {:>12} {:>12} {:>12}".format(
        "n",
        "Naive (ms)",
        "Memo (ms)",
        "Bottom (ms)",
    ))

    time_naive_list: List[float] = []
    time_memo_small: List[float] = []
    time_bottom_small: List[float] = []

    for n in n_values_naive:
        t_naive = measure_time(fibonacci_naive, n, repeats=3)
        t_memo = measure_time(fibonacci_memo, n, repeats=3)
        t_bottom = measure_time(fibonacci_bottom_up, n, repeats=3)

        time_naive_list.append(t_naive)
        time_memo_small.append(t_memo)
        time_bottom_small.append(t_bottom)

        print("{:>6} {:>12.3f} {:>12.3f} {:>12.3f}".format(
            n,
            t_naive,
            t_memo,
            t_bottom,
        ))

    # Сравнение memo и bottom-up на больших n
    print("\nMemo vs bottom-up (большие n):")
    print("{:>6} {:>12} {:>12}".format(
        "n",
        "Memo (ms)",
        "Bottom (ms)",
    ))

    time_memo_big: List[float] = []
    time_bottom_big: List[float] = []

    for n in n_values_dp:
        t_memo = measure_time(fibonacci_memo, n, repeats=3)
        t_bottom = measure_time(fibonacci_bottom_up, n, repeats=3)

        time_memo_big.append(t_memo)
        time_bottom_big.append(t_bottom)

        print("{:>6} {:>12.3f} {:>12.3f}".format(
            n,
            t_memo,
            t_bottom,
        ))

    # Графики
    plt.figure()
    plt.plot(
        n_values_naive,
        time_naive_list,
        marker="o",
        label="Naive recursion",
    )
    plt.plot(
        n_values_naive,
        time_memo_small,
        marker="o",
        label="Memo (top-down)",
    )
    plt.plot(
        n_values_naive,
        time_bottom_small,
        marker="o",
        label="Bottom-up",
    )
    plt.xlabel("n")
    plt.ylabel("Время, мс")
    plt.title("Числа Фибоначчи: сравнение подходов (малые n)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("fib_small_comparison.png", dpi=300)

    plt.figure()
    plt.plot(
        n_values_dp,
        time_memo_big,
        marker="o",
        label="Memo (top-down)",
    )
    plt.plot(
        n_values_dp,
        time_bottom_big,
        marker="o",
        label="Bottom-up",
    )
    plt.xlabel("n")
    plt.ylabel("Время, мс")
    plt.title("Числа Фибоначчи: memo vs bottom-up (большие n)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("fibonacchi.png", dpi=300)


# 2. Масштабируемость рюкзака 0-1


def generate_random_knapsack_items(
    n: int,
    max_weight: int = 50,
    max_value: int = 100,
) -> List[KnapsackItem]:
    """
    Сгенерировать случайные предметы для задачи рюкзака.
    """
    items: List[KnapsackItem] = []
    for i in range(n):
        weight = random.randint(1, max_weight)
        value = random.randint(1, max_value)
        items.append(
            KnapsackItem(weight=weight, value=value, name=f"item_{i}"),
        )
    return items


def benchmark_knapsack() -> None:
    """
    Исследовать масштабируемость bottom-up алгоритма рюкзака.
    Для набора размеров n генерируются случайные наборы предметов,
    вместимость выбирается пропорционально n. Строится график зависимости
    времени выполнения от n.
    """
    print("\n=== Масштабируемость рюкзака 0-1 (bottom-up) ===")

    random.seed(42)
    sizes = [10, 20, 30, 40, 50]
    capacity_factor = 5

    times: List[float] = []

    print("{:>6} {:>12}".format("n", "Time (ms)"))
    for n in sizes:
        items = generate_random_knapsack_items(n)
        capacity = capacity_factor * n

        t = measure_time(
            knapsack_01_bottom_up,
            items,
            capacity,
            repeats=3,
        )
        times.append(t)
        print("{:>6} {:>12.3f}".format(n, t))

    plt.figure()
    plt.plot(sizes, times, marker="o")
    plt.xlabel("Число предметов n")
    plt.ylabel("Время, мс")
    plt.title("Рюкзак 0-1: время работы bottom-up алгоритма")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("knapsack.png", dpi=300)


# 3. Примеры визуализации таблиц ДП


def demo_visualizations() -> None:
    """
    Показать примеры визуализации таблиц ДП для небольших данных.
    """
    print("\n=== Визуализация таблиц ДП ===")

    # Рюкзак
    print("\n-- Рюкзак 0-1 --")
    items = [
        KnapsackItem(2, 3, "item1"),
        KnapsackItem(3, 4, "item2"),
        KnapsackItem(4, 5, "item3"),
    ]
    capacity = 5
    print_knapsack_table(items, capacity)

    # LCS
    print("\n-- LCS --")
    s1, s2 = "ABCBDAB", "BDCAB"
    print_lcs_table(s1, s2)

    # Levenshtein
    print("\n-- Levenshtein distance --")
    s1_lev, s2_lev = "kitten", "sitting"
    print(f"Расстояние Левенштейна между '{s1_lev}' и '{s2_lev}': "
          f"{levenshtein_distance(s1_lev, s2_lev)}")
    print_levenshtein_table(s1_lev, s2_lev)

    # Размен монет
    print("\n-- Размен монет --")
    amount = 11
    coins = [1, 2, 5]
    print_coin_change_table(amount, coins)

    # LIS
    print("\n-- LIS --")
    seq = [3, 10, 2, 1, 20]
    print_lis_table(seq)


# 4. Мини-демо для остальных задач ДП


def demo_other_dp_tasks() -> None:
    """
    Краткая демонстрация задач:

    * размен монет (ДП),
    * LIS,
    * LCS — длина и строка.
    """
    print("\n=== Примеры работы других задач ДП ===")

    # Размен монет
    print("\nРазмен монет (DP):")
    amount = 27
    coins = [1, 5, 10]
    min_coins, decomposition = coin_change_min_coins(amount, coins)
    print(f"Amount = {amount}, min coins = {min_coins}")
    print("Decomposition:", decomposition)

    # LIS
    print("\nНаибольшая возрастающая подпоследовательность (LIS):")
    seq = [10, 9, 2, 5, 3, 7, 101, 18]
    length, subseq = lis_dp(seq)
    print("Sequence:", seq)
    print(f"LIS length = {length}, subsequence = {subseq}")

    # LCS
    print("\nLCS для строк:")
    s1, s2 = "XMJYAUZ", "MZJAWXU"
    length, lcs_str = lcs_bottom_up(s1, s2)
    print(f"s1 = '{s1}', s2 = '{s2}'")
    print(f"LCS length = {length}, LCS = '{lcs_str}'")

    # Levenshtein
    print("\nРасстояние Левенштейна (ещё раз, без таблицы):")
    s1_lev, s2_lev = "algorithm", "altruistic"
    dist = levenshtein_distance(s1_lev, s2_lev)
    print(f"'{s1_lev}' -> '{s2_lev}', distance = {dist}")


def main() -> None:
    """
    Основная функция: запускает сравнение и демонстрации.
    """
    print(PC_INFO)
    compare_fibonacci()
    benchmark_knapsack()
    demo_visualizations()
    demo_other_dp_tasks()


if __name__ == "__main__":
    main()
