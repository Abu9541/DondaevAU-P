# graph_representation.py


from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

Weight = float


@dataclass(frozen=True)
class Edge:
    """
    Ребро графа.

    Атрибуты
    ----------
    u : int
        Начальная вершина.
    v : int
        Конечная вершина.
    w : float
        Вес ребра.
    """
    u: int
    v: int
    w: Weight = 1.0


class GraphAdjMatrix:
    """
    Граф на матрице смежности.

    Память
    ------
    O(V^2).
    """

    def __init__(self, num_vertices: int, directed: bool = False) -> None:
        if num_vertices <= 0:
            raise ValueError("num_vertices must be positive.")
        self._directed = directed
        self._n = num_vertices
        self._m: List[List[Optional[Weight]]] = [
            [None for _ in range(self._n)] for _ in range(self._n)
        ]

    @property
    def directed(self) -> bool:
        """True, если граф ориентированный. O(1)."""
        return self._directed

    @property
    def num_vertices(self) -> int:
        """Количество вершин. O(1)."""
        return self._n

    def _check_vertex(self, v: int) -> None:
        if v < 0 or v >= self._n:
            raise IndexError(f"Vertex {v} is out of range 0..{self._n - 1}.")

    def add_edge(self, u: int, v: int, w: Weight = 1.0) -> None:
        """
        Добавить ребро u->v (и v->u для неориентированного).

        Сложность
        ----------
        O(1).
        """
        self._check_vertex(u)
        self._check_vertex(v)
        self._m[u][v] = float(w)
        if not self._directed:
            self._m[v][u] = float(w)

    def remove_edge(self, u: int, v: int) -> None:
        """
        Удалить ребро u->v (и v->u для неориентированного).

        Сложность
        ----------
        O(1).
        """
        self._check_vertex(u)
        self._check_vertex(v)
        self._m[u][v] = None
        if not self._directed:
            self._m[v][u] = None

    def has_edge(self, u: int, v: int) -> bool:
        """
        Проверка наличия ребра u->v.

        Сложность
        ----------
        O(1).
        """
        self._check_vertex(u)
        self._check_vertex(v)
        return self._m[u][v] is not None

    def weight(self, u: int, v: int) -> Optional[Weight]:
        """
        Вес ребра u->v или None, если ребра нет.

        Сложность
        ----------
        O(1).
        """
        self._check_vertex(u)
        self._check_vertex(v)
        return self._m[u][v]

    def neighbors(self, u: int) -> List[Tuple[int, Weight]]:
        """
        Соседи вершины u: список (v, w) по всем v, где есть ребро u->v.

        Сложность
        ----------
        O(V).
        """
        self._check_vertex(u)
        result: List[Tuple[int, Weight]] = []
        for v, w in enumerate(self._m[u]):
            if w is not None:
                result.append((v, w))
        return result

    def edges(self) -> List[Edge]:
        """
        Список всех рёбер.

        Сложность
        ----------
        O(V^2).
        """
        result: List[Edge] = []
        for u in range(self._n):
            for v in range(self._n):
                w = self._m[u][v]
                if w is not None:
                    if self._directed or u <= v:
                        result.append(Edge(u, v, w))
        return result

    def add_vertex(self) -> int:
        """
        Добавить новую вершину, вернуть её индекс.

        Сложность
        ----------
        O(V^2) (пересоздание/расширение матрицы).
        """
        self._n += 1
        for row in self._m:
            row.append(None)
        self._m.append([None for _ in range(self._n)])
        return self._n - 1

    def remove_vertex(self, v: int) -> None:
        """
        Удалить вершину v (с переиндексацией).

        Сложность
        ----------
        O(V^2).
        """
        self._check_vertex(v)
        self._m.pop(v)
        for row in self._m:
            row.pop(v)
        self._n -= 1


class GraphAdjList:
    """
    Граф на списках смежности.

    Память
    ------
    O(V + E).
    """

    def __init__(self, num_vertices: int, directed: bool = False) -> None:
        if num_vertices <= 0:
            raise ValueError("num_vertices must be positive.")
        self._directed = directed
        self._adj: List[List[Tuple[int, Weight]]] = [[] for _ in range(num_vertices)]

    @property
    def directed(self) -> bool:
        """True, если граф ориентированный. O(1)."""
        return self._directed

    @property
    def num_vertices(self) -> int:
        """Количество вершин. O(1)."""
        return len(self._adj)

    def _check_vertex(self, v: int) -> None:
        if v < 0 or v >= self.num_vertices:
            raise IndexError(f"""Vertex {v} is
                             out of range 0..{self.num_vertices - 1}.""")

    def add_vertex(self) -> int:
        """
        Добавить новую вершину, вернуть индекс.

        Сложность
        ----------
        O(1) амортизированно.
        """
        self._adj.append([])
        return self.num_vertices - 1

    def remove_vertex(self, v: int) -> None:
        """
        Удалить вершину v (с переиндексацией).

        Сложность
        ----------
        O(V + E) из-за правки списков и индексов.
        """
        self._check_vertex(v)
        self._adj.pop(v)

        for u in range(self.num_vertices):
            new_list: List[Tuple[int, Weight]] = []
            for to, w in self._adj[u]:
                if to == v:
                    continue
                new_to = to - 1 if to > v else to
                new_list.append((new_to, w))
            self._adj[u] = new_list

    def add_edge(self, u: int, v: int, w: Weight = 1.0) -> None:
        """
        Добавить ребро u->v (и v->u для неориентированного).

        Сложность
        ----------
        O(deg(u)) для проверки/обновления.
        """
        self._check_vertex(u)
        self._check_vertex(v)
        self._set_edge(u, v, float(w))
        if not self._directed:
            self._set_edge(v, u, float(w))

    def _set_edge(self, u: int, v: int, w: Weight) -> None:
        for i, (to, _) in enumerate(self._adj[u]):
            if to == v:
                self._adj[u][i] = (v, w)
                return
        self._adj[u].append((v, w))

    def remove_edge(self, u: int, v: int) -> None:
        """
        Удалить ребро u->v (и v->u для неориентированного).

        Сложность
        ----------
        O(deg(u)).
        """
        self._check_vertex(u)
        self._check_vertex(v)
        self._adj[u] = [(to, w) for (to, w) in self._adj[u] if to != v]
        if not self._directed:
            self._adj[v] = [(to, w) for (to, w) in self._adj[v] if to != u]

    def has_edge(self, u: int, v: int) -> bool:
        """
        Проверка наличия ребра u->v.

        Сложность
        ----------
        O(deg(u)).
        """
        self._check_vertex(u)
        self._check_vertex(v)
        return any(to == v for (to, _) in self._adj[u])

    def weight(self, u: int, v: int) -> Optional[Weight]:
        """
        Вес ребра u->v или None, если ребра нет.

        Сложность
        ----------
        O(deg(u)).
        """
        self._check_vertex(u)
        self._check_vertex(v)
        for to, w in self._adj[u]:
            if to == v:
                return w
        return None

    def neighbors(self, u: int) -> List[Tuple[int, Weight]]:
        """
        Соседи вершины u: список (v, w).

        Сложность
        ----------
        O(deg(u)).
        """
        self._check_vertex(u)
        return list(self._adj[u])

    def edges(self) -> List[Edge]:
        """
        Список всех рёбер.

        Сложность
        ----------
        O(V + E).
        """
        result: List[Edge] = []
        for u in range(self.num_vertices):
            for v, w in self._adj[u]:
                if self._directed or u <= v:
                    result.append(Edge(u, v, w))
        return result


def build_graph_from_edges(
    num_vertices: int,
    edges: Iterable[Edge],
    *,
    representation: str = "list",
    directed: bool = False,
):
    """
    Вспомогательная фабрика: построить граф по списку рёбер.

    Параметры
    ----------
    num_vertices : int
        Число вершин.
    edges : Iterable[Edge]
        Рёбра.
    representation : {"list", "matrix"}
        Тип представления.
    directed : bool
        Ориентированный ли граф.

    Returns
    -------
    GraphAdjList | GraphAdjMatrix
        Экземпляр графа.

    Сложность
    ----------
    Зависит от представления. Добавление E ребер:
    - list: суммарно ~ O(E * avg_deg) при обновлениях, обычно близко к O(E)
    - matrix: O(E)
    """
    if representation == "list":
        g = GraphAdjList(num_vertices, directed=directed)
    elif representation == "matrix":
        g = GraphAdjMatrix(num_vertices, directed=directed)
    else:
        raise ValueError("representation must be 'list' or 'matrix'")

    for e in edges:
        g.add_edge(e.u, e.v, e.w)
    return g
