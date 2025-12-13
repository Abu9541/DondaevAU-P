# string_matching.py


from __future__ import annotations

from dataclasses import dataclass
from typing import List, Literal, Sequence

from kmp_search import kmp_search
from prefix_function import prefix_function
from z_function import z_function

SearchMethod = Literal["naive", "kmp", "z", "rk"]


# 1) Поиск всех вхождений (базовые реализации)

def naive_search(text: str, pattern: str) -> List[int]:
    """Наивный поиск всех вхождений pattern в text."""
    n = len(text)
    m = len(pattern)

    if m == 0:
        return list(range(n + 1))

    res: List[int] = []
    for i in range(n - m + 1):
        if text[i: i + m] == pattern:
            res.append(i)
    return res


def z_search(text: str, pattern: str, sep: str = "#") -> List[int]:
    """Поиск всех вхождений pattern в text через Z-функцию.

    Идея: строим строку pattern + sep + text, считаем Z-функцию.
    Если z[i] >= len(pattern) — найдено вхождение.

    sep должен не встречаться в pattern и text.
    """
    if pattern == "":
        return list(range(len(text) + 1))

    if sep in pattern or sep in text:
        sep = "\x00"
        if sep in pattern or sep in text:
            raise ValueError("Не удалось подобрать разделитель для Z-поиска.")

    combined = pattern + sep + text
    z = z_function(combined)

    m = len(pattern)
    res: List[int] = []
    for i in range(m + 1, len(combined)):
        if z[i] >= m:
            res.append(i - (m + 1))
    return res


# 2) Рабин–Карп

@dataclass(frozen=True)
class RKParams:
    """Параметры rolling-hash для Рабина–Карпа."""
    base: int = 911382323
    mod: int = 1_000_000_007


def _rk_hash_init(s: str, params: RKParams) -> int:
    h = 0
    for ch in s:
        h = (h * params.base + ord(ch)) % params.mod
    return h


def _rk_prepare_power(length: int, params: RKParams) -> int:
    power = 1
    for _ in range(length):
        power = (power * params.base) % params.mod
    return power


def rabin_karp_search(text: str,
                      pattern: str,
                      params: RKParams | None = None) -> List[int]:
    """Поиск всех вхождений pattern в text методом Рабина–Карпа.

    При совпадении хеша выполняется проверка подстроки для исключения коллизий.
    """
    if params is None:
        params = RKParams()

    n = len(text)
    m = len(pattern)

    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []

    pat_hash = _rk_hash_init(pattern, params)
    window_hash = _rk_hash_init(text[:m], params)

    power = _rk_prepare_power(m - 1, params)

    res: List[int] = []
    if window_hash == pat_hash and text[:m] == pattern:
        res.append(0)

    for i in range(1, n - m + 1):
        left = ord(text[i - 1])
        right = ord(text[i + m - 1])

        window_hash = (window_hash - left * power) % params.mod
        window_hash = (window_hash * params.base + right) % params.mod

        if window_hash == pat_hash and text[i: i + m] == pattern:
            res.append(i)

    return res


# 3) Единый интерфейс: поиск всех вхождений

def find_all_occurrences(text: str,
                         pattern: str,
                         method: SearchMethod = "kmp") -> List[int]:
    """Найти все вхождения pattern в text выбранным методом.

    Параметры
    ----------
    text : str
        Текст.
    pattern : str
        Шаблон (паттерн).
    method : {"naive", "kmp", "z", "rk"}
        Метод поиска.

    Returns
    -------
    List[int]
        Список позиций начала всех вхождений.

    Сложность
    ----------
    Зависит от method.
    """
    if method == "naive":
        return naive_search(text, pattern)
    if method == "kmp":
        return kmp_search(text, pattern)
    if method == "z":
        return z_search(text, pattern)
    if method == "rk":
        return rabin_karp_search(text, pattern)
    raise ValueError("method must be one of: 'naive', 'kmp', 'z', 'rk'")


# 4) Практическая задача: циклический сдвиг

def is_cyclic_shift(a: str, b: str, method: SearchMethod = "kmp") -> bool:
    """Проверить, является ли b циклическим сдвигом a.

    Условие:
    b — циклический сдвиг a <=>
    len(a) == len(b) и b является подстрокой (a + a).

    Parameters
    ----------
    a : str
        Исходная строка.
    b : str
        Проверяемая строка.
    method : {"naive", "kmp", "z", "rk"}
        Алгоритм поиска подстроки в (a + a).

    Returns
    -------
    bool
        True, если b — циклический сдвиг a.

    Complexity
    ----------
    Пусть n = len(a). Тогда поиск в строке длины 2n:
    - kmp / z: O(n)
    - naive: O(n^2) в худшем
    - rk: ожидаемо O(n)
    """
    if len(a) != len(b):
        return False
    if a == b:
        return True
    if len(a) == 0:
        return True  # обе пустые

    doubled = a + a
    return len(find_all_occurrences(doubled, b, method=method)) > 0


# 5) Практическая задача: минимальный период

def minimal_period_prefix(s: str) -> int:
    """Длина минимального периода строки через π-функцию."""
    n = len(s)
    if n == 0:
        return 0

    pi = prefix_function(s)
    p = n - pi[-1]
    if p != 0 and n % p == 0:
        return p
    return n


def minimal_period_z(s: str) -> int:
    """Длина минимального периода строки через Z-функцию."""
    n = len(s)
    if n == 0:
        return 0

    z = z_function(s)
    for p in range(1, n + 1):
        if n % p == 0:
            if p < n and z[p] >= n - p:
                return p
            if p == n:
                return n
    return n


def count_occurrences(positions: Sequence[int]) -> int:
    """Число вхождений по списку позиций."""
    return len(positions)
