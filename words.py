"""Модуль для работы со словами в боте

Содержит функции для:
- Получения пользовательских и общих слов
- Добавления и удаления слов
- Формирования полного списка слов для практики
"""

from database import get_connection


def get_user_words(user_id):
    """Получает список слов, добавленных пользователем

    Args:
        user_id (int): Telegram-ID пользователя

    Returns:
        list of tuple: Список кортежей (русское слово, английское)
                       Пустой список, если слов нет
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT word, translation FROM user_words WHERE user_id = %s", (user_id,)
        )
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def get_general_words():
    """Получает список общих слов из базы данных

    Returns:
        list of tuple: Список кортежей (word, translation) с общими словами
                       Возвращает пустой список, если слов нет
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT word, translation FROM general_words")
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def get_all_words(user_id):
    """Получает все слова для пользователя: его + общие

    Args:
        user_id (int): Telegram-ID пользователя

    Returns:
        list of tuple: полный список слов (пользовательские + общие)
    """
    user_words = get_user_words(user_id)
    general_words = get_general_words()
    return user_words + general_words


def delete_word(user_id, word):
    """Удаляет слово из пользовательского словаря

    Args:
        user_id (int): Telegram-ID пользователя
        word (str): русское слово, которое нужно удалить

    Примечания:
        Удаление происходит только если слово было добавлено пользователем
        Общие слова не удаляются
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM user_words WHERE user_id = %s AND word = %s",
            (user_id, word),
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()


def add_word(user_id, word, translation):
    """Добавляет новое слово в пользовательский словарь

    Args:
        user_id (int): TelegramID пользователя
        word (str): Русское слово
        translation (str): Перевод на английский

    Returns:
        bool: True — если слово успешно добавлено
              False — если слово уже существует у пользователя

    Примечание:
        Проверяется уникальность слова для данного пользователя
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT 1 FROM user_words WHERE user_id = %s AND word = %s",
            (user_id, word),
        )
        if cur.fetchone() is None:
            cur.execute(
                "INSERT INTO user_words (user_id, word, translation) "
                "VALUES (%s, %s, %s)",
                (user_id, word, translation),
            )
            conn.commit()
            return True
        else:
            return False
    finally:
        cur.close()
        conn.close()
