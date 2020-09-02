import requests
import random
import time
import json
import telebot
from telebot import types
from datetime import datetime, date
from threading import Thread
from config import Config
import os

cfg = Config()
bot = telebot.TeleBot(cfg.token)
DaysOfWeek = "mon tue wed thu fri sat"
myID = cfg.getDataStr("myID")
timePickToday = (7,00)
timePickTomorrow = (20,00)

# <Markups>

# Main markups
mainMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
items = [
types.KeyboardButton("Расписание")
]
mainMarkup.add(*items)

# Schedule markup
scheduleMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
items = [
types.KeyboardButton("Сегодня"),
types.KeyboardButton("Завтра"),
types.KeyboardButton("Полное расписание"),
types.KeyboardButton("Выбрать день недели")
]
scheduleMarkup.add(*items)

# All week markup
AllInlinemarkup = types.InlineKeyboardMarkup(row_width=1)
items = [
types.InlineKeyboardButton("Понедельник", callback_data="mon"),
types.InlineKeyboardButton("Вторник", callback_data="tue"),
types.InlineKeyboardButton("Среда", callback_data="wed"),
types.InlineKeyboardButton("Четверг", callback_data="thu"),
types.InlineKeyboardButton("Пятница", callback_data="fri"),
types.InlineKeyboardButton("Суббота", callback_data="sat")
]
AllInlinemarkup.add(*items)

# </Markups>

# <Help methods>

def GenerateFullSchedule():
    res = ""
    for i in range(7):
        res += cfg.getData(i) + ("\n\n" if i < 6 else "")
    return res

def GetDayOfWeek():
    return datetime.now().weekday()

def GetTomorrow():
    res = datetime.now().weekday() + 1
    if res > 6: res = 0
    return res

# </HelpMethods>

# <TimeMetods>

def Timer():
    while True:
        t = datetime.now()
        turple = (t.hour,t.minute)
        if(tuple == timePickToday):
            bot.send_message(myID,cfg.getData(GetDayOfWeek()))
        elif(turple == timePickTomorrow):
            bot.send_message(myID,cfg.getData(GetTomorrow()))
        time.sleep(60)

Thread(target=Timer).start()
# </TimeMethods>

# <BotMethods>

@bot.message_handler(commands=['start'])
def welcome(message):

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы помочь с учебой.".format(message.from_user, bot.get_me()),
		parse_mode='html', reply_markup=mainMarkup)



@bot.message_handler(content_types=['text'])
def mes(message):
    if message.chat.type == 'private':

        if message.text == 'Расписание':
            bot.send_message(message.chat.id, 'Какое?', reply_markup=scheduleMarkup)

        elif message.text == 'Сегодня':
            bot.send_message(message.chat.id, cfg.getData(GetDayOfWeek()), reply_markup=mainMarkup)

        elif message.text == 'Завтра':
            bot.send_message(message.chat.id, cfg.getData(GetTomorrow()), reply_markup=mainMarkup)

        elif message.text == 'Полное расписание':
            bot.send_message(message.chat.id, GenerateFullSchedule(), reply_markup=mainMarkup)

        elif message.text == "Выбрать день недели":
            bot.send_message(message.chat.id, 'День недели?', reply_markup=AllInlinemarkup)

        elif message.text.lower() == "спасибо":
            bot.send_message(message.chat.id, 'Позязя)) (^_^)')

        else:
            bot.send_message(message.chat.id, 'Пользуйся к  нопочками)')



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data in DaysOfWeek:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='День недели?',reply_markup=None)
                bot.send_message(call.message.chat.id, cfg.getDataStr(call.data), reply_markup=mainMarkup)


    except Exception as e:
        bot.send_message(call.message.chat.id, 'Ой, кажется я сломалась(\n' + str(e))

# </BotMethods>

# RUN
bot.polling(none_stop=True)
