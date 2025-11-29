# recursion.py
"""Модуль с классическими рекурсивными алгоритмами."""


from typing import Union


def factorial(n: int) -> int:
    """Вычисляет факториал числа n рекурсивным методом.

    Args:
        n: Целое неотрицательное число.

    Returns:
        Факториал числа n.

    Raises:
        ValueError: Если n отрицательное.
    """
    if n < 0:  # O(1) - проверка условия
        raise ValueError('Факториал определен для неотрицательных чисел')
    if n == 0 or n == 1:  # O(1) - базовый случай
        return 1  # O(1) - возврат значения
    return n * factorial(n - 1)  # O(n) - рекурсивный вызов
    # Общая сложность: O(n), глубина рекурсии: O(n)


def fibonacci_naive(n: int) -> int:
    """Вычисляет n-е число Фибоначчи наивным рекурсивным методом.

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
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)
    # O(2^n) - два рекурсивных вызова
    # Общая сложность: O(2^n), глубина рекурсии: O(n)


def fast_power(a: Union[int, float], n: int) -> Union[int, float]:
    """Быстрое возведение числа a в степень n через степень двойки.

    Args:
        a: Основание степени.
        n: Показатель степени (целое неотрицательное число).

    Returns:
        Результат возведения a в степень n.

    Raises:
        ValueError: Если n отрицательное.
    """
    if n < 0:  # O(1)
        raise ValueError('Показатель степени должен быть неотрицательным')
    if n == 0:  # O(1) - базовый случай
        return 1  # O(1)
    if n == 1:  # O(1) - базовый случай
        return a  # O(1)

    half_power = fast_power(a, n // 2)
    # O(log n) - рекурсивный вызов для половины степени

    if n % 2 == 0:  # O(1) - четная степень
        return half_power * half_power  # O(1)
    else:  # O(1) - нечетная степень
        return a * half_power * half_power  # O(1)
    # Общая сложность: O(log n), глубина рекурсии: O(log n)


if __name__ == '__main__':
    # Демонстрация работы функций
    print('Факториал 5:', factorial(5))  # O(n)
    print('10-е число Фибоначчи:', fibonacci_naive(10))  # O(2^n)
    print('2^10 =', fast_power(2, 10))  # O(log n)
