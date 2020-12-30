import telebot
import game
import os
import random
import time
from telebot import types
from config import Config

# Global variables
cfg = Config()
bot = telebot.TeleBot(cfg.token)
myID = cfg.get_data_str("myID")
users = {}
words = []
with open("words.txt", "r", encoding='utf-8') as f:
    words = [i.strip() for i in f.readlines()]



def ReplyKeyboardGenerate(*args):
    for i in args:
        yield types.KeyboardButton(i)

mainMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
items = ReplyKeyboardGenerate("Играть")
mainMarkup.add(*[i for i in items])

gameMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
items = ReplyKeyboardGenerate("Закончить")
gameMarkup.add(*[i for i in items])



def send_next_img(chat_id):
    img_name = random.choice(os.listdir("img"))
    name = game.get_img(img_name)
    bot.send_photo(chat_id, photo=game.resize_image(f"img/{img_name}/{name}"))
    users[chat_id]["last_img"] = f"{img_name}/{name}"
    users[chat_id]["answer"] = img_name



@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\n\
Я - <b>{1.first_name}</b>, бот созданный @KawaiiAxonny.".format(message.from_user, bot.get_me()),
		parse_mode='html', reply_markup=mainMarkup)

@bot.message_handler(content_types=['text'])
def mes(message):
    if message.chat.type == 'private':
        mes = message.text.lower()
        chat_id = message.chat.id

        if not chat_id in users:
            users[chat_id] = {
                "in_game": False,
                "last_img": "",
                "answer": ""
            }

        if mes == "играть":
            bot.send_message(chat_id, "Начинаем игру...", reply_markup=gameMarkup)
            users[chat_id]["in_game"] = True
            send_next_img(chat_id)

        elif users[chat_id]["in_game"] and mes == "закончить":
            bot.send_message(chat_id, "Игра закончена", reply_markup=mainMarkup)
            users[chat_id]["in_game"] = False

        elif users[chat_id]["in_game"]:
            bot.send_photo(chat_id, photo=open(f'img/{users[chat_id]["last_img"]}', "rb"))
            if users[chat_id]["answer"] == mes:
                bot.send_message(chat_id, "Правильно", reply_markup=gameMarkup)
            else:
                bot.send_message(chat_id, f'Неправильно, это {users[chat_id]["answer"]}', reply_markup=gameMarkup)
            send_next_img(chat_id)

        else:
            bot.send_message(chat_id, 'чтобы сыграть отправь мне слово "Играть"', reply_markup=mainMarkup)

# RUN
bot.polling(none_stop=True)
