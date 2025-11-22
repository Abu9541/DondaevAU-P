# task_solutions.py
"""
Модуль с решениями практических задач.
"""


from collections import deque
from typing import List

from linked_list import LinkedList
from performance_analysis import run_performance_analysis


def check_brackets_balance(expression: str) -> bool:
    """
    Проверяет сбалансированность скобок в выражении.

    Args:
        expression: Строка с выражением

    Returns:
        True если скобки сбалансированы, иначе False
    """
    stack = []  # O(1) - создание стека
    brackets = {')': '(', ']': '[', '}': '{'}  # O(1) - создание словаря

    for char in expression:  # O(n) - цикл по символам строки
        if char in '([{':  # O(1) - проверка принадлежности
            stack.append(char)  # O(1) - добавление в стек
        elif char in brackets:  # O(1) - проверка принадлежности
            if not stack or stack[-1] != brackets[char]:  # O(1) - проверки
                return False  # O(1) - возврат значения
            stack.pop()  # O(1) - удаление из стека

    return len(stack) == 0  # O(1) - проверка условия
    # Общая сложность: O(n)


def simulate_print_queue(tasks: List[str]) -> List[str]:
    """
    Симулирует обработку задач в очереди печати.

    Args:
        tasks: Список задач

    Returns:
        Список обработанных задач в порядке обработки
    """
    queue = deque(tasks)  # O(n) - создание дека из списка
    processed = []  # O(1) - создание списка

    while queue:  # O(n) - цикл пока очередь не пуста
        task = queue.popleft()  # O(1) - извлечение из начала
        processed.append(task)  # O(1) - добавление в список

    return processed  # O(1) - возврат значения
    # Общая сложность: O(n)


def is_palindrome(sequence: str) -> bool:
    """
    Проверяет, является ли последовательность палиндромом.

    Args:
        sequence: Проверяемая последовательность

    Returns:
        True если палиндром, иначе False
    """
    dq = deque(sequence.lower())  # O(n) - создание дека из строки

    while len(dq) > 1:  # O(n) - цикл пока больше 1 элемента
        if dq.popleft() != dq.pop():  # O(1) - сравнение и удаление
            return False  # O(1) - возврат значения

    return True  # O(1) - возврат значения
    # Общая сложность: O(n)


def test_practical_tasks() -> None:
    """
    Тестирует решения практических задач.
    """
    print('Тестирование практических задач:')

    # Тест проверки скобок
    test_cases = [
        ('((()))', True),
        ('([{}])', True),
        ('((())', False),
        ('([)]', False),
        ('', True)
    ]

    print('1. Проверка сбалансированности скобок:')
    for expr, expected in test_cases:
        result = check_brackets_balance(expr)
        status = '✓' if result == expected else '✗'
        print(f'   {status} "{expr}" -> {result} (ожидалось: {expected})')

    # Тест симуляции очереди печати
    tasks = ['task1', 'task2', 'task3', 'task4']
    processed = simulate_print_queue(tasks)
    print('2. Симуляция очереди печати:')
    print(f'   Входные задачи: {tasks}')
    print(f'   Обработанные: {processed}')

    # Тест проверки палиндромов
    palindromes = [
        'racecar',
        'A man a plan a canal Panama',
        'level',
        'hello'
    ]

    print('3. Проверка палиндромов:')
    for text in palindromes:
        # Убираем пробелы и приводим к нижнему регистру для корректной проверки
        clean_text = ''.join(text.lower().split())
        result = is_palindrome(clean_text)
        print(f'   "{text}" -> {result}')


def analyze_results() -> None:
    """
    Анализирует и выводит результаты экспериментов.
    """
    print('\nАнализ результатов:')
    print('1. Теоретическая сложность операций:')
    print('- List.insert(0): O(n) - линейная сложность')
    print('- LinkedList.insert_at_start(): O(1) - постоянная сложность')
    print('- List.pop(0): O(n) - линейная сложность')
    print('- Deque.popleft(): O(1) - постоянная сложность')

    print('2. Практические наблюдения:')
    print('''- List:
          демонстрирует квадратичный рост времени при вставке в начало''')
    print('- LinkedList показывает линейный рост времени')
    print('- Deque значительно эффективнее List для операций очереди')
    print('- Теоретические оценки подтверждены экспериментально')

    print('3. Выводы:')
    print('''- Для частых операций в начале структуры:
          лучше использовать LinkedList''')
    print('- Для реализации очереди оптимально использовать deque')
    print('- List эффективен для операций в конце и доступа по индексу')


# Тестирование связного списка
print('Тестирование связного списка:')
ll = LinkedList()

# Вставка в начало
for i in range(5):
    ll.insert_at_start(i)
print(f'Список после вставки в начало: {ll.traversal()}')

# Вставка в конец
for i in range(5, 10):
    ll.insert_at_end(i)
print(f'Список после вставки в конец: {ll.traversal()}')

# Удаление из начала
removed = ll.delete_from_start()
print(f'Удаленный элемент: {removed}')
print(f'Список после удаления: {ll.traversal()}')

print()

# Тестирование практических задач
test_practical_tasks()

print()

# Запуск анализа производительности
run_performance_analysis()

# Анализ результатов
analyze_results()
