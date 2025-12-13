# demo_string_matching.py


from __future__ import annotations

from string_matching import (
    find_all_occurrences,
    is_cyclic_shift,
    minimal_period_prefix,
    minimal_period_z,
)


def demo_find_all_occurrences() -> None:
    print("=== Задача 1: Поиск всех вхождений паттерна в тексте ===")

    text = "aabaaabaaac"
    pattern = "aa"

    print(f"Текст:    {text}")
    print(f"Паттерн: {pattern}")
    print()

    methods = ["naive", "kmp", "z", "rk"]
    for method in methods:
        positions = find_all_occurrences(text, pattern, method=method)
        print(f"Метод {method:>6}: позиции вхождений = {positions}")

    print()


def demo_cyclic_shift() -> None:
    print("=== Задача 2: Проверка циклического сдвига строк ===")

    test_cases = [
        ("abcd", "cdab"),
        ("abcd", "dabc"),
        ("abcd", "acbd"),
        ("aaaa", "aaaa"),
        ("abc", "abc"),
    ]

    for a, b in test_cases:
        result = is_cyclic_shift(a, b, method="kmp")
        print(f"'{b}' является циклическим сдвигом '{a}': {result}")

    print()


def demo_minimal_period() -> None:
    print("=== Задача 3: Поиск минимального периода строки ===")

    strings = [
        "abababab",
        "aaaaaa",
        "abacaba",
        "abcabcabc",
        "a",
        "",
    ]

    for s in strings:
        p1 = minimal_period_prefix(s)
        p2 = minimal_period_z(s)
        print(f"Строка: '{s}'")
        print(f"  Минимальный период (π-функция): {p1}")
        print(f"  Минимальный период (Z-функция): {p2}")
        print()

    print()


def main() -> None:
    print("ДЕМОНСТРАЦИЯ АЛГОРИТМОВ НА СТРОКАХ (ТЕМА 11)\n")

    demo_find_all_occurrences()
    demo_cyclic_shift()
    demo_minimal_period()

    print("Демонстрация завершена.")


if __name__ == "__main__":
    main()
