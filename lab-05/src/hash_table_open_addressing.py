# hash_table_open_addressing.py
"""Реализация хеш-таблицы с открытой адресацией."""

from typing import Any, Optional, Tuple, List

from hash_functions import djb2_hash


class HashTableOpenAddressing:
    """Хеш-таблица с разрешением коллизий методом открытой адресации."""

    def __init__(self, capacity: int = 16, load_factor_threshold: float = 0.7):
        """Инициализация хеш-таблицы.

        Args:
            capacity: Начальная емкость таблицы.
            load_factor_threshold:
            Порог коэффициента заполнения для рехеширования.
        """
        self.capacity = capacity  # O(1)
        self.load_factor_threshold = load_factor_threshold  # O(1)
        self.size = 0  # O(1)
        self.table: List[Optional[Tuple[str, Any]]] = [None] * capacity  # O(n)
        self.DELETED = object()  # O(1) - маркер удаленного элемента

    def _hash(self, key: str) -> int:
        """Основная хеш-функция.

        Args:
            key: Ключ для хеширования.

        Returns:
            Начальный индекс для поиска.
        """
        return djb2_hash(key, self.capacity)  # O(n)

    def _probe_hash(self, key: str) -> int:
        """Вторая хеш-функция для двойного хеширования.

        Args:
            key: Ключ для хеширования.

        Returns:
            Шаг для пробирования.
        """
        step_size = max(1, self.capacity - 2)  # O(1) - избегаем деления на 0
        step = 1 + (djb2_hash(key, step_size))  # O(n)
        return step % (self.capacity - 1) + 1  # O(1) - шаг от 1 до capacity-1

    def _find_index(self, key: str, for_insert: bool = False) -> int:
        """Находит индекс для ключа с использованием двойного хеширования.

        Args:
            key: Ключ для поиска.
            for_insert: True если поиск для вставки.

        Returns:
            Индекс для вставки/поиска или -1 если не найден (для поиска).
        """
        index = self._hash(key)  # O(n)
        step = self._probe_hash(key)  # O(n)

        first_deleted = -1  # O(1) - запоминаем первый удаленный индекс

        for i in range(self.capacity):  # O(n) в худшем случае
            current_index = (index + i * step) % self.capacity  # O(1)
            item = self.table[current_index]  # O(1)

            if item is None:  # O(1)
                if for_insert and first_deleted != -1:  # O(1)
                    return first_deleted  # O(1)
                return current_index if for_insert else -1  # O(1)

            if item is self.DELETED:  # O(1)
                if first_deleted == -1:  # O(1)
                    first_deleted = current_index  # O(1)
                continue  # O(1)

            if item[0] == key:  # O(1)
                return current_index  # O(1)

        return -1  # O(1)
        # Общая сложность: O(1) в среднем, O(n) в худшем

    def _resize(self, new_capacity: int) -> None:
        """Изменяет размер таблицы и перехеширует все элементы.

        Args:
            new_capacity: Новая емкость таблицы.
        """
        old_table = self.table  # O(1)
        old_capacity = self.capacity  # O(1)

        self.capacity = new_capacity  # O(1)
        self.table = [None] * new_capacity  # O(n)
        self.size = 0  # O(1)

        for i in range(old_capacity):  # O(m)
            item = old_table[i]  # O(1)
            if item is not None and item is not self.DELETED:  # O(1)
                self.insert(item[0], item[1])  # O(n)
        # Общая сложность: O(m*n)

    def insert(self, key: str, value: Any) -> None:
        """Вставляет пару ключ-значение в таблицу.

        Args:
            key: Ключ для вставки.
            value: Значение для вставки.
        """
        # Проверяем нужно ли рехеширование ДО вставки (учитывая возможное увеличение размера)
        if (self.size + 1) / self.capacity > self.load_factor_threshold:  # O(1)
            self._resize(self.capacity * 2)  # O(n) амортизированно

        index = self._find_index(key, for_insert=True)  # O(1) в среднем
        if index == -1:  # O(1)
            # Если не нашли место для вставки, выполняем рехеширование и пробуем снова
            self._resize(self.capacity * 2)  # O(n)
            index = self._find_index(key, for_insert=True)  # O(1)
            if index == -1:  # O(1)
                raise MemoryError('Hash table is full even after resizing')  # O(1)

        if self.table[index] is None or self.table[index] is self.DELETED:  # O(1)
            self.size += 1  # O(1)

        self.table[index] = (key, value)  # O(1)

    def get(self, key: str) -> Optional[Any]:
        """Возвращает значение по ключу.

        Args:
            key: Ключ для поиска.

        Returns:
            Значение или None, если ключ не найден.
        """
        index = self._find_index(key)  # O(1) в среднем
        if index == -1:  # O(1)
            return None  # O(1) - ключ не найден

        return self.table[index][1]  # O(1) - возвращаем значение, даже если оно None

    def delete(self, key: str) -> bool:
        """Удаляет пару ключ-значение из таблицы.

        Args:
            key: Ключ для удаления.

        Returns:
            True если удаление успешно, иначе False.

        Сложность:
            Средний случай: O(1)
            Худший случай: O(n)
        """
        index = self._find_index(key)  # O(1) в среднем
        if index == -1:  # O(1)
            return False  # O(1)

        self.table[index] = self.DELETED  # O(1)
        self.size -= 1  # O(1)
        return True  # O(1)
        # Общая сложность: O(1) в среднем

    @property
    def load_factor(self) -> float:
        """Возвращает текущий коэффициент заполнения.

        Returns:
            Коэффициент заполнения таблицы.
        """
        return self.size / self.capacity  # O(1)

    def __contains__(self, key: str) -> bool:
        """Проверяет наличие ключа в таблице.

        Args:
            key: Ключ для проверки.

        Returns:
            True если ключ существует, иначе False.
        """
        return self._find_index(key) != -1  # O(1) в среднем

    def __str__(self) -> str:
        """Строковое представление таблицы."""
        result = []  # O(1)
        for i, item in enumerate(self.table):  # O(m)
            if item is None:  # O(1)
                result.append(f'{i}: None')  # O(1)
            elif item is self.DELETED:  # O(1)
                result.append(f'{i}: DELETED')  # O(1)
            else:  # O(1)
                result.append(f'{i}: {item}')  # O(1)
        return '\n'.join(result)  # O(m)


class HashTableLinearProbing(HashTableOpenAddressing):
    """Хеш-таблица с линейным пробированием."""

    def _find_index(self, key: str, for_insert: bool = False) -> int:
        """Находит индекс для ключа с использованием линейного пробирования.

        Args:
            key: Ключ для поиска.
            for_insert: True если поиск для вставки.

        Returns:
            Индекс для вставки/поиска или -1 если не найден (для поиска).
        """
        index = self._hash(key)  # O(n)
        first_deleted = -1  # O(1)

        for i in range(self.capacity):  # O(n)
            current_index = (index + i) % self.capacity  # O(1)
            item = self.table[current_index]  # O(1)

            if item is None:  # O(1)
                if for_insert and first_deleted != -1:  # O(1)
                    return first_deleted  # O(1)
                return current_index if for_insert else -1  # O(1)

            if item is self.DELETED:  # O(1)
                if first_deleted == -1:  # O(1)
                    first_deleted = current_index  # O(1)
                continue  # O(1)

            if item[0] == key:  # O(1)
                return current_index  # O(1)

        return -1  # O(1)


if __name__ == '__main__':
    # Демонстрация работы хеш-таблицы с открытой адресацией
    print('Двойное хеширование:')  # O(1)
    ht_double = HashTableOpenAddressing(capacity=5)  # O(n)

    test_data = [('apple', 1), ('banana', 2), ('cherry', 3),  # O(1)
                 ('date', 4), ('elderberry', 5)]  # O(1)

    for key, value in test_data:  # O(k)
        ht_double.insert(key, value)  # O(1) в среднем
        print(f'''Вставка ({key}, {value}),
              коэффициент: {ht_double.load_factor:.2f}''')  # O(1)

    print('\nСостояние таблицы:')  # O(1)
    print(ht_double)  # O(m)

    print('\nЛинейное пробирование:')  # O(1)
    ht_linear = HashTableLinearProbing(capacity=5)  # O(n)

    for key, value in test_data:  # O(k)
        ht_linear.insert(key, value)  # O(1) в среднем
        print(f'''Вставка ({key}, {value}),
              коэффициент: {ht_linear.load_factor:.2f}''')  # O(1)

    print('\nСостояние таблицы:')  # O(1)
    print(ht_linear)  # O(m)
