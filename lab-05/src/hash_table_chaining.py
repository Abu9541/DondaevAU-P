# hash_table_chaining.py
"""Реализация хеш-таблицы с методом цепочек."""

from typing import Any, Optional, List, Tuple
from hash_functions import djb2_hash


class HashTableChaining:
    """Хеш-таблица с разрешением коллизий методом цепочек."""

    def __init__(self, capacity: int = 16,
                 load_factor_threshold: float = 0.75):
        """Инициализация хеш-таблицы.

        Args:
            capacity: Начальная емкость таблицы.
            load_factor_threshold:
            Порог коэффициента заполнения для рехеширования.
        """
        self.capacity = capacity  # O(1)
        self.load_factor_threshold = load_factor_threshold  # O(1)
        self.size = 0  # O(1) - количество элементов
        self.table: List[List[Tuple[str, Any]]] = [[] for _ in range(capacity)]
        # O(n)

    def _hash(self, key: str) -> int:
        """Вычисляет хеш ключа.

        Args:
            key: Ключ для хеширования.

        Returns:
            Индекс в таблице.
        """
        return djb2_hash(key, self.capacity)  # O(n)

    def _resize(self, new_capacity: int) -> None:
        """Изменяет размер таблицы и перехеширует все элементы.

        Args:
            new_capacity: Новая емкость таблицы.
        """
        # Гарантируем минимальную емкость и используем простое число для лучшего распределения
        new_capacity = max(new_capacity, 8)  # O(1)

        old_table = self.table  # O(1)
        old_size = self.size  # O(1)

        self.capacity = new_capacity  # O(1)
        self.table = [[] for _ in range(new_capacity)]  # O(n)
        self.size = 0  # O(1)

        # Перехешируем все элементы
        for bucket in old_table:  # O(m)
            for key, value in bucket:  # O(k)
                # Используем прямой вызов insert для правильного подсчета размера
                self.insert(key, value)  # O(1) в среднем

        # Проверяем что все элементы перенесены
        assert self.size == old_size, f"Resize error: {self.size} != {old_size}"  # O(1)

    def insert(self, key: str, value: Any) -> None:
        """Вставляет пару ключ-значение в таблицу.

        Args:
            key: Ключ для вставки.
            value: Значение для вставки.
        """
        # Проверяем нужно ли рехеширование ДО вставки
        if (self.size + 1) / self.capacity > self.load_factor_threshold:  # O(1)
            self._resize(self.capacity * 2)  # O(n) амортизированно

        index = self._hash(key)  # O(n)
        bucket = self.table[index]  # O(1)

        # Проверяем, есть ли уже ключ в цепочке
        for i, (k, v) in enumerate(bucket):  # O(k)
            if k == key:  # O(1)
                bucket[i] = (key, value)  # O(1) - обновление значения
                return  # O(1)

        # Ключ не найден, добавляем новый
        bucket.append((key, value))  # O(1)
        self.size += 1  # O(1)

    def get(self, key: str) -> Optional[Any]:
        """Возвращает значение по ключу.

        Args:
            key: Ключ для поиска.

        Returns:
            Значение или None, если ключ не найден.
        """
        index = self._hash(key)  # O(n)
        bucket = self.table[index]  # O(1)

        for k, v in bucket:  # O(k)
            if k == key:  # O(1)
                return v  # O(1) - возвращаем значение, даже если оно None

        return None  # O(1) - ключ не найден

    def delete(self, key: str) -> bool:
        """Удаляет пару ключ-значение из таблицы.

        Args:
            key: Ключ для удаления.

        Returns:
            True если удаление успешно, иначе False.

        Сложность:
            Средний случай: O(1)
            Худший случай: O(n) - все элементы в одной ячейке
        """
        index = self._hash(key)  # O(n)
        bucket = self.table[index]  # O(1)

        for i, (k, v) in enumerate(bucket):  # O(k)
            if k == key:  # O(1)
                del bucket[i]  # O(k) - удаление из списка
                self.size -= 1  # O(1)
                return True  # O(1)

        return False  # O(1)
        # Общая сложность: O(1) в среднем, O(n) в худшем

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
        index = self._hash(key)  # O(n)
        bucket = self.table[index]  # O(1)

        # Проверяем наличие ключа в цепочке, независимо от значения
        for k, v in bucket:  # O(k)
            if k == key:  # O(1)
                return True  # O(1)

        return False  # O(1)

    def __str__(self) -> str:
        """Строковое представление таблицы."""
        result = []  # O(1)
        for i, bucket in enumerate(self.table):  # O(m)
            if bucket:  # O(1)
                result.append(f'{i}: {bucket}')  # O(1)
        return '\n'.join(result)  # O(m)


if __name__ == '__main__':
    # Демонстрация работы хеш-таблицы с цепочками
    ht = HashTableChaining(capacity=5)  # O(n)

    print('Вставка элементов:')  # O(1)
    test_data = [('apple', 1), ('banana', 2), ('cherry', 3),  # O(1)
                 ('date', 4), ('elderberry', 5), ('fig', 6)]  # O(1)

    for key, value in test_data:  # O(k)
        ht.insert(key, value)  # O(1) в среднем
        print(f'''Вставка ({key}, {value}),
              коэффициент заполнения: {ht.load_factor:.2f}''')  # O(1)

    print('\nТекущее состояние таблицы:')  # O(1)
    print(ht)  # O(m)

    print('\nПоиск элементов:')  # O(1)
    for key in ['apple', 'banana', 'grape']:  # O(k)
        value = ht.get(key)  # O(1) в среднем
        print(f'Ключ "{key}": {value}')  # O(1)

    print('\nУдаление элементов:')  # O(1)
    print(f'Удаление "banana": {ht.delete("banana")}')  # O(1) в среднем
    print(f'Удаление "grape": {ht.delete("grape")}')  # O(1) в среднем

    print('\nСостояние после удаления:')  # O(1)
    print(ht)  # O(m)
