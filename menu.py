from telebot import types


# -----------------------------------------------------------------------
class Menu:
    markups = {}

    def __init__(self, name, buttons=None):
        self.__class__.markups[name] = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        self.__class__.markups[name].add(*buttons)  # Обратите внимание - звёздочка используется для распаковки списка

    @classmethod
    def getMenu(cls, name):
        return cls.markups.get(name)


main_menu = Menu("Основное меню", buttons=["Мультиплеер", "Игра",  "Первая кнопка меню", "Вторая кнопка меню", "Об авторе", "Получить оскорбление", "Курс доллара", "Курс евро", "Получить анекдот"])
highlow_menu = Menu("Игра", buttons=["Выше", "Ниже"])