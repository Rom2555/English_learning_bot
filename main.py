"""
Главный файл запуска бота. Содержит инициализацию бота, загрузку токена,
настройку обработчиков и запуск polling-режима
"""
# в ТГ - English_Learning_Bot
import telebot
import os
from dotenv import load_dotenv
from database import init_db
from handlers import setup_handlers


def main():
    """Основная функция запуска бота

    Действия:
    - Загружает переменные окружения из .env
    - Инициализирует базу данных
    - Настраивает обработчики сообщений
    - Запускает бота в режиме long polling

    Обрабатывает исключения, связанные с запуском бота
    """
    load_dotenv()

    token = os.getenv("TOKEN")
    if not token:
        print("Ошибка: TOKEN не найден в .env файле")
        return

    try:
        bot = telebot.TeleBot(token)
        init_db()
        setup_handlers(bot)
        print("Бот запущен")
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")


if __name__ == '__main__':
    main()
