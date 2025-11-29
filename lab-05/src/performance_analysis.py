# performance_analysis.py
"""Анализ производительности хеш-таблиц с визуализацией."""

import timeit
import random
import string
import matplotlib.pyplot as plt
from typing import List, Dict, Any
from hash_table_chaining import HashTableChaining
from hash_table_open_addressing import (HashTableOpenAddressing,
                                        HashTableLinearProbing)
from hash_functions import simple_hash, polynomial_hash, djb2_hash


# Характеристики ПК для тестирования
PC_INFO = """
Характеристики ПК для тестирования:
- Процессор: Intel Core i7-13620H @ 2.40GHz
- Оперативная память: 32 GB DDR5
- ОС: Windows 11
- Python: 3.13.3
"""


def generate_test_data(num_items: int, key_length: int = 5) -> List[tuple[str,
                                                                          int]]:
    """Генерирует тестовые данные.

    Args:
        num_items: Количество тестовых элементов.
        key_length: Длина ключей.

    Returns:
        Список пар (ключ, значение).
    """
    data = []  # O(1)
    for i in range(num_items):  # O(n)
        key = ''.join(random.choices(string.ascii_letters, k=key_length))
        # O(k)
        data.append((key, i))  # O(1)
    return data  # O(1)


def measure_performance(hash_table_class: Any,
                        test_data: List[tuple[str, int]],
                        load_factors: List[float]) -> Dict[str, List[float]]:
    """Измеряет производительность хеш-таблицы.

    Args:
        hash_table_class: Класс хеш-таблицы для тестирования.
        test_data: Тестовые данные.
        load_factors: Коэффициенты заполнения для тестирования.

    Returns:
        Результаты измерений времени операций.
    """
    results = {'insert': [], 'search': [], 'delete': []}  # O(1)

    for load_factor in load_factors:  # O(l)
        # Определяем емкость для достижения нужного коэффициента заполнения
        target_size = int(len(test_data) * load_factor)  # O(1)
        test_subset = test_data[:target_size]  # O(n)

        # Для открытой адресации
        # используем большую начальную емкость чтобы избежать переполнения
        if hash_table_class.__name__ in ['HashTableOpenAddressing',
                                         'HashTableLinearProbing']:
            initial_capacity = max(50, int(target_size * 1.5))
            # O(1) - запас для открытой адресации
        else:
            initial_capacity = max(16, target_size)
            # O(1) - для метода цепочек

        ht = hash_table_class(capacity=initial_capacity)  # O(n)

        # Измеряем время вставки
        def insert_operations():  # O(1)
            for key, value in test_subset:  # O(k)
                ht.insert(key, value)  # O(1) в среднем

        try:
            insert_time = timeit.timeit(insert_operations, number=1)  # O(k)
            results['insert'].append(insert_time * 1000)
            # O(1) - в миллисекундах
        except MemoryError:
            print(f"""Предупреждение:
                  {hash_table_class.__name__} переполнена
                  при коэффициенте {load_factor}""")
            results['insert'].append(float('inf'))
            # O(1) - помечаем как бесконечное время

        # Измеряем время поиска (только если вставка прошла успешно)
        if results['insert'][-1] != float('inf'):
            def search_operations():  # O(1)
                for key, _ in test_subset:  # O(k)
                    ht.get(key)  # O(1) в среднем

            search_time = timeit.timeit(search_operations, number=1)  # O(k)
            results['search'].append(search_time * 1000)  # O(1)

            # Измеряем время удаления
            def delete_operations():  # O(1)
                for key, _ in test_subset:  # O(k)
                    ht.delete(key)  # O(1) в среднем

            delete_time = timeit.timeit(delete_operations, number=1)  # O(k)
            results['delete'].append(delete_time * 1000)  # O(1)
        else:
            results['search'].append(float('inf'))  # O(1)
            results['delete'].append(float('inf'))  # O(1)

    return results  # O(1)


def plot_operation_time_vs_load_factor(results: Dict[str, Dict[str,
                                                               List[float]]],
                                       load_factors: List[float]) -> None:
    """Строит графики зависимости времени операций от коэффициента заполнения.

    Args:
        results: Результаты измерений для всех реализаций.
        load_factors: Коэффициенты заполнения.
    """
    operations = ['insert', 'search', 'delete']  # O(1)
    colors = ['red', 'blue', 'green']  # O(1)
    markers = ['o', 's', '^']  # O(1)
    linestyles = ['-', '--', '-.']  # O(1)

    for operation in operations:  # O(m)
        plt.figure(figsize=(10, 6))  # O(1)

        for i, (impl_name, impl_results) in enumerate(results.items()):  # O(k)
            times = impl_results[operation]  # O(1)
            # Фильтруем бесконечные значения для построения графика
            valid_load_factors = []  # O(1)
            valid_times = []  # O(1)

            for j, time_val in enumerate(times):  # O(l)
                if time_val != float('inf'):  # O(1)
                    valid_load_factors.append(load_factors[j])  # O(1)
                    valid_times.append(time_val)  # O(1)

            if valid_times:  # O(1)
                plt.plot(valid_load_factors, valid_times,  # O(l)
                         marker=markers[i],  # O(1)
                         color=colors[i],  # O(1)
                         linestyle=linestyles[i],  # O(1)
                         label=impl_name,  # O(1)
                         linewidth=2,  # O(1)
                         markersize=8)  # O(1)

        plt.xlabel('Коэффициент заполнения', fontsize=12)  # O(1)
        plt.ylabel('Время выполнения (мс)', fontsize=12)  # O(1)
        plt.title(f'''Зависимость времени {operation}
                  от коэффициента заполнения''',
                  # O(1)
                  fontsize=14, fontweight='bold')  # O(1)
        plt.grid(True, alpha=0.3, linestyle='--')  # O(1)
        plt.legend(fontsize=10)  # O(1)

        # Сохраняем график
        filename = f'time_vs_load_factor_{operation}.png'  # O(1)
        plt.savefig(filename, dpi=300, bbox_inches='tight')  # O(1)
        print(f'Сохранен график: {filename}')  # O(1)
        plt.close()  # O(1) - закрываем без показа


def plot_collision_histograms() -> None:
    """Строит гистограммы распределения коллизий для разных хеш-функций."""
    print('Анализ коллизий для разных хеш-функций...')  # O(1)

    hash_functions = [  # O(1)
        ('Simple Hash', simple_hash),  # O(1)
        ('Polynomial Hash', polynomial_hash),  # O(1)
        ('DJB2 Hash', djb2_hash)  # O(1)
    ]

    table_size = 100  # O(1)
    num_keys = 1000  # O(1)
    test_keys = [''.join(random.choices(string.ascii_letters, k=5))
                 # O(1000*5)
                 for _ in range(num_keys)]  # O(1000)

    # Создаем subplot для гистограмм
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))  # O(1)
    fig.suptitle('Распределение коллизий для разных хеш-функций',  # O(1)
                 fontsize=16, fontweight='bold')  # O(1)

    for idx, (name, hash_func) in enumerate(hash_functions):  # O(m)
        distribution = {}  # O(1)

        for key in test_keys:  # O(k)
            hash_val = hash_func(key, table_size)  # O(n)
            if hash_val in distribution:  # O(1)
                distribution[hash_val] += 1  # O(1)
            else:  # O(1)
                distribution[hash_val] = 1  # O(1)

        # Статистика
        chain_lengths = list(distribution.values())  # O(u)
        collisions_count = sum(1 for length in chain_lengths if length > 1)
        # O(u)
        max_chain = max(chain_lengths) if chain_lengths else 0  # O(u)

        # Строим гистограмму для текущей хеш-функции
        axes[idx].hist(chain_lengths, bins=range(1, max_chain + 2),  # O(u)
                       alpha=0.7,  # O(1)
                       color=['red', 'blue', 'green'][idx],  # O(1)
                       edgecolor='black')  # O(1)

        axes[idx].set_title(f'{name}\n'  # O(1)
                            f'Коллизий: {collisions_count}\n'  # O(1)
                            f'Макс. цепочка: {max_chain}',  # O(1)
                            fontsize=12)  # O(1)
        axes[idx].set_xlabel('Длина цепочки', fontsize=10)  # O(1)
        axes[idx].set_ylabel('Частота', fontsize=10)  # O(1)
        axes[idx].grid(True, alpha=0.3)  # O(1)

    plt.tight_layout()  # O(1)
    plt.savefig('cols.png', dpi=300, bbox_inches='tight')  # O(1)
    print('Сохранен график: cols.png')  # O(1)
    plt.close()  # O(1) - закрываем без показа


def analyze_collisions_comparison() -> None:
    """Строит сравнительную диаграмму коллизий для разных хеш-функций."""
    hash_functions = [  # O(1)
        ('Simple Hash', simple_hash),  # O(1)
        ('Polynomial Hash', polynomial_hash),  # O(1)
        ('DJB2 Hash', djb2_hash)  # O(1)
    ]

    table_size = 100  # O(1)
    num_keys = 1000  # O(1)
    test_keys = [''.join(random.choices(string.ascii_letters, k=5))
                 # O(1000*5)
                 for _ in range(num_keys)]  # O(1000)

    collisions_data = []  # O(1)
    names = []  # O(1)

    for name, hash_func in hash_functions:  # O(m)
        distribution = {}  # O(1)

        for key in test_keys:  # O(k)
            hash_val = hash_func(key, table_size)  # O(n)
            if hash_val in distribution:  # O(1)
                distribution[hash_val] += 1  # O(1)
            else:  # O(1)
                distribution[hash_val] = 1  # O(1)

        # Подсчитываем коллизии (цепи длиной > 1)
        collisions = sum(1 for length in distribution.values() if length > 1)
        # O(u)
        collisions_data.append(collisions)  # O(1)
        names.append(name)  # O(1)

    # Строим столбчатую диаграмму
    plt.figure(figsize=(10, 6))  # O(1)
    bars = plt.bar(names, collisions_data,  # O(m)
                   color=['lightcoral', 'lightblue', 'lightgreen'],  # O(m)
                   edgecolor='black',  # O(1)
                   alpha=0.7)  # O(1)

    plt.title('Сравнение количества коллизий для разных хеш-функций',  # O(1)
              fontsize=14, fontweight='bold')  # O(1)
    plt.ylabel('Количество коллизий', fontsize=12)  # O(1)
    plt.grid(True, alpha=0.3, axis='y')  # O(1)

    # Добавляем значения на столбцы
    for bar in bars:  # O(m)
        height = bar.get_height()  # O(1)
        plt.text(bar.get_x() + bar.get_width() / 2., height + 5,  # O(1)
                 f'{int(height)}',  # O(1)
                 ha='center', va='bottom', fontsize=11, fontweight='bold')
        # O(1)

    plt.savefig('collisions_comparison.png', dpi=300, bbox_inches='tight')
    # O(1)
    print('Сохранен график: collisions_comparison.png')  # O(1)
    plt.close()  # O(1) - закрываем без показа


def print_performance_table(results: Dict[str, Dict[str, List[float]]],
                            load_factors: List[float]) -> None:
    """Выводит таблицу с результатами производительности.

    Args:
        results: Результаты измерений.
        load_factors: Коэффициенты заполнения.
    """
    print('\nТАБЛИЦА ПРОИЗВОДИТЕЛЬНОСТИ (время в мс):')
    print('=' * 80)

    for operation in ['insert', 'search', 'delete']:  # O(m)
        print(f'\n{operation.upper():^80}')
        print('-' * 80)
        print('Метод           ', end='')
        for lf in load_factors:  # O(l)
            print(f' | {lf:>5} ', end='')
        print()
        print('-' * 80)

        for impl_name, impl_results in results.items():  # O(k)
            print(f'{impl_name:15}', end='')
            for time_val in impl_results[operation]:  # O(l)
                if time_val == float('inf'):
                    print(f' | {"N/A":>5} ', end='')
                else:
                    print(f' | {time_val:5.1f} ', end='')
            print()


def main() -> None:
    """Основная функция для анализа производительности и визуализации."""
    print(PC_INFO)  # O(1)

    print("=" * 60)  # O(1)
    print("АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ ХЕШ-ТАБЛИЦ")  # O(1)
    print("=" * 60)  # O(1)

    # Уменьшаем объем тестовых данных для избежания переполнения
    print('\nГенерация тестовых данных...')  # O(1)
    test_data = generate_test_data(2000)  # O(2000) - уменьшили с 5000 до 2000
    load_factors = [0.1, 0.3, 0.5, 0.7]
    # O(1) - убрали 0.9 для открытой адресации

    # Тестируемые реализации
    implementations = [  # O(1)
        ('Chaining', HashTableChaining),  # O(1)
        ('Linear Probing', HashTableLinearProbing),  # O(1)
        ('Double Hashing', HashTableOpenAddressing)  # O(1)
    ]

    # Измерение производительности
    print('\nИзмерение производительности...')  # O(1)
    all_results = {}  # O(1)

    for name, impl_class in implementations:  # O(m)
        print(f'  Тестирование {name}...')  # O(1)
        results = measure_performance(impl_class, test_data, load_factors)
        # O(l*k)
        all_results[name] = results  # O(1)

    # Выводим таблицу результатов
    print_performance_table(all_results, load_factors)  # O(m*l)

    # 1. Графики зависимости времени операций от коэффициента заполнения
    print('\n1. Построение графиков зависимости времени от коэффициента заполнения...')  # O(1)
    plot_operation_time_vs_load_factor(all_results, load_factors)  # O(m*l)

    # 2. Гистограммы распределения коллизий
    print('\n2. Построение гистограмм распределения коллизий...')  # O(1)
    plot_collision_histograms()  # O(m*k*n)

    # 3. Сравнительная диаграмма коллизий
    print('\n3. Построение сравнительной диаграммы коллизий...')  # O(1)
    analyze_collisions_comparison()  # O(m*k*n)

    print('\n' + '=' * 60)  # O(1)
    print('ВИЗУАЛИЗАЦИЯ ЗАВЕРШЕНА!')  # O(1)
    print('Созданы файлы:')  # O(1)
    print('  - ins_oper.png')  # O(1)
    print('  - s_oper.png')  # O(1)
    print('  - del_oper.png')  # O(1)
    print('  - cols.png')  # O(1)
    print('  - collisions_comparison.png')  # O(1)
    print('=' * 60)  # O(1)


if __name__ == '__main__':
    # Используем неинтерактивный бэкенд для избежания проблем с PyCharm
    plt.switch_backend('Agg')  # O(1) - устанавливаем неинтерактивный бэкенд
    main()  # O(все операции)
