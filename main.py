"""English Learning Bot (NetologyFirst)"""

import telebot
import os
from dotenv import load_dotenv
from database import init_db
from handlers import setup_handlers

# Загружаем .env
load_dotenv()

# Получаем токен из .env
TOKEN = os.getenv("TOKEN")

if __name__ == '__main__':
    try:
        bot = telebot.TeleBot(TOKEN)
        init_db()
        setup_handlers(bot)
        print("Бот запущен")
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")