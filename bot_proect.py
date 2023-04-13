import telebot
from telebot import types

bot = telebot.TeleBot('6250441055:AAHxwYcMT0l8oWquuYTyJiPQD35vJeTBz4w')

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