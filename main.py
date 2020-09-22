import time
import telebot
from telebot import types
from datetime import datetime, timedelta
from threading import Thread
from config import Config

# Global variables
cfg = Config()
bot = telebot.TeleBot(cfg.token)
DaysOfWeek = ["mon", "tue", "wed", "thu", "fri", "sat", "san"]
current_week = cfg.getDataStr("current_week")
myID = cfg.getDataStr("myID")
timePickToday = (7,00)
timePickTomorrow = (20,00)
call_data_weekday = ""

# <Markups>

# generate methods

def ReplyKeyboardGenerate(*args):
    for i in args:
        yield types.KeyboardButton(i)

def InlineKeyboardGenerate(*args):
    for i in args:
        yield types.InlineKeyboardButton(i[0],callback_data=i[1])

# Main markups
mainMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
items = ReplyKeyboardGenerate("Расписание")
mainMarkup.add(*[i for i in items])

# Schedule markup
scheduleMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
items = ReplyKeyboardGenerate("Сегодня", "Завтра", "Полное расписание", "Выбрать день недели")
scheduleMarkup.add(*[i for i in items])

# All week markup
AllInlinemarkup = types.InlineKeyboardMarkup(row_width=1)
items = InlineKeyboardGenerate( ("Понедельник", "mon"), ("Вторник", "tue"), ("Среда", "wed"),
("Четверг", "thu"), ("Пятница", "fri"), ("Суббота", "sat"),("Воскресенье", "san"))
AllInlinemarkup.add(*[i for i in items])

# Parity markup
Paritymarkup = types.InlineKeyboardMarkup(row_width=1)
items = InlineKeyboardGenerate( ("Четная", "even"), ("Нечетная", "odd"))
Paritymarkup.add(*[i for i in items])

# </Markups>

# <Help methods>

def GenerateFullSchedule() -> str:
    res = ""
    for i in range(6):
        res += cfg.getData(i) + ("\n\n" if i < 5 else "")
    return res

def GetDayOfWeek() -> int:
    return datetime.now().weekday()

def swapParity(parity: str) -> str:
    if(parity == "odd"):
        return "even"
    else:
        return "odd"

def GetTomorrow():
    res = datetime.now().weekday() + 1
    parity = current_week
    if res > 6:
        res = 0
        parity = swapParity(parity)
    return res, parity

# </HelpMethods>

# <TimeMetods>

def Timer():
    while True:
        t = datetime.now()
        turple = (t.hour,t.minute)
        if(tuple == timePickToday):
            bot.send_message(myID,cfg.getData(GetDayOfWeek()))
        elif(turple == timePickTomorrow):
            bot.send_message(myID,cfg.getData(*GetTomorrow()))
        if(datetime.now().weekday() == 6 and turple == timePickTomorrow):
            cfg.swapParity()
        time.sleep(60)

Thread(target=Timer, daemon=True).start()
# </TimeMethods>

# <BotMethods>

@bot.message_handler(commands=['start'])
def welcome(message):

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\n\
Я - <b>{1.first_name}</b>, бот созданный чтобы помочь с учебой.".format(message.from_user, bot.get_me()),
		parse_mode='html', reply_markup=(mainMarkup if message.chat.id == myID else None))

@bot.message_handler(content_types=['text'])
def mes(message):
    if message.chat.type == 'private':
        mes = message.text.lower()
        chatId = message.chat.id
        answer = False
        if chatId == myID:
            answer = True
            if mes == 'расписание':
                bot.send_message(chatId, 'Какое?', reply_markup=scheduleMarkup)
                isWork = False

            elif mes == 'сегодня':
                bot.send_message(chatId, cfg.getData(GetDayOfWeek()), reply_markup=mainMarkup)

            elif mes == 'завтра':
                bot.send_message(chatId, cfg.getData(*GetTomorrow()), reply_markup=mainMarkup)

            elif mes == 'полное расписание':
                bot.send_message(chatId, GenerateFullSchedule(), reply_markup=mainMarkup)

            elif mes == "выбрать день недели":
                bot.send_message(chatId, 'День недели?', reply_markup=AllInlinemarkup)

            else:
                answer = False

        if not answer:
            if mes == "спасибо":
                bot.send_message(chatId, 'Позязя)) (^_^)')

            else:
                bot.send_message(chatId, 'Прости я не знаю что ответить 😢')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global call_data_weekday
    if call.message and call.data in DaysOfWeek:
        chatId = call.message.chat.id
        bot.edit_message_text(chat_id=chatId, message_id=call.message.message_id, text='День недели?',reply_markup=None)
        bot.send_message(chatId, "Четная или нечетная?", reply_markup=Paritymarkup)
        call_data_weekday = call.data
    elif call.message and call.data in ["odd", "even"]:
        chatId = call.message.chat.id
        bot.edit_message_text(chat_id=chatId, message_id=call.message.message_id, text="Четная или нечетная?",reply_markup=None)
        bot.send_message(chatId, cfg.getDataStr(call.data)[call_data_weekday], reply_markup=mainMarkup)

# </BotMethods>

# RUN
bot.polling(none_stop=True)
