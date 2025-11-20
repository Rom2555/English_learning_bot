"""База данных english_bot_db2"""

import psycopg2
import json
from config import DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )

def init_db():
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Таблица: общие слова
        cur.execute('''
            CREATE TABLE IF NOT EXISTS general_words (
                id SERIAL PRIMARY KEY,
                word TEXT NOT NULL,
                translation TEXT NOT NULL,
                UNIQUE (word)
            );
        ''')

        # Таблица: пользовательские слова
        cur.execute('''
            CREATE TABLE IF NOT EXISTS user_words (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                word TEXT NOT NULL,
                translation TEXT NOT NULL,
                UNIQUE (user_id, word)
            );
        ''')

        # Таблица: результаты
        cur.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                word TEXT NOT NULL,
                correct BOOLEAN NOT NULL,
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
            conn.rollback() # Откат транзакции, всё обнуляется
        print(f"Ошибка при инициализации БД: {e}")
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()