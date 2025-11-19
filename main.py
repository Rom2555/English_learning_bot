"""NetologyFirst"""

import telebot
from dotenv import load_dotenv
import os
from telebot import types

# Загружаем переменные из .env
load_dotenv()

token = os.getenv("TOKEN")
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    item1 = types.KeyboardButton("добавить слово 💬")
    item2 = types.KeyboardButton("удалить слово 🗑️")
    item3 = types.KeyboardButton("Дальше ⏭")

    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, 'Привет 🌟 Давай попрактикуемся в английском языке! '
                                      'Ты можешь тренироваться в удобном для себя темпе 🚀. '
                                      'Используй тренажёр как конструктор — '
                                      'создавай свою собственную базу слов 🧩! '
                                      'Для этого используй инструменты: '
                                      'добавить слово 💬, '
                                      'удалить слово 🗑️. '
                                      'Готов? Тогда вперёд — начнём прямо сейчас! 💪🔥',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text == "добавить слово 💬":
        bot.send_message(message.chat.id, "Была нажата кнопка_1")
    elif message.text == "удалить слово 🗑️":
        bot.send_message(message.chat.id, "Была нажата кнопка_2")
    elif message.text == "Дальше ⏭":
        bot.send_message(message.chat.id, "Была нажата кнопка_3")


if __name__ == '__main__':
    print('Бот запущен...')
    bot.polling(none_stop=True)
