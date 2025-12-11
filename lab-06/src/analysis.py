# analysis.py


from __future__ import annotations

import random
import timeit
from typing import List

import matplotlib.pyplot as plt
from binary_search_tree import (
    BinarySearchTree,
    build_bst_from_iterable,
)
from tree_traversal import inorder_iterative

# Характеристики ПК.
PC_INFO = """
Характеристики ПК для тестирования:
- Процессор: Intel Core i7-13620H @ 2.40GHz
- Оперативная память: 32 GB DDR5
- ОС: Windows 11
- Python: 3.13.3
"""


def generate_random_values(size: int) -> List[int]:
    """Генерирует список уникальных случайных значений.

    Используем диапазон шире size для гарантии уникальности.

    Сложность: O(n).
    """
    # random.sample создаёт список из size уникальных чисел.
    return random.sample(range(size * 10), size)


def generate_sorted_values(size: int) -> List[int]:
    """Генерирует возрастающую последовательность из size уникальных значений.

    Такая последовательность при вставке в BST создаёт вырожденное дерево
    (цепочку).

    Сложность: O(n).
    """
    # Для наглядности используем просто range.
    return list(range(size))


def build_balanced_like_tree(size: int) -> BinarySearchTree:
    """Строит дерево с "примерно сбалансированной" структурой.

    Вставка элементов в случайном порядке → в среднем высота O(log n).

    Сложность: в среднем O(n log n).
    """
    values = generate_random_values(size)
    tree = build_bst_from_iterable(values)
    return tree


def build_degenerate_tree(size: int) -> BinarySearchTree:
    """Строит вырожденное дерево (почти линейный список).

    Вставка отсортированных значений приводит к высоте ~ n.

    Сложность: O(n²) в худшем случае.
    """
    values = generate_sorted_values(size)
    tree = build_bst_from_iterable(values)
    return tree


def measure_search_time(
    tree: BinarySearchTree,
    targets: List[int],
    repeat: int = 5,
) -> float:
    """Замеряет время выполнения поиска всех целей в дереве.

    Замер выполняется repeat раз и усредняется.
    Возвращает время в миллисекундах.

    Пусть k = len(targets), h — высота дерева.
    Сложность одного прогона: O(k * h).
    """
    def run() -> None:
        for value in targets:  # O(k)
            _ = tree.search(value)  # O(h)

    # timeit.timeit запускает функцию run repeat раз. O(repeat * k * h)
    total = timeit.timeit(run, number=repeat)  # O(repeat * k * h)
    avg_seconds = total / repeat  # O(1)
    return avg_seconds * 1000.0  # O(1)


def run_experiments() -> None:
    """Основная функция для проведения экспериментов.

    - Строит деревья разных размеров;
    - измеряет время поиска;
    - вычисляет высоты деревьев;
    - строит графики и выводит краткий анализ.

    Сложность доминируется построением деревьев и замерами:
    примерно O(sum_n (n log n + k * h)).
    """
    print(PC_INFO)

    # Размеры деревьев для эксперимента.
    sizes = [1000, 5000, 10000, 20000, 50000]

    times_balanced: List[float] = []
    times_degenerate: List[float] = []
    heights_balanced: List[int] = []
    heights_degenerate: List[int] = []

    print("Замеры времени поиска в BST (1000 успешных поисков):")
    header = "{:>10} {:>15} {:>15} {:>10} {:>10}".format(
        "N",
        "T_bal (мс)",
        "T_deg (мс)",
        "h_bal",
        "h_deg",
    )
    print(header)

    for size in sizes:
        # Строим почти сбалансированное дерево.
        balanced_tree = build_balanced_like_tree(size)

        # Строим вырожденное дерево.
        degenerate_tree = build_degenerate_tree(size)

        # Для справедливости замеров берём значения
        # из сбалансированного дерева.
        all_values = inorder_iterative(balanced_tree.root)
        # 1000 случайных целей для поиска.
        targets = random.choices(all_values, k=1000)

        # Замер времени поиска.
        t_bal = measure_search_time(balanced_tree, targets, repeat=5)
        t_deg = measure_search_time(degenerate_tree, targets, repeat=5)

        times_balanced.append(t_bal)
        times_degenerate.append(t_deg)

        # Замер высоты деревьев.
        h_bal = balanced_tree.height()
        h_deg = degenerate_tree.height()
        heights_balanced.append(h_bal)
        heights_degenerate.append(h_deg)

        row = "{:>10} {:>15.3f} {:>15.3f} {:>10} {:>10}".format(
            size,
            t_bal,
            t_deg,
            h_bal,
            h_deg,
        )
        print(row)

    # Построение графика времени поиска

    plt.figure(figsize=(10, 6))
    plt.plot(
        sizes,
        times_balanced,
        "o-",
        label="Случайная вставка (≈сбалансированное)",
    )
    plt.plot(
        sizes,
        times_degenerate,
        "s-",
        label="Отсортированная вставка (вырожденное)",
    )
    plt.xlabel("Число элементов в дереве (N)")
    plt.ylabel("Время 1000 поисков (мс)")
    plt.title(
        "Зависимость времени поиска в BST\n"
        "сбалансированный vs вырожденный случай",
    )
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig("search.png", dpi=300)
    # plt.show()  # Раскомментируйте при запуске локально

    # График высоты деревьев

    plt.figure(figsize=(10, 6))
    plt.plot(
        sizes,
        heights_balanced,
        "o-",
        label="Высота (случайная вставка)",
    )
    plt.plot(
        sizes,
        heights_degenerate,
        "s-",
        label="Высота (отсортированная вставка)",
    )
    plt.xlabel("Число элементов в дереве (N)")
    plt.ylabel("Высота дерева h")
    plt.title("Рост высоты BST в сбалансированном и вырожденном случае")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig("bst_heights.png", dpi=300)
    # plt.show()  # Раскомментируйте при запуске локально

    # Краткая текстовая визуализация для небольшого дерева

    print("\nПример текстовой визуализации дерева (N = 15):")
    small_tree = build_balanced_like_tree(15)
    small_tree.visualize()

    # Анализ результатов

    print("\nАнализ результатов:")
    print(
        """- В сбалансированном (случайном) BST
        высота растет примерно как O(log N), """
        "а время поиска — почти линейно от log N.",
    )
    print(
        "- В вырожденном BST высота приблизительно равна N, "
        "а время поиска растет почти линейно от N.",
    )
    print(
        "- Сравнение высот и времен показывает важность балансировки дерева: "
        "вырождение BST превращает все операции из условно O(log N) в O(N).",
    )


if __name__ == "__main__":
    run_experiments()
