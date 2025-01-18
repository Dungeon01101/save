#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
import datetime
import telebot
import sqlite3 

from telebot import types

API_TOKEN = '7622630770:AAHu_b5OrPxPfwTNqphMN688X2wSwx2l5RU'

bot = telebot.TeleBot(API_TOKEN)

admins = []

you_is_admin = False

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Посмотреть историю сообщений")
    markup.add(item1)
    bot.reply_to(message, """Привет, я Бот для сохранения переписки. Я здесь, чтобы сохранять всё, что вы мне написали """, parse_mode='html', reply_markup=markup)
    if message.from_user.id in admins:
        bot.send_message(message.chat.id, 'вы админ')
        you_is_admin = True
    else:
        bot.send_message(message.chat.id, 'вы не админ')

@bot.message_handler(content_types=['text'])
def answer(message):
    if message.chat.type == 'private':
        if message.text == 'Посмотреть историю сообщений':
            bot.send_message(message.chat.id, 'Введите ключ')
            def process_reply(message):
                if message.text != '3123kdcvws*&ft8y321':
                    bot.send_message(message.chat.id, 'Вы ввели неправильный ключ')
                else:
                    bot.send_message(message.chat.id, 'Вы ввели правильный ключ')
                    admins.append(message.from_user.id)
                    print(admins)
            bot.register_next_step_handler(message, process_reply)           
# Handle all other messages with content_type 'text' (content_types defaults to ['text'])

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    text = message.text
    date = datetime.datetime.fromtimestamp(message.date)
    chat_id = message.chat.id
    user_id = message.from_user.id

    con = sqlite3.connect('history_db.db')
    with con:
        con.execute("INSERT INTO history (text, date, chat_id, user_id) VALUES (?, ?, ?, ?)", (text, date, chat_id, user_id))
        con.commit()
    #bot.reply_to(message, message.text)


bot.infinity_polling()
