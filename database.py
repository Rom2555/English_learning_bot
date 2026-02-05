"""
Модуль для работы с SQLite-базой данных бота
Создаёт таблицы, управляет подключением и загружает начальные данные
"""

import json
import os
import sqlite3

# Путь к файлу базы данных
DB_PATH = os.path.join(os.path.dirname(__file__), "english_bot.db")


def get_connection():
    """Создаёт и возвращает соединение с SQLite базой данных"""
    return sqlite3.connect(DB_PATH)


def init_db():
    """Инициализирует структуру базы данных

    Создаёт три таблицы, если они ещё не существуют:
    - general_words: общие слова из JSON-файла
    - user_words: слова, добавленные пользователем
    - results: результаты практики пользователей

    Также загружает начальные данные из файла `general_words.json`,
    игнорируя дубликаты

    Raises:
        Exception: При ошибках выполнения SQL или чтения файла
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Таблица: общие слова
        cur.execute("""
            CREATE TABLE IF NOT EXISTS general_words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL UNIQUE,
                translation TEXT NOT NULL
            );
        """)

        # Таблица: пользовательские слова
        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                word TEXT NOT NULL,
                translation TEXT NOT NULL,
                UNIQUE(user_id, word)
            );
        """)

        # Таблица: результаты
        cur.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                word TEXT NOT NULL,
                correct INTEGER NOT NULL,
                date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Загружаем общие слова из JSON
        try:
            json_path = os.path.join(os.path.dirname(__file__), "general_words.json")
            with open(json_path, "r", encoding="utf-8") as f:
                words_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка загрузки general_words.json: {e}")
            words_data = []

        # Заполнение с игнорированием дубликатов
        for item in words_data:
            word = item.get("word")
            translation = item.get("translation")
            if word and translation:
                cur.execute(
                    "INSERT OR IGNORE INTO general_words (word, translation) VALUES (?, ?)",
                    (word, translation),
                )

        conn.commit()
        print("База данных ОК (SQLite)")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Ошибка при инициализации БД: {e}")
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
