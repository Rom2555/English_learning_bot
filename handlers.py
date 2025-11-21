from telebot import types
from keyboards import get_main_menu, get_words_keyboard
from words import get_user_words, delete_word


def setup_handlers(bot):
    user_states = {}

    @bot.message_handler(commands=['start'])
    def start_command(message):
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
            reply_markup=get_main_menu()  # кнопки внизу
        )

    @bot.message_handler(content_types=['text'])
    def message_reply(message):
        user_id = message.chat.id
        text = message.text.strip().lower()
        state = user_states.get(user_id, {}).get('mode', 'menu')  # узнаем в каком процессе находится пользователь,
        # если нет, то по умолчанию menu
        if state == 'menu':

            if text == 'Дальше ⏭':
                pass

            elif text == 'добавить слово 💬':
                user_states[user_id]['mode'] = 'adding_word'
                bot.send_message(user_id, "Напиши новое слово на русском:")
                # добавление слова

            elif text == "удалить слово 🗑️":
                words = get_user_words(user_id)
                if not words:
                    bot.send_message(user_id, "У вас нет добавленных слов")
                    return
                bot.send_message(user_id, "Какое слово хотите удалить?", reply_markup=get_words_keyboard(words))
                user_states[user_id] = {'mode': 'deleting_word'}


        elif state == 'adding_word':
            # тут добавление слова в базу
            bot.send_message(user_id, f"Слово '{text}' добавлено!")
            user_states[user_id]['mode'] = 'menu'
            bot.send_message(user_id, "Что дальше?", reply_markup=get_main_menu())

        elif state == 'deleting_word':
            handle_deleting_word(user_id, text)
            bot.send_message(user_id, f"Слово '{text}' удалено!")
            user_states[user_id]['mode'] = 'menu'
            bot.send_message(user_id, "Что дальше?", reply_markup=get_main_menu())

    def handle_deleting_word(user_id, text):
        if text == "Отмена":
            bot.send_message(user_id, "Удаление отменено", reply_markup=get_main_menu())
            user_states[user_id] = {'mode': 'menu'}
        else:
            delete_word(user_id, text)
            bot.send_message(user_id, f"Слово '{text}' удалено", reply_markup=get_main_menu())
            user_states[user_id] = {'mode': 'menu'}