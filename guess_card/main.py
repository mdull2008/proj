import os
from itertools import cycle

from colorama import Fore, Style, init

from card import Card
from game_data import Colors, Suits, WinLose
from menu import Menu

init(autoreset=True)

BLACK = ["♠️", "♣️"]
RED = ["♦️", "♥️"]

messages = WinLose(
    win=["Ты угадал!", "Везучий!", "Попал в яблочко!"],
    lose=["Не угадал", "Мимо", "Не повезло"],
)


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def ask_number(text, options):
    while True:
        print(text)
        for i, item in enumerate(options, 1):
            print("   ", i, ".", item)
        choice = input("> ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice) - 1
        print("Введите номер из списка")


def round_game():
    Card.shuffle_desk_card()
    Card.select_card()

    picked_color = None
    picked_suit = None
    picked_rank = None

    steps = cycle(["color", "suit", "rank"])
    for step in steps:
        clear()
        if step == "color":
            print(Fore.CYAN + Menu.get("color"))
            idx = ask_number("", ["⬛️", "🟥"])
            if idx == 0:
                picked_color = Colors("⬛️")
            else:
                picked_color = Colors("🟥")
        elif step == "suit":
            print(Fore.CYAN + Menu.get("suit"))
            if picked_color.value == "⬛️":
                suits = BLACK
            else:
                suits = RED
            idx = ask_number("", suits)
            picked_suit = Suits(suits[idx])
        elif step == "rank":
            print(Fore.CYAN + Menu.get("rank"))
            cards = []
            for rank in Card.ranks:
                cards.append(rank + picked_suit.value)
            idx = ask_number("", cards)
            picked_rank = cards[idx]
            break

    clear()
    guess = picked_rank
    secret = Card.selected_card
    print(Fore.YELLOW + Menu.get("result"))
    print()
    if guess == secret:
        print(Fore.GREEN + messages.pick_win())
    else:
        print(Fore.RED + messages.pick_lose())
    print("Ваш выбор:", guess)
    print("Карта компьютера:", secret)
    input("Enter...")


def main():
    Card.creatind_desk_cards()

    while True:
        round_game()
        clear()
        print(Fore.MAGENTA + Menu.get("again"))
        while True:
            x = input("> ").strip()
            if x == "1":
                break
            if x == "2":
                print("Пока")
                return
            print("Введите 1 или 2")
        clear()


if __name__ == "__main__":
    main()
