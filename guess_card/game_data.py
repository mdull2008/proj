import random
from dataclasses import dataclass


@dataclass
class Colors:
    value: str


@dataclass
class Suits:
    value: str


@dataclass
class WinLose:
    win: list
    lose: list

    def pick_win(self):
        return random.choice(self.win)

    def pick_lose(self):
        return random.choice(self.lose)
