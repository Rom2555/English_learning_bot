import random
from words import get_all_words, get_general_words
from database import get_connection

def get_practice_data(user_id):
    words = get_all_words(user_id)
    if not words:
        return None, None, None

    russian, correct = random.choice(words)
    all_translations = [trans for _, trans in words]

    # Проблема: get_general_words() может возвращать dict или list
    general_words = get_general_words()
    if hasattr(general_words, 'values'):  # Проверяем, словарь ли это
        all_translations += list(general_words.values())
    else:
        # Предполагаем, что это список вида [('cat', 'кот'), ...]
        all_translations += [pair[1] for pair in general_words]

    choices = list(set([correct] + random.sample(all_translations, min(3, len(all_translations)))))
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