from keyboards import get_main_menu, get_practice_keyboard, get_cancel_keyboard
from practice import get_practice_data, save_result
from words import get_user_words, delete_word, add_word, get_all_words


def setup_handlers(bot):
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
            'Добавить слово, '
            'Удалить слово. '
            'Готов? Тогда вперёд — начнём прямо сейчас! 💪🔥',
            reply_markup=get_main_menu()  # кнопки внизу
        )

    @bot.message_handler(content_types=['text'])
    def reply(message):
        user_id = message.chat.id
        text = message.text.strip()
        state = user_states.get(user_id, {}).get('mode', 'menu')

        # --- Главное меню ---
        if state == 'menu':
            if text == 'Добавить слово':
                user_states[user_id] = {'mode': 'wait_russian'}
                bot.send_message(
                    user_id,
                    "Напиши слово на русском или нажмите 'Отмена'",
                    reply_markup=get_cancel_keyboard()
                )

            elif text == 'Удалить слово':
                user_states[user_id] = {'mode': 'delete_word'}
                words = get_user_words(user_id)
                if not words:
                    bot.send_message(
                        user_id,
                        "У вас нет добавленных слов для удаления",
                        reply_markup=get_main_menu()
                    )
                    user_states[user_id] = {'mode': 'menu'}
                else:
                    bot.send_message(
                        user_id,
                        "Введите слово на русском языке, которое хотите удалить, или нажмите 'Отмена'",
                        reply_markup=get_cancel_keyboard()
                    )


            elif text == 'Практика':
                russian, correct, choices = get_practice_data(user_id)
                if not russian or not correct or not choices:
                    bot.send_message(
                        user_id,
                        "Нет слов для практики",
                        reply_markup=get_main_menu()
                    )
                    return
                bot.send_message(
                    user_id,
                    f"Как переводится слово: {russian}?",
                    reply_markup=get_practice_keyboard(choices)
                )
                user_states[user_id] = {'mode': 'practice', 'correct': correct, 'word': russian}

        # --- Ждём русское слово ---
        elif state == 'wait_russian':
            if text == "Отмена":
                bot.send_message(
                    user_id,
                    "Добавление отменено",
                    reply_markup=get_main_menu()
                )
                user_states[user_id] = {'mode': 'menu'}
            else:
                user_states[user_id] = {'mode': 'wait_english', 'russian': text}
                bot.send_message(
                    user_id,
                    f"Теперь введите перевод слова '{text}' на английском или нажмите 'Отмена'",
                    reply_markup=get_cancel_keyboard()
                )

        # --- Ждём английское слово ---
        elif state == 'wait_english':
            if text == "Отмена":
                bot.send_message(
                    user_id,
                    "Добавление отменено",
                    reply_markup=get_main_menu()
                )
                user_states[user_id] = {'mode': 'menu'}
            else:
                russian = user_states[user_id].get('russian')
                add_word(user_id, russian, text)

                # Получаем обновлённое количество добавленных слов
                user_word_count = len(get_user_words(user_id))
                # Получаем обновлённое количество всех слов
                all_word_count = len(get_all_words(user_id))

                bot.send_message(
                    user_id,
                    f"Слово '{russian} - {text}' добавлено в ваш словарь!\n"
                    f"Сейчас вы изучаете {user_word_count} новых слов(а).\n"
                    f"Всего вы изучаете {all_word_count} слов(а).",
                    reply_markup=get_main_menu()
                )
                user_states[user_id] = {'mode': 'menu'}  # возврат в меню

        # --- Удаление слова ---
        elif state == 'delete_word':
            if text == "Отмена":
                bot.send_message(
                    user_id,
                    "Удаление отменено",
                    reply_markup=get_main_menu()
                )
                user_states[user_id] = {'mode': 'menu'}
            else:
                words = get_user_words(user_id)
                if any(word[0] == text for word in words):  # word[0] — русское слово
                    delete_word(user_id, text)
                    bot.send_message(
                        user_id,
                        f"Слово '{text}' удалено из вашего словаря.",
                        reply_markup=get_main_menu()
                    )
                    user_states[user_id] = {'mode': 'menu'}
                else:
                    bot.send_message(
                        user_id,
                        f"Слово '{text}' не найдено в вашем словаре. Попробуйте ещё раз или нажмите 'Отмена'",
                        reply_markup=get_cancel_keyboard()
                    )

        # --- Режим практика ---
        elif state == 'practice':
            correct = user_states[user_id].get('correct')
            word = user_states[user_id].get('word')

            if text == "Меню":
                bot.send_message(
                    user_id,
                    "Вы вышли из режима практики.",
                    reply_markup=get_main_menu()
                )
                user_states[user_id] = {'mode': 'menu'}
            else:
                is_correct = (text.lower() == correct.lower())
                save_result(user_id, word, is_correct)

                if is_correct:
                    bot.send_message(
                        user_id,
                        f"Правильно! '{word}' — это '{correct}'",
                        reply_markup=get_main_menu()
                    )
                else:
                    bot.send_message(
                        user_id,
                        f"Неправильно! '{word}' — это '{correct}'",
                        reply_markup=get_main_menu()
                    )
                user_states[user_id] = {'mode': 'menu'}