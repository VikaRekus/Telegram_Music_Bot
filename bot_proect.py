import telebot
from telebot import types
from selenium import webdriver
from time import sleep

driver = webdriver.Chrome()
bot = telebot.TeleBot('6077503747:AAG2VNsh3fXjhFrENc7gLze7mAJ7H5zibpA')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    btn2 = types.KeyboardButton("🎶 Найти музыку")
    btn3 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я помогу тебе найти нужную музыку".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def inline_key(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, 'Привет!))')
        mainmenu = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton(text='Кнопка 1', callback_data='key1')
        key2 = types.InlineKeyboardButton(text='Кнопка 2', callback_data='key2')
        key3 = types.InlineKeyboardButton(text='Кнопка 3', callback_data='key3')
        mainmenu.add(key1, key2, key3)
        bot.send_message(message.chat.id, 'Выбери стиль песни:', reply_markup=mainmenu)
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
        btn2 = types.KeyboardButton("Сгенерировать любую")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Выбери действие", reply_markup=markup)

    elif message.text == "Как тебя зовут?":
        bot.send_message(message.chat.id, "У меня нет имени....")

    elif message.text == "Что ты можешь?":
        bot.send_message(message.chat.id, text="Могу найти вам определенную песню, а могу порекомендовать свою😜")

    elif message.text == "Найти по названию":
        sm = bot.send_message(message.chat.id, "Введите название песни, которую хотите найти")
        bot.register_next_step_handler(sm, search(message))

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
    video_href = "https://www.youtube.com/results?search_query=" + message.text
    driver.get(video_href)
    sleep(2)
    videos = driver.find_elements("video_title")
    for i in range(len(videos)):
        bot.send_message(message.chat.id, videos[i].get_attribute("href"))
        if i == 1:
            break

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "mainmenu":
        mainmenu = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton(text='Кнопка 1', callback_data='key1')
        key2 = types.InlineKeyboardButton(text='Кнопка 2', callback_data='key2')
        key3 = types.InlineKeyboardButton(text='Кнопка 3', callback_data='key3')
        mainmenu.add(key1, key2, key3)
        bot.edit_message_text('Выбери стиль песни:', call.message.chat.id, call.message.message_id,
                              reply_markup=mainmenu)
    elif call.data == "key1":
        next_menu = types.InlineKeyboardMarkup()
        key4 = types.InlineKeyboardButton(text='Кнопка 4', callback_data='key4')
        back = types.InlineKeyboardButton(text='Назад', callback_data='mainmenu')
        next_menu.add(key4, back)
        bot.edit_message_text('Это меню уровня 2, для кнопки1!', call.message.chat.id, call.message.message_id,
                              reply_markup=next_menu)
    elif call.data == "key2":
        next_menu2 = types.InlineKeyboardMarkup()
        key5 = types.InlineKeyboardButton(text='Кнопка 5', callback_data='key5')
        back = types.InlineKeyboardButton(text='Назад', callback_data='mainmenu')
        next_menu2.add(key5, back)
        bot.edit_message_text('Это меню уровня 2, для кнопки2!', call.message.chat.id, call.message.message_id,
                              reply_markup=next_menu2)

    elif call.data == "key3":
        next_menu2 = types.InlineKeyboardMarkup()
        key6 = types.InlineKeyboardButton(text='Кнопка 6', callback_data='key6')
        back = types.InlineKeyboardButton(text='Назад', callback_data='mainmenu')
        next_menu2.add(key6, back)
        bot.edit_message_text('Это меню уровня 2, для кнопки3!', call.message.chat.id, call.message.message_id,
                              reply_markup=next_menu2)

bot.polling()
