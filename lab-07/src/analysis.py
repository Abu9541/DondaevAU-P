# analysis.py


from __future__ import annotations

import random
import timeit
from typing import List

import matplotlib.pyplot as plt

from heap import Heap
from heapsort import heapsort_with_heap, heapsort_inplace

PC_INFO = """
Характеристики ПК для тестирования:
- Процессор: Intel Core i7-13620H @ 2.40GHz
- Оперативная память: 32 GB DDR5
- ОС: Windows 11
- Python: 3.13.3
"""


def generate_random_array(size: int) -> List[int]:
    """Генерирует массив случайных целых чисел.

    Время: O(n).
    """
    return [random.randint(0, size * 10) for _ in range(size)]


def build_heap_by_inserts(values: List[int], is_min: bool = True) -> Heap:
    """Строит кучу, последовательно вставляя элементы.

    Это "медленный" способ построения: O(n log n).

    Время: O(n log n) в среднем.
    """
    heap = Heap(is_min=is_min)
    for v in values:
        heap.insert(v)
    return heap


def measure_time(func, *args, repeat: int = 5, **kwargs) -> float:
    """Замеряет среднее время выполнения функции в миллисекундах.

    Время:
        - O(repeat * T_func)
    """
    def wrapper() -> None:
        func(*args, **kwargs)

    total = timeit.timeit(wrapper, number=repeat)
    avg = total / repeat
    return avg * 1000.0  # в миллисекундах.


def experiment_build_heap() -> None:
    """Сравнивает время двух способов построения кучи.

    - по вставкам (O(n log n));
    - build_heap (O(n)).

    Результат:
        - печать таблицы;
        - график build.png.
    """
    sizes = [1_000, 5_000, 10_000, 20_000, 50_000]

    times_insert: List[float] = []
    times_build: List[float] = []

    print("Сравнение способов построения min-heap:")
    print("{:>10} {:>15} {:>15}".format("N", "insert (мс)", "build_heap (мс)"))

    for n in sizes:
        data = generate_random_array(n)

        t_insert = measure_time(build_heap_by_inserts, data, True)
        heap_for_build = Heap(is_min=True)
        t_build = measure_time(heap_for_build.build_heap, data)

        times_insert.append(t_insert)
        times_build.append(t_build)

        print("{:>10} {:>15.3f} {:>15.3f}".format(n, t_insert, t_build))

    # График времени построения кучи.
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times_insert, "o-",
             label="Построение через insert (O(n log n))")
    plt.plot(sizes, times_build, "s-", label="build_heap (O(n))")
    plt.xlabel("Размер массива N")
    plt.ylabel("Время построения (мс)")
    plt.title("Сравнение методов построения кучи")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig("build.png", dpi=300)
    # plt.show()


def experiment_heapsort() -> None:
    """Сравнивает время работы разных алгоритмов сортировки.

    - heapsort_with_heap (с вспомогательной кучей);
    - heapsort_inplace (in-place Heapsort);
    - встроенная sorted() (Timsort).

    Результат:
        - печать таблицы;
        - график heapsort.png.
    """
    sizes = [1_000, 5_000, 10_000, 20_000, 50_000]

    times_heap_with: List[float] = []
    times_heap_inplace: List[float] = []
    times_sorted: List[float] = []

    print("\nСравнение Heapsort и встроенной сортировки:")
    print(
        "{:>10} {:>15} {:>18} {:>15}".format(
            "N",
            "with_heap (мс)",
            "inplace_heap (мс)",
            "sorted (мс)",
        ),
    )

    for n in sizes:
        data = generate_random_array(n)

        t_with = measure_time(heapsort_with_heap, list(data))
        arr_inplace = list(data)
        t_inplace = measure_time(heapsort_inplace, arr_inplace)
        t_sorted = measure_time(sorted, data)

        times_heap_with.append(t_with)
        times_heap_inplace.append(t_inplace)
        times_sorted.append(t_sorted)

        print(
            "{:>10} {:>15.3f} {:>18.3f} {:>15.3f}".format(
                n,
                t_with,
                t_inplace,
                t_sorted,
            ),
        )

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times_heap_with, "o-", label="heapsort_with_heap")
    plt.plot(sizes, times_heap_inplace, "s-", label="heapsort_inplace")
    plt.plot(sizes, times_sorted, "^-", label="sorted (Timsort)")
    plt.xlabel("Размер массива N")
    plt.ylabel("Время сортировки (мс)")
    plt.title("Сравнение Heapsort и встроенной сортировки Python")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig("heapsort.png", dpi=300)
    # plt.show()


def main() -> None:
    """Точка входа для запуска всех экспериментов. O(Σ экспериментов)."""
    print(PC_INFO)
    experiment_build_heap()
    experiment_heapsort()
    print(
        "\nАнализ:\n"
        "- Построение кучи через build_heap растет примерно линейно, что "
        "соответствует теории O(n).\n"
        "- Построение через последовательные insert растет быстрее, близко "
        "к O(n log n).\n"
        "- Heapsort in-place по времени близок к Heapsort с вспомогательной "
        "кучей, но использует O(1) дополнительной памяти.\n"
        "- Встроенная sorted() обычно быстрее за счет оптимизаций Timsort, "
        "но Heapsort гарантирует O(n log n) в худшем случае.",
    )


if __name__ == "__main__":
    main()
