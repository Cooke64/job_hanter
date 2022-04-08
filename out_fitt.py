import time
from telebot import types

from main import get_parsed_vacancy_page, get_requested_job, bot
from bd import create_user, delete_user


bot = bot


@bot.message_handler(commands=['start'])
def start_bot_process(message):
    """Запускаем работу бота. Отображение начального экрана бота."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Отображение меню из кнопок
    markup.row("Найдем работу мечты?", "Задать вопрос",)
    file = open('main.jpg', 'rb')
    bot.send_message(
        message.chat.id,
        text=f"Привет, {message.from_user.first_name}! Я помогу тебе найти работу в айти",
        reply_markup=markup
    )
    # Отправляет изображение при начальном экране
    bot.send_photo(message.chat.id, file)
    create_user(message)


@bot.message_handler(commands=['stop'])
def stop_bot_process(message):
    """Завершение работы бота при команде stop."""
    bot.send_message(message.from_user.id, text='Прекращаю работу', )
    delete_user(message)


@bot.message_handler(commands=['help'])
def help_user(message):
    """При команде help отображает основные команды."""
    if message.text == "/help":
        bot.send_message(
            message.from_user.id, "Напиши /start"
        )
    else:
        bot.send_message(
            message.from_user.id, "Я тебя не понимаю. Напиши /help."
        )


@bot.message_handler(commands=['about'])
def get_out_ifo_about(message):
    """При команде about отображает ссылку на мой гит."""
    if message.text == "/about":
        markup = types.InlineKeyboardMarkup()
        btn_my_site = types.InlineKeyboardButton(
            text='Github', url='https://github.com/Cooke64'
        )
        markup.add(btn_my_site)
        bot.send_message(
            message.chat.id, "Нажми на кнопку и перейди", reply_markup=markup
        )


def sender_messages(text, message, markup=None):
    """Функция отправки сообщения в телеграм.
    Принимает текст сообщения, конкретный чат, разметку кнопок.
    """
    message = bot.send_message(
        message.chat.id,
        text=text,
        reply_markup=markup
    )
    return message


def represent_available_choices(name, message):
    keyboard = types.InlineKeyboardMarkup()
    key_junior = types.InlineKeyboardButton(
        text='Junior',
        callback_data=f'junior + {name} + developer '
    )
    keyboard.add(key_junior)
    key_middle = types.InlineKeyboardButton(
        text='Middle ',
        callback_data=f'middle + {name} + developer '
    )
    keyboard.add(key_middle)
    text = 'Выбери уровень',
    sender_messages(text, message, markup=keyboard)


@bot.message_handler(content_types=['text'])
def make_queries(message):
    """Отображает запросы пользователя и отображает полученную информацию."""
    if message.text == "Найдем работу мечты?":
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            selective=False,
        )
        markup.row("Python?", "Java?", "Back?")
        text = "Выбери язык программирования",
        sender_messages(text, message, markup)

    elif message.text == "Python?":
        name = 'python'
        represent_available_choices(name, message)

    elif message.text == "Java?":
        name = 'java'
        represent_available_choices(name, message)

    elif message.text == "Задать вопрос":
        markup = types.ForceReply(
            selective=False,
        )
        text = "Что хочешь узнать?",
        sender_messages(text, message, markup)

    elif message.text == "Back?":
        # При нажатии кнопки Back возвращает в главное меню и
        # вызывается функция start_bot_process
        start_bot_process(message)
        text = "Вы вернулись в главное меню",
        sender_messages(text, message)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    """Вывод результатов запроса на экран бота."""
    if call.data is not None:
        bot.answer_callback_query(
            callback_query_id=call.id,
            show_alert=False,
            text='Начинаю искать вакансии'
        )
        for a in get_parsed_vacancy_page(call.data):
            search = (get_requested_job(a))
            time.sleep(5)
            bot.send_message(call.message.chat.id, search)


bot.polling(none_stop=True)
