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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Кнопка")
    markup.add(item1)
    bot.send_message(message.chat.id, 'Привет! Нажми на кнопку', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text == "Кнопка":
        bot.send_message(message.chat.id, "Была нажата кнопка")


if __name__ == '__main__':
    print('Бот запущен...')
    bot.polling(none_stop=True)
