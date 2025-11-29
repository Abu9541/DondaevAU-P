# memoization.py
"""Модуль с оптимизированными рекурсивными алгоритмами с мемоизацией."""


import time
from functools import wraps
from typing import Dict, Any, Callable


def memoize(func: Callable) -> Callable:
    """Декоратор для мемоизации функций.

    Args:
        func: Функция для мемоизации.

    Returns:
        Обернутая функция с мемоизацией.
    """
    cache: Dict[Any, Any] = {}  # O(1) - инициализация кэша

    @wraps(func)
    def wrapper(*args: Any) -> Any:
        if args in cache:  # O(1) - проверка наличия в кэше
            return cache[args]  # O(1) - возврат из кэша
        result = func(*args)  # O(?) - вызов оригинальной функции
        cache[args] = result  # O(1) - сохранение в кэш
        return result  # O(1) - возврат результата

    return wrapper
    # Общая сложность декоратора: O(1) для кэшированных вызовов


@memoize
def fibonacci_memoized(n: int) -> int:
    """Вычисляет n-е число Фибоначчи с мемоизацией.

    Args:
        n: Порядковый номер числа Фибоначчи (n >= 0).

    Returns:
        n-е число Фибоначчи.

    Raises:
        ValueError: Если n отрицательное.
    """
    if n < 0:  # O(1)
        raise ValueError('Номер числа Фибоначчи должен быть неотрицательным')
    if n == 0:  # O(1) - базовый случай 1
        return 0  # O(1)
    if n == 1:  # O(1) - базовый случай 2
        return 1  # O(1)
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)
    # O(n) - рекурсивные вызовы
    # Общая сложность с мемоизацией: O(n), глубина рекурсии: O(n)


def compare_fibonacci_performance() -> None:
    """Сравнивает производительность наивной и мемоизированной версий."""
    test_n = 35

    print(f'Сравнение производительности для n={test_n}:')

    # Наивная версия
    start_time = time.time()  # O(1)
    result_naive = fibonacci_naive(test_n)  # O(2^n)
    time_naive = time.time() - start_time  # O(1)

    # Мемоизированная версия
    start_time = time.time()  # O(1)
    result_memoized = fibonacci_memoized(test_n)  # O(n)
    time_memoized = time.time() - start_time  # O(1)

    print(f'Наивная версия: {result_naive}, время: {time_naive:.6f} сек')
    # O(1)
    print(f'''Мемоизированная версия: {result_memoized},
          Время: {time_memoized:.6f} сек''')  # O(1)
    print(f'Ускорение: {time_naive / time_memoized:.2f} раз')  # O(1)


if __name__ == '__main__':
    # Импорт наивной версии для сравнения
    from recursion import fibonacci_naive

    compare_fibonacci_performance()  # O(2^n) vs O(n)
