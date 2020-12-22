import time
import telebot
from telebot import types
from datetime import datetime, timedelta
from threading import Thread
from config import Config

# Global variables
cfg = Config()
bot = telebot.TeleBot(cfg.token)
myID = cfg.get_data_str("myID")

# <Markups>

# generate methods

def ReplyKeyboardGenerate(*args):
    for i in args:
        yield types.KeyboardButton(i)

# Main markups

# </Markups>

# <BotMethods>

@bot.message_handler(commands=['start'])
def welcome(message):

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\n\
Я - <b>{1.first_name}</b>, бот созданный @KawaiiAxonny.".format(message.from_user, bot.get_me()),
		parse_mode='html', reply_markup=(mainMarkup if message.chat.id == myID else None))

@bot.message_handler(content_types=['text'])
def mes(message):
    if message.chat.type == 'private':
        mes = message.text.lower()
        chatId = message.chat.id

# </BotMethods>

# RUN
bot.polling(none_stop=True)
