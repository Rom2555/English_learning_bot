from telebot import types

def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("Добавить слово", "Удалить слово", "Практика")
    return markup

def get_words_keyboard(words):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[types.KeyboardButton(word) for word, _ in words])
    markup.add("Отмена")
    return markup

def get_practice_keyboard(choices):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[types.KeyboardButton(ans) for ans in choices])
    markup.add("Меню")
    return markup