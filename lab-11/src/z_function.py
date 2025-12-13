# z_function.py


from __future__ import annotations

from typing import List


def z_function(s: str) -> List[int]:
    """Вычислить Z-функцию строки.

    Параметры
    ----------
    s : str
        Входная строка.

    Returns
    -------
    List[int]
        Массив z длины len(s), где z[0] = 0 (принятая конвенция),
        а z[i] — длина наибольшего общего префикса s и s[i:].

    Сложность
    ----------
    Пусть n = len(s).
    Время: O(n).
    Память: O(n).
    """
    n = len(s)
    z: List[int] = [0] * n
    l = 0
    r = 0

    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])

        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1

        if i + z[i] - 1 > r:
            l = i
            r = i + z[i] - 1

    return z
