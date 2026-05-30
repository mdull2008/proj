import json
import os


class Bank:
    users_card_database = {}

    def __init__(self, filename):
        self.bank_id = "Bank_" + str(id(self))
        self.filename = filename
        self.load_users()

    def get_user(self, number):
        for user_id, user in self.users_card_database.items():
            if user["card_number"] == number or user["phone_number"] == number:
                result = user.copy()
                result["user_id"] = user_id
                result["bank_id"] = self.bank_id
                return result
        return None

    def save_users(self):
        folder = os.path.dirname(self.filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
        data = {}
        for user_id, user in self.users_card_database.items():
            u = user.copy()
            if "bank_id" in u:
                del u["bank_id"]
            data[str(user_id)] = u
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_users(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.users_card_database = {}
        for key, user in data.items():
            user_id = int(key)
            user["bank_id"] = self.bank_id
            self.users_card_database[user_id] = user
