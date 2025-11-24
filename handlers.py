"""Модуль обработчиков сообщений для Telegram-бота

Содержит функцию setup_handlers,
которая регистрирует обработчики команд и текстовых сообщений
Реализует логику взаимодействия с пользователем:
добавление\\удаление слов, режим практики
"""

import logging

from keyboards import get_main_menu, get_practice_keyboard, get_cancel_keyboard
from practice import get_practice_data, save_result
from words import get_user_words, delete_word, add_word, get_all_words

# настройка логов
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def setup_handlers(bot):
    """Настраивает обработчики команд и текстовых сообщений для бота

    Args:
        bot (telebot.TeleBot): Экземпляр бота, к которому привязываются обработчики

    Обрабатывает:
        - Команду /start
        - Текстовые сообщения в зависимости от текущего состояния пользователя
        - Действия: добавление, удаление слов, практика

    Использует внутренний словарь user_states для отслеживания состояния каждого пользователя
    """
    # Словарь состояния пользователя
    user_states = {}

    @bot.message_handler(commands=["start"])
    def start(message):
        """Обработчик команды /start

        Приветствует пользователя и показывает главное меню

        Args:
            message: Входящее сообщение от пользователя
        """
        user_states[message.chat.id] = {"mode": "menu"}
        try:
            bot.send_message(
                message.chat.id,
                "Привет!"
                "\nЯ бот-тренажёр для изучения английских слов."
                "\nТы можешь тренироваться в удобном для себя темпе 🚀. "
                "\nИспользуй тренажёр как конструктор - "
                " создавай свою собственную базу слов 🧩! "
                "\nДля этого используй инструменты: "
                "Добавить слово, "
                "Удалить слово. "
                "\nГотов? Тогда вперёд — начнём прямо сейчас! 💪🔥",
                reply_markup=get_main_menu(),  # кнопки внизу
            )
        except Exception as e:
            logging.error(
                f"Ошибка при отправке приветствия пользователю {message.chat.id}: {e}"
            )
            bot.send_message(message.chat.id, "Произошла ошибка. Попробуйте позже.")

    @bot.message_handler(content_types=["text"])
    def reply(message):
        """Основной обработчик текстовых сообщений

        Направляет логику в зависимости от текущего состояния пользователя

        Args:
            message: Входящее текстовое сообщение
        """
        user_id = message.chat.id
        text = message.text.strip()
        state = user_states.get(user_id, {}).get("mode", "menu")

        # --- Главное меню ---
        if state == "menu":
            if text == "Добавить слово":
                user_states[user_id] = {"mode": "wait_russian"}
                try:
                    bot.send_message(
                        user_id,
                        "Напиши слово на русском или нажмите 'Отмена'",
                        reply_markup=get_cancel_keyboard(),
                    )
                except Exception as e:
                    logging.error(
                        f"Ошибка при отправке сообщения пользователю {user_id}: {e}"
                    )
                    bot.send_message(
                        user_id,
                        "Произошла ошибка. Попробуйте позже.",
                        reply_markup=get_main_menu(),
                    )

            elif text == "Удалить слово":
                user_states[user_id] = {"mode": "delete_word"}
                try:
                    words = get_user_words(user_id)
                    if not words:
                        bot.send_message(
                            user_id,
                            "У вас нет добавленных слов для удаления",
                            reply_markup=get_main_menu(),
                        )
                        user_states[user_id] = {"mode": "menu"}
                    else:
                        bot.send_message(
                            user_id,
                            "Введите слово на русском языке,"
                            " которое хотите удалить, или нажмите 'Отмена'",
                            reply_markup=get_cancel_keyboard(),
                        )
                except Exception as e:
                    logging.error(
                        f"Ошибка при получении слов пользователя {user_id}: {e}"
                    )
                    bot.send_message(
                        user_id,
                        "Не удалось получить список слов. Попробуйте позже.",
                        reply_markup=get_main_menu(),
                    )
                    user_states[user_id] = {"mode": "menu"}

            elif text == "Практика":
                try:
                    russian, correct, choices = get_practice_data(user_id)
                    if not russian or not correct or not choices:
                        bot.send_message(
                            user_id,
                            "Нет слов для практики",
                            reply_markup=get_main_menu(),
                        )
                        return
                    bot.send_message(
                        user_id,
                        f"Как переводится слово: {russian}?",
                        reply_markup=get_practice_keyboard(choices),
                    )
                    user_states[user_id] = {
                        "mode": "practice",
                        "correct": correct,
                        "word": russian,
                    }
                except Exception as e:
                    logging.error(
                        f"Ошибка при подготовке практики для пользователя {user_id}: {e}"
                    )
                    bot.send_message(
                        user_id,
                        "Произошла ошибка при запуске практики.",
                        reply_markup=get_main_menu(),
                    )

        # --- Ждём русское слово ---
        elif state == "wait_russian":
            if text == "Отмена":
                try:
                    bot.send_message(
                        user_id, "Добавление отменено", reply_markup=get_main_menu()
                    )
                    user_states[user_id] = {"mode": "menu"}
                except Exception as e:
                    logging.error(
                        f"Ошибка при отмене добавления слова для пользователя {user_id}: {e}"
                    )
            else:
                user_states[user_id] = {"mode": "wait_english", "russian": text}
                try:
                    bot.send_message(
                        user_id,
                        f"Теперь введите перевод слова '{text}' на английском или нажмите 'Отмена'",
                        reply_markup=get_cancel_keyboard(),
                    )
                except Exception as e:
                    logging.error(
                        f"Ошибка при запросе перевода для пользователя {user_id}: {e}"
                    )
                    bot.send_message(
                        user_id,
                        "Произошла ошибка. Попробуйте позже.",
                        reply_markup=get_main_menu(),
                    )
                    user_states[user_id] = {"mode": "menu"}

        # --- Ждём английское слово ---
        elif state == "wait_english":
            if text == "Отмена":
                try:
                    bot.send_message(
                        user_id, "Добавление отменено", reply_markup=get_main_menu()
                    )
                    user_states[user_id] = {"mode": "menu"}
                except Exception as e:
                    logging.error(
                        f"Ошибка при отмене добавления для пользователя {user_id}: {e}"
                    )
            else:
                try:
                    russian = user_states[user_id].get("russian")
                    success = add_word(user_id, russian, text)
                    if not success:
                        bot.send_message(
                            user_id,
                            f"Слово '{russian}' уже есть в вашем словаре.",
                            reply_markup=get_main_menu(),
                        )
                    else:
                        # Получаем обновлённое количество добавленных слов
                        user_word_count = len(get_user_words(user_id))
                        # Получаем обновлённое количество всех слов
                        all_word_count = len(get_all_words(user_id))

                        bot.send_message(
                            user_id,
                            f"Слово '{russian} - {text}' добавлено в ваш словарь!\n"
                            f"Сейчас вы изучаете {user_word_count} новых слов(а).\n"
                            f"Всего вы изучаете {all_word_count} слов(а).",
                            reply_markup=get_main_menu(),
                        )
                    user_states[user_id] = {"mode": "menu"}  # возврат в меню
                except Exception as e:
                    logging.error(
                        f"Ошибка при добавлении слова для пользователя {user_id}: {e}"
                    )
                    bot.send_message(
                        user_id,
                        "Не удалось добавить слово. Попробуйте позже.",
                        reply_markup=get_main_menu(),
                    )
                    user_states[user_id] = {"mode": "menu"}

        # --- Удаление слова ---
        elif state == "delete_word":
            if text == "Отмена":
                try:
                    bot.send_message(
                        user_id, "Удаление отменено", reply_markup=get_main_menu()
                    )
                    user_states[user_id] = {"mode": "menu"}
                except Exception as e:
                    logging.error(
                        f"Ошибка при отмене удаления для пользователя {user_id}: {e}"
                    )
            else:
                try:
                    words = get_user_words(user_id)
                    if any(word[0] == text for word in words):
                        delete_word(user_id, text)
                        bot.send_message(
                            user_id,
                            f"Слово '{text}' удалено из вашего словаря.",
                            reply_markup=get_main_menu(),
                        )

                    else:
                        bot.send_message(
                            user_id,
                            f"Слово '{text}' не найдено в вашем словаре. Попробуйте ещё раз или нажмите 'Отмена'",
                            reply_markup=get_cancel_keyboard(),
                        )
                    user_states[user_id] = {"mode": "menu"}
                except Exception as e:
                    logging.error(
                        f"Ошибка при удалении слова '{text}' у пользователя {user_id}: {e}"
                    )
                    bot.send_message(
                        user_id,
                        "Не удалось удалить слово. Попробуйте позже.",
                        reply_markup=get_main_menu(),
                    )
                    user_states[user_id] = {"mode": "menu"}

        # --- Режим практика ---
        elif state == "practice":
            correct = user_states[user_id].get("correct")
            word = user_states[user_id].get("word")

            if text == "Меню":
                try:
                    bot.send_message(
                        user_id,
                        "Вы вышли из режима практики.",
                        reply_markup=get_main_menu(),
                    )
                    user_states[user_id] = {"mode": "menu"}
                except Exception as e:
                    logging.error(
                        f"Ошибка при выходе из практики для пользователя {user_id}: {e}"
                    )
            else:
                try:
                    is_correct = text.lower() == correct.lower()
                    save_result(user_id, word, is_correct)

                    if is_correct:
                        bot.send_message(
                            user_id,
                            f"Правильно! '{word}' — это '{correct}'",
                            reply_markup=get_main_menu(),
                        )
                    else:
                        bot.send_message(
                            user_id,
                            f"Неправильно! '{word}' — это '{correct}'",
                            reply_markup=get_main_menu(),
                        )
                    user_states[user_id] = {"mode": "menu"}
                except Exception as e:
                    logging.error(
                        f"Ошибка при обработке ответа на практике для пользователя {user_id}: {e}"
                    )
                    bot.send_message(
                        user_id,
                        "Произошла ошибка. Возврат в меню.",
                        reply_markup=get_main_menu(),
                    )
                    user_states[user_id] = {"mode": "menu"}
