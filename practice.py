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

    # Убираем правильный перевод, чтобы не было его в списке неправильных
    wrong_translations = [trans for trans in all_translations if trans != correct]

    # Добавим переводы из общих слов, которых нет в all_translations, чтобы избежать дублей
    general_translations = [trans for _, trans in get_general_words() if trans not in all_translations]
    all_wrong = wrong_translations + general_translations

    # Убираем дубликаты и перемешиваем
    unique_wrong = list(set(all_wrong))

    # Выбираем 3 неправильных варианта
    if len(unique_wrong) < 3:
        # Если не хватает слов, дублируем. (лучше, чем ошибка)
        choices = random.choices(unique_wrong, k=3) if unique_wrong else ["cat", "dog", "bird"]
    else:
        choices = random.sample(unique_wrong, 3)

    # Добавляем правильный ответ и перемешиваем
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
