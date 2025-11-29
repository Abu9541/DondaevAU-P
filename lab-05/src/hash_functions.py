# hash_functions.py
"""Модуль с реализацией различных хеш-функций для строковых ключей."""

from typing import Callable


def simple_hash(key: str, table_size: int) -> int:
    """Простая хеш-функция - сумма кодов символов.

    Args:
        key: Строковый ключ для хеширования.
        table_size: Размер хеш-таблицы.

    Returns:
        Хеш-код в диапазоне [0, table_size-1].

    Особенности:
        - Быстрая вычисление
        - Плохое распределение для анаграмм и строк
        с одинаковым набором символов
        - Высокая вероятность коллизий
    """
    hash_value = 0  # O(1) - инициализация
    for char in key:  # O(n) - проход по всем символам строки
        hash_value += ord(char)  # O(1) - получение кода символа и сложение
    return hash_value % table_size  # O(1) - приведение к диапазону таблицы
    # Общая сложность: O(n), где n - длина строки


def polynomial_hash(key: str, table_size: int, base: int = 31) -> int:
    """Полиномиальная хеш-функция с rolling hash.

    Args:
        key: Строковый ключ для хеширования.
        table_size: Размер хеш-таблицы.
        base: Основание полинома (простое число).

    Returns:
        Хеш-код в диапазоне [0, table_size-1].

    Особенности:
        - Хорошее распределение для строк с общими префиксами/суффиксами
        - Учитывает порядок символов
        - Меньше коллизий по сравнению с простой суммой
    """
    hash_value = 0  # O(1)
    for char in key:  # O(n)
        hash_value = (hash_value * base + ord(char)) % table_size  # O(1)
    return hash_value  # O(1)
    # Общая сложность: O(n)


def djb2_hash(key: str, table_size: int) -> int:
    """Хеш-функция DJB2 - популярная и эффективная хеш-функция.

    Args:
        key: Строковый ключ для хеширования.
        table_size: Размер хеш-таблицы.

    Returns:
        Хеш-код в диапазоне [0, table_size-1].
    """
    hash_value = 5381  # O(1) - магическое число (prime number)
    for char in key:  # O(n)
        # hash_value * 33 + ord(char) - классическая формула DJB2
        hash_value = ((hash_value << 5) + hash_value) + ord(char)  # O(1)
    # Гарантируем, что table_size >= 1
    if table_size <= 0:  # O(1)
        table_size = 1  # O(1)
    return abs(hash_value) % table_size  # O(1)
    # Общая сложность: O(n)


def test_hash_function(hash_func: Callable[[str, int], int],
                       test_keys: list[str],
                       table_size: int) -> dict:
    """Тестирует качество хеш-функции.

    Args:
        hash_func: Функция для тестирования.
        test_keys: Список тестовых ключей.
        table_size: Размер таблицы для тестирования.

    Returns:
        Статистика распределения хешей.
    """
    distribution = {}  # O(1) - словарь для распределения
    collisions = 0  # O(1) - счетчик коллизий

    for key in test_keys:  # O(k)
        hash_val = hash_func(key, table_size)  # O(n)
        if hash_val in distribution:  # O(1)
            distribution[hash_val] += 1  # O(1)
            collisions += 1  # O(1)
        else:  # O(1)
            distribution[hash_val] = 1  # O(1)

    return {  # O(1)
        'total_keys': len(test_keys),  # O(1)
        'unique_hashes': len(distribution),  # O(1)
        'collisions': collisions,  # O(1)
        'load_factor': len(test_keys) / table_size,  # O(1)
        'distribution': distribution  # O(1)
    }


if __name__ == '__main__':
    # Демонстрация работы хеш-функций
    test_keys = ['hello', 'world', 'test', 'hash', 'function', 'collision']
    # O(1)
    table_size = 10  # O(1)

    hash_functions = [  # O(1)
        ('Simple Hash', simple_hash),  # O(1)
        ('Polynomial Hash', polynomial_hash),  # O(1)
        ('DJB2 Hash', djb2_hash)  # O(1)
    ]

    print('Тестирование хеш-функций:')  # O(1)
    for name, func in hash_functions:  # O(m)
        print(f'\n{name}:')  # O(1)
        for key in test_keys:  # O(k)
            hash_val = func(key, table_size)  # O(n)
            print(f'  "{key}" -> {hash_val}')  # O(1)

    # Тестирование качества распределения
    print('\nКачество распределения (1000 случайных ключей):')  # O(1)
    import random  # O(1)
    import string  # O(1)

    # Генерация случайных ключей
    random_keys = [''.join(random.choices(string.ascii_letters, k=5))
                   # O(1000*5)
                   for _ in range(1000)]  # O(1000)

    for name, func in hash_functions:  # O(m)
        stats = test_hash_function(func, random_keys, 100)  # O(1000*n)
        print(f'\n{name}:')  # O(1)
        print(f'  Уникальных хешей: {stats["unique_hashes"]}/100')  # O(1)
        print(f'  Коллизий: {stats["collisions"]}')  # O(1)
        print(f'  Коэффициент заполнения: {stats["load_factor"]:.2f}')  # O(1)
