# analysis.py


from __future__ import annotations

import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Sequence, Tuple

import matplotlib.pyplot as plt
from string_matching import (
    kmp_search,
    naive_search,
    rabin_karp_search,
    z_search,
)

OUTPUT_DIR = Path(__file__).resolve().parent


PC_INFO = """
Характеристики ПК для тестирования:
- Процессор: Intel Core i7-13620H @ 2.40GHz
- Оперативная память: 32 GB DDR5
- ОС: Windows 11
- Python: 3.13.3
"""


@dataclass(frozen=True)
class Case:
    """Описание тестового случая."""
    name: str
    make_text: Callable[[int], str]
    make_pattern: Callable[[str], str]


def timer_ms(func: Callable[[], None], repeats: int) -> float:
    """Среднее время выполнения func в миллисекундах."""
    total = 0.0
    for _ in range(repeats):
        t0 = time.perf_counter()
        func()
        total += time.perf_counter() - t0
    return (total / max(1, repeats)) * 1000.0


def random_text(n: int, alphabet: str = "abcdefghijklmnopqrstuvwxyz") -> str:
    return "".join(random.choice(alphabet) for _ in range(n))


def periodic_text(n: int, period: str = "abac") -> str:
    if not period:
        return ""
    reps = (n + len(period) - 1) // len(period)
    return (period * reps)[:n]


def worst_for_naive(n: int) -> str:
    return "a" * n


def pattern_from_text(text: str, m: int, force_present: bool = True) -> str:
    if m <= 0:
        return ""
    if not text:
        return "a" * m
    if force_present and len(text) >= m:
        start = max(0, len(text) // 2 - m // 2)
        return text[start: start + m]
    return "b" * m


def benchmark_case(
    case: Case,
    sizes: Sequence[int],
    pattern_len: int,
    repeats: int,
    seed: int = 42,
) -> Tuple[List[int], Dict[str, List[float]]]:
    """Замеры времени для одного тестового случая."""
    random.seed(seed)

    algos: Dict[str, Callable[[str, str], List[int]]] = {
        "Наивный": naive_search,
        "KMP": kmp_search,
        "Z-поиск": z_search,
        "Рабин–Карп": rabin_karp_search,
    }

    x: List[int] = []
    y: Dict[str, List[float]] = {name: [] for name in algos}

    for n in sizes:
        text = case.make_text(n)
        pattern = case.make_pattern(text)

        x.append(n)
        for name, algo in algos.items():
            t = timer_ms(lambda: algo(text, pattern), repeats=repeats)
            y[name].append(t)

    return x, y


def plot_benchmark(
    x: Sequence[int],
    y: Dict[str, Sequence[float]],
    title: str,
    output_name: str,
) -> None:
    """Один график сравнения алгоритмов (подписи на русском)."""
    plt.figure()
    for name, values in y.items():
        plt.plot(list(x), list(values), marker="o", label=name)

    plt.title(title)
    plt.xlabel("Длина текста, n")
    plt.ylabel("Среднее время поиска, мс")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / output_name, dpi=200)
    plt.close()


def print_table(title: str,
                x: Sequence[int],
                y: Dict[str, Sequence[float]]) -> None:
    """Печать таблицы результатов в консоль."""
    print()
    print(title)

    headers = ["n"] + list(y.keys())
    widths = [max(len(h), 6) for h in headers]

    rows: List[List[str]] = []
    for i, n in enumerate(x):
        row = [str(n)]
        for name in y.keys():
            row.append(f"{y[name][i]:.3f}")
        rows.append(row)

    for r in rows:
        for j, v in enumerate(r):
            widths[j] = max(widths[j], len(v))

    def fmt(row: Sequence[str]) -> str:
        return " | ".join(row[j].ljust(widths[j]) for j in range(len(row)))

    sep = "-+-".join("-" * w for w in widths)

    print(fmt(headers))
    print(sep)
    for r in rows:
        print(fmt(r))


def main() -> None:
    print(PC_INFO)

    sizes = [1_000, 2_000, 4_000, 8_000, 16_000]
    pattern_len = 20
    repeats = 5

    cases = [
        Case(
            name="Случайный текст",
            make_text=lambda n: random_text(n),
            make_pattern=lambda text: pattern_from_text(text,
                                                        pattern_len,
                                                        force_present=True),
        ),
        Case(
            name="Периодический текст",
            make_text=lambda n: periodic_text(n),
            make_pattern=lambda text: pattern_from_text(text,
                                                        pattern_len,
                                                        force_present=True),
        ),
        Case(
            name="Худший случай для наивного",
            make_text=lambda n: worst_for_naive(n),
            make_pattern=lambda text: ("a" * (pattern_len - 1) + "b"),
        ),
    ]

    outputs = [
        ("perf_random.png",
         "Сравнение алгоритмов поиска подстроки (случайный текст)"),
        ("perf_periodic.png",
         "Сравнение алгоритмов поиска подстроки (периодический текст)"),
        ("perf_worst_naive.png",
         "Сравнение алгоритмов (сложный случай для наивного поиска)"),
    ]

    for case, (fname, title) in zip(cases, outputs):
        x, y = benchmark_case(case, sizes, pattern_len, repeats, seed=42)
        print_table(f"Таблица: {case.name}", x, y)
        plot_benchmark(x, y, title, fname)

    print()
    print("Готово. Графики сохранены в директорию src:")
    for fname, _ in outputs:
        print(f"- {fname}")


if __name__ == "__main__":
    main()
