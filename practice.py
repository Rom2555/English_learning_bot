"""Модуль для работы с режимом практики

Содержит функции:
- Случайного выбора слова для тренировки
- Генерации вариантов ответов (включая неверные)
- Сохранения результатов ответов пользователя
"""

import random
from words import get_all_words, get_general_words
from database import get_connection


def get_practice_data(user_id):
    """Генерирует данные для одного сеанса практики

    Выбирает случайное слово из словаря пользователя и общих слов,
    создаёт 4 варианта ответа (1 правильный, 3 неправильных)

    Args:
        user_id (int): Telegram-ID пользователя

    Returns:
        tuple: (russian, correct, choices), где:
            russian (str): слово на русском,
            correct (str): правильный перевод,
            choices (list of str): перемешанные варианты ответов
    Примечание:
        Если слов нет, возвращает (None, None, None)
    """
    words = get_all_words(user_id)
    if not words:
        return None, None, None

    russian, correct = random.choice(words)
    # Получаем все возможные переводы из слов пользователя (уже включают общие слова)
    # дублирование убрано!
    all_translations = [trans for _, trans in words]


    # Убираем правильный перевод из общего списка, чтобы не было дубликатов при выборе
    wrong_choices = set([trans for trans in all_translations if trans != correct])

    # Выбираем 3 уникальных неправильных варианта
    choices = random.sample(list(wrong_choices), 3)
    choices.append(correct)
    random.shuffle(choices)

    return russian, correct, choices


def save_result(user_id, word, correct):
    """Сохраняет результат одного ответа пользователя

    Args:
        user_id (int): Telegram-ID пользователя
        word (str): Слово, по которому был дан ответ (на русском)
        correct (bool): True - если ответ правильный, False - если нет

    Примечание:
        Данные сохраняются в таблицу `results` с отметкой даты-времени(для статистики)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO results (user_id, word, correct) VALUES (%s, %s, %s)",
        (user_id, word, correct)
    )
    conn.commit()
    cur.close()
    conn.close()
