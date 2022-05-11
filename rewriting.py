import random, string
from menu import Menu
from bot import bot


class Rewriting:
    # all rooms instances
    # {
    #  %user_id%: {
    #   "word": string,
    #   "participants": array<string>,
    #   "started": boolean
    #  }
    # }
    rooms = {}

    def __init__(self):
        print('[success] rewriting game initialized')

    @classmethod
    def showRooms(cls, chat_id):
        seed = cls.generateRandomWord(5)
        print(list(cls.rooms.keys()))
        Menu(f"Доступные комнаты{seed}", [str(i) for i in list(cls.rooms.keys())])

        bot.send_message(chat_id, text=f"Доступные комнаты:", reply_markup=Menu.getMenu(f"Доступные комнаты{seed}"))

    @classmethod
    def joinRoom(cls, chat_id, joiningRoom):
        if(joiningRoom in cls.rooms):
            print(cls.rooms[joiningRoom])
            if cls.rooms[joiningRoom]["started"] == False:
                cls.rooms[joiningRoom]["participants"].append(chat_id)
                bot.send_message(joiningRoom, f"Новый участник в комнате: {chat_id}, всего {len(cls.rooms[joiningRoom]['participants'])} участников")
                return True
            else:
                return False
        else:
            return False
    @classmethod
    def startRoom(cls, chat_id):
        if(chat_id in cls.rooms):
            currentRoom = cls.rooms[chat_id]
            currentRoom["started"] = True
            for i in currentRoom["participants"]:
                bot.send_message(i, text="Игра началась, загаданное слово: " + currentRoom["word"], reply_markup=Menu.getMenu('Основное меню'))
    @classmethod
    def createRoom(cls, chat_id):
        seed = cls.generateRandomWord(5)
        if chat_id not in cls.rooms:
            cls.rooms[chat_id] = {
                "word": seed,
                "participants": [chat_id],
                "started": False
            }
            return True
        else:
            return False
    @classmethod
    def validateMessage(cls, chat_id, msg):
        for key in cls.rooms:
            print(cls.rooms[key])
            if chat_id in cls.rooms[key]['participants']:
                if msg == cls.rooms[key]['word']:
                    bot.send_message(chat_id, text=f"Вы победили в игре, ID{ key }")
                    cls.rooms[key]["participants"].remove(chat_id)
                    for i in cls.rooms[key]["participants"]:
                        bot.send_message(i, text=f"Вы проиграли игроку, ID{ chat_id }", reply_markup=Menu.getMenu("Основное меню"))
                    del cls.rooms[key]
                    return True
                else:
                    return False
        return False

    @classmethod
    def generateRandomWord(cls, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))


rewriting = Rewriting()
