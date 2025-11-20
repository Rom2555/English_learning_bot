"""English Learning Bot (NetologyFirst)"""

import telebot
from config import TOKEN
from database import init_db

if __name__ == '__main__':
    try:
        bot = telebot.TeleBot(TOKEN)
        init_db()
        print("Бот запущен")
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")