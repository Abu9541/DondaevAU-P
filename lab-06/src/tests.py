# tests.py


from __future__ import annotations

import unittest

from binary_search_tree import (
    BinarySearchTree,
    TreeNode,
    build_bst_from_iterable,
)
from tree_traversal import (
    inorder_list,
    preorder_list,
    postorder_list,
    inorder_iterative,
)


class TestBinarySearchTree(unittest.TestCase):
    """Набор тестов для BST."""

    def setUp(self) -> None:
        """Создание небольшого дерева перед каждым тестом. O(n)."""
        self.values = [5, 3, 7, 2, 4, 6, 8]
        self.tree = build_bst_from_iterable(self.values)

    def test_insert_and_search(self) -> None:
        """Проверка вставки и поиска элементов. O(n log n)."""
        for value in self.values:
            node = self.tree.search(value)
            self.assertIsNotNone(node)
            self.assertEqual(node.value, value)

        self.assertIsNone(self.tree.search(42))

    def test_inorder_traversal_sorted(self) -> None:
        """In-order обход должен возвращать отсортированный список. O(n)."""
        in_order = inorder_list(self.tree.root)
        self.assertEqual(in_order, sorted(self.values))

    def test_preorder_and_postorder_lengths(self) -> None:
        """Обходы pre/post-order должны иметь правильную длину. O(n)."""
        pre = preorder_list(self.tree.root)
        post = postorder_list(self.tree.root)
        self.assertEqual(len(pre), len(self.values))
        self.assertEqual(len(post), len(self.values))

    def test_iterative_inorder_equals_recursive(self) -> None:
        """Итеративный in-order совпадает с рекурсивным. O(n)."""
        rec = inorder_list(self.tree.root)
        it = inorder_iterative(self.tree.root)
        self.assertEqual(rec, it)

    def test_find_min_and_max(self) -> None:
        """Проверка поиска минимума и максимума. O(h)."""
        min_node = self.tree.find_min(self.tree.root)
        max_node = self.tree.find_max(self.tree.root)
        self.assertIsNotNone(min_node)
        self.assertIsNotNone(max_node)
        self.assertEqual(min_node.value, min(self.values))
        self.assertEqual(max_node.value, max(self.values))

    def test_delete_leaf(self) -> None:
        """Удаление листа должно сохранять свойство BST. O(h)."""
        self.tree.delete(2)
        self.assertIsNone(self.tree.search(2))
        self.assertTrue(self.tree.is_valid_bst())

    def test_delete_node_with_one_child(self) -> None:
        """Удаление узла с одним потомком. O(h)."""
        # Добавим узел, чтобы гарантировать один потомок.
        self.tree.insert(9)  # 8 будет родителем 9
        self.tree.delete(9)  # удаляем лист сначала.
        self.tree.delete(8)  # теперь у 7 один правый потомок (None).
        self.assertIsNone(self.tree.search(8))
        self.assertTrue(self.tree.is_valid_bst())

    def test_delete_node_with_two_children(self) -> None:
        """Удаление узла с двумя потомками (классический случай). O(h)."""
        self.tree.delete(3)
        self.assertIsNone(self.tree.search(3))
        self.assertTrue(self.tree.is_valid_bst())

    def test_height_balanced_vs_degenerate(self) -> None:
        """Сравнение высоты сбалансированного и вырожденного деревьев. O(n)."""
        # Сбалансированное дерево (в среднем) из случайных значений.
        import random

        random_values = random.sample(range(100), 20)
        balanced_tree = build_bst_from_iterable(random_values)

        # Вырожденное дерево (отсортированные значения).
        sorted_values = list(range(20))
        degenerate_tree = build_bst_from_iterable(sorted_values)

        h_bal = balanced_tree.height()
        h_deg = degenerate_tree.height()

        # Высота вырожденного дерева должна быть значительно больше.
        self.assertGreater(h_deg, h_bal)

    def test_is_valid_bst_false_for_invalid_structure(self) -> None:
        """Проверка, что is_valid_bst обнаруживает некорректную структуру.
        O(n)."""
        # Нарушим свойство BST вручную.
        bad_root = TreeNode(10)
        bad_root.left = TreeNode(20)  # 20 > 10 → нарушение
        bad_tree = BinarySearchTree()
        bad_tree.root = bad_root

        self.assertFalse(bad_tree.is_valid_bst())


if __name__ == "__main__":
    unittest.main()
