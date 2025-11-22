# performance_analysis.py
"""
Модуль для анализа производительности структур данных.
"""


import timeit
from collections import deque
from typing import List

import matplotlib.pyplot as plt
from linked_list import LinkedList


def measure_list_insert_start(n: int) -> float:
    """
    Измеряет время вставки n элементов в начало списка.

    Args:
        n: Количество элементов для вставки

    Returns:
        Время выполнения в миллисекундах
    """
    def operation():  # O(1) - обертка для замера
        lst = []  # O(1) - создание списка
        for i in range(n):  # O(n) - цикл по n элементам
            lst.insert(0, i)  # O(n) - вставка в начало
        return lst  # O(1) - возврат значения

    execution_time = timeit.timeit(operation, number=10)  # O(10 * n^2)
    return (execution_time / 10) * 1000  # O(1) - конвертация в мс


def measure_linked_list_insert_start(n: int) -> float:
    """
    Измеряет время вставки n элементов в начало связного списка.

    Args:
        n: Количество элементов для вставки

    Returns:
        Время выполнения в миллисекундах
    """
    def operation():  # O(1) - обертка для замера
        ll = LinkedList()  # O(1) - создание списка
        for i in range(n):  # O(n) - цикл по n элементам
            ll.insert_at_start(i)  # O(1) - вставка в начало
        return ll  # O(1) - возврат значения

    execution_time = timeit.timeit(operation, number=10)  # O(10 * n)
    return (execution_time / 10) * 1000  # O(1) - конвертация в мс


def measure_list_queue_dequeue(n: int) -> float:
    """
    Измеряет время выполнения n операций удаления из начала списка.

    Args:
        n: Количество операций

    Returns:
        Время выполнения в миллисекундах
    """
    def operation():  # O(1) - обертка для замера
        lst = list(range(n))  # O(n) - создание списка
        for _ in range(n):  # O(n) - цикл по n элементам
            if lst:  # O(1) - проверка условия
                lst.pop(0)  # O(n) - удаление из начала
        return lst  # O(1) - возврат значения

    execution_time = timeit.timeit(operation, number=10)  # O(10 * n^2)
    return (execution_time / 10) * 1000  # O(1) - конвертация в мс


def measure_deque_queue_dequeue(n: int) -> float:
    """
    Измеряет время выполнения n операций удаления из начала дека.

    Args:
        n: Количество операций

    Returns:
        Время выполнения в миллисекундах
    """
    def operation():  # O(1) - обертка для замера
        dq = deque(range(n))  # O(n) - создание дека
        for _ in range(n):  # O(n) - цикл по n элементам
            if dq:  # O(1) - проверка условия
                dq.popleft()  # O(1) - удаление из начала
        return dq  # O(1) - возврат значения

    execution_time = timeit.timeit(operation, number=10)  # O(10 * n)
    return (execution_time / 10) * 1000  # O(1) - конвертация в мс


def run_performance_analysis() -> None:
    """
    Проводит сравнительный анализ производительности структур данных.
    """
    # Характеристики ПК для тестирования
    pc_info: str = """
    Характеристики ПК для тестирования:
    - Процессор: Intel Core i7-13620H @ 2.40GHz
    - Оперативная память: 32 GB DDR5
    - ОС: Windows 11
    - Python: 3.13.3
    """
    print(pc_info)

    # Размеры данных для тестирования
    sizes: List[int] = [100, 500, 1000, 2000, 5000]

    # Результаты измерений
    list_insert_times: List[float] = []
    linked_list_insert_times: List[float] = []
    list_dequeue_times: List[float] = []
    deque_dequeue_times: List[float] = []

    print('Сравнение производительности вставки в начало:')
    print('{:>10} {:>15} {:>20}'.format(
        'Размер (N)', 'List (мс)', 'LinkedList (мс)'))

    for size in sizes:  # O(k) - цикл по количеству размеров
        list_time = measure_list_insert_start(size)  # O(n^2)
        linked_list_time = measure_linked_list_insert_start(size)  # O(n)

        list_insert_times.append(list_time)  # O(1)
        linked_list_insert_times.append(linked_list_time)  # O(1)

        print('{:>10} {:>15.4f} {:>20.4f}'.format(
            size, list_time, linked_list_time))

    print('\nСравнение производительности операций очереди:')
    print('{:>10} {:>15} {:>20}'.format(
        'Размер (N)', 'List (мс)', 'Deque (мс)'))

    for size in sizes:  # O(k) - цикл по количеству размеров
        list_time = measure_list_queue_dequeue(size)  # O(n^2)
        deque_time = measure_deque_queue_dequeue(size)  # O(n)

        list_dequeue_times.append(list_time)  # O(1)
        deque_dequeue_times.append(deque_time)  # O(1)

        print('{:>10} {:>15.4f} {:>20.4f}'.format(
            size, list_time, deque_time))

    # Построение графиков
    plot_performance_results(sizes, list_insert_times,
                             linked_list_insert_times,
                             list_dequeue_times, deque_dequeue_times)


def plot_performance_results(sizes: List[int],
                             list_insert_times: List[float],
                             linked_list_insert_times: List[float],
                             list_dequeue_times: List[float],
                             deque_dequeue_times: List[float]) -> None:
    """
    Строит графики результатов анализа производительности.

    Args:
        sizes: Размеры данных
        list_insert_times: Время вставки в список
        linked_list_insert_times: Время вставки в связный список
        list_dequeue_times: Время удаления из списка
        deque_dequeue_times: Время удаления из дека
    """
    plt.figure(figsize=(12, 10))

    # График сравнения вставки в начало
    plt.subplot(2, 1, 1)
    plt.plot(sizes, list_insert_times, 'ro-',
             label='List.insert(0) - O(n)', linewidth=2)
    plt.plot(sizes, linked_list_insert_times, 'bo-',
             label='LinkedList.insert_at_start() - O(1)', linewidth=2)
    plt.xlabel('Количество элементов (N)')
    plt.ylabel('Время выполнения (мс)')
    plt.title('Сравнение вставки в начало: List vs LinkedList')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    # График сравнения операций очереди
    plt.subplot(2, 1, 2)
    plt.plot(sizes, list_dequeue_times, 'ro-',
             label='List.pop(0) - O(n)', linewidth=2)
    plt.plot(sizes, deque_dequeue_times, 'go-',
             label='Deque.popleft() - O(1)', linewidth=2)
    plt.xlabel('Количество элементов (N)')
    plt.ylabel('Время выполнения (мс)')
    plt.title('Сравнение операций очереди: List vs Deque')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    plt.tight_layout()
    plt.savefig('img_1.png', dpi=300, bbox_inches='tight')
    plt.show()
