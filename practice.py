import random
from words import get_all_words, get_general_words
from database import get_connection


def get_practice_data(user_id):
    words = get_all_words(user_id)
    if not words:
        return None, None, None

    russian, correct = random.choice(words)
    all_translations = [trans for _, trans in words]
    all_translations += [pair[1] for pair in get_general_words()]

    # Убираем правильный перевод из общего списка, чтобы не было дубликатов при выборе
    wrong_choices = set([trans for trans in all_translations if trans != correct])

    # Выбираем 3 уникальных неправильных варианта
    choices = random.sample(list(wrong_choices), 3)
    choices.append(correct)
    random.shuffle(choices)

    return russian, correct, choices


def save_result(user_id, word, correct):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO results (user_id, word, correct) VALUES (%s, %s, %s)",
        (user_id, word, correct)
    )
    conn.commit()
    cur.close()
    conn.close()
