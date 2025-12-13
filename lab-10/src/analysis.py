# analysis.py


from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Callable, List, Optional, Sequence, Tuple

import matplotlib.pyplot as plt  # type: ignore
from graph_representation import Edge, build_graph_from_edges
from graph_traversal import bfs
from shortest_path import dijkstra

# Информация о ПК (в отчёт)

PC_INFO = """
Характеристики ПК для тестирования:
- Процессор: Intel Core i7-13620H @ 2.40GHz
- Оперативная память: 32 GB DDR5
- ОС: Windows 11
- Python: 3.13.3
"""


# Константы и типы

Weight = float
INF = float("inf")


@dataclass(frozen=True)
class ExperimentConfig:
    """
    Конфигурация эксперимента.

    Атрибуты
    ----------
    sizes : list[int]
        Набор размеров графа (число вершин).
    density : float
        Плотность ребер (0..1) для случайного графа.
    directed : bool
        Ориентированный ли граф.
    repeats : int
        Количество повторов измерения для усреднения.
    operations_per_repeat : int
        Зарезервировано для операций с множеством запросов (в этой версии
        не используется, оставлено для совместимости/расширения).
    seed : int
        Seed генератора случайных чисел.
    """
    sizes: List[int]
    density: float
    directed: bool
    repeats: int
    operations_per_repeat: int
    seed: int = 42


# Вспомогательные функции


def now_seconds() -> float:
    """
    Точное время в секундах (perf_counter).

    Сложность
    ----------
    O(1).
    """
    return time.perf_counter()


def measure_ms(func: Callable[[], None], repeats: int) -> float:
    """
    Измерить среднее время выполнения функции (в миллисекундах).

    Параметры
    ----------
    func : Callable[[], None]
        Функция без аргументов, которую измеряем.
    repeats : int
        Число повторов.

    Returns
    -------
    float
        Среднее время (мс).

    Сложность
    ----------
    O(repeats * T(func)).
    """
    total = 0.0
    for _ in range(repeats):
        t0 = now_seconds()
        func()
        t1 = now_seconds()
        total += (t1 - t0)
    return (total / max(1, repeats)) * 1000.0


def random_weighted_edges_undirected(
    n: int,
    density: float,
    *,
    min_w: float = 1.0,
    max_w: float = 10.0,
    seed: Optional[int] = None,
) -> List[Edge]:
    """
    Сгенерировать случайный неориентированный взвешенный граф.

    Генерация идет по вероятности ребра между каждой парой (i, j), i < j:
    - с вероятностью density добавляется ребро i-j с весом w.

    Сложность
    ----------
    Время: O(n^2).
    Память: O(E).
    """
    if n <= 0:
        raise ValueError("n must be positive.")
    if density < 0.0 or density > 1.0:
        raise ValueError("density must be in [0, 1].")
    if seed is not None:
        random.seed(seed)

    edges: List[Edge] = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() <= density:
                w = random.uniform(min_w, max_w)
                edges.append(Edge(i, j, w))
    return edges


def print_table(
    title: str,
    headers: Sequence[str],
    rows: Sequence[Sequence[str]],
) -> None:
    """
    Печать таблицы в консоль (моноширинный формат).

    Параметры
    ----------
    title : str
        Заголовок таблицы.
    headers : Sequence[str]
        Заголовки столбцов.
    rows : Sequence[Sequence[str]]
        Строки таблицы (каждая строка — список строковых значений).

    Сложность
    ----------
    O(R * C) по количеству ячеек.
    """
    print()
    print(title)

    col_count = len(headers)
    widths = [len(h) for h in headers]

    for row in rows:
        for i in range(col_count):
            widths[i] = max(widths[i], len(row[i]))

    def fmt_row(values: Sequence[str]) -> str:
        parts = []
        for i in range(col_count):
            parts.append(values[i].ljust(widths[i]))
        return " | ".join(parts)

    sep = "-+-".join("-" * w for w in widths)

    print(fmt_row(headers))
    print(sep)
    for row in rows:
        print(fmt_row(row))


# Эксперименты времени


@dataclass(frozen=True)
class Series:
    """
    Одна серия результатов для построения графика.

    Атрибуты
    ----------
    label : str
        Название серии (легенда).
    x : list[int]
        Значения |V|.
    y_ms : list[float]
        Время (мс).
    """
    label: str
    x: List[int]
    y_ms: List[float]


def run_time_experiments(cfg: ExperimentConfig) -> Tuple[Series, Series, Series, Series]:
    """
    Провести эксперименты времени для BFS и Dijkstra:
    - список смежности
    - матрица смежности

    Возвращает 4 серии:
    - BFS (список)
    - BFS (матрица)
    - Dijkstra (список)
    - Dijkstra (матрица)
    """
    random.seed(cfg.seed)

    bfs_list_times: List[float] = []
    bfs_mat_times: List[float] = []
    dij_list_times: List[float] = []
    dij_mat_times: List[float] = []

    for n in cfg.sizes:
        edges = random_weighted_edges_undirected(
            n,
            cfg.density,
            seed=cfg.seed + n,
        )

        g_list = build_graph_from_edges(n,
                                        edges,
                                        representation="list",
                                        directed=cfg.directed)
        g_mat = build_graph_from_edges(n,
                                       edges,
                                       representation="matrix",
                                       directed=cfg.directed)

        start = 0

        bfs_list_times.append(measure_ms(lambda: bfs(g_list, start), cfg.repeats))
        bfs_mat_times.append(measure_ms(lambda: bfs(g_mat, start), cfg.repeats))

        dij_list_times.append(measure_ms(lambda: dijkstra(g_list, start), cfg.repeats))
        dij_mat_times.append(measure_ms(lambda: dijkstra(g_mat, start), cfg.repeats))

    bfs_list = Series("BFS (список смежности)",
                      x=list(cfg.sizes),
                      y_ms=bfs_list_times)
    bfs_mat = Series("BFS (матрица смежности)",
                     x=list(cfg.sizes),
                     y_ms=bfs_mat_times)
    dij_list = Series("Дейкстра (список смежности)",
                      x=list(cfg.sizes),
                      y_ms=dij_list_times)
    dij_mat = Series("Дейкстра (матрица смежности)",
                     x=list(cfg.sizes),
                     y_ms=dij_mat_times)

    return bfs_list, bfs_mat, dij_list, dij_mat


def plot_series(
    series_list: Sequence[Series],
    *,
    title: str,
    xlabel: str,
    ylabel: str,
    output_path: str,
) -> None:
    """
    Построить один график (без subplots) для набора серий.
    """
    plt.figure()
    for s in series_list:
        plt.plot(s.x, s.y_ms, marker="o", label=s.label)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


# Визуализация графа (базовая)


Point = Tuple[float, float]


def circular_layout(n: int, radius: float = 1.0) -> List[Point]:
    """
    Круговая раскладка вершин (координаты на окружности).

    Сложность
    ----------
    O(n).
    """
    import math

    coords: List[Point] = []
    for i in range(n):
        angle = 2.0 * math.pi * i / n
        coords.append((radius * math.cos(angle), radius * math.sin(angle)))
    return coords


def draw_graph_undirected(
    n: int,
    edges: Sequence[Edge],
    *,
    title: str,
    output_path: str,
) -> None:
    """
    Нарисовать неориентированный граф (круговая раскладка) и сохранить PNG.

    Сложность
    ----------
    O(n + E).
    """
    coords = circular_layout(n, radius=1.0)

    plt.figure()

    for e in edges:
        x1, y1 = coords[e.u]
        x2, y2 = coords[e.v]
        plt.plot([x1, x2], [y1, y2], linewidth=1.0)

    xs = [coords[i][0] for i in range(n)]
    ys = [coords[i][1] for i in range(n)]
    plt.scatter(xs, ys)

    for i, (x, y) in enumerate(coords):
        plt.text(x, y, f" {i}", fontsize=10)

    plt.title(title)
    plt.axis("equal")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def visualize_graph_example() -> None:
    """
    Сохранить базовую визуализацию случайного графа без подсветки алгоритмов.

    Выходной файл:
    - graph.png
    """
    n = 10
    density = 0.25
    edges = random_weighted_edges_undirected(n, density, seed=123)

    draw_graph_undirected(
        n,
        edges,
        title="Пример случайного неориентированного графа",
        output_path="../report/graph.png",
    )


# Main


def main() -> None:
    """
    Запуск анализа.

    Сохраняемые файлы:
    - time_bfs.png
    - time_dijkstra.png
    - graph.png

    Дополнительно:
    - вывод в консоль характеристик ПК
    - вывод таблиц результатов замеров
    """
    print(PC_INFO)

    cfg = ExperimentConfig(
        sizes=[50, 100, 150, 200, 250, 300],
        density=0.05,
        directed=False,
        repeats=5,
        operations_per_repeat=300,
        seed=42,
    )

    bfs_list, bfs_mat, dij_list, dij_mat = run_time_experiments(cfg)

    # ===== Таблицы результатов =====
    bfs_rows: List[List[str]] = []
    for n, t_list, t_mat in zip(bfs_list.x, bfs_list.y_ms, bfs_mat.y_ms):
        bfs_rows.append([str(n), f"{t_list:.3f}", f"{t_mat:.3f}"])

    print_table(
        title="Таблица результатов: время выполнения BFS",
        headers=["|V| (число вершин)", "Список смежности (мс)", "Матрица смежности (мс)"],
        rows=bfs_rows,
    )

    dij_rows: List[List[str]] = []
    for n, t_list, t_mat in zip(dij_list.x, dij_list.y_ms, dij_mat.y_ms):
        dij_rows.append([str(n), f"{t_list:.3f}", f"{t_mat:.3f}"])

    print_table(
        title="Таблица результатов: время выполнения алгоритма Дейкстры",
        headers=["|V| (число вершин)", "Список смежности (мс)", "Матрица смежности (мс)"],
        rows=dij_rows,
    )

    # ===== Графики =====
    plot_series(
        [bfs_list, bfs_mat],
        title="Зависимость времени BFS от числа вершин графа",
        xlabel="Число вершин графа |V|",
        ylabel="Среднее время выполнения BFS, мс",
        output_path="../report/time_bfs.png",
    )

    plot_series(
        [dij_list, dij_mat],
        title="Зависимость времени алгоритма Дейкстры от числа вершин графа",
        xlabel="Число вершин графа |V|",
        ylabel="Среднее время выполнения алгоритма Дейкстры, мс",
        output_path="../report/time_dijkstra.png",
    )

    # ===== Визуализация =====
    visualize_graph_example()

    print()
    print("Готово. Сохранены файлы:")
    print("  time_bfs.png")
    print("  time_dijkstra.png")
    print("  graph.png")


if __name__ == "__main__":
    main()
