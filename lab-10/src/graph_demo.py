# graph_demo.py


from __future__ import annotations

from graph_representation import Edge, build_graph_from_edges
from graph_traversal import (
    bfs,
    connected_components,
    dfs_iterative,
    dfs_recursive,
    restore_path as restore_path_bfs,
    topological_sort_kahn,
)
from shortest_path import (
    dijkstra,
    is_connected_undirected,
    restore_path as restore_path_dijkstra,
    shortest_path_in_maze_bfs,
)


def print_sep(title: str) -> None:
    line = "-" * 60
    print()
    print(line)
    print(title)
    print(line)


def demo_representations() -> None:
    print_sep("1) Представления графа: матрица и список смежности")

    edges = [
        Edge(0, 1, 2.0),
        Edge(0, 2, 1.0),
        Edge(1, 2, 3.0),
        Edge(2, 3, 1.0),
    ]

    g_list = build_graph_from_edges(4, edges,
                                    representation="list", directed=False)
    g_mat = build_graph_from_edges(4, edges, representation="matrix",
                                   directed=False)

    print("Список смежности: соседи(0) =", g_list.neighbors(0))
    print("Матрица смежности: соседи(0) =", g_mat.neighbors(0))
    print("Проверка ребра 1-3 (list) =", g_list.has_edge(1, 3))
    print("Проверка ребра 1-3 (matrix) =", g_mat.has_edge(1, 3))


def demo_bfs_dfs() -> None:
    print_sep("2) BFS/DFS")

    edges = [
        Edge(0, 1),
        Edge(0, 2),
        Edge(1, 3),
        Edge(2, 3),
        Edge(3, 4),
    ]
    g = build_graph_from_edges(5, edges, representation="list", directed=False)

    dist, parent = bfs(g, start=0)
    print("BFS расстояния от 0:", dist)
    print("BFS путь 0 -> 4:", restore_path_bfs(parent, 0, 4))

    print("DFS рекурсивный от 0:", dfs_recursive(g, 0))
    print("DFS итеративный от 0:", dfs_iterative(g, 0))


def demo_components() -> None:
    print_sep("3) Компоненты связности")

    edges = [
        Edge(0, 1),
        Edge(1, 2),
        Edge(3, 4),
    ]
    g = build_graph_from_edges(5, edges, representation="list", directed=False)
    comps = connected_components(g)
    print("Компоненты:", comps)


def demo_toposort() -> None:
    print_sep("4) Топологическая сортировка (DAG)")

    # 0->1, 0->2, 1->3, 2->3 (типичный граф зависимостей)
    edges = [
        Edge(0, 1),
        Edge(0, 2),
        Edge(1, 3),
        Edge(2, 3),
    ]
    g = build_graph_from_edges(4, edges, representation="list", directed=True)
    order = topological_sort_kahn(g)
    print("Топологический порядок:", order)


def demo_dijkstra() -> None:
    print_sep("5) Алгоритм Дейкстры")

    edges = [
        Edge(0, 1, 7.0),
        Edge(0, 2, 9.0),
        Edge(0, 5, 14.0),
        Edge(1, 2, 10.0),
        Edge(1, 3, 15.0),
        Edge(2, 3, 11.0),
        Edge(2, 5, 2.0),
        Edge(3, 4, 6.0),
        Edge(4, 5, 9.0),
    ]
    g = build_graph_from_edges(6, edges, representation="list", directed=False)

    dist, parent = dijkstra(g, start=0)
    print("Расстояния от 0:", dist)
    print("Путь 0 -> 4:", restore_path_dijkstra(parent, 0, 4))
    print("Длина пути 0 -> 4:", dist[4])


def practical_maze() -> None:
    print_sep("Практическая задача 1: кратчайший путь в лабиринте (BFS)")

    grid = [
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
    ]
    start = (0, 0)
    goal = (4, 4)

    path = shortest_path_in_maze_bfs(grid, start, goal)
    print("Путь:", path)
    print("Длина (в шагах):", max(0, len(path) - 1))


def practical_network_connectivity() -> None:
    print_sep("Практическая задача 2: связность сети")

    edges = [
        Edge(0, 1),
        Edge(1, 2),
        Edge(2, 3),
        Edge(3, 4),
    ]
    g = build_graph_from_edges(5, edges, representation="list", directed=False)
    print("Сеть связна?", is_connected_undirected(g))

    g.remove_edge(2, 3)
    print("После удаления ребра 2-3 сеть связна?", is_connected_undirected(g))


def practical_dependencies() -> None:
    print_sep("Практическая задача 3: порядок выполнения задач (топосорт)")

    # Задачи 0..5, зависимости:
    # 0 -> 2, 1 -> 2, 2 -> 3, 2 -> 4, 3 -> 5, 4 -> 5
    edges = [
        Edge(0, 2),
        Edge(1, 2),
        Edge(2, 3),
        Edge(2, 4),
        Edge(3, 5),
        Edge(4, 5),
    ]
    g = build_graph_from_edges(6, edges, representation="list", directed=True)
    order = topological_sort_kahn(g)
    print("Допустимый порядок выполнения:", order)


def main() -> None:
    demo_representations()
    demo_bfs_dfs()
    demo_components()
    demo_toposort()
    demo_dijkstra()
    practical_maze()
    practical_network_connectivity()
    practical_dependencies()


if __name__ == "__main__":
    main()
