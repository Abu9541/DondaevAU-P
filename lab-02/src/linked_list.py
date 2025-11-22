# linked_list.py
"""
Модуль для реализации связного списка.
"""


from typing import Any, Optional, List


class Node:
    """Узел связного списка."""

    def __init__(self, data: Any) -> None:
        """
        Инициализация узла.

        Args:
            data: Данные для хранения в узле
        """
        self.data: Any = data  # O(1) - присваивание
        self.next: Optional['Node'] = None  # O(1) - присваивание


class LinkedList:
    """Односвязный список."""

    def __init__(self) -> None:
        """Инициализация пустого связного списка."""
        self.head: Optional[Node] = None  # O(1) - инициализация
        self.tail: Optional[Node] = None  # O(1) - инициализация
        self.length: int = 0  # O(1) - инициализация

    def insert_at_start(self, data: Any) -> None:
        """
        Вставка элемента в начало списка.

        Args:
            data: Данные для вставки
        """
        new_node = Node(data)  # O(1) - создание узла
        new_node.next = self.head  # O(1) - присваивание
        self.head = new_node  # O(1) - присваивание

        if self.tail is None:  # O(1) - проверка условия
            self.tail = new_node  # O(1) - присваивание

        self.length += 1  # O(1) - инкремент
        # Общая сложность: O(1)

    def insert_at_end(self, data: Any) -> None:
        """
        Вставка элемента в конец списка.

        Args:
            data: Данные для вставки
        """
        new_node = Node(data)  # O(1) - создание узла

        if self.head is None:  # O(1) - проверка условия
            self.head = new_node  # O(1) - присваивание
            self.tail = new_node  # O(1) - присваивание
        else:
            if self.tail is not None:  # O(1) - проверка для mypy
                self.tail.next = new_node  # O(1) - присваивание
            self.tail = new_node  # O(1) - присваивание

        self.length += 1  # O(1) - инкремент
        # Общая сложность: O(1)

    def delete_from_start(self) -> Optional[Any]:
        """
        Удаление элемента из начала списка.

        Returns:
            Удаленные данные или None, если список пуст
        """
        if self.head is None:  # O(1) - проверка условия
            return None  # O(1) - возврат значения

        data = self.head.data  # O(1) - доступ к данным
        self.head = self.head.next  # O(1) - присваивание

        if self.head is None:  # O(1) - проверка условия
            self.tail = None  # O(1) - присваивание

        self.length -= 1  # O(1) - декремент
        return data  # O(1) - возврат значения
        # Общая сложность: O(1)

    def traversal(self) -> List[Any]:
        """
        Обход всех элементов списка.

        Returns:
            Список всех элементов
        """
        elements = []  # O(1) - создание списка
        current = self.head  # O(1) - присваивание
        while current is not None:  # O(n) - цикл по всем элементам
            elements.append(current.data)  # O(1) - добавление в список
            current = current.next  # O(1) - присваивание

        return elements  # O(1) - возврат значения
        # Общая сложность: O(n)

    def is_empty(self) -> bool:
        """
        Проверка, пуст ли список.

        Returns:
            True если список пуст, иначе False
        """
        return self.head is None  # O(1) - проверка условия
        # Общая сложность: O(1)
