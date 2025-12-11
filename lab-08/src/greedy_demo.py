# greedy_demo.py


from __future__ import annotations

from typing import Dict, List

from greedy_algorithms import (
    Interval,
    Item,
    build_huffman_codes,
    build_huffman_tree,
    fractional_knapsack,
    greedy_change,
    kruskal_mst,
    pretty_print_huffman_tree,
    select_intervals_greedy,
)


def print_separator(title: str) -> None:
    """
    Напечатать разделитель с заголовком.
    """
    line = "-" * 60
    print()
    print(line)
    print(title)
    print(line)


# 1. Демонстрация задачи о выборе заявок (интервалы)


def demo_interval_scheduling() -> None:
    """
    Демонстрация работы жадного алгоритма выбора интервалов.
    """
    print_separator("Демонстрация: выбор заявок (Interval Scheduling)")

    intervals: List[Interval] = [
        Interval(start=1, end=4),
        Interval(start=3, end=5),
        Interval(start=0, end=6),
        Interval(start=5, end=7),
        Interval(start=3, end=9),
        Interval(start=5, end=9),
        Interval(start=6, end=10),
        Interval(start=8, end=11),
        Interval(start=8, end=12),
        Interval(start=2, end=13),
        Interval(start=12, end=14),
    ]

    print("Исходные интервалы (start, end):")
    for interval in intervals:
        print(f"  [{interval.start}, {interval.end})")

    selected = select_intervals_greedy(intervals)

    print("\nВыбранные интервалы жадным алгоритмом:")
    for interval in selected:
        print(f"  [{interval.start}, {interval.end})")

    print(f"\nОбщее количество выбранных интервалов: {len(selected)}")


# 2. Демонстрация непрерывной задачи о рюкзаке


def demo_fractional_knapsack() -> None:
    """
    Демонстрация работы жадного алгоритма для дробного рюкзака.

    Создаётся небольшой набор предметов с весом и стоимостью,
    задаётся вместимость рюкзака и выводится:
    * общая полученная стоимость,
    * какие предметы и в каких долях были взяты.
    """
    print_separator("Демонстрация: непрерывная задача о рюкзаке")

    items: List[Item] = [
        Item(weight=10, value=60, name="gold_bar"),
        Item(weight=20, value=100, name="silver_bar"),
        Item(weight=30, value=120, name="bronze_bar"),
    ]
    capacity = 50

    print(f"Вместимость рюкзака: {capacity}")
    print("Предметы (name, weight, value, value/weight):")
    for item in items:
        print(
            f"  {item.name:>10}  w={item.weight:>3}, "
            f"v={item.value:>3}, v/w={item.value_density:.2f}",
        )

    total_value, taken = fractional_knapsack(items, capacity)

    print("\nРезультат жадного алгоритма:")
    for item, fraction in taken:
        percent = fraction * 100
        print(
            f"  Взято {percent:6.2f}% предмета {item.name} "
            f"(w={item.weight}, v={item.value})",
        )

    print(f"\nИтоговая стоимость: {total_value:.2f}")


# 3. Демонстрация алгоритма Хаффмана


def demo_huffman() -> None:
    """
    Демонстрация построения и вывода дерева Хаффмана.

    Используются заранее заданные частоты символов.
    Выводятся:
    * частоты,
    * коды Хаффмана для каждого символа,
    * дерево Хаффмана в текстовом виде.
    """
    print_separator("Демонстрация: алгоритм Хаффмана")

    frequencies: Dict[str, int] = {
        "a": 5,
        "b": 9,
        "c": 12,
        "d": 13,
        "e": 16,
        "f": 45,
    }

    print("Частоты символов:")
    for symbol, freq in frequencies.items():
        print(f"  '{symbol}': {freq}")

    root = build_huffman_tree(frequencies)
    codes = build_huffman_codes(frequencies)

    print("\nКоды Хаффмана для символов:")
    for symbol, code in sorted(codes.items(), key=lambda kv: kv[0]):
        print(f"  '{symbol}': {code}")

    print("\nДерево Хаффмана (частоты и символы):")
    pretty_print_huffman_tree(root)


# 4. Демонстрация алгоритма Краскала (MST)


def demo_mst() -> None:
    """
    Демонстрация алгоритма Краскала для минимального остовного дерева.

    Строится небольшой неориентированный взвешенный граф.
    Выводятся:
    * список рёбер графа,
    * рёбра, входящие в MST,
    * суммарный вес остовного дерева.
    """
    print_separator("Демонстрация: минимальное остовное дерево (Краскал)")

    num_vertices = 6
    edges = [
        (0, 1, 4.0),
        (0, 2, 4.0),
        (1, 2, 2.0),
        (1, 0, 4.0),
        (2, 0, 4.0),
        (2, 1, 2.0),
        (2, 3, 3.0),
        (2, 5, 2.0),
        (2, 4, 4.0),
        (3, 2, 3.0),
        (3, 4, 3.0),
        (4, 2, 4.0),
        (4, 3, 3.0),
        (5, 2, 2.0),
        (5, 4, 3.0),
    ]

    print(f"Количество вершин: {num_vertices}")
    print("Рёбра графа (u, v, weight):")
    for u, v, w in edges:
        print(f"  ({u}, {v}, {w})")

    total_weight, mst_edges = kruskal_mst(num_vertices, edges)

    print("\nРёбра минимального остовного дерева:")
    for u, v, w in mst_edges:
        print(f"  ({u}, {v}, {w})")

    print(f"\nСуммарный вес MST: {total_weight}")


# 5. Демонстрация задачи о размене монет


def demo_greedy_change() -> None:
    """
    Демонстрация жадного алгоритма размена монет.

    Используются типичные «канонические» номиналы, для которых
    жадный алгоритм даёт оптимальное решение по числу монет.
    """
    print_separator("Демонстрация: задача о размене монет")

    denominations = [1, 2, 5, 10]
    amount = 28

    print(f"Номиналы монет: {denominations}")
    print(f"Сумма для размена: {amount}")

    total_coins, decomposition = greedy_change(denominations, amount)

    print("\nРазмен суммы жадным алгоритмом:")
    for coin, count in decomposition:
        print(f"  номинал {coin}: {count} шт.")

    print(f"\nВсего монет: {total_coins}")


def main() -> None:
    """
    Основная функция: последовательно запускает все демонстрации.

    Запускает:

    * demo_interval_scheduling()
    * demo_fractional_knapsack()
    * demo_huffman()
    * demo_mst()
    * demo_greedy_change()
    """
    demo_interval_scheduling()
    demo_fractional_knapsack()
    demo_huffman()
    demo_mst()
    demo_greedy_change()


if __name__ == "__main__":
    main()
