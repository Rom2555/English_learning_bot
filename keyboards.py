from telebot import types

def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("добавить слово 💬", "удалить слово 🗑️", "Дальше ⏭")
    return markup