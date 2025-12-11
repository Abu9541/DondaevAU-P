# tree_traversal.py


from __future__ import annotations

from typing import List, Optional

from binary_search_tree import TreeNode


def inorder_print(node: Optional[TreeNode]) -> None:
    """Рекурсивный in-order обход (лево-корень-право) с печатью.

    Сложность: O(n).
    """
    if node is None:  # O(1)
        return  # O(1)

    inorder_print(node.left)  # O(n_left)
    print(node.value, end=" ")  # O(1)
    inorder_print(node.right)  # O(n_right)


def preorder_print(node: Optional[TreeNode]) -> None:
    """Рекурсивный pre-order обход (корень-лево-право) с печатью.

    Сложность: O(n).
    """
    if node is None:  # O(1)
        return  # O(1)

    print(node.value, end=" ")  # O(1)
    preorder_print(node.left)  # O(n_left)
    preorder_print(node.right)  # O(n_right)


def postorder_print(node: Optional[TreeNode]) -> None:
    """Рекурсивный post-order обход (лево-право-корень) с печатью.

    Сложность: O(n).
    """
    if node is None:  # O(1)
        return  # O(1)

    postorder_print(node.left)  # O(n_left)
    postorder_print(node.right)  # O(n_right)
    print(node.value, end=" ")  # O(1)


def inorder_list(node: Optional[TreeNode]) -> List[int]:
    """Рекурсивный in-order обход, возвращающий список значений.

    Сложность: O(n).
    """
    if node is None:  # O(1)
        return []  # O(1)

    # Формируем результат из левого поддерева,
    # текущего узла и правого поддерева. O(n)
    left = inorder_list(node.left)  # O(n_left)
    right = inorder_list(node.right)  # O(n_right)
    return left + [node.value] + right  # O(n)


def preorder_list(node: Optional[TreeNode]) -> List[int]:
    """Рекурсивный pre-order обход, возвращающий список значений. O(n)."""
    if node is None:  # O(1)
        return []  # O(1)
    return [node.value] + preorder_list(node.left) + preorder_list(node.right)
    # O(n)


def postorder_list(node: Optional[TreeNode]) -> List[int]:
    """Рекурсивный post-order обход, возвращающий список значений. O(n)."""
    if node is None:  # O(1)
        return []  # O(1)
    return (postorder_list(node.left)
            + postorder_list(node.right)
            + [node.value])
    # O(n)


def inorder_iterative(node: Optional[TreeNode]) -> List[int]:
    """Итеративный in-order обход с использованием стека.

    Возвращает список значений в порядке возрастания.

    Сложность: O(n) по времени, O(h) по памяти, где h — высота дерева.
    """
    result: List[int] = []  # O(1)
    stack: List[TreeNode] = []  # O(1)
    current = node  # O(1)

    # Пока есть узлы для обработки. O(n)
    while stack or current is not None:  # O(n)
        # Спускаемся как можно левее. O(h за каждую цепочку)
        while current is not None:  # O(h)
            stack.append(current)  # O(1)
            current = current.left  # O(1)

        # Берём следующий узел из стека. O(1)
        current = stack.pop()  # O(1)
        result.append(current.value)  # O(1)
        # Переходим в правое поддерево. O(1)
        current = current.right  # O(1)

    return result  # O(1)
