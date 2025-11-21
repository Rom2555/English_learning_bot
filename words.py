from database import get_connection

def get_user_words(user_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT word, translation FROM user_words WHERE user_id = %s", (user_id,))
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def get_general_words():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT word, translation FROM general_words")
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def get_all_words(user_id):
    user_words = get_user_words(user_id)
    general_words = get_general_words()
    return user_words + general_words

def delete_word(user_id, word):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM user_words WHERE user_id = %s AND word = %s", (user_id, word))
    conn.commit()
    cur.close()
    conn.close()