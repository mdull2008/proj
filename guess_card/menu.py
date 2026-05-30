class Menu:
    data = {
        "color": "Выберите цвет масти:",
        "suit": "Выберите масть",
        "rank": "Выберите карту:",
        "result": "Результат",
        "again": "1. Продолжить игру\n2. Выход",
    }

    @classmethod
    def get(cls, key):
        return cls.data[key]
