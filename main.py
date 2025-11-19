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
    item1 = types.KeyboardButton("Кнопка_1")
    item2 = types.KeyboardButton("Кнопка_2")
    item3 = types.KeyboardButton("Кнопка_3")

    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, 'Привет! Нажми на любую кнопку', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text == "Кнопка_1":
        bot.send_message(message.chat.id, "Была нажата кнопка_1")
    elif message.text == "Кнопка_2":
        bot.send_message(message.chat.id, "Была нажата кнопка_2")
    elif message.text == "Кнопка_3":
        bot.send_message(message.chat.id, "Была нажата кнопка_3")


if __name__ == '__main__':
    print('Бот запущен...')
    bot.polling(none_stop=True)