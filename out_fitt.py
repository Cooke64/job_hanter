import time
import telebot
from telebot import types

from main import get_html, get_job
from bd import create_user, delete_user
bot = telebot.TeleBot("token")


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Найдем работу мечты?", "Задать вопрос", 'Курс валюты')
    file = open('main.jpg', 'rb')
    bot.send_message(
        message.chat.id,
        text="Привет, {0.first_name}! Я помогу тебе найти работу в айти".format(
            message.from_user),
        reply_markup=markup)
    bot.send_photo(message.chat.id, file)
    create_user(message)


@bot.message_handler(commands=['stop'])
def start(message):
    bot.send_message(message.from_user.id, text='Прекращаю работу', )
    delete_user(message)


@bot.message_handler(commands=['help'])
def help_user(message):
    if message.text == "/help":
        bot.send_message(
            message.from_user.id,
            "Напиши /start")
    else:
        bot.send_message(
            message.from_user.id,
            "Я тебя не понимаю. Напиши /help.")


@bot.message_handler(commands=['about'])
def get_out_ifo_about(message):
    if message.text == "/about":
        markup = types.InlineKeyboardMarkup()
        btn_my_site = types.InlineKeyboardButton(text='Github',
                                                 url='https://github.com/Cooke64')
        markup.add(btn_my_site)
        bot.send_message(message.chat.id, "Нажми на кнопку и перейди",
                         reply_markup=markup)


# @bot.message_handler(commands=['stop'])
# def make_bot_stop(message):
#     keyboard = types.InlineKeyboardMarkup()
#     key_stop = types.InlineKeyboardButton(
#         text='stop',
#         callback_data='stop'
#     )
#     keyboard.add(key_stop)
#     bot.send_message(message.from_user.id, text='Прекращаю работу', )


@bot.message_handler(content_types=['text'])
def make_queries(message):
    if message.text == "Найдем работу мечты?":
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            selective=False,
        )
        markup.row("Python?", "Java?", "Back?")
        bot.send_message(
            message.chat.id,
            text="Выбери язык программирования",
            reply_markup=markup)
    elif message.text == "Python?":
        name = 'python'
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
        bot.send_message(message.from_user.id, text='Выбери уровень',
                         reply_markup=keyboard)
    elif message.text == "Java?":
        name = 'java'
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
        bot.send_message(
            message.from_user.id,
            text='Выбери уровень',
            reply_markup=keyboard)

    elif message.text == "Задать вопрос":
        markup = types.ForceReply(
            selective=False,
        )
        bot.send_message(
            message.chat.id,
            text="Что хочешь узнать?",
            reply_markup=markup,
        )

    elif message.text == "Back?":
        # При нажатии кнопки Back возвращает в главное меню и
        # вызывается функция start
        start(message)
        bot.send_message(
            message.chat.id,
            text="Вы вернулись в главное меню",
        )


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):

    if call.data is not None:
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                  text='Начинаю искать вакансии')
        for a in get_html(call.data):
            search = (get_job(a))
            time.sleep(1)
            bot.send_message(call.message.chat.id, search)


bot.polling(none_stop=True)
