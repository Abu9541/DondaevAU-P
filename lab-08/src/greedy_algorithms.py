# greedy_algorithms.py


from __future__ import annotations

from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class Interval:
    """
    Отрезок времени [start, end).

    Атрибуты
    ----------
    start : int | float
        Время начала интервала.
    end : int | float
        Время окончания интервала (не входит).
    """
    start: float
    end: float


@dataclass(frozen=True)
class Item:
    """
    Предмет для задачи о рюкзаке.

    Атрибуты
    ----------
    weight : float
        Вес предмета ( > 0 ).
    value : float
        Стоимость (полезность) предмета ( >= 0 ).
    name : str | None
        Необязательное имя для удобства интерпретации результата.
    """
    weight: float
    value: float
    name: Optional[str] = None

    @property
    def value_density(self) -> float:
        """
        Отношение ценности к весу (value / weight).

        Сложность
        ----------
        O(1)
        """
        if self.weight <= 0:
            raise ValueError("Weight must be positive.")
        return self.value / self.weight


@dataclass
class HuffmanNode:
    """
    Узел дерева Хаффмана.

    Атрибуты
    ----------
    freq : int
        Частота символа (или суммарная частота поддерева).
    symbol : str | None
        Символ (для листа) или None (для внутреннего узла).
    left : HuffmanNode | None
        Левый потомок.
    right : HuffmanNode | None
        Правый потомок.
    """
    freq: int
    symbol: Optional[str] = None
    left: Optional["HuffmanNode"] = None
    right: Optional["HuffmanNode"] = None

    def is_leaf(self) -> bool:
        """
        Проверка, что узел — лист.

        Сложность
        ----------
        O(1)
        """
        return self.left is None and self.right is None


# 1. Задача о выборе заявок (IS)


def select_intervals_greedy(intervals: Iterable[Interval]) -> List[Interval]:
    """
    Жадный алгоритм выбора максимального количества
    непересекающихся интервалов.

    Стратегия
    --------
    1. Отсортировать интервалы по времени окончания по возрастанию.
    2. Идти слева направо, каждый раз выбирая первый интервал, который
       начинается не раньше,
       чем заканчивается уже выбранный последний интервал.

    Параметры
    ----------
    intervals : Iterable[Interval]
        Коллекция интервалов [start, end).

    Returns
    -------
    List[Interval]
        Список выбранных интервалов, образующих решение максимального размера.

    Корректность
    --------------------
    Жадный выбор по наименьшему окончанию оптимален, потому что:
    * Любое оптимальное решение можно преобразовать так, чтобы его первый
      интервал завершался не позже, чем первый интервал жадного решения,
      без уменьшения количества интервалов.
    * Далее можно применить тот же аргумент к остаточной задаче (инвариант).

    Сложность
    ----------
    Время: O(n log n) на сортировку + O(n) на один проход = O(n log n).
    Память: O(n) для хранения отсортированных интервалов и ответа.
    """
    intervals_list = sorted(intervals, key=lambda x: x.end)  # O(n log n)

    result: List[Interval] = []
    current_end: float = float("-inf")

    for interval in intervals_list:  # O(n)
        if interval.start >= current_end:  # O(1)
            result.append(interval)        # O(1) (амортизированно)
            current_end = interval.end     # O(1)

    return result


# 2. Непрерывная (дробная) задача рюкзака


def fractional_knapsack(
    items: Iterable[Item],
    capacity: float,
) -> Tuple[float, List[Tuple[Item, float]]]:
    """
    Жадный алгоритм для непрерывной (дробной) задачи о рюкзаке.

    Можно брать дробные части предметов. Цель — максимизировать суммарную
    стоимость при ограничении по суммарному весу.

    Стратегия
    --------
    1. Отсортировать предметы по убыванию плотности стоимости (value/weight).
    2. Добавлять предметы в рюкзак, пока хватает вместимости.
       Если следующий предмет не помещается целиком, взять его дробную часть.

    Параметры
    ----------
    items : Iterable[Item]
        Предметы с полями weight > 0 и value >= 0.
    capacity : float
        Вместимость рюкзака ( capacity >= 0 ).

    Returns
    -------
    total_value : float
        Максимально достигнутая суммарная стоимость.
    taken : list[tuple[Item, float]]
        Список пар (предмет, доля_0_1), отражающий стратегию набора.

    Корректность
    --------------------
    Из-за того, что можно делить предметы, оптимальное решение имеет
    следующую структуру: все взятые предметы — полностью, кроме, возможно,
    одного последнего частично. Доказано, что при таком ограничении
    выбор по убыванию value/weight даёт оптимум (уравнение Куна-Таккера /
    классическое доказательство перестановками).

    Сложность
    ----------
    Время: O(n log n) (сортировка по плотности) + O(n) обход = O(n log n).
    Память: O(n) для отсортированного списка и результата.
    """
    if capacity < 0:
        raise ValueError("Capacity must be non-negative.")

    items_sorted = sorted(
        items,
        key=lambda x: x.value_density,
        reverse=True,
    )  # O(n log n)

    remaining_capacity = capacity
    total_value = 0.0
    taken: List[Tuple[Item, float]] = []

    for item in items_sorted:  # O(n)
        if remaining_capacity <= 0:
            break

        if item.weight <= remaining_capacity:
            # Берём предмет целиком.
            taken.append((item, 1.0))  # O(1)
            remaining_capacity -= item.weight
            total_value += item.value
        else:
            # Берём лишь часть предмета.
            fraction = remaining_capacity / item.weight  # O(1)
            taken.append((item, fraction))
            total_value += item.value * fraction
            remaining_capacity = 0.0

    return total_value, taken


# 3. Алгоритм Хаффмана (Huffman coding)


def build_huffman_tree(frequencies: Dict[str, int]) -> Optional[HuffmanNode]:
    """
    Построение дерева Хаффмана по заданным частотам символов.

    Параметры
    ----------
    frequencies : dict[str, int]
        Словарь вида {символ: частота}, частоты > 0.

    Returns
    -------
    HuffmanNode | None
        Корень дерева Хаффмана или None, если частоты пусты.

    Корректность
    -------------------
    Алгоритм последовательно объединяет два наименее частотных дерева.
    Доказывается, что в оптимальном префиксном коде два символа с
    наименьшей частотой будут на максимально глубокой паре листьев,
    поэтому локальный выбор двух минимальных частот согласуется с
    глобальным оптимумом.

    Сложность
    ----------
    Пусть k — число различных символов.
    Время: O(k log k) — k извлечений и вставок в мин-кучу.
    Память: O(k) — для хранения дерева.
    """
    if not frequencies:
        return None

    # Инициализация мин-кучи
    # Элемент кучи: (частота, порядковый_номер, узел)
    # Порядковый номер нужен, чтобы избежать сравнения узлов при равных freq.
    heap: List[Tuple[int, int, HuffmanNode]] = []
    counter = 0

    for symbol, freq in frequencies.items():  # O(k)
        node = HuffmanNode(freq=freq, symbol=symbol)
        heappush(heap, (freq, counter, node))  # O(log k)
        counter += 1

    # Особый случай: единственный символ
    if len(heap) == 1:
        return heap[0][2]

    # Итеративно объединяем два наименее частотных узла
    while len(heap) > 1:  # O(k)
        freq1, _, node1 = heappop(heap)  # O(log k)
        freq2, _, node2 = heappop(heap)  # O(log k)
        merged = HuffmanNode(
            freq=freq1 + freq2,
            left=node1,
            right=node2,
        )
        heappush(heap, (merged.freq, counter, merged))  # O(log k)
        counter += 1

    return heap[0][2]


def build_huffman_codes(frequencies: Dict[str, int]) -> Dict[str, str]:
    """
    Построение оптимального префиксного кода Хаффмана.

    Параметры
    ----------
    frequencies : dict[str, int]
        Частоты символов.

    Returns
    -------
    dict[str, str]
        Словарь {символ: битовая_строка}.

    Сложность
    ----------
    Время: O(k log k + k), где k — число символов.
    Память: O(k).
    """
    root = build_huffman_tree(frequencies)  # O(k log k)

    if root is None:
        return {}

    codes: Dict[str, str] = {}

    # Обход дерева в глубину для назначения кодов.
    def dfs(node: HuffmanNode, prefix: str) -> None:
        """
        Рекурсивно обходит дерево и заполняет словарь codes.

        Сложность
        ----------
        Время: O(k), каждый узел посещается один раз.
        Память: O(h) для стека, где h — высота дерева.
        """
        if node.is_leaf():
            # Особый случай: один символ в алфавите — ему даём код '0'.
            codes[node.symbol if node.symbol is not None else ""] = (
                prefix or "0"
            )
            return

        if node.left is not None:
            dfs(node.left, prefix + "0")
        if node.right is not None:
            dfs(node.right, prefix + "1")

    dfs(root, "")

    return codes


def huffman_encode(text: str, codes: Dict[str, str]) -> str:
    """
    Кодирует строку `text` с помощью словаря кодов Хаффмана.

    Параметры
    ----------
    text : str
        Исходная строка.
    codes : dict[str, str]
        Словарь {символ: код}.

    Returns
    -------
    str
        Битовая строка ('0' и '1').

    Сложность
    ----------
    Время: O(len(text)).
    Память: O(len(text)).
    """
    return "".join(codes[ch] for ch in text)


def huffman_decode(encoded: str, codes: Dict[str, str]) -> str:
    """
    Декодирует битовую строку, используя словарь кодов Хаффмана.

    Параметры
    ----------
    encoded : str
        Битовая строка.
    codes : dict[str, str]
        Словарь {символ: код}.

    Returns
    -------
    str
        Восстановленная строка.

    Сложность
    ----------
    Время: O(len(encoded)).
    Память: O(len(encoded)).
    """
    # Строим обратный словарь для декодирования.
    reverse_codes: Dict[str, str] = {v: k for k, v in codes.items()}  # O(k)

    decoded_chars: List[str] = []
    current = ""

    for bit in encoded:  # O(L)
        current += bit
        if current in reverse_codes:
            decoded_chars.append(reverse_codes[current])
            current = ""

    return "".join(decoded_chars)


def pretty_print_huffman_tree(
    root: Optional[HuffmanNode],
    indent: str = "",
    edge_label: str = "",
) -> None:
    """
    Напечатать дерево Хаффмана в текстовом виде (для отчёта/отладки).

    Узлы выводятся в виде:

        [freq] 'symbol' (edge_label)

    где edge_label — метка ребра от родителя: '0' или '1'.

    Параметры
    ----------
    root : HuffmanNode | None
        Корень дерева Хаффмана.
    indent : str
        Левый отступ для текущего уровня (используется рекурсивно).
    edge_label : str
        Метка ребра ('0' или '1'), ведущего к этому узлу.

    Сложность
    ----------
    Время: O(k), где k — число узлов дерева.
    Память: O(h) для стека рекурсии, h — высота дерева.
    """
    if root is None:
        print("<empty tree>")
        return

    # Печатаем текущий узел
    label = f" ({edge_label})" if edge_label else ""
    if root.symbol is None:
        node_repr = f"[{root.freq}]{label}"
    else:
        node_repr = f"[{root.freq}] '{root.symbol}'{label}"

    print(indent + node_repr)

    # Рекурсивно печатаем детей, если они есть
    if root.left is not None:
        pretty_print_huffman_tree(
            root.left,
            indent=indent + "  ",
            edge_label="0",
        )
    if root.right is not None:
        pretty_print_huffman_tree(
            root.right,
            indent=indent + "  ",
            edge_label="1",
        )

# 4. Минимальное остовное дерево (алгоритм Краскала)


class DisjointSetUnion:
    """
    Структура «Система непересекающихся множеств» (DSU / Union-Find).

    Используется для алгоритма Краскала.

    Сложность
    ----------
    Для m операций объединения/поиска на n элементах
    амортизированная сложность почти O(1):
    O(m * α(n)), где α — обратная функция Аккермана.
    """

    def __init__(self, size: int) -> None:
        if size <= 0:
            raise ValueError("Size must be positive.")
        self.parent: List[int] = list(range(size))
        self.rank: List[int] = [0] * size

    def find(self, x: int) -> int:
        """
        Поиск представителя множества с сжатием пути.

        Сложность
        ----------
        Амортизированно почти O(1).
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, a: int, b: int) -> bool:
        """
        Объединение двух множеств.

        Параметры
        ----------
        a, b : int
            Индексы элементов (вершин графа).

        Returns
        -------
        bool
            True, если множества были разными и произошёл union,
            False, если a и b уже в одном множестве.

        Сложность
        ----------
        Амортизированно почти O(1).
        """
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return False

        # Union by rank
        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a
        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1

        return True


def kruskal_mst(
    num_vertices: int,
    edges: Iterable[Tuple[int, int, float]],
) -> Tuple[float, List[Tuple[int, int, float]]]:
    """
    Алгоритм Краскала для построения минимального остовного дерева (MST).

    Параметры
    ----------
    num_vertices : int
        Количество вершин в графе (нумеруются 0..num_vertices-1).
    edges : Iterable[tuple[int, int, float]]
        Рёбра в форме (u, v, weight). Предполагается, что граф связен
        или рассматривается MST каждой компоненты.

    Return
    -------
    total_weight : float
        Общий вес остовного дерева.
    mst_edges : list[tuple[int, int, float]]
        Список рёбер MST.

    Стратегия
    -----------------
    1. Отсортировать все рёбра по весу по возрастанию.
    2. Идти по списку, добавляя ребро, если оно соединяет две разные
       компоненты (проверка через DSU). Иначе игнорировать (чтобы
       не образовывать цикл).

    Корректность
    --------------------
    Используется «свойство безопасного ребра»: ребро минимального веса,
    пересекающее некоторый разрез, не нарушающий уже выбранный частичный
    остов, всегда может входить в некоторый MST. Алгоритм Краскала
    на каждом шаге выбирает именно такие минимальные безопасные рёбра.

    Сложность
    ----------
    Пусть m — число рёбер, n — число вершин.
    Время: O(m log m + m * α(n)) ≈ O(m log m) из-за сортировки.
    Память: O(m + n).
    """
    if num_vertices <= 0:
        raise ValueError("Number of vertices must be positive.")

    edges_list = list(edges)
    # Сортировка рёбер по весу
    edges_list.sort(key=lambda e: e[2])  # O(m log m)

    dsu = DisjointSetUnion(num_vertices)
    mst_edges: List[Tuple[int, int, float]] = []
    total_weight = 0.0

    for u, v, w in edges_list:  # O(m * α(n))
        if dsu.union(u, v):
            mst_edges.append((u, v, w))
            total_weight += w
            if len(mst_edges) == num_vertices - 1:
                break

    return total_weight, mst_edges

# 5. Задача о размене монет (минимум монет)


def greedy_change(
    denominations: Iterable[int],
    amount: int,
) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Жадный алгоритм размена суммы на минимальное число монет.

    Предполагается, что набор номиналов *канонический* (как в рублях):
    жадный выбор даёт оптимальное решение (например, 1, 2, 5, 10, 50).

    Стратегия
    --------
    1. Отсортировать номиналы по убыванию.
    2. Идти от большего к меньшему:
       - на каждом шаге брать максимально возможное количество монет
         текущего номинала, не превышая оставшуюся сумму.

    Параметры
    ----------
    denominations : Iterable[int]
        Доступные номиналы монет (положительные целые числа).
    amount : int
        Сумма, которую нужно выдать (неотрицательное целое число).

    Return
    -------
    total_coins : int
        Общее количество выданных монет.
    result : list[tuple[int, int]]
        Список пар (номинал, количество монет с этим номиналом) в порядке
        убывания номиналов.

    Проверки
    ------
    ValueError
        Если `amount` отрицательно или нет способа разменять сумму
        при данных номиналах (например, нет монеты 1).

    Корректность
    ------------------
    Жадный алгоритм не всегда оптимален для произвольных номиналов.
    Однако для стандартных денежных систем (1, 2, 5, 10, 50, 100, ...)
    можно доказать, что жадный выбор "брать как можно больше монет крупного
    номинала" даёт оптимум.

    Сложность
    ----------
    Пусть k = число различных номиналов.
    Время: O(k log k) на сортировку + O(k) проход = O(k log k).
    Память: O(k).
    """
    if amount < 0:
        raise ValueError("Amount must be non-negative.")

    coins = sorted(set(denominations), reverse=True)  # O(k log k)
    if not coins:
        if amount == 0:
            return 0, []
        raise ValueError("No denominations provided.")

    remaining = amount
    result: List[Tuple[int, int]] = []
    total_coins = 0

    for coin in coins:  # O(k)
        if coin <= 0:
            raise ValueError("Coin denominations must be positive.")

        count = remaining // coin  # O(1)
        if count > 0:
            result.append((coin, count))
            total_coins += count
            remaining -= coin * count

        if remaining == 0:
            break

    if remaining != 0:
        # Для данной системы номиналов и суммы размена нет
        raise ValueError(
            f"Cannot make change for {amount} "
            f"with given denominations {coins}",
        )

    return total_coins, result
