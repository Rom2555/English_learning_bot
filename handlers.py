from telebot import types
from keyboards import get_main_menu, get_words_keyboard, get_practice_keyboard
from practice import get_practice_data
from words import get_user_words, delete_word, add_word


def setup_handlers(bot):
    # состояние пользователя: user_id ---> словарь {mode: '...', data: {...}}
    user_states = {}

    @bot.message_handler(commands=['start'])
    def start(message):
        user_states[message.chat.id] = {'mode': 'menu'}
        bot.send_message(
            message.chat.id,
            'Привет 🌟 Давай попрактикуемся в английском языке! '
            'Ты можешь тренироваться в удобном для себя темпе 🚀. '
            'Используй тренажёр как конструктор — '
            'создавай свою собственную базу слов 🧩! '
            'Для этого используй инструменты: '
            'добавить слово 💬, '
            'удалить слово 🗑️. '
            'Готов? Тогда вперёд — начнём прямо сейчас! 💪🔥',
            reply_markup=get_main_menu() # кнопки внизу
        )

    @bot.message_handler(content_types=['text'])
    def reply(message):
        user_id = message.chat.id
        text = message.text.strip()
        state = user_states.get(user_id, {}).get('mode', 'menu')

        # --- Главное меню ---
        if state == 'menu':
            if text == 'добавить слово 💬':
                user_states[user_id] = {'mode': 'wait_russian'}
                bot.send_message(user_id, "Напиши слово на русском:")

            elif text == 'удалить слово 🗑️':
                words = get_user_words(user_id)
                if not words:
                    bot.send_message(user_id, "У вас нет слов для удаления")
                else:
                    bot.send_message(user_id, "Выберите слово для удаления:", reply_markup=get_words_keyboard(words))
                    user_states[user_id] = {'mode': 'delete_word'}

            elif text == 'Дальше ⏭':
                russian, correct, choices = get_practice_data(user_id)
                if not russian or not correct or not choices:
                    bot.send_message(user_id, "Нет слов для практики")
                    return
                bot.send_message(
                    user_id,
                    f"Как переводится слово: {russian}?",
                    reply_markup=get_practice_keyboard(choices)
                )
                user_states[user_id] = {'mode': 'practice', 'correct': correct, 'word': russian}

        # --- Ждём русское слово ---
        elif state == 'wait_russian':
            user_states[user_id] = {'mode': 'wait_english', 'russian': text}
            bot.send_message(user_id, f"Теперь введите перевод слова '{text}' на английском:")

        # --- Ждём английское слово ---
        elif state == 'wait_english':
            russian = user_states[user_id].get('russian')
            add_word(user_id, russian, text)
            bot.send_message(
                user_id,
                f"Слово '{russian} - {text}' добавлено в ваш словарь!",
                reply_markup=get_main_menu()
            )
            user_states[user_id] = {'mode': 'menu'}  # возврат в меню

        # --- Удаление слова ---
        elif state == 'delete_word':
            if text == "Отмена":
                bot.send_message(user_id, "Удаление отменено", reply_markup=get_main_menu())
            else:
                delete_word(user_id, text)
                bot.send_message(user_id, f"Слово '{text}' удалено", reply_markup=get_main_menu())
            user_states[user_id] = {'mode': 'menu'}

        # --- Режим практика ---
        elif state == 'practice':
            correct = user_states[user_id].get('correct')
            print(correct)
            word = user_states[user_id].get('word')
            print(word)

            if text == "Меню":
                bot.send_message(user_id, "Вы вышли из режима практики.", reply_markup=get_main_menu())
                user_states[user_id] = {'mode': 'menu'}
            else:
                if text.lower() == correct.lower():
                    bot.send_message(
                        user_id,
                        f"Правильно! *{word}* — это *{correct}*",
                        reply_markup=get_main_menu()
                    )
                else:
                    bot.send_message(
                        user_id,
                        f"Неправильно! *{word}* — это *{correct}*",
                        reply_markup=get_main_menu()
                    )
                user_states[user_id] = {'mode': 'menu'}