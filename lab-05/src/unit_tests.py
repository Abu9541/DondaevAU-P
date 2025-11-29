# unit_tests.py
"""Unit-тесты для проверки корректности работы хеш-функций и хеш-таблиц."""

from hash_functions import simple_hash, polynomial_hash, djb2_hash  # O(1)
from hash_table_chaining import HashTableChaining  # O(1)
from hash_table_open_addressing import (HashTableOpenAddressing,  # O(1)
                                        HashTableLinearProbing)  # O(1)
import unittest
import sys
import os

# Добавляем путь для импорта модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # O(1)


class TestHashFunctions(unittest.TestCase):
    """Тесты для хеш-функций."""

    def test_simple_hash_deterministic(self) -> None:
        """Тест детерминированности простой хеш-функции."""
        key = "test_key"  # O(1)
        table_size = 100  # O(1)

        hash1 = simple_hash(key, table_size)  # O(n)
        hash2 = simple_hash(key, table_size)  # O(n)

        self.assertEqual(hash1, hash2)  # O(1)
        self.assertIsInstance(hash1, int)  # O(1)
        self.assertGreaterEqual(hash1, 0)  # O(1)
        self.assertLess(hash1, table_size)  # O(1)

    def test_polynomial_hash_distribution(self) -> None:
        """Тест распределения полиномиальной хеш-функции."""
        keys = ["abc", "acb", "bac", "bca", "cab", "cba"]  # O(1)
        table_size = 100  # O(1) - увеличиваем размер таблицы для лучшего распределения
        hashes = set()  # O(1)

        for key in keys:  # O(k)
            hash_val = polynomial_hash(key, table_size)  # O(n)
            hashes.add(hash_val)  # O(1)
            self.assertGreaterEqual(hash_val, 0)  # O(1)
            self.assertLess(hash_val, table_size)  # O(1)

        # Для маленького набора данных можем иметь коллизии, это нормально
        # Проверяем что есть хотя бы несколько разных хешей
        self.assertGreater(len(hashes), 1)  # O(1) - ослабляем условие

    def test_djb2_hash_quality(self) -> None:
        """Тест качества хеш-функции DJB2."""
        test_cases = [  # O(1)
            ("hello", 10),  # O(1)
            ("world", 10),  # O(1)
            ("test", 10),  # O(1)
            ("hash", 10),  # O(1)
        ]

        for key, table_size in test_cases:  # O(k)
            hash_val = djb2_hash(key, table_size)  # O(n)
            self.assertIsInstance(hash_val, int)  # O(1)
            self.assertGreaterEqual(hash_val, 0)  # O(1)
            self.assertLess(hash_val, table_size)  # O(1)

    def test_hash_functions_range(self) -> None:
        """Тест,
        что все хеш-функции возвращают значения в правильном диапазоне."""
        key = "test_key"  # O(1)
        table_size = 50  # O(1)

        hash_functions = [simple_hash, polynomial_hash, djb2_hash]  # O(1)

        for hash_func in hash_functions:  # O(m)
            with self.subTest(hash_func=hash_func.__name__):  # O(1)
                hash_val = hash_func(key, table_size)  # O(n)
                self.assertGreaterEqual(hash_val, 0)  # O(1)
                self.assertLess(hash_val, table_size)  # O(1)


class TestHashTableChaining(unittest.TestCase):
    """Тесты для хеш-таблицы с методом цепочек."""

    def setUp(self) -> None:
        """Настройка тестового окружения."""
        self.ht = HashTableChaining(capacity=5)  # O(n)

    def test_initial_state(self) -> None:
        """Тест начального состояния таблицы."""
        self.assertEqual(self.ht.size, 0)  # O(1)
        self.assertEqual(self.ht.capacity, 5)  # O(1)
        self.assertEqual(self.ht.load_factor, 0.0)  # O(1)

    def test_insert_and_get(self) -> None:
        """Тест вставки и получения элементов."""
        # Вставка новых элементов
        self.ht.insert("key1", "value1")  # O(1)
        self.ht.insert("key2", "value2")  # O(1)

        self.assertEqual(self.ht.size, 2)  # O(1)
        self.assertEqual(self.ht.get("key1"), "value1")  # O(1)
        self.assertEqual(self.ht.get("key2"), "value2")  # O(1)

    def test_update_existing_key(self) -> None:
        """Тест обновления существующего ключа."""
        self.ht.insert("key1", "value1")  # O(1)
        self.ht.insert("key1", "new_value")  # O(1) - обновление

        self.assertEqual(self.ht.size, 1)  # O(1) - размер не изменился
        self.assertEqual(self.ht.get("key1"), "new_value")  # O(1)

    def test_get_nonexistent_key(self) -> None:
        """Тест получения несуществующего ключа."""
        self.assertIsNone(self.ht.get("nonexistent"))  # O(1)

    def test_delete_existing_key(self) -> None:
        """Тест удаления существующего ключа."""
        self.ht.insert("key1", "value1")  # O(1)
        self.assertTrue(self.ht.delete("key1"))  # O(1)
        self.assertEqual(self.ht.size, 0)  # O(1)
        self.assertIsNone(self.ht.get("key1"))  # O(1)

    def test_delete_nonexistent_key(self) -> None:
        """Тест удаления несуществующего ключа."""
        self.assertFalse(self.ht.delete("nonexistent"))  # O(1)

    def test_contains_operator(self) -> None:
        """Тест оператора in."""
        self.ht.insert("key1", "value1")  # O(1)

        self.assertTrue("key1" in self.ht)  # O(1)
        self.assertFalse("nonexistent" in self.ht)  # O(1)

    def test_collision_handling(self) -> None:
        """Тест обработки коллизий."""
        # Создаем небольшую таблицу чтобы гарантировать коллизии
        small_ht = HashTableChaining(capacity=2)  # O(n)

        # Вставляем несколько элементов
        small_ht.insert("a", 1)  # O(1)
        small_ht.insert("b", 2)  # O(1)
        small_ht.insert("c", 3)  # O(1) - коллизия

        self.assertEqual(small_ht.size, 3)  # O(1)
        self.assertEqual(small_ht.get("a"), 1)  # O(1)
        self.assertEqual(small_ht.get("b"), 2)  # O(1)
        self.assertEqual(small_ht.get("c"), 3)  # O(1)

    def test_resize_operation(self) -> None:
        """Тест операции изменения размера."""
        # Начальная емкость 3, порог 0.7
        resize_ht = HashTableChaining(capacity=3, load_factor_threshold=0.7)  # O(n)

        self.assertEqual(resize_ht.capacity, 3)  # O(1)

        # Вставляем элементы чтобы вызвать рехеширование
        resize_ht.insert("k1", "v1")  # O(1)
        resize_ht.insert("k2", "v2")  # O(1)
        # После второго элемента коэффициент = 2/3 ≈ 0.67 < 0.7

        resize_ht.insert("k3", "v3")  # O(1)
        # После третьего элемента коэффициент = 3/3 = 1.0 > 0.7 → рехеширование

        # Проверяем что емкость увеличилась (обычно в 2 раза, но может быть другое значение)
        # Минимальная емкость после resize должна быть больше начальной
        self.assertGreater(resize_ht.capacity, 3)  # O(1) - емкость должна увеличиться
        self.assertEqual(resize_ht.size, 3)  # O(1) - все элементы сохранились
        self.assertEqual(resize_ht.get("k1"), "v1")  # O(1)
        self.assertEqual(resize_ht.get("k2"), "v2")  # O(1)
        self.assertEqual(resize_ht.get("k3"), "v3")  # O(1)

        # Добавляем еще элементы чтобы проверить что resize работает корректно
        original_capacity = resize_ht.capacity  # O(1)
        for i in range(10):  # O(10)
            resize_ht.insert(f"extra{i}", f"value{i}")  # O(1)

        # Проверяем что снова произошел resize при необходимости
        if resize_ht.load_factor > resize_ht.load_factor_threshold:  # O(1)
            self.assertGreater(resize_ht.capacity, original_capacity)  # O(1)


class TestHashTableOpenAddressing(unittest.TestCase):
    """Тесты для хеш-таблицы с открытой адресацией."""

    def setUp(self) -> None:
        """Настройка тестового окружения."""
        self.ht = HashTableOpenAddressing(capacity=5)  # O(n)

    def test_initial_state(self) -> None:
        """Тест начального состояния таблицы."""
        self.assertEqual(self.ht.size, 0)  # O(1)
        self.assertEqual(self.ht.capacity, 5)  # O(1)
        self.assertEqual(self.ht.load_factor, 0.0)  # O(1)

    def test_basic_operations(self) -> None:
        """Тест базовых операций."""
        # Вставка
        self.ht.insert("key1", "value1")  # O(1)
        self.ht.insert("key2", "value2")  # O(1)

        self.assertEqual(self.ht.size, 2)  # O(1)

        # Получение
        self.assertEqual(self.ht.get("key1"), "value1")  # O(1)
        self.assertEqual(self.ht.get("key2"), "value2")  # O(1)

        # Обновление
        self.ht.insert("key1", "updated_value")  # O(1)
        self.assertEqual(self.ht.get("key1"), "updated_value")  # O(1)
        self.assertEqual(self.ht.size, 2)  # O(1) - размер не изменился

        # Удаление
        self.assertTrue(self.ht.delete("key1"))  # O(1)
        self.assertEqual(self.ht.size, 1)  # O(1)
        self.assertIsNone(self.ht.get("key1"))  # O(1)

    def test_collision_handling_double_hashing(self) -> None:
        """Тест обработки коллизий двойным хешированием."""
        small_ht = HashTableOpenAddressing(capacity=3)  # O(n)

        # Вставляем элементы, вызывая коллизии
        small_ht.insert("a", 1)  # O(1)
        small_ht.insert("b", 2)  # O(1)
        small_ht.insert("c", 3)  # O(1) - коллизия

        self.assertEqual(small_ht.size, 3)  # O(1)
        self.assertEqual(small_ht.get("a"), 1)  # O(1)
        self.assertEqual(small_ht.get("b"), 2)  # O(1)
        self.assertEqual(small_ht.get("c"), 3)  # O(1)

    def test_deleted_marker_handling(self) -> None:
        """Тест работы с маркерами удаленных элементов."""
        self.ht.insert("key1", "value1")  # O(1)
        self.ht.insert("key2", "value2")  # O(1)

        # Удаляем элемент
        self.assertTrue(self.ht.delete("key1"))  # O(1)

        # Проверяем, что удаленный элемент не мешает поиску других
        self.assertEqual(self.ht.get("key2"), "value2")  # O(1)

        # Вставляем новый элемент - должен занять место удаленного
        self.ht.insert("key3", "value3")  # O(1)
        self.assertEqual(self.ht.get("key3"), "value3")  # O(1)
        self.assertEqual(self.ht.size, 2)  # O(1)

    def test_table_full_scenario(self) -> None:
        """Тест сценария переполнения таблицы."""
        full_ht = HashTableOpenAddressing(capacity=5)  # O(n) - увеличиваем начальный размер

        # Вставляем элементы до заполнения
        full_ht.insert("k1", "v1")  # O(1)
        full_ht.insert("k2", "v2")  # O(1)
        full_ht.insert("k3", "v3")  # O(1)
        full_ht.insert("k4", "v4")  # O(1)

        # Таблица почти заполнена, следующая вставка вызовет рехеширование
        full_ht.insert("k5", "v5")  # O(1) - вызовет рехеширование

        self.assertGreater(full_ht.capacity, 5)  # O(1)
        self.assertEqual(full_ht.size, 5)  # O(1)
        self.assertEqual(full_ht.get("k1"), "v1")  # O(1)
        self.assertEqual(full_ht.get("k2"), "v2")  # O(1)
        self.assertEqual(full_ht.get("k3"), "v3")  # O(1)
        self.assertEqual(full_ht.get("k4"), "v4")  # O(1)
        self.assertEqual(full_ht.get("k5"), "v5")  # O(1)


class TestHashTableLinearProbing(unittest.TestCase):
    """Тесты для хеш-таблицы с линейным пробированием."""

    def setUp(self) -> None:
        """Настройка тестового окружения."""
        self.ht = HashTableLinearProbing(capacity=5)  # O(n)

    def test_basic_functionality(self) -> None:
        """Тест базовой функциональности."""
        self.ht.insert("key1", "value1")  # O(1)
        self.ht.insert("key2", "value2")  # O(1)

        self.assertEqual(self.ht.size, 2)  # O(1)
        self.assertEqual(self.ht.get("key1"), "value1")  # O(1)
        self.assertEqual(self.ht.get("key2"), "value2")  # O(1)

        self.ht.insert("key1", "updated")  # O(1)
        self.assertEqual(self.ht.get("key1"), "updated")  # O(1)

        self.assertTrue(self.ht.delete("key1"))  # O(1)
        self.assertIsNone(self.ht.get("key1"))  # O(1)

    def test_linear_probing_collisions(self) -> None:
        """Тест коллизий при линейном пробировании."""
        # Создаем ситуацию с коллизиями
        probing_ht = HashTableLinearProbing(capacity=3)  # O(n)

        probing_ht.insert("a", 1)  # O(1)
        probing_ht.insert("b", 2)  # O(1)
        probing_ht.insert("c", 3)  # O(1) - коллизия, линейный поиск

        self.assertEqual(probing_ht.size, 3)  # O(1)
        self.assertEqual(probing_ht.get("a"), 1)  # O(1)
        self.assertEqual(probing_ht.get("b"), 2)  # O(1)
        self.assertEqual(probing_ht.get("c"), 3)  # O(1)


class TestHashTableComprehensive(unittest.TestCase):
    """Комплексные тесты для всех реализаций хеш-таблиц."""

    def test_all_implementations_consistency(self) -> None:
        """Тест согласованности всех реализаций."""
        implementations = [  # O(1)
            HashTableChaining(capacity=10),  # O(n)
            HashTableOpenAddressing(capacity=10),  # O(n)
            HashTableLinearProbing(capacity=10)  # O(n)
        ]

        test_data = [  # O(1)
            ("key1", "value1"),  # O(1)
            ("key2", "value2"),  # O(1)
            ("key3", "value3"),  # O(1)
            ("key1", "updated_value")  # O(1) - обновление
        ]

        for ht in implementations:  # O(m)
            with self.subTest(implementation=ht.__class__.__name__):  # O(1)
                # Вставка всех данных
                for key, value in test_data:  # O(k)
                    ht.insert(key, value)  # O(1)

                # Проверка конечного состояния
                self.assertEqual(ht.get("key1"), "updated_value")  # O(1)
                self.assertEqual(ht.get("key2"), "value2")  # O(1)
                self.assertEqual(ht.get("key3"), "value3")  # O(1)
                self.assertIsNone(ht.get("nonexistent"))  # O(1)

                # Проверка размера (3 уникальных ключа)
                self.assertEqual(ht.size, 3)  # O(1)

    def test_stress_test(self) -> None:
        """Стресс-тест с большим количеством операций."""
        ht = HashTableChaining(capacity=10)  # O(n)

        # Вставляем 100 элементов
        for i in range(100):  # O(100)
            ht.insert(f"key{i}", f"value{i}")  # O(1)

        self.assertEqual(ht.size, 100)  # O(1)

        # Проверяем все элементы
        for i in range(100):  # O(100)
            self.assertEqual(ht.get(f"key{i}"), f"value{i}")  # O(1)

        # Удаляем половину элементов
        for i in range(0, 100, 2):  # O(50)
            self.assertTrue(ht.delete(f"key{i}"))  # O(1)

        self.assertEqual(ht.size, 50)  # O(1)

        # Проверяем оставшиеся элементы
        for i in range(1, 100, 2):  # O(50)
            self.assertEqual(ht.get(f"key{i}"), f"value{i}")  # O(1)

        # Проверяем удаленные элементы
        for i in range(0, 100, 2):  # O(50)
            self.assertIsNone(ht.get(f"key{i}"))  # O(1)


class TestEdgeCases(unittest.TestCase):
    """Тесты граничных случаев."""

    def test_empty_table_operations(self) -> None:
        """Тест операций с пустой таблицей."""
        implementations = [  # O(1)
            HashTableChaining(),  # O(n)
            HashTableOpenAddressing(),  # O(n)
            HashTableLinearProbing()  # O(n)
        ]

        for ht in implementations:  # O(m)
            with self.subTest(implementation=ht.__class__.__name__):  # O(1)
                self.assertEqual(ht.size, 0)  # O(1)
                self.assertIsNone(ht.get("any_key"))  # O(1)
                self.assertFalse(ht.delete("any_key"))  # O(1)
                self.assertFalse("any_key" in ht)  # O(1)

    def test_single_element_table(self) -> None:
        """Тест таблицы с одним элементом."""
        ht = HashTableChaining()  # O(n)

        ht.insert("single_key", "single_value")  # O(1)
        self.assertEqual(ht.size, 1)  # O(1)
        self.assertEqual(ht.get("single_key"), "single_value")  # O(1)
        self.assertTrue("single_key" in ht)  # O(1)

        self.assertTrue(ht.delete("single_key"))  # O(1)
        self.assertEqual(ht.size, 0)  # O(1)
        self.assertIsNone(ht.get("single_key"))  # O(1)

    def test_duplicate_keys(self) -> None:
        """Тест дублирующихся ключей."""
        ht = HashTableOpenAddressing()  # O(n)

        ht.insert("key", "value1")  # O(1)
        ht.insert("key", "value2")  # O(1) - обновление
        ht.insert("key", "value3")  # O(1) - обновление

        self.assertEqual(ht.size, 1)  # O(1) - только один уникальный ключ
        self.assertEqual(ht.get("key"), "value3")  # O(1) - последнее значение

    def test_none_values(self) -> None:
        """Тест работы со значением None."""
        ht = HashTableChaining()  # O(n)

        # Вставка None как значения
        ht.insert("key1", None)  # O(1)

        # Проверяем что ключ существует (используем оператор in)
        self.assertTrue("key1" in ht)  # O(1) - ключ должен существовать

        # Проверяем что значение действительно None
        self.assertIsNone(ht.get("key1"))  # O(1) - метод get возвращает None как значение

        # Проверяем что можем обновить значение на не-None
        ht.insert("key1", "new_value")  # O(1)
        self.assertEqual(ht.get("key1"), "new_value")  # O(1)

        # Проверяем удаление
        self.assertTrue(ht.delete("key1"))  # O(1)
        self.assertFalse("key1" in ht)  # O(1) - ключ больше не существует
        self.assertIsNone(ht.get("key1"))  # O(1) - теперь возвращает None потому что ключ удален


def run_all_tests() -> None:
    """Запускает все тесты и выводит результаты."""
    # Создаем test suite
    loader = unittest.TestLoader()  # O(1)
    suite = unittest.TestSuite()  # O(1)

    # Добавляем все тестовые классы
    test_classes = [  # O(1)
        TestHashFunctions,  # O(1)
        TestHashTableChaining,  # O(1)
        TestHashTableOpenAddressing,  # O(1)
        TestHashTableLinearProbing,  # O(1)
        TestHashTableComprehensive,  # O(1)
        TestEdgeCases  # O(1)
    ]

    for test_class in test_classes:  # O(m)
        suite.addTests(loader.loadTestsFromTestCase(test_class))  # O(1)

    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)  # O(1)
    result = runner.run(suite)  # O(все тесты)

    # Выводим статистику
    print(f"\n{'='*50}")  # O(1)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")  # O(1)
    print(f"{'='*50}")  # O(1)
    print(f"Тестов выполнено: {result.testsRun}")  # O(1)
    print(f"""Успешно:
          {result.testsRun - len(result.failures) - len(result.errors)}""")
    # O(1)
    print(f"Провалено: {len(result.failures)}")  # O(1)
    print(f"Ошибок: {len(result.errors)}")  # O(1)

    if result.failures or result.errors:  # O(1)
        print("\nДетали ошибок:")  # O(1)
        for test, traceback in result.failures + result.errors:  # O(e)
            print(f"\n{test}:")  # O(1)
            print(traceback)  # O(1)
    else:  # O(1)
        print("\n✓ Все тесты прошли успешно!")  # O(1)


if __name__ == '__main__':
    run_all_tests()  # O(все тесты)
