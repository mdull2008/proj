import time

from users import Users


class ATMmachine:
    def __init__(self, bank_id, amount_cash, atm_limit, banks):
        self.bank_id = bank_id
        self.amount_cash = amount_cash
        self.atm_limit = atm_limit
        self.banks = banks
        self.user = None
        self.user_bank = None
        self.client = None
        self.pin_errors = 0
        self.withdraw_today = 0

    @classmethod
    def control_input_digital(cls, text):
        while True:
            value = input(text)
            if value.isdigit():
                return int(value)
            print("Нужно ввести число")

    def reset(self):
        self.user = None
        self.user_bank = None
        self.client = None
        self.pin_errors = 0
        self.withdraw_today = 0

    def find_in_all_banks(self, card_number):
        for bank in self.banks:
            user = bank.get_user(card_number)
            if user:
                return user, bank
        return None, None

    def find_recipient(self, number):
        for bank in self.banks:
            user = bank.get_user(number)
            if user:
                return user, bank
        return None, None

    def validation_card(self, card_number):
        user, bank = self.find_in_all_banks(card_number)
        if not user:
            print("Карты нет в системе")
            return False
        if user["card_blocked"] != "0":
            print("Карта заблокирована")
            return False
        return True

    def blocking_card(self):
        if not self.client:
            return
        uid = self.client["user_id"]
        self.user_bank.users_card_database[uid]["card_blocked"] = "1"
        self.user_bank.save_users()
        print("Карта заблокирована")
        self.reset()

    def check_pin(self, pin):
        if pin == self.client["card_pin"]:
            return True
        self.pin_errors += 1
        left = 3 - self.pin_errors
        if left > 0:
            print("Неверный пин. Осталось попыток:", left)
        else:
            print("Пин неверный три раза")
            self.blocking_card()
        return False

    def confirm(self):
        print("Подтверждение через 3 секунды...")
        for sec in range(3, 0, -1):
            print(sec)
            time.sleep(1)
        print("Операция подтверждена")

    def view_balance(self):
        print("Баланс:", self.client["card_balance"], "руб.")

    def withdraw(self):
        amount = self.control_input_digital("Сумма снятия: ")
        if amount <= 0:
            print("Сумма должна быть больше нуля")
            return
        if amount > self.client["card_balance"]:
            print("На карте не хватает денег")
            return
        if amount > self.amount_cash:
            print("В банкомате нет такой суммы")
            return
        if self.withdraw_today + amount > self.atm_limit:
            print("Превышен лимит снятия за сутки")
            return
        self.confirm()
        uid = self.client["user_id"]
        self.user_bank.users_card_database[uid]["card_balance"] -= amount
        self.client["card_balance"] -= amount
        self.amount_cash -= amount
        self.withdraw_today += amount
        self.user_bank.save_users()
        print("Снято:", amount, "руб.")

    def deposit(self):
        amount = self.control_input_digital("Сумма внесения: ")
        if amount <= 0:
            print("Сумма должна быть больше нуля")
            return
        self.confirm()
        uid = self.client["user_id"]
        self.user_bank.users_card_database[uid]["card_balance"] += amount
        self.client["card_balance"] += amount
        self.amount_cash += amount
        self.user_bank.save_users()
        print("Внесено:", amount, "руб.")

    def transfer(self):
        number = input("Номер карты или телефона получателя: ").strip()
        if number == self.client["card_number"] or number == self.client["phone_number"]:
            print("Нельзя перевести себе")
            return
        recipient, rec_bank = self.find_recipient(number)
        if not recipient:
            print("Получатель не найден")
            return
        if recipient["card_blocked"] != "0":
            print("Карта получателя заблокирована")
            return
        amount = self.control_input_digital("Сумма перевода: ")
        if amount <= 0:
            print("Сумма должна быть больше нуля")
            return
        if amount > self.client["card_balance"]:
            print("На карте не хватает денег")
            return
        self.confirm()
        sender_id = self.client["user_id"]
        self.user_bank.users_card_database[sender_id]["card_balance"] -= amount
        self.client["card_balance"] -= amount
        rec_id = recipient["user_id"]
        rec_bank.users_card_database[rec_id]["card_balance"] += amount
        self.user_bank.save_users()
        rec_bank.save_users()
        print("Перевод выполнен")

    def show_menu(self):
        print()
        print("1 - Баланс")
        print("2 - Снять наличные")
        print("3 - Внести наличные")
        print("4 - Перевод")
        print("0 - Выход")
        choice = input("Выберите пункт: ").strip()
        if choice == "1":
            self.view_balance()
        elif choice == "2":
            self.withdraw()
        elif choice == "3":
            self.deposit()
        elif choice == "4":
            self.transfer()
        elif choice == "0":
            print("До свидания")
            self.reset()
            return False
        else:
            print("Нет такого пункта")
        return True

    def start_session(self):
        card = input("Вставьте карту (16 цифр), q - выход: ").strip()
        if card == "q":
            return False
        if len(card) != 16 or not card.isdigit():
            print("Номер карты должен быть 16 цифр")
            return True
        if not self.validation_card(card):
            return True
        user, bank = self.find_in_all_banks(card)
        self.client = user
        self.user_bank = bank
        self.user = Users(card, bank.bank_id)
        if bank.bank_id == self.bank_id:
            print("Добрый день,", user["card_owner"])
        else:
            print("Добрый день!")
        pin = input("Введите пин: ").strip()
        if not self.check_pin(pin):
            if self.client:
                return True
            return True
        while True:
            if not self.show_menu():
                break
        return True
