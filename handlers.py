from telebot import types
from keyboards import get_main_menu

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
            reply_markup=get_main_menu() # кнопки внизу
        )

    @bot.message_handler(content_types=['text'])
    def message_reply(message):
        user_id = message.chat.id
        text = message.text.strip().lower()
        state = user_states.get(user_id, {}).get('mode', 'menu')
        if state == 'menu':

            if text == 'Дальше ⏭':
                pass

            elif text == 'добавить слово 💬':
                user_states[user_id]['mode'] = 'adding_word'
                bot.send_message(user_id, "Напиши новое слово на русском:")
                # добавление слова

            elif text == 'удалить слово 🗑️':
                user_states[user_id]['mode'] = 'deleting_word'
                bot.send_message(user_id, "Какое слово хочешь удалить?")


        elif state == 'adding_word':
            # тут добавление слова в базу
            bot.send_message(user_id, f"Слово '{text}' добавлено!")
            user_states[user_id]['mode'] = 'menu'
            bot.send_message(user_id, "Что дальше?", reply_markup=get_main_menu())

        elif state == 'deleting_word':
            # тут удаление слова из базы
            bot.send_message(user_id, f"Слово '{text}' удалено!")
            user_states[user_id]['mode'] = 'menu'
            bot.send_message(user_id, "Что дальше?", reply_markup=get_main_menu())


