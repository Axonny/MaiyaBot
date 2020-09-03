import time
import telebot
from telebot import types
from datetime import datetime, timedelta
from threading import Thread
from config import Config
from database import Database

# Global variables
cfg = Config()
db = Database()
bot = telebot.TeleBot(cfg.token)
DaysOfWeek = ["mon", "tue", "wed", "thu", "fri", "sat", "san"]
myID = cfg.getDataStr("myID")
timePickToday = (7,00)
timePickTomorrow = (20,00)

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
items = ReplyKeyboardGenerate("Добавить ДЗ", "Напоминания / ДЗ","Удалить ДЗ", "Расписание")
mainMarkup.add(*[i for i in items])

# Schedule markup
scheduleMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
items = ReplyKeyboardGenerate("Сегодня", "Завтра", "Полное расписание", "Выбрать день недели")
scheduleMarkup.add(*[i for i in items])

# Work markup
WorkMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
items = ReplyKeyboardGenerate("Сегодня", "Завтра", "Выбрать дату", "Выбрать день недели")
WorkMarkup.add(*[i for i in items])

# All week markup
AllInlinemarkup = types.InlineKeyboardMarkup(row_width=1)
items = InlineKeyboardGenerate( ("Понедельник", "mon"), ("Вторник", "tue"), ("Среда", "wed"),
("Четверг", "thu"), ("Пятница", "fri"), ("Суббота", "sat"),("Воскресенье", "san"))
AllInlinemarkup.add(*[i for i in items])

# Input markup
InputMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
items = ReplyKeyboardGenerate("Отмена")
InputMarkup.add(*[i for i in items])

# </Markups>

# <Help methods>

def GenerateFullSchedule() -> str:
    res = ""
    for i in range(6):
        res += cfg.getData(i) + ("\n\n" if i < 5 else "")
    return res

def GetDayOfWeek() -> int:
    return datetime.now().weekday()

def GetTomorrow():
    res = datetime.now().weekday() + 1
    if res > 6: res = 0
    return res

def ConveertWeekdayToDate(day: str) -> str:
    n = DaysOfWeek.index(day)
    d = datetime.now()
    d += timedelta(days=(n-d.weekday()))
    return f"{d.day}.{d.month}"


def GetWeekdayWork(id: int,day: str) -> str:
    date = ConveertWeekdayToDate(day)
    return GetDateWork(id,date)

def GetDateWork(id: int,date: str) -> str:
    res = date + '\n'
    tasks = db.getDataDate(id,date)
    if(tasks):
        for task in tasks:
            res += task["data"] + '\n'
    else:
        res += "Заданий нет, отдыхай)"
    return res

def CheckValidDate(date: str) -> bool:
    try:
        dd,mm = map(int,date.split("."))
        datetime(2020,mm,dd)
        return True
    except: return False

def AddWeekdayTask(id:int, day: str):
    date = ConveertWeekdayToDate(day)
    return date

def GenerateInlineTasks(id):
    db.DelitePastTasks(id)
    fullData = db.data[str(id)]["tasks"]
    Inlinemarkup = types.InlineKeyboardMarkup(row_width=1)
    items = [types.InlineKeyboardButton("Отмена",callback_data=f"dback")]
    for index,elem in enumerate(fullData):
        s = f"({elem['date']}) {elem['data']}"
        items.append(types.InlineKeyboardButton(s,callback_data=f"d{index}"))
    Inlinemarkup.add(*items)
    print(fullData,items)
    return Inlinemarkup

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

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\n\
Я - <b>{1.first_name}</b>, бот созданный чтобы помочь с учебой.".format(message.from_user, bot.get_me()),
		parse_mode='html', reply_markup=mainMarkup)



@bot.message_handler(content_types=['text'])
def mes(message):
    if message.chat.type == 'private':
        mes = message.text.lower()
        chatId = message.chat.id
        isWork, isDateInput, isWorkAdd, isWorkInput = db.IsData(chatId,"isWork","isDateInput","isWorkAdd","isWorkInput")

        if mes == "отмена":
            bot.send_message(chatId, 'Отменяю',reply_markup=mainMarkup)
            isWork, isDateInput, isWorkAdd, isWorkInput = False,False,False,False

        elif isWorkInput:
            db.addDataProfile(chatId,mes)
            bot.send_message(chatId, 'Готово!',reply_markup=mainMarkup)
            isWorkInput = False

        elif isDateInput:
            if(CheckValidDate(mes)):
                isDateInput = False
                if isWork:
                    bot.send_message(chatId,GetDateWork(chatId,mes),reply_markup=mainMarkup)
                    isWork = False
                elif isWorkAdd:
                    db.SetDateTask(chatId,mes)
                    bot.send_message(chatId, "Напиши о чем напомнить", reply_markup=InputMarkup)
                    isWorkAdd = False
                    isWorkInput = True
            else:
                bot.send_message(chatId, 'Некоректный ввод!')

        elif mes == "добавить дз":
            bot.send_message(chatId, 'На какой день?', reply_markup=WorkMarkup)
            isWorkAdd = True

        elif mes == 'напоминания / дз':
            bot.send_message(chatId, 'На какой день?', reply_markup=WorkMarkup)
            isWork = True

        elif mes == "удалить дз":
            bot.send_message(chatId, 'Какое удаляем?', reply_markup=GenerateInlineTasks(chatId))

        elif mes == 'расписание':
            bot.send_message(chatId, 'Какое?', reply_markup=scheduleMarkup)
            isWork = False

        elif mes == 'сегодня':
            d = datetime.now()
            if isWork:
                bot.send_message(chatId, GetDateWork(chatId, f"{d.day}.{d.month}"), reply_markup=mainMarkup)
                isWork = False
            elif isWorkAdd:
                db.SetDateTask(chatId,f"{d.day}.{d.month}")
                bot.send_message(chatId, "Напиши о чем напомнить", reply_markup=InputMarkup)
                isWorkAdd = False
                isWorkInput = True
            else:
                bot.send_message(chatId, cfg.getData(GetDayOfWeek()), reply_markup=mainMarkup)

        elif mes == 'завтра':
            d = datetime.now() + timedelta(days=1)
            if isWork:
                bot.send_message(chatId,GetDateWork(chatId,f"{d.day}.{d.month}"), reply_markup=mainMarkup)
                isWork = False
            elif isWorkAdd:
                db.SetDateTask(chatId,f"{d.day}.{d.month}")
                bot.send_message(chatId, "Напиши о чем напомнить", reply_markup=InputMarkup)
                isWorkAdd = False
                isWorkInput = True
            else:
                bot.send_message(chatId, cfg.getData(GetTomorrow()), reply_markup=mainMarkup)

        elif mes == 'полное расписание':
            bot.send_message(chatId, GenerateFullSchedule(), reply_markup=mainMarkup)

        elif mes == "выбрать день недели":
            bot.send_message(chatId, 'День недели?', reply_markup=AllInlinemarkup)

        elif mes == "выбрать дату":
            bot.send_message(chatId, 'Введите дату в формате dd.mm', reply_markup=InputMarkup)
            isDateInput = True

        elif mes == "спасибо":
            bot.send_message(chatId, 'Позязя)) (^_^)')

        else:
            bot.send_message(chatId, 'Пользуйся кнопочками)')

        db.SetData(chatId,"isWork",isWork)
        db.SetData(chatId,"isDateInput",isDateInput)
        db.SetData(chatId,"isWorkAdd",isWorkAdd)
        db.SetData(chatId,"isWorkInput",isWorkInput)



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message and call.data in DaysOfWeek:
        chatId = call.message.chat.id
        isWork,isWorkAdd,isWorkInput = db.IsData(chatId,"isWork","isWorkAdd", "isWorkInput")
        if isWork:
            bot.edit_message_text(chat_id=chatId, message_id=call.message.message_id, text='День недели?',reply_markup=None)
            bot.send_message(chatId, GetWeekdayWork(chatId,call.data), reply_markup=mainMarkup)
            isWork = False
        elif isWorkAdd:
            db.SetDateTask(chatId,AddWeekdayTask(chatId, call.data))
            bot.edit_message_text(chat_id=chatId, message_id=call.message.message_id, text='День недели?',reply_markup=None)
            bot.send_message(chatId, "Напиши о чем напомнить", reply_markup=InputMarkup)
            isWorkAdd = False
            isWorkInput = True
        else:
            bot.edit_message_text(chat_id=chatId, message_id=call.message.message_id, text='День недели?',reply_markup=None)
            bot.send_message(chatId, cfg.getDataStr(call.data), reply_markup=mainMarkup)

        db.SetData(chatId,"isWork",isWork)
        db.SetData(chatId,"isWorkAdd",isWorkAdd)
        db.SetData(chatId,"isWorkInput",isWorkInput)
    elif call.message and call.data:
        if( call.data[1:] == "back"):
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Отменено',reply_markup=None)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Удалено!',reply_markup=None)
        try: db.DeliteTask(call.message.chat.id,int(call.data[1:]))
        except: pass

# </BotMethods>

# RUN
bot.polling(none_stop=True)
