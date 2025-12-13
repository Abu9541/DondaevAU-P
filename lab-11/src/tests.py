# tests.py

from __future__ import annotations

import unittest

from prefix_function import prefix_function
from z_function import z_function
from kmp_search import kmp_search
from string_matching import (
    naive_search,
    z_search,
    rabin_karp_search,
    find_all_occurrences,
    is_cyclic_shift,
    minimal_period_prefix,
    minimal_period_z,
)


SEARCH_METHODS = ["naive", "kmp", "z", "rk"]


# Prefix / Z functions

class TestPrefixFunction(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertEqual(prefix_function(""), [])
        self.assertEqual(prefix_function("a"), [0])
        self.assertEqual(prefix_function("aaaa"), [0, 1, 2, 3])
        self.assertEqual(prefix_function("abacaba"), [0, 0, 1, 0, 1, 2, 3])


class TestZFunction(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertEqual(z_function(""), [])
        self.assertEqual(z_function("a"), [0])
        self.assertEqual(z_function("aaaaa"), [0, 4, 3, 2, 1])
        self.assertEqual(z_function("abacaba"), [0, 0, 1, 0, 3, 0, 1])


# Базовые алгоритмы поиска

class TestBasicSearchAlgorithms(unittest.TestCase):
    def test_consistency(self) -> None:
        text = "ababa"
        pattern = "aba"
        expected = [0, 2]

        self.assertEqual(naive_search(text, pattern), expected)
        self.assertEqual(kmp_search(text, pattern), expected)
        self.assertEqual(z_search(text, pattern), expected)
        self.assertEqual(rabin_karp_search(text, pattern), expected)

    def test_no_match(self) -> None:
        text = "abcdef"
        pattern = "xyz"
        expected: list[int] = []

        self.assertEqual(naive_search(text, pattern), expected)
        self.assertEqual(kmp_search(text, pattern), expected)
        self.assertEqual(z_search(text, pattern), expected)
        self.assertEqual(rabin_karp_search(text, pattern), expected)

    def test_empty_pattern(self) -> None:
        text = "abc"
        expected = [0, 1, 2, 3]

        self.assertEqual(naive_search(text, ""), expected)
        self.assertEqual(kmp_search(text, ""), expected)
        self.assertEqual(z_search(text, ""), expected)
        self.assertEqual(rabin_karp_search(text, ""), expected)


# find_all_occurrences

class TestFindAllOccurrences(unittest.TestCase):
    def test_all_methods_match(self) -> None:
        text = "aabaaabaaac"
        pattern = "aa"

        expected = naive_search(text, pattern)

        for method in SEARCH_METHODS:
            with self.subTest(method=method):
                result = find_all_occurrences(text, pattern, method=method)
                self.assertEqual(result, expected)

    def test_empty_pattern(self) -> None:
        text = "abc"
        expected = [0, 1, 2, 3]

        for method in SEARCH_METHODS:
            with self.subTest(method=method):
                self.assertEqual(
                    find_all_occurrences(text, "", method=method),
                    expected,
                )

    def test_no_occurrences(self) -> None:
        text = "abcdef"
        pattern = "zzz"

        for method in SEARCH_METHODS:
            with self.subTest(method=method):
                self.assertEqual(
                    find_all_occurrences(text, pattern, method=method),
                    [],
                )


# Проверка циклического сдвига

class TestCyclicShift(unittest.TestCase):
    def test_positive_cases(self) -> None:
        cases = [
            ("abcd", "cdab"),
            ("abcd", "dabc"),
            ("aaaa", "aaaa"),
            ("abcabc", "bcabca"),
        ]

        for a, b in cases:
            for method in SEARCH_METHODS:
                with self.subTest(a=a, b=b, method=method):
                    self.assertTrue(is_cyclic_shift(a, b, method=method))

    def test_negative_cases(self) -> None:
        cases = [
            ("abcd", "acbd"),
            ("abcd", "abc"),
            ("abcd", "abce"),
        ]

        for a, b in cases:
            for method in SEARCH_METHODS:
                with self.subTest(a=a, b=b, method=method):
                    self.assertFalse(is_cyclic_shift(a, b, method=method))

    def test_empty_strings(self) -> None:
        for method in SEARCH_METHODS:
            with self.subTest(method=method):
                self.assertTrue(is_cyclic_shift("", "", method=method))

    def test_same_string(self) -> None:
        for method in SEARCH_METHODS:
            with self.subTest(method=method):
                self.assertTrue(is_cyclic_shift("abc", "abc", method=method))


# Период строки

class TestMinimalPeriod(unittest.TestCase):
    def test_periodic(self) -> None:
        s = "abababab"
        self.assertEqual(minimal_period_prefix(s), 2)
        self.assertEqual(minimal_period_z(s), 2)

    def test_not_periodic(self) -> None:
        s = "abacaba"
        self.assertEqual(minimal_period_prefix(s), len(s))
        self.assertEqual(minimal_period_z(s), len(s))

    def test_empty(self) -> None:
        self.assertEqual(minimal_period_prefix(""), 0)
        self.assertEqual(minimal_period_z(""), 0)


if __name__ == "__main__":
    unittest.main()
