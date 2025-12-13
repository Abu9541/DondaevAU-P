# shortest_path.py

from __future__ import annotations

import heapq
from collections import deque
from typing import Deque, List, Optional, Sequence, Tuple, TypeVar

TGraph = TypeVar("TGraph")
INF = float("inf")


def dijkstra(
    graph: TGraph,
    start: int,
) -> Tuple[List[float], List[Optional[int]]]:
    """
    Алгоритм Дейкстры для графа с неотрицательными весами.

    Параметры
    ----------
    graph : граф
    start : int
        Стартовая вершина.

    Returns
    -------
    dist : list[float]
        dist[v] = кратчайшее расстояние от start до v (INF если недостижимо).
    parent : list[Optional[int]]
        parent[v] = предыдущая вершина на кратчайшем пути.

    Сложность
    ----------
    O((V + E) log V) при использовании двоичной кучи.
    """
    n = graph.num_vertices
    if start < 0 or start >= n:
        raise IndexError("start vertex out of range")

    dist = [INF] * n
    parent: List[Optional[int]] = [None] * n
    dist[start] = 0.0

    pq: List[Tuple[float, int]] = [(0.0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue

        for v, w in graph.neighbors(u):
            if w < 0:
                raise ValueError("""Dijkstra does not support
                                 negative edge weights.""")
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))

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
    O(L).
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


# Прикладная задача 1: лабиринт (BFS)


Grid = List[List[int]]  # 0=свободно, 1=стена
Cell = Tuple[int, int]


def shortest_path_in_maze_bfs(
    grid: Grid,
    start: Cell,
    goal: Cell,
) -> List[Cell]:
    """
    Кратчайший путь в лабиринте по клеткам (4-соседство) через BFS.

    Параметры
    ----------
    grid : Grid
        0 = проход, 1 = стена.
    start : (r, c)
    goal : (r, c)

    Returns
    -------
    path : list[Cell]
        Список клеток от start до goal (включая), либо [] если пути нет.

    Сложность
    ----------
    O(R*C) по времени и памяти.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    if rows == 0 or cols == 0:
        return []

    sr, sc = start
    gr, gc = goal
    if not (0 <= sr < rows and 0 <= sc < cols):
        raise IndexError("start is out of grid bounds")
    if not (0 <= gr < rows and 0 <= gc < cols):
        raise IndexError("goal is out of grid bounds")
    if grid[sr][sc] == 1 or grid[gr][gc] == 1:
        return []

    parent: List[List[Optional[Cell]]] = [[None] * cols for _ in range(rows)]
    visited = [[False] * cols for _ in range(rows)]
    q: Deque[Cell] = deque([start])
    visited[sr][sc] = True

    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while q:
        r, c = q.popleft()
        if (r, c) == goal:
            break

        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < rows and 0 <= nc < cols
                and not visited[nr][nc]
                and grid[nr][nc] == 0
            ):
                visited[nr][nc] = True
                parent[nr][nc] = (r, c)
                q.append((nr, nc))

    if not visited[gr][gc]:
        return []

    # восстановление пути
    path: List[Cell] = []
    cur: Optional[Cell] = goal
    while cur is not None:
        path.append(cur)
        if cur == start:
            break
        cr, cc = cur
        cur = parent[cr][cc]

    if not path or path[-1] != start:
        return []
    path.reverse()
    return path


# Прикладная задача 2: связность сети


def is_connected_undirected(graph: TGraph) -> bool:
    """
    Проверка связности неориентированного графа.

    Сложность
    ----------
    O(V + E).
    """
    if graph.directed:
        raise ValueError("""is_connected_undirected expects
                         an undirected graph.""")

    n = graph.num_vertices
    if n == 0:
        return True

    visited = [False] * n
    q: Deque[int] = deque([0])
    visited[0] = True

    while q:
        u = q.popleft()
        for v, _ in graph.neighbors(u):
            if not visited[v]:
                visited[v] = True
                q.append(v)

    return all(visited)
