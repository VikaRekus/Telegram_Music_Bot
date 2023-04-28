import urllib
import telebot
import sqlite3
import random
import logging
from telebot import types
from youtubesearchpython import VideosSearch
import pytube


class AuthHandler:
    def __init__(self, chat):
        self.bot = bot
        self.pending = False
        self.innertube = None
        self.last_link = None

    def complete(self):
        if self.pending and self.innertube is not None:
            self.innertube.oauth_completion_handler()
            self.pending = False

    def __call__(self, chat, link):
        def notification(verification_url, user_code, innertube):
            self.bot.send_message(chat.id,
                                  f'Пожалуйста отройте ссылку {verification_url} и введите код \n {user_code} \n'
                                  'чтобы разрешить работу бота')
            self.pending = True
            self.innertube = innertube

        self.last_link = link
        return notification


logging.basicConfig(level=logging.DEBUG)

bot = telebot.TeleBot('1707038541:AAFknwZspucuP4i4AqQPeI4K-EBwZQvg0KE')
auth = AuthHandler(bot)


# обработка команды старт
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button1 = types.KeyboardButton("👋 Привет")
    button2 = types.KeyboardButton("🎶 Найти музыку")
    button3 = types.KeyboardButton("❓ Задать вопрос")

    markup.add(button1, button2, button3)

    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я помогу тебе найти нужную музыку".format(
        message.from_user),
                     reply_markup=markup)


# обработка команды помощь
@bot.message_handler(commands=['help'])
def help(message):
    returned(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    bot.send_message(message.chat.id,
                     text="{0.first_name}! Я помогу тебе разобраться с управлением и выяснить в чем проблема.".format(
                         message.from_user),
                     reply_markup=markup)
    bot.send_message(message.chat.id,
                     text="Если вы здесь, потому что не знаете как работает бот, вам сюда 👉🏻 /control")
    bot.send_message(message.chat.id, text="Если у вас не загружается трек, вам сюда 👉 /error")


# обработка команды помощи с ошибками
@bot.message_handler(commands=['error'])
def error(message):
    returned(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    bot.send_message(message.chat.id,
                     text="{0.first_name}! Если у вас не загружается трек, то можно попробовать это исправить тем, что 👉".format(
                         message.from_user),
                     reply_markup=markup)
    bot.send_message(message.chat.id, text="1 - Попробовать скачать трек снова")
    bot.send_message(message.chat.id, text="2 - Попробовать скачать трек через некоторое время")
    bot.send_message(message.chat.id,
                     text="Если трек всё равно не скачался, то скорее всего это из-за ограничений по возрасту или слишком большого размера.😞 "
                          "Поэтому попробуйте скачать что-нибудь другое...")


# обработка команды помощи с управлением
@bot.message_handler(commands=['control'])
def control(message):
    returned(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    bot.send_message(message.chat.id, text="{0.first_name}! Я помогу тебе разобраться с управлением".format(
        message.from_user),
                     reply_markup=markup)
    bot.send_message(message.chat.id,
                     text="Я могу найти вам трек по названию, когда вы выберите 👉 🎶 Найти музыку 👉 Найти по названию 👉 и введете название")
    bot.send_message(message.chat.id,
                     text="Также я могу посоветовать вам песню из своих запасов, для этого выберите 👉 🎶 Найти музыку 👉 Песня на выбор бота 👉 и подождите")


# обработка команд вводящихся с клавиатуры
@bot.message_handler(content_types=['text'])
def comands(message):
    # обработка команды "Привет"
    if message.text == "👋 Привет":
        bot.send_message(message.chat.id, text="Привеееет. Рад вас видеть)")

    # Обработка команды "Задать вопрос"
    elif message.text == "❓ Задать вопрос":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        button1 = types.KeyboardButton("Как тебя зовут?")
        button2 = types.KeyboardButton("Что ты можешь?")
        back_button = types.KeyboardButton("Вернуться в главное меню")

        markup.add(button1, button2, back_button)

        bot.send_message(message.chat.id,
                         text="Задай мне вопрос",
                         reply_markup=markup)

    # Обработка команды "Найти музыку"
    elif message.text == "🎶 Найти музыку":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        button1 = types.KeyboardButton("Найти по названию")
        button2 = types.KeyboardButton("Песня на выбор бота")
        back_button = types.KeyboardButton("Вернуться в главное меню")

        markup.add(button1, button2, back_button)

        bot.send_message(message.chat.id,
                         text="Выбери действие",
                         reply_markup=markup)

    # Обработка вопросов:

    # Обработка 1го вопроса
    elif message.text == "Как тебя зовут?":
        bot.send_message(message.chat.id, "У меня нет имени....")

    # Обработка 2го вопроса
    elif message.text == "Что ты можешь?":
        bot.send_message(message.chat.id,
                         text="Могу найти вам определенную песню, а могу порекомендовать свою😜")

    # Обработка команд для поиска песен:

    # Обработка команды для поиска песни по названию
    elif message.text == "Найти по названию":
        sm = bot.send_message(message.chat.id, "Введите название песни, которую хотите найти")
        bot.register_next_step_handler(sm, search)

    # Обработка команды для генерации песни из базы данных
    elif message.text == "Песня на выбор бота":
        bot.send_message(message.chat.id, "Подождите немного...")

        sqlite_connection = sqlite3.connect('MyDB3.db')
        cursor = sqlite_connection.cursor()

        sqlite_select_query = """SELECT * from links"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        row = random.choice(records)
        try:
            downloading(row[1], message)
        except urllib.error.HTTPError as ex:
            if ex.code == 401:
                bot.send_message(message.chat.id, text="Похоже вы не авторизованы")
        # downloaded =False
        # while not downloaded:
        #     try:
        #         row = random.choice(records)
        #         downloading(row[1], message)
        #         downloaded = True
        #
        #     except Exception as ex:
        #         print(ex.__repr__(), row[1])

    # Обработка возращения в главное меню
    elif message.text == "Вернуться в главное меню":
        returned(message)
    elif auth.pending and message.text == "Продолжить":
        auth.complete()
        if auth.last_link:
            downloading(auth.last_link, message)
    # Обработка непонятных для бота команд
    else:
        bot.send_message(message.chat.id,
                         text="Я не очень вас понял, повторите пожалуйста((....")


# Функция для возвращения в главное меню
def returned(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button1 = types.KeyboardButton("👋 Привет")
    button2 = types.KeyboardButton("🎶 Найти музыку")
    button3 = types.KeyboardButton("❓ Задать вопрос")

    markup.add(button1, button2, button3)

    bot.send_message(message.chat.id, "Вы вернулись в главное меню",
                     reply_markup=markup)


# Функция для поиска видео по названию в YouTube и его скачиванию
def search(message):
    result = VideosSearch(message.text, limit=1).result()

    for i in range(len(result["result"])):
        try:
            bot.send_message(message.chat.id, "Скачиваем...\n" + result["result"][i]["link"])
            downloading(result["result"][i]["link"], message)

        except:
            bot.send_message(message.chat.id, "Не получилось скачать...😢")
            bot.send_message(message.chat.id, "Чтобы узнать проблему попробуйте команду /help")
            returned(message)


# Функция для скачивания звука из видео с YouTube
def downloading(link, message):
    my_video = pytube.YouTube(link,
                              use_oauth=True,
                              allow_oauth_cache=True,
                              oath_callback=auth(message.chat, link))
    path = my_video.streams.filter(only_audio=True)[0].download()
    audio = open(path, 'rb')
    print(path)
    bot.send_audio(message.chat.id, audio)
    bot.send_message(message.chat.id, f"Успешно скачан.....")


bot.polling()
