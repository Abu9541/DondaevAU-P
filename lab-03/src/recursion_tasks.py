# recursion_tasks.py
"""Практические задачи с применением рекурсии."""


import os
from typing import List, Optional, Any


def binary_search_recursive(arr: List[Any], target: Any, low: int = 0,
                            high: Optional[int] = None) -> Optional[int]:
    """Рекурсивный бинарный поиск в отсортированном массиве.

    Args:
        arr: Отсортированный массив для поиска.
        target: Искомый элемент.
        low: Нижняя граница поиска.
        high: Верхняя граница поиска.

    Returns:
        Индекс элемента или None, если элемент не найден.
    """
    if high is None:  # O(1) - инициализация high
        high = len(arr) - 1  # O(1)

    if low > high:  # O(1) - базовый случай: элемент не найден
        return None  # O(1)

    mid = (low + high) // 2  # O(1) - вычисление середины

    if arr[mid] == target:  # O(1) - базовый случай: элемент найден
        return mid  # O(1)
    elif arr[mid] > target:  # O(1) - поиск в левой половине
        return binary_search_recursive(arr, target, low, mid - 1)  # O(log n)
    else:  # O(1) - поиск в правой половине
        return binary_search_recursive(arr, target, mid + 1, high)  # O(log n)
    # Общая сложность: O(log n), глубина рекурсии: O(log n)


def file_system_walk(path: str, level: int = 0,
                     max_depth: Optional[int] = None) -> None:
    """Рекурсивный обход файловой системы с выводом дерева каталогов.

    Args:
        path: Начальный путь для обхода.
        level: Текущий уровень вложенности.
        max_depth: Максимальная глубина рекурсии.
    """
    if max_depth is not None and level > max_depth:  # O(1) - проверка глубины
        return  # O(1)

    try:
        entries = os.listdir(path)
        # O(k) - чтение директории (k - количество элементов)
    except PermissionError:  # O(1) - обработка ошибки доступа
        print('  ' * level + f'[Доступ запрещен: {os.path.basename(path)}]')
        # O(1)
        return  # O(1)
    except FileNotFoundError:  # O(1) - обработка ошибки несуществующего пути
        print('  ' * level + f'[Путь не существует: {path}]')  # O(1)
        return  # O(1)

    for entry in entries:  # O(k) - цикл по элементам директории
        full_path = os.path.join(path, entry)
        # O(1) - формирование полного пути

        if os.path.isdir(full_path):  # O(1) - проверка является ли директорией
            print('  ' * level + f'📁 {entry}/')  # O(1) - вывод директории
            file_system_walk(full_path, level + 1, max_depth)
            # O(n) - рекурсивный вызов
        else:  # O(1) - файл
            print('  ' * level + f'📄 {entry}')  # O(1) - вывод файла
    # Общая сложность: O(n), где n - общее количество элементов в дереве


def hanoi_towers(n: int, source: str = 'A', auxiliary: str = 'B',
                 target: str = 'C') -> None:
    """Решает задачу 'Ханойские башни' для n дисков.

    Args:
        n: Количество дисков.
        source: Исходный стержень.
        auxiliary: Вспомогательный стержень.
        target: Целевой стержень.
    """
    if n == 1:  # O(1) - базовый случай: один диск
        print(f'Переместить диск 1 с {source} на {target}')  # O(1)
        return  # O(1)

    # Переместить n-1 дисков на вспомогательный стержень
    hanoi_towers(n - 1, source, target, auxiliary)  # O(2^n)

    # Переместить самый большой диск на целевой стержень
    print(f'Переместить диск {n} с {source} на {target}')  # O(1)

    # Переместить n-1 дисков с вспомогательного на целевой стержень
    hanoi_towers(n - 1, auxiliary, source, target)  # O(2^n)
    # Общая сложность: O(2^n), глубина рекурсии: O(n)


if __name__ == '__main__':
    # Демонстрация бинарного поиска
    sorted_array = [1, 3, 5, 7, 9, 11, 13, 15]  # O(1)
    target_value = 7  # O(1)
    result_idx = binary_search_recursive(sorted_array, target_value)
    # O(log n)
    print(f'''Бинарный поиск {target_value} в {sorted_array}:
          индекс {result_idx}''')  # O(1)

    # Демонстрация обхода файловой системы (ограниченная глубина)
    print('\nОбход файловой системы (максимум 2 уровня):')
    file_system_walk('.', max_depth=2)  # O(n)

    # Демонстрация Ханойских башен
    print('\nРешение Ханойских башен для 3 дисков:')
    hanoi_towers(3)  # O(2^n)
