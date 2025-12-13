# prefix_function.py


from __future__ import annotations

from typing import List


def prefix_function(s: str) -> List[int]:
    """Вычислить префикс-функцию строки.

    Параметры
    ----------
    s : str
        Входная строка.

    Returns
    -------
    List[int]
        Массив π длины len(s), где π[i] — длина наибольшего собственного
        префикса s, совпадающего с суффиксом подстроки s[:i+1].

    Сложность
    ----------
    Пусть n = len(s).
    Время: O(n).
    Память: O(n).
    """
    n = len(s)
    pi: List[int] = [0] * n
    j = 0

    for i in range(1, n):
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]

        if s[i] == s[j]:
            j += 1

        pi[i] = j

    return pi
