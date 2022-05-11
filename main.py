# Вариант 1 - самый простой чат бот, просто отзывается
from bot import bot
import requests
import json
from bs4 import BeautifulSoup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from random import randrange
from menu import Menu
from higherlower import HigherLower
from rewriting import Rewriting
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--debug', default="false", help="Доп. вывод информации")
isDebug = parser.parse_args().debug

if(isDebug):
    print("Debugging is on")
# custom functions
def generateButtons():
    if (isDebug):
        print("Line 20: generateButtons()")
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Кнопка 1", callback_data="btn_1"),
               InlineKeyboardButton("Кнопка 2", callback_data="btn_2"))
    return markup

def getInsult():
    if (isDebug):
        print("Line 29: getInsult()")
    return requests.get('https://evilinsult.com/generate_insult.php?lang=ru&amp;type=json')

def getCourse(type):
    if (isDebug):
        print("Line 34: getCourse()")
    res = json.loads(requests.get('https://currate.ru/api/?get=rates&pairs=USDRUB,EURRUB&key=b23092c1b26910ad801656c855c04d23').content)
    if(type == "usd"):
        return res["data"]["USDRUB"]
    if(type == "eur"):
        return res["data"]["EURRUB"]

def getAnecdote():
    if(isDebug):
        print("Line 43: getAnecdote()")

    res = requests.get('https://www.anekdot.ru/').text
    parsedHTML = BeautifulSoup(res, "html.parser")

    foundAnecdote = parsedHTML.select(".texts > .topicbox > .text")[randrange(15)].getText().strip()

    return foundAnecdote


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "btn_1":
        bot.answer_callback_query(call.id, "Нажата первая кнопка")
    elif call.data == "btn_2":
        bot.answer_callback_query(call.id, "Нажата вторая кнопка")


# -----------------------------------------------------------------------
# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(message, res=False):
    chat_id = message.chat.id

    bot.send_message(chat_id, text="{0.first_name}, я работаю".format(message.from_user))


# -----------------------------------------------------------------------
# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    gameInstance = HigherLower(chat_id)

    match ms_text.lower():
        case "доступные комнаты":
            Rewriting.showRooms(chat_id)
        case "создать комнату":
            flag = Rewriting.createRoom(chat_id)
            if flag:
                bot.send_message(chat_id, text="Комната успешно создана", reply_markup=Menu.getMenu("Начать игру"))
            else:
                bot.send_message(chat_id, text="Ошибка при создании комнаты")
        case "начать игру":
            Rewriting.startRoom(chat_id)
        case "игра":
            bot.send_photo(chat_id, photo=gameInstance.getCard("first", chat_id), caption="Игра запущена, первая карта:", reply_markup=Menu.getMenu("Игра"))
        case "кнопки":
            bot.send_message(chat_id, text="Сообщение с кнопками", reply_markup=generateButtons())
        case "меню":
            bot.send_message(chat_id, text="Меню открыто", reply_markup=Menu.getMenu("Основное меню"))
        case "первая кнопка меню":
            bot.send_message(chat_id, text="Нажата первая кнопка меню")
        case "вторая кнопка меню":
            bot.send_message(chat_id, text="Нажата вторая кнопка меню")
        case "об авторе":
            bot.send_photo(chat_id, photo="https://i.pinimg.com/originals/b4/b9/64/b4b9649495d7c5c64d9884ffb44575bf.jpg", caption="Артем Гаспарян, студент 1 курса, 1-МД-20."
            "Направление ИТ-технологии создания цифрового контента")
        case "получить оскорбление":
            insult = getInsult()
            bot.send_message(chat_id, text=insult)
        case "курс доллара":
            course = getCourse('usd')
            bot.send_message(chat_id, text=course)
        case "курс евро":
            course = getCourse('eur')
            bot.send_message(chat_id, text=course)
        case "получить анекдот":
            anecdote = getAnecdote()
            bot.send_message(chat_id, text=anecdote)
        case "выше":
            status = gameInstance.getResults("higher", chat_id)
            if status == True:
                bot.send_photo(chat_id, photo=gameInstance.getCard("second", chat_id), caption="Вы победили, вторая карта:", reply_markup=Menu.getMenu("Основное меню"))
            else:
                bot.send_photo(chat_id, photo=gameInstance.getCard("second", chat_id), caption="Вы проиграли, вторая карта:", reply_markup=Menu.getMenu("Основное меню"))
            gameInstance.resetGame(chat_id)
        case "ниже":
            status = gameInstance.getResults("lower", chat_id)
            if status == True:
                bot.send_photo(chat_id, photo=gameInstance.getCard("second", chat_id), caption="Вы победили, вторая карта:", reply_markup=Menu.getMenu("Основное меню"))
            else:
                bot.send_photo(chat_id, photo=gameInstance.getCard("second", chat_id), caption="Вы проиграли, вторая карта:", reply_markup=Menu.getMenu("Основное меню"))
            gameInstance.resetGame(chat_id)
        case _:
            if ms_text.isdecimal():
                flag = Rewriting.joinRoom(chat_id, int(ms_text))
                if flag:
                    bot.send_message(chat_id, text="Вы успешно присоединились к комнате", reply_markup=Menu.getMenu("Основное меню"))
                else:
                    bot.send_message(chat_id, text="Ошибка при присоединении к комнате", reply_markup=Menu.getMenu("Основное меню"))
            else:
                # if user typed not a command, he's probably trying to type game's string
                Rewriting.validateMessage(chat_id, ms_text.lower())


# -----------------------------------------------------------------------
bot.polling(none_stop = True, interval = 0) # Запускаем бота