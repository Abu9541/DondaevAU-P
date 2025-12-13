# kmp_search.py


from __future__ import annotations

from typing import List

from prefix_function import prefix_function


def kmp_search(text: str, pattern: str) -> List[int]:
    """Найти все вхождения pattern в text с помощью KMP.

    Параметры
    ----------
    text : str
        Текст, в котором ищем.
    pattern : str
        Искомая подстрока.

    Returns
    -------
    List[int]
        Список позиций начала всех вхождений pattern в text.

    Сложность
    ----------
    Время: O(n + m).
    Память: O(m).
    """
    n = len(text)
    m = len(pattern)

    if m == 0:
        return list(range(n + 1))

    pi = prefix_function(pattern)
    result: List[int] = []
    j = 0

    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]

        if text[i] == pattern[j]:
            j += 1

        if j == m:
            result.append(i - m + 1)
            j = pi[j - 1]

    return result
