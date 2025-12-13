# tests.py


from __future__ import annotations

import unittest

from graph_representation import (Edge,
                                  GraphAdjList,
                                  GraphAdjMatrix,
                                  build_graph_from_edges)
from graph_traversal import (bfs,
                             connected_components,
                             restore_path,
                             topological_sort_kahn)
from shortest_path import (dijkstra,
                           restore_path as restore_path_dijkstra,
                           shortest_path_in_maze_bfs)


class TestRepresentations(unittest.TestCase):
    def test_matrix_add_and_has_edge(self) -> None:
        g = GraphAdjMatrix(3, directed=False)
        g.add_edge(0, 1, 2.0)
        self.assertTrue(g.has_edge(0, 1))
        self.assertTrue(g.has_edge(1, 0))
        self.assertEqual(g.weight(0, 1), 2.0)

    def test_list_add_and_remove_edge(self) -> None:
        g = GraphAdjList(3, directed=True)
        g.add_edge(0, 2, 5.0)
        self.assertTrue(g.has_edge(0, 2))
        g.remove_edge(0, 2)
        self.assertFalse(g.has_edge(0, 2))


class TestTraversal(unittest.TestCase):
    def test_bfs_restore_path(self) -> None:
        edges = [Edge(0, 1), Edge(1, 2), Edge(0, 2)]
        g = build_graph_from_edges(3, edges, representation="list",
                                   directed=False)
        dist, parent = bfs(g, 0)
        self.assertEqual(dist[2], 1)
        self.assertEqual(restore_path(parent, 0, 2), [0, 2])

    def test_connected_components(self) -> None:
        edges = [Edge(0, 1), Edge(2, 3)]
        g = build_graph_from_edges(4, edges,
                                   representation="list", directed=False)
        comps = connected_components(g)
        sizes = sorted(len(c) for c in comps)
        self.assertEqual(sizes, [2, 2])

    def test_toposort(self) -> None:
        edges = [Edge(0, 1), Edge(0, 2), Edge(1, 3), Edge(2, 3)]
        g = build_graph_from_edges(4, edges, representation="list",
                                   directed=True)
        order = topological_sort_kahn(g)
        self.assertEqual(set(order), {0, 1, 2, 3})
        self.assertLess(order.index(0), order.index(1))
        self.assertLess(order.index(0), order.index(2))
        self.assertLess(order.index(1), order.index(3))
        self.assertLess(order.index(2), order.index(3))


class TestShortestPaths(unittest.TestCase):
    def test_dijkstra(self) -> None:
        edges = [Edge(0, 1, 1.0), Edge(1, 2, 2.0), Edge(0, 2, 10.0)]
        g = build_graph_from_edges(3, edges,
                                   representation="list", directed=False)
        dist, parent = dijkstra(g, 0)
        self.assertAlmostEqual(dist[2], 3.0)
        self.assertEqual(restore_path_dijkstra(parent, 0, 2), [0, 1, 2])

    def test_maze_bfs(self) -> None:
        grid = [
            [0, 0, 1],
            [0, 0, 0],
            [1, 0, 0],
        ]
        path = shortest_path_in_maze_bfs(grid, (0, 0), (2, 2))
        self.assertTrue(path)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (2, 2))


if __name__ == "__main__":
    unittest.main()
