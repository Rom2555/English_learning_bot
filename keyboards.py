"""Модуль клавиатур для Telegram-бота

Содержит функции для создания клавиатур,
используемых в интерфейсе бота для изучения английских слов
"""

from telebot import types


def get_main_menu():
    """Создаёт главное меню с основными функциями бота

    Кнопки:
        - Добавить слово
        - Удалить слово
        - Практика

    Returns:
        types.ReplyKeyboardMarkup: Клавиатура с основными командами
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("Добавить слово", "Удалить слово", "Практика")
    return markup


def get_practice_keyboard(choices):
    """Создаёт клавиатуру с вариантами перевода для режима практики

    Args:
        choices (list): Список слов на английском (варианты ответа)

    Returns:
        types.ReplyKeyboardMarkup: Клавиатура с вариантами ответов и кнопкой "Меню'
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[types.KeyboardButton(ans) for ans in choices])
    markup.add("Меню")
    return markup


def get_cancel_keyboard():
    """Создаёт клавиатуру с кнопкой отмены действия

    Returns:
        types.ReplyKeyboardMarkup: Клавиатура с кнопкой "Отмена"
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Отмена")
    return markup
