# binary_search_tree.py


from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class TreeNode:
    """Узел бинарного дерева поиска.

    Атрибуты:
        value: Значение, хранящееся в узле.
        left: Ссылка на левое поддерево.
        right: Ссылка на правое поддерево.
    """

    value: int  # O(1)
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


class BinarySearchTree:
    """Класс бинарного дерева поиска (BST)."""

    def __init__(self) -> None:
        """Создает пустое дерево.

        Время: O(1)
        Память: O(1)
        """
        self.root: Optional[TreeNode] = None  # O(1)

    def insert(self, value: int) -> None:
        """Вставка значения в дерево (итеративная реализация).

        Средняя сложность: O(log n).
        Худшая (вырожденное дерево): O(n).
        """
        # Если дерево пустое — создаем корень. O(1)
        if self.root is None:
            self.root = TreeNode(value)  # O(1)
            return  # O(1)

        current = self.root  # O(1)
        while True:  # O(h)
            if value < current.value:  # O(1)
                if current.left is None:  # O(1)
                    current.left = TreeNode(value)  # O(1)
                    return  # O(1)
                current = current.left  # O(1)
            elif value > current.value:  # O(1)
                if current.right is None:  # O(1)
                    current.right = TreeNode(value)  # O(1)
                    return  # O(1)
                current = current.right  # O(1)
            else:
                # Дубликаты не вставляем. O(1)
                return  # O(1)

    def search(self, value: int) -> Optional[TreeNode]:
        """Поиск узла со значением value (итеративная реализация).

        Средняя сложность: O(log n).
        Худшая: O(n).
        """
        current = self.root  # O(1)
        while current is not None:  # O(h)
            if value == current.value:  # O(1)
                return current  # O(1)
            if value < current.value:  # O(1)
                current = current.left  # O(1)
            else:
                current = current.right  # O(1)
        return None  # O(1)

    def delete(self, value: int) -> None:
        """Итеративное удаление узла со значением value.

        Сложность: O(h), где h — высота дерева (O(log n) в среднем,
        O(n) в худшем).
        """
        parent: Optional[TreeNode] = None  # Родитель текущего узла. O(1)
        current: Optional[TreeNode] = self.root  # Текущий узел. O(1)

        while current is not None and current.value != value:  # O(h)
            parent = current  # O(1)
            if value < current.value:  # O(1)
                current = current.left  # O(1)
            else:
                current = current.right  # O(1)

        if current is None:
            return  # O(1)

        def replace_child(
            parent_node: Optional[TreeNode],
            old_child: Optional[TreeNode],
            new_child: Optional[TreeNode],
        ) -> None:
            if parent_node is None:
                self.root = new_child  # O(1)
            elif parent_node.left is old_child:
                parent_node.left = new_child  # O(1)
            else:
                parent_node.right = new_child  # O(1)

        if current.left is None and current.right is None:
            replace_child(parent, current, None)  # O(1)
            return  # O(1)

        if current.left is None or current.right is None:
            child = current.left if current.left is not None else current.right
            # O(1)
            replace_child(parent, current, child)  # O(1)
            return  # O(1)

        succ_parent = current  # O(1)
        succ = current.right  # O(1)
        while succ.left is not None:  # O(h)
            succ_parent = succ  # O(1)
            succ = succ.left  # O(1)

        current.value = succ.value  # O(1)

        succ_child = succ.right  # O(1)

        if succ_parent.left is succ:
            succ_parent.left = succ_child  # O(1)
        else:
            succ_parent.right = succ_child  # O(1)

    def find_min(self, node: Optional[TreeNode]) -> Optional[TreeNode]:
        """Поиск минимального значения в поддереве.

        Сложность: O(h).
        """
        current = node  # O(1)
        while current is not None and current.left is not None:  # O(h)
            current = current.left  # O(1)
        return current  # O(1)

    def find_max(self, node: Optional[TreeNode]) -> Optional[TreeNode]:
        """Поиск максимального значения в поддереве.

        Сложность: O(h).
        """
        current = node  # O(1)
        while current is not None and current.right is not None:  # O(h)
            current = current.right  # O(1)
        return current  # O(1)

    def height(self, node: Optional[TreeNode] = None) -> int:
        """Вычисление высоты дерева (итеративно).

        Высота пустого дерева = 0.
        Сложность: O(n) по времени, O(h) по памяти.
        """
        # Если явно передан узел — считаем высоту поддерева с этим корнем.
        root = node if node is not None else self.root  # O(1)
        if root is None:  # O(1)
            return 0  # O(1)

        max_height = 0  # O(1)
        stack: list[tuple[TreeNode, int]] = [(root, 1)]  # O(1)

        while stack:  # O(n)
            current, h = stack.pop()  # O(1)
            if h > max_height:  # O(1)
                max_height = h  # O(1)
            if current.left is not None:  # O(1)
                stack.append((current.left, h + 1))  # O(1)
            if current.right is not None:  # O(1)
                stack.append((current.right, h + 1))  # O(1)

        return max_height  # O(1)

    def is_valid_bst(self) -> bool:
        """Проверка, что дерево удовлетворяет свойству BST.

        Сложность: O(n), каждый узел посещается один раз.
        """

        def _validate(
            node: Optional[TreeNode],
            min_value: Optional[int],
            max_value: Optional[int],
        ) -> bool:
            if node is None:  # O(1)
                return True  # O(1)

            # Проверяем границы:
            # левый потомок строго меньше, правый строго больше. O(1)
            if (min_value is not None and node.value <= min_value) or (
                max_value is not None and node.value >= max_value
            ):
                return False  # O(1)

            # Рекурсивно проверяем левое и правое поддеревья. O(n)
            left_ok = _validate(node.left, min_value, node.value)  # O(n_left)
            right_ok = _validate(node.right, node.value, max_value)
            # O(n_right)
            return left_ok and right_ok  # O(1)

        return _validate(self.root, None, None)  # O(n)

    def visualize(self) -> None:
        """Печатает дерево в виде "ёлочки" в консоль.

        Использует отступы и псевдографику для отображения структуры.

        Сложность: O(n), каждый узел выводится один раз.
        """

        def _visualize(
            node: Optional[TreeNode],
            prefix: str,
            is_left: bool,
        ) -> None:
            if node is None:  # O(1)
                return  # O(1)

            # Определяем символ ветки. O(1)
            branch = "├── " if is_left else "└── "  # O(1)
            print(prefix + branch + str(node.value))  # O(1)

            # Префикс для потомков. O(1)
            child_prefix = prefix + ("│   " if is_left else "    ")  # O(1)

            # Рекурсивно выводим левое и правое поддерево. O(n)
            if node.left is not None or node.right is not None:  # O(1)
                _visualize(node.left, child_prefix, True)  # O(n_left)
                _visualize(node.right, child_prefix, False)  # O(n_right)

        if self.root is None:  # O(1)
            print("<пустое дерево>")  # O(1)
            return  # O(1)

        _visualize(self.root, "", True)  # O(n)


def build_bst_from_iterable(values: list[int]) -> BinarySearchTree:
    """Вспомогательная функция для построения BST из списка значений.

    Каждый элемент поочередно вставляется в дерево.

    Средняя сложность: O(n log n).
    Худшая (вырожденный случай): O(n²).
    """
    tree = BinarySearchTree()  # O(1)
    for value in values:  # O(n)
        tree.insert(value)  # O(h)
    return tree  # O(1)
