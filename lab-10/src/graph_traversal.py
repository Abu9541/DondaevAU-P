# graph_traversal.py


from __future__ import annotations

from collections import deque
from typing import Deque, List, Optional, Sequence, Tuple, TypeVar

TGraph = TypeVar("TGraph")


def bfs(
    graph: TGraph,
    start: int,
) -> Tuple[List[Optional[int]], List[Optional[int]]]:
    """
    BFS (поиск в ширину): возвращает массивы расстояний и родителей.

    Параметры
    ----------
    graph : граф с neighbors(u)
    start : int
        Стартовая вершина.

    Returns
    -------
    dist : list[Optional[int]]
        dist[v] = длина кратчайшего пути (по числу ребер) от start до v,
        либо None, если v недостижима.
    parent : list[Optional[int]]
        parent[v] = предыдущая вершина на кратчайшем пути, либо None.

    Сложность
    ----------
    O(V + E).
    """
    n = graph.num_vertices
    if start < 0 or start >= n:
        raise IndexError("start vertex out of range")

    dist: List[Optional[int]] = [None] * n
    parent: List[Optional[int]] = [None] * n

    q: Deque[int] = deque()
    dist[start] = 0
    q.append(start)

    while q:
        u = q.popleft()
        for v, _ in graph.neighbors(u):
            if dist[v] is None:
                dist[v] = dist[u] + 1 if dist[u] is not None else 1
                parent[v] = u
                q.append(v)

    return dist, parent


def restore_path(
    parent: Sequence[Optional[int]],
    start: int,
    target: int,
) -> List[int]:
    """
    Восстановить путь start -> target по массиву parent.

    Сложность
    ----------
    O(L), где L — длина пути.
    """
    if start == target:
        return [start]

    path: List[int] = []
    cur: Optional[int] = target
    while cur is not None:
        path.append(cur)
        if cur == start:
            break
        cur = parent[cur]

    if not path or path[-1] != start:
        return []
    path.reverse()
    return path


def dfs_recursive(graph: TGraph, start: int) -> List[int]:
    """
    DFS рекурсивный: возвращает порядок посещения.

    Сложность
    ----------
    O(V + E).
    """
    n = graph.num_vertices
    if start < 0 or start >= n:
        raise IndexError("start vertex out of range")

    visited = [False] * n
    order: List[int] = []

    def go(u: int) -> None:
        visited[u] = True
        order.append(u)
        for v, _ in graph.neighbors(u):
            if not visited[v]:
                go(v)

    go(start)
    return order


def dfs_iterative(graph: TGraph, start: int) -> List[int]:
    """
    DFS итеративный: возвращает порядок посещения.

    Сложность
    ----------
    O(V + E).
    """
    n = graph.num_vertices
    if start < 0 or start >= n:
        raise IndexError("start vertex out of range")

    visited = [False] * n
    order: List[int] = []
    stack: List[int] = [start]

    while stack:
        u = stack.pop()
        if visited[u]:
            continue
        visited[u] = True
        order.append(u)

        # Чтобы порядок был ближе к рекурсивному,
        # добавляем соседей в обратном порядке.
        neigh = [v for v, _ in graph.neighbors(u)]
        for v in reversed(neigh):
            if not visited[v]:
                stack.append(v)

    return order


def connected_components(graph: TGraph) -> List[List[int]]:
    """
    Компоненты связности (для неориентированного графа).

    Returns
    -------
    components : list[list[int]]
        Список компонент, каждая компонента — список вершин.

    Сложность
    ----------
    O(V + E).
    """
    if graph.directed:
        raise ValueError("connected_components expects an undirected graph.")

    n = graph.num_vertices
    visited = [False] * n
    components: List[List[int]] = []

    for s in range(n):
        if visited[s]:
            continue
        comp: List[int] = []
        q: Deque[int] = deque([s])
        visited[s] = True

        while q:
            u = q.popleft()
            comp.append(u)
            for v, _ in graph.neighbors(u):
                if not visited[v]:
                    visited[v] = True
                    q.append(v)

        components.append(comp)

    return components


def topological_sort_kahn(graph: TGraph) -> List[int]:
    """
    Топологическая сортировка (алгоритм Кана) для DAG.

    Сложность
    ----------
    O(V + E).

    Returns
    -------
    order : list[int]
        Топологический порядок.
    """
    if not graph.directed:
        raise ValueError("Topological sort requires a directed graph.")

    n = graph.num_vertices
    indeg = [0] * n

    for u in range(n):
        for v, _ in graph.neighbors(u):
            indeg[v] += 1

    q: Deque[int] = deque([v for v in range(n) if indeg[v] == 0])
    order: List[int] = []

    while q:
        u = q.popleft()
        order.append(u)
        for v, _ in graph.neighbors(u):
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    if len(order) != n:
        raise ValueError("""Graph has a cycle;
                         topological order does not exist.""")

    return order


def has_cycle_directed(graph: TGraph) -> bool:
    """
    Проверка наличия цикла в ориентированном графе через цвета (DFS).

    Сложность
    ----------
    O(V + E).

    Returns
    -------
    bool
        True, если найден цикл.
    """
    if not graph.directed:
        raise ValueError("Cycle check here is for directed graphs only.")

    n = graph.num_vertices
    color = [0] * n  # 0=white, 1=gray, 2=black

    def dfs(u: int) -> bool:
        color[u] = 1
        for v, _ in graph.neighbors(u):
            if color[v] == 1:
                return True
            if color[v] == 0 and dfs(v):
                return True
        color[u] = 2
        return False

    for s in range(n):
        if color[s] == 0 and dfs(s):
            return True
    return False
