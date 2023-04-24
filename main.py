import re
import os
import urllib

from moviepy.editor import *
import telebot
import sqlite3
import random
from telebot import types
#from selenium import webdriver
import time
from youtubesearchpython import VideosSearch
from pytube import YouTube
import pytube

import logging

#driver = webdriver.Chrome()
bot = telebot.TeleBot('6077503747:AAG2VNsh3fXjhFrENc7gLze7mAJ7H5zibpA')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    btn2 = types.KeyboardButton("🎶 Найти музыку")
    btn3 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я помогу тебе найти нужную музыку".format(message.from_user),
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def inline_key(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, 'Привет!))')

    elif message.text == "👋 Поздороваться":
        bot.send_message(message.chat.id, text="Привеееет. Рад вас видеть)")

    elif message.text == "❓ Задать вопрос":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как тебя зовут?")
        btn2 = types.KeyboardButton("Что ты можешь?")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)

    elif message.text == "🎶 Найти музыку":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Найти по названию")
        btn2 = types.KeyboardButton("Песня на выбор бота")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Выбери действие", reply_markup=markup)

    elif message.text == "Как тебя зовут?":
        bot.send_message(message.chat.id, "У меня нет имени....")

    elif message.text == "Что ты можешь?":
        bot.send_message(message.chat.id, text="Могу найти вам определенную песню, а могу порекомендовать свою😜")

    elif message.text == "Найти по названию":
        sm = bot.send_message(message.chat.id, "Введите название песни, которую хотите найти")
        bot.register_next_step_handler(sm, search)

    elif message.text == "Песня на выбор бота":
        bot.send_message(message.chat.id, "Подождите немного...")
        time.sleep(3)
        sqlite_connection = sqlite3.connect('MyDB3.db')
        cursor = sqlite_connection.cursor()

        sqlite_select_query = """SELECT * from links"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        downloaded =False
        while not downloaded:
            try:
                row = random.choice(records)
                downloading(row[1], message)
                downloaded = True
            except Exception as e:
                print(e, row[1])

    elif message.text == "Вернуться в главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("👋 Поздороваться")
        button2 = types.KeyboardButton("🎶 Найти музыку")
        button3 = types.KeyboardButton("❓ Задать вопрос")
        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)

    else:
        bot.send_message(message.chat.id, text="На такую команду я не запрограммирован((....")


def search(message):
    bot.send_message(message.chat.id, "Ищем и скачиваем, подождите немного...")
    #result = YouTubeMusicAPI.search(message.text)
    #bot.send_message(message.chat.id, result["url"])
    #downloading(result["url"])
    # video_href = "https://www.youtube.com/results?search_query=" + message.text
    # driver.get(video_href)
    # sleep(2)
    # videos = driver.find_elements(by="video-title")
    result = VideosSearch(message.text, limit=1).result()
    for i in range(len(result["result"])):
        try:
            downloading(result["result"][i]["link"], message)
        except pytube.exceptions.VideoUnavailable as e:
            print(e, result["result"][i]["link"])

            bot.send_message(message.chat.id, 'Не получилось скачать ☹️' + result["result"][i]["link"])
            bot.send_message(message.chat.id, "Попробуйте что-нибудь другое...")
        except Exception as e:
            print(e, result["result"][i]["link"])

    #    # bot.send_message(message.chat.id, videos[i].get_attribute("href"))
    #    # bot.send_message(message.chat.id, result["result"][i]["link"])
    #    if i == 1:
    #        break


def retry(link, message):
    for i in range(10):
        try:
            print(f'Try #: {i}')
            downloading(link, message)
            return True
        except:
             return False


def downloading(link, message):
    my_video = YouTube(link)
    path = my_video.streams.filter(only_audio=True).first().download()
    video = open(path, 'rb')
    print(path)
    bot.send_message(message.chat.id, 'Успешно скачан... ' + link)
    bot.send_audio(message.chat.id, video)


bot.polling()
