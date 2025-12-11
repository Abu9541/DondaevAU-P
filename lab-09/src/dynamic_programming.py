# dynamic_programming.py


from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


sys.setrecursionlimit(20000)


@dataclass(frozen=True)
class KnapsackItem:
    """
    Описание предмета для задачи о рюкзаке.

    Атрибуты
    ----------
    weight : int
        Вес предмета (положительное целое).
    value : int
        Стоимость предмета (целое число, обычно неотрицательное).
    name : str | None
        Необязательное текстовое имя предмета.
    """
    weight: int
    value: int
    name: Optional[str] = None


# Визуализация таблиц ДП


def print_dp_table_2d(
    dp: Sequence[Sequence[int]],
    row_labels: Optional[Sequence[str]] = None,
    col_labels: Optional[Sequence[str]] = None,
) -> None:
    """
    Напечатать двумерную таблицу ДП в удобном текстовом виде.

    Параметры
    ----------
    dp : Sequence[Sequence[int]]
        Таблица значений ДП.
    row_labels : Sequence[str] | None
        Необязательные подписи строк.
    col_labels : Sequence[str] | None
        Необязательные подписи столбцов.

    Сложность
    ----------
    Пусть n = число строк, m = число столбцов.
    Время: O(n * m).
    Память: O(1) дополнительная.
    """
    rows = len(dp)
    cols = len(dp[0]) if rows > 0 else 0

    # Заголовок таблицы
    if col_labels is not None:
        header = "      "
        for label in col_labels:
            header += f"{label:>5}"
        print(header)

    for i in range(rows):
        row_str = ""
        if row_labels is not None and i < len(row_labels):
            row_str += f"{row_labels[i]:>4} "
        else:
            row_str += f"{i:>4} "

        for j in range(cols):
            row_str += f"{dp[i][j]:>5}"
        print(row_str)


def print_dp_table_1d(
    dp: Sequence[int],
    index_labels: Optional[Sequence[str]] = None,
) -> None:
    """
    Напечатать одномерную таблицу ДП.

    Параметры
    ----------
    dp : Sequence[int]
        Массив значений ДП.
    index_labels : Sequence[str] | None
        Необязательные подписи индексов.

    Сложность
    ----------
    Время: O(n), где n = len(dp).
    Память: O(1) дополнительная.
    """
    n = len(dp)
    if index_labels is not None:
        label_line = "Index: "
        for label in index_labels:
            label_line += f"{label:>5}"
        print(label_line)

    value_line = "Value: "
    for value in dp:
        value_line += f"{value:>5}"
    print(value_line)


# 1. Числа Фибоначчи


def fibonacci_naive(n: int) -> int:
    """
    Наивный рекурсивный алгоритм вычисления n-го числа Фибоначчи.

    F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2) для n >= 2.

    Параметры
    ----------
    n : int
        Номер числа Фибоначчи (n >= 0).

    Returns
    -------
    int
        Значение F(n).

    Сложность
    ----------
    Время: O(2^n) — экспоненциальное из-за повторных вычислений.
    Память: O(n) для глубины стека.
    """
    if n < 0:
        raise ValueError("n must be non-negative.")

    if n <= 1:
        return n

    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


def fibonacci_memo(n: int, memo: Optional[Dict[int, int]] = None) -> int:
    """
    Нисходящее ДП (top-down) с мемоизацией для чисел Фибоначчи.

    Параметры
    ----------
    n : int
        Номер числа Фибоначчи (n >= 0).
    memo : dict[int, int] | None
        Словарь для сохранения уже вычисленных значений.

    Returns
    -------
    int
        Значение F(n).

    Сложность
    ----------
    Время: O(n) — каждая F(k) вычисляется один раз.
    Память: O(n) для memo и глубины стека.
    """
    if n < 0:
        raise ValueError("n must be non-negative.")

    if memo is None:
        memo = {}

    if n in memo:
        return memo[n]

    if n <= 1:
        memo[n] = n
    else:
        memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(
            n - 2,
            memo,
        )

    return memo[n]


def fibonacci_bottom_up(n: int) -> int:
    """
    Восходящее ДП (bottom-up) для чисел Фибоначчи.

    Строится таблица dp[0..n], где dp[i] = F(i).

    Параметры
    ----------
    n : int
        Номер числа Фибоначчи (n >= 0).

    Returns
    -------
    int
        Значение F(n).

    Сложность
    ----------
    Время: O(n).
    Память: O(n) — можно улучшить до O(1), храня только два последних значения.
    """
    if n < 0:
        raise ValueError("n must be non-negative.")

    if n <= 1:
        return n

    dp: List[int] = [0] * (n + 1)
    dp[0] = 0
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


# 2. Задача о рюкзаке 0-1 (DP)


def knapsack_01_bottom_up(
    items: Sequence[KnapsackItem],
    capacity: int,
) -> Tuple[int, List[int]]:
    """
    Восходящее ДП для задачи о рюкзаке 0-1.

    dp[i][w] — максимальная стоимость при рассмотрении первых i предметов
    и вместимости w.

    Параметры
    ----------
    items : Sequence[KnapsackItem]
        Список предметов.
    capacity : int
        Вместимость рюкзака (целое >= 0).

    Returns
    -------
    max_value : int
        Максимально достижимая стоимость.
    chosen_indices : list[int]
        Индексы предметов, которые входят в одно из оптимальных решений.

    Сложность
    ----------
    Пусть n = число предметов.
    Время: O(n * capacity).
    Память: O(n * capacity).
    """
    if capacity < 0:
        raise ValueError("Capacity must be non-negative.")

    n = len(items)
    dp: List[List[int]] = [
        [0] * (capacity + 1) for _ in range(n + 1)
    ]

    # Заполнение таблицы
    for i in range(1, n + 1):
        item = items[i - 1]
        for w in range(capacity + 1):
            if item.weight <= w:
                dp[i][w] = max(
                    dp[i - 1][w],
                    dp[i - 1][w - item.weight] + item.value,
                )
            else:
                dp[i][w] = dp[i - 1][w]

    max_value = dp[n][capacity]

    # Восстановление решения (множество предметов)
    chosen_indices: List[int] = []
    w = capacity
    i = n
    while i > 0 and w >= 0:
        if dp[i][w] != dp[i - 1][w]:
            chosen_indices.append(i - 1)
            w -= items[i - 1].weight
        i -= 1

    chosen_indices.reverse()
    return max_value, chosen_indices


def print_knapsack_table(
    items: Sequence[KnapsackItem],
    capacity: int,
) -> None:
    """
    Построить и вывести таблицу ДП для задачи рюкзака 0-1.

    Функция полезна для визуализации на маленьких примерах.

    Параметры
    ----------
    items : Sequence[KnapsackItem]
        Предметы.
    capacity : int
        Вместимость рюкзака.

    Сложность
    ----------
    Время: O(n * capacity).
    Память: O(n * capacity).
    """
    n = len(items)
    dp: List[List[int]] = [
        [0] * (capacity + 1) for _ in range(n + 1)
    ]

    for i in range(1, n + 1):
        item = items[i - 1]
        for w in range(capacity + 1):
            if item.weight <= w:
                dp[i][w] = max(
                    dp[i - 1][w],
                    dp[i - 1][w - item.weight] + item.value,
                )
            else:
                dp[i][w] = dp[i - 1][w]

    row_labels = ["0"] + [f"i={i}" for i in range(1, n + 1)]
    col_labels = [f"w={w}" for w in range(capacity + 1)]
    print_dp_table_2d(dp, row_labels=row_labels, col_labels=col_labels)


# 3. Наибольшая общая подпоследовательность LCS


def lcs_bottom_up(
    s1: str,
    s2: str,
) -> Tuple[int, str]:
    """
    Восходящее ДП для поиска LCS (наибольшей общей подпоследовательности).

    dp[i][j] — длина LCS для префиксов s1[:i] и s2[:j].

    Параметры
    ----------
    s1, s2 : str
        Входные строки.

    Returns
    -------
    length : int
        Длина LCS.
    lcs_string : str
        Одна из возможных наибольших общих подпоследовательностей.

    Сложность
    ----------
    Пусть n = len(s1), m = len(s2).
    Время: O(n * m).
    Память: O(n * m).
    """
    n = len(s1)
    m = len(s2)

    dp: List[List[int]] = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(
                    dp[i - 1][j],
                    dp[i][j - 1],
                )

    # Восстановление LCS
    i, j = n, m
    result_chars: List[str] = []
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            result_chars.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    result_chars.reverse()
    return dp[n][m], "".join(result_chars)


def print_lcs_table(s1: str, s2: str) -> None:
    """
    Вывести таблицу ДП для задачи LCS.

    Параметры
    ----------
    s1, s2 : str
        Строки, для которых строится LCS.

    Сложность
    ----------
    Время: O(n * m).
    Память: O(n * m).
    """
    n = len(s1)
    m = len(s2)
    dp: List[List[int]] = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(
                    dp[i - 1][j],
                    dp[i][j - 1],
                )

    row_labels = [" "] + list(s1)
    col_labels = [" "] + list(s2)
    print_dp_table_2d(dp, row_labels=row_labels, col_labels=col_labels)


# 4. Расстояние Левенштейна


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Восходящее ДП для расстояния Левенштейна между строками s1 и s2.

    dp[i][j] — минимальная стоимость превращения префикса s1[:i]
    в префикс s2[:j] с помощью операций:
    * вставка символа,
    * удаление символа,
    * замена символа.

    Стоимости всех операций считаются равными 1.

    Параметры
    ----------
    s1, s2 : str
        Входные строки.

    Returns
    -------
    int
        Расстояние Левенштейна между s1 и s2.

    Сложность
    ----------
    Пусть n = len(s1), m = len(s2).
    Время: O(n * m).
    Память: O(n * m).
    """
    n = len(s1)
    m = len(s2)

    # dp имеет размер (n+1) x (m+1)
    dp: List[List[int]] = [[0] * (m + 1) for _ in range(n + 1)]

    # База: превращение пустой строки в префикс s2 и наоборот
    for i in range(1, n + 1):
        dp[i][0] = i  # удалить i символов из s1
    for j in range(1, m + 1):
        dp[0][j] = j  # вставить j символов в s1

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost_replace = 0 if s1[i - 1] == s2[j - 1] else 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,          # удаление символа из s1
                dp[i][j - 1] + 1,          # вставка символа в s1
                dp[i - 1][j - 1] + cost_replace,  # замена / совпадение
            )

    return dp[n][m]


def print_levenshtein_table(s1: str, s2: str) -> None:
    """
    Построить и вывести таблицу ДП для расстояния Левенштейна.

    dp[i][j] — минимальная стоимость превращения s1[:i] в s2[:j].

    Параметры
    ----------
    s1, s2 : str
        Входные строки.

    Сложность
    ----------
    Время: O(n * m).
    Память: O(n * m).
    """
    n = len(s1)
    m = len(s2)
    dp: List[List[int]] = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        dp[i][0] = i
    for j in range(1, m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost_replace = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost_replace,
            )

    # Метки — пустой символ + сами строки
    row_labels = [" "] + list(s1)
    col_labels = [" "] + list(s2)
    print_dp_table_2d(dp, row_labels=row_labels, col_labels=col_labels)


# 5. Размен монет (минимум монет, DP)


def coin_change_min_coins(
    amount: int,
    coins: Iterable[int],
) -> Tuple[int, List[int]]:
    """
    ДП-решение задачи размена монет: минимум монет для заданной суммы.

    dp[x] — минимальное количество монет, чтобы набрать сумму x.
    prev_coin[x] — номинал монеты, которой заканчивается оптимальный размен
    суммы x.

    Параметры
    ----------
    amount : int
        Сумма, которую нужно набрать (amount >= 0).
    coins : Iterable[int]
        Номиналы монет (положительные целые).

    Returns
    -------
    min_coins : int
        Минимальное количество монет.
    decomposition : list[int]
        Список номиналов монет, дающих оптимальный размен.

    Сложность
    ----------
    Пусть n = amount, k = число номиналов.
    Время: O(n * k).
    Память: O(n).
    """
    if amount < 0:
        raise ValueError("Amount must be non-negative.")

    coin_list = sorted(set(coins))
    if amount == 0:
        return 0, []

    if not coin_list:
        raise ValueError("No coins provided.")

    if any(c <= 0 for c in coin_list):
        raise ValueError("Coin denominations must be positive.")

    # Инициализация
    INF = amount + 1
    dp: List[int] = [INF] * (amount + 1)
    prev_coin: List[int] = [-1] * (amount + 1)
    dp[0] = 0

    for x in range(1, amount + 1):
        for coin in coin_list:
            if coin <= x and dp[x - coin] + 1 < dp[x]:
                dp[x] = dp[x - coin] + 1
                prev_coin[x] = coin

    if dp[amount] == INF:
        raise ValueError(
            f"Cannot make amount {amount} with coins {coin_list}",
        )

    # Восстановление размена
    result: List[int] = []
    current = amount
    while current > 0:
        coin = prev_coin[current]
        if coin == -1:
            break
        result.append(coin)
        current -= coin

    return dp[amount], result


def print_coin_change_table(amount: int, coins: Iterable[int]) -> None:
    """
    Построить и вывести таблицу dp для задачи размена монет.

    Параметры
    ----------
    amount : int
        Целевая сумма.
    coins : Iterable[int]
        Номиналы монет.

    Сложность
    ----------
    Время: O(amount * k).
    Память: O(amount).
    """
    coin_list = sorted(set(coins))
    INF = amount + 1
    dp: List[int] = [INF] * (amount + 1)
    dp[0] = 0

    for x in range(1, amount + 1):
        for coin in coin_list:
            if coin <= x and dp[x - coin] + 1 < dp[x]:
                dp[x] = dp[x - coin] + 1

    index_labels = [str(x) for x in range(amount + 1)]
    print_dp_table_1d(dp, index_labels=index_labels)


# 6. Наибольшая возрастающая подпоследовательность (LIS)


def lis_dp(sequence: Sequence[int]) -> Tuple[int, List[int]]:
    """
    ДП-решение задачи о наибольшей возрастающей подпоследовательности (LIS).

    dp[i] — длина LIS, оканчивающейся на позиции i.
    prev[i] — индекс предыдущего элемента в LIS, оканчивающейся в i.

    Параметры
    ----------
    sequence : Sequence[int]
        Входная последовательность чисел.

    Returns
    -------
    length : int
        Длина LIS.
    subsequence : list[int]
        Одна из наибольших возрастающих подпоследовательностей.

    Сложность
    ----------
    Пусть n = len(sequence).
    Время: O(n^2), так как для каждого i просматриваются все j < i.
    Память: O(n).
    """
    n = len(sequence)
    if n == 0:
        return 0, []

    dp: List[int] = [1] * n
    prev: List[int] = [-1] * n

    for i in range(n):
        for j in range(i):
            if (
                sequence[j] < sequence[i]
                and dp[j] + 1 > dp[i]
            ):
                dp[i] = dp[j] + 1
                prev[i] = j

    max_len = max(dp)
    max_index = dp.index(max_len)

    # Восстановление LIS
    lis_indices: List[int] = []
    k = max_index
    while k != -1:
        lis_indices.append(k)
        k = prev[k]
    lis_indices.reverse()

    subsequence = [sequence[i] for i in lis_indices]
    return max_len, subsequence


def print_lis_table(sequence: Sequence[int]) -> None:
    """
    Вывести массив dp для задачи LIS (наглядность).

    Параметры
    ----------
    sequence : Sequence[int]
        Входная последовательность.

    Сложность
    ----------
    Время: O(n^2).
    Память: O(n).
    """
    n = len(sequence)
    if n == 0:
        print("Пустая последовательность.")
        return

    dp: List[int] = [1] * n

    for i in range(n):
        for j in range(i):
            if sequence[j] < sequence[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1

    index_labels = [str(i) for i in range(n)]
    print("Последовательность:", sequence)
    print_dp_table_1d(dp, index_labels=index_labels)


# Примеры использования (для ручного тестирования)


def main() -> None:
    """
    Пример ручного запуска модуля.
    Включает демонстрацию работы основных функций ДП.
    """
    print("=== Fibonacci ===")
    n = 10
    print(f"F_naive({n}) = {fibonacci_naive(n)}")
    print(f"F_memo({n}) = {fibonacci_memo(n)}")
    print(f"F_bottom_up({n}) = {fibonacci_bottom_up(n)}")

    print("\n=== Knapsack 0-1 ===")
    items = [
        KnapsackItem(2, 3, "item1"),
        KnapsackItem(3, 4, "item2"),
        KnapsackItem(4, 5, "item3"),
        KnapsackItem(5, 8, "item4"),
    ]
    capacity = 5
    max_value, chosen = knapsack_01_bottom_up(items, capacity)
    print(f"Max value = {max_value}")
    print("Chosen items:", [items[i].name for i in chosen])
    print_knapsack_table(items, capacity)

    print("\n=== LCS ===")
    s1, s2 = "ABCBDAB", "BDCAB"
    length, lcs_str = lcs_bottom_up(s1, s2)
    print(f"LCS length = {length}, LCS = '{lcs_str}'")
    print_lcs_table(s1, s2)

    print("\n=== Levenshtein distance ===")
    s1_lev, s2_lev = "kitten", "sitting"
    dist = levenshtein_distance(s1_lev, s2_lev)
    print(f"Levenshtein('{s1_lev}', '{s2_lev}') = {dist}")
    print_levenshtein_table(s1_lev, s2_lev)

    print("\n=== Coin change (DP) ===")
    amount = 11
    coins = [1, 2, 5]
    min_coins, decomp = coin_change_min_coins(amount, coins)
    print(f"Amount {amount}, min coins = {min_coins}")
    print("Decomposition:", decomp)
    print_coin_change_table(amount, coins)

    print("\n=== LIS ===")
    seq = [10, 9, 2, 5, 3, 7, 101, 18]
    length, subseq = lis_dp(seq)
    print(f"LIS length = {length}, subsequence = {subseq}")
    print_lis_table(seq)


if __name__ == "__main__":
    main()
