"""База данных english_bot_db2

Модуль для работы с PostgreSQL-базой данных бота
Создаёт таблицы, управляет подключением и загружает начальные данные
"""

import psycopg2
import json
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Конфигурация БД
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = int(os.getenv("DB_PORT", 5432))


def get_connection():
    """Создаёт и возвращает соединение с PostgreSQL базой данных"""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )


def init_db():
    """Инициализирует структуру базы данных

    Создаёт три таблицы, если они ещё не существуют:
    - general_words: общие слова из JSON-файла
    - user_words: слова, добавленные пользоваателем
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
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS general_words
                    (
                        id          SERIAL PRIMARY KEY,
                        word        TEXT NOT NULL,
                        translation TEXT NOT NULL,
                        UNIQUE (word)
                    );
                    ''')

        # Таблица: пользовательские слова
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS user_words
                    (
                        id          SERIAL PRIMARY KEY,
                        user_id     BIGINT NOT NULL,
                        word        TEXT   NOT NULL,
                        translation TEXT   NOT NULL,
                        UNIQUE (user_id, word)
                    );
                    ''')

        # Таблица: результаты
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS results
                    (
                        id        SERIAL PRIMARY KEY,
                        user_id   BIGINT  NOT NULL,
                        word      TEXT    NOT NULL,
                        correct   BOOLEAN NOT NULL,
                        date_time TIMESTAMP DEFAULT NOW()
                    );
                    ''')

        # Загружаем общие слова из JSON
        try:
            with open('general_words.json', 'r', encoding='utf-8') as f:
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
                    "INSERT INTO general_words (word, translation) VALUES (%s, %s) ON CONFLICT (word) DO NOTHING",
                    (word, translation)
                )

        conn.commit()
        print("База данных ОК")

    except Exception as e:
        if conn:
            conn.rollback()  # Откат транзакции, всё обнуляется
        print(f"Ошибка при инициализации БД: {e}")
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
