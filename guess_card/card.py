import random


class Card:
    suits = ["♠️", "♣️", "♦️", "♥️"]
    ranks = ["6", "7", "8", "9", "10", "В", "Д", "К", "Т"]
    desk_card = []
    selected_card = None

    @classmethod
    def creatind_desk_cards(cls):
        cls.desk_card = []
        for suit in cls.suits:
            for rank in cls.ranks:
                cls.desk_card.append(rank + suit)

    @classmethod
    def shuffle_desk_card(cls):
        for i in range(3):
            random.shuffle(cls.desk_card)

    @classmethod
    def get_desk_card(cls):
        return cls.desk_card

    @classmethod
    def select_card(cls):
        cls.selected_card = random.choice(cls.desk_card)
        return cls.selected_card
