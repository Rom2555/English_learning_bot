"""В телеграмме FirstBot"""

import telebot
from dotenv import load_dotenv
import os

# Загружаем переменные из .env
load_dotenv()

token = os.getenv("TOKEN")
name = 'Роман'
bot = telebot.TeleBot(token)


@bot.message_handler(content_types=["text"])
def echo(message):
    if name in message.text:
        bot.send_message(message.chat.id, 'Привет Роман!')
    else:
        bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    print('Бот запущен...')
    bot.polling(none_stop=True)