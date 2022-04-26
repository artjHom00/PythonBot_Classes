import random, string
from bot import bot


class Rewriting:
    # all games instances
    # {
    #   %randomWord%: [ %chat_id1%, %chat_id2% ]
    # }
    games = {}

    # chat_ids wanting to join the game
    participants = []

    def __init__(self):
        print('[success] rewriting game initialized')

    @classmethod
    def validateMessage(cls, chat_id, msg):
        for key in cls.games:
            if chat_id in cls.games[key]:
                if msg == key:
                    otherParticipant = cls.games[key][1 - cls.games[key].index(chat_id)]
                    bot.send_message(chat_id, text=f"Вы победили игрока, ID{ otherParticipant }")
                    bot.send_message(otherParticipant, text=f"Вы проиграли игроку, ID{ chat_id }")
                    del cls.games[key]
                    return True
                else:
                    return False
        return False

    @classmethod
    def addParticipant(cls, chat_id):
        if chat_id not in cls.participants:
            cls.participants.append(chat_id)

            # if participants array contains enough players to start a new game
            # we call "newGame" method
            if len(cls.participants) % 2 == 0:
                return cls.newGame()

    @classmethod
    def newGame(cls):
        seed = cls.generateRandomWord(5)
        cls.games[seed] = [cls.participants[0], cls.participants[1]]

        bot.send_message(cls.participants[0], text=f'Игра началась, ваш соперник - ID{ cls.participants[1] }.\n Слово: { seed }')
        bot.send_message(cls.participants[1], text=f'Игра началась, ваш соперник - ID{ cls.participants[0] }.\n Слово: { seed }')

        cls.participants.pop(1)
        cls.participants.pop(0)

        return True

    @classmethod
    def generateRandomWord(cls, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))


rewriting = Rewriting()
