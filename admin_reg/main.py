import hashlib
import random
import sqlite3
import tkinter as tk
from tkinter import messagebox

DB = "admins.db"


def hash_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Admins ("
        "id INTEGER PRIMARY KEY, fsp TEXT, username TEXT UNIQUE, "
        "password TEXT, email TEXT)"
    )
    cur.execute("SELECT COUNT(*) FROM Admins")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO Admins (fsp, username, password, email) VALUES (?, ?, ?, ?)",
            ("Мамедова Мадина Айдынгызы", None, None, None),
        )
    con.commit()
    con.close()


class App:
    def __init__(self):
        init_db()
        self.okno = tk.Tk()
        self.okno.title("Админы")
        self.okno.geometry("420x320")

        self.ramka = tk.Frame(self.okno)
        self.ramka.pack(fill="both", expand=True, padx=20, pady=20)

        self.kod = None
        self.fsp = None

        self.pokazat_vhod()

    def ochistit(self):
        for w in self.ramka.winfo_children():
            w.destroy()

    def pokazat_vhod(self):
        self.ochistit()
        tk.Label(self.ramka, text="Вход").pack(pady=5)
        self.pole_login = tk.Entry(self.ramka, width=30)
        self.pole_login.pack(pady=3)
        tk.Label(self.ramka, text="Пароль").pack()
        self.pole_parol = tk.Entry(self.ramka, width=30, show="*")
        self.pole_parol.pack(pady=3)
        self.reg_flag = tk.IntVar()
        tk.Checkbutton(self.ramka, text="Регистрация", variable=self.reg_flag).pack(
            pady=8
        )
        tk.Button(self.ramka, text="Войти", command=self.vhod).pack(pady=5)

    def vhod(self):
        if self.reg_flag.get() == 1:
            self.pokazat_reg_fsp()
            return
        login = self.pole_login.get().strip()
        parol = self.pole_parol.get().strip()
        if login == "" or parol == "":
            messagebox.showwarning("Ошибка", "Заполните поля")
            return
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute(
            "SELECT fsp FROM Admins WHERE username=? AND password=?",
            (hash_text(login), hash_text(parol)),
        )
        row = cur.fetchone()
        con.close()
        if row:
            self.pokazat_uspeshno(row[0])
        else:
            messagebox.showwarning("Ошибка", "Неверный логин или пароль")

    def pokazat_reg_fsp(self):
        self.ochistit()
        tk.Label(self.ramka, text="Регистрация").pack(pady=5)
        tk.Label(self.ramka, text="Введите ФИО").pack()
        self.pole_fsp = tk.Entry(self.ramka, width=35)
        self.pole_fsp.pack(pady=5)
        self.label_kod = tk.Label(self.ramka, text="")
        self.label_kod.pack(pady=5)
        tk.Button(self.ramka, text="Получить код", command=self.poluchit_kod).pack(
            pady=5
        )
        tk.Button(self.ramka, text="Назад", command=self.pokazat_vhod).pack()

    def poluchit_kod(self):
        fsp = self.pole_fsp.get().strip()
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute(
            "SELECT id, username FROM Admins WHERE fsp=?",
            (fsp,),
        )
        row = cur.fetchone()
        con.close()
        if not row:
            messagebox.showwarning(
                "Ошибка",
                "Вас нет в базе. Обратитесь к главному администратору",
            )
            return
        if row[1] is not None:
            messagebox.showwarning("Ошибка", "Профиль уже создан")
            return
        self.fsp = fsp
        self.kod = str(random.randint(100000, 999999))
        self.label_kod.config(text="Код: " + self.kod)
        self.pokazat_reg_kod()

    def pokazat_reg_kod(self):
        self.ochistit()
        tk.Label(self.ramka, text="Введите код").pack(pady=5)
        self.pole_kod = tk.Entry(self.ramka, width=20)
        self.pole_kod.pack(pady=5)
        tk.Button(self.ramka, text="Проверить", command=self.proverit_kod).pack(
            pady=5
        )
        tk.Button(self.ramka, text="Назад", command=self.pokazat_reg_fsp).pack()

    def proverit_kod(self):
        if self.pole_kod.get().strip() != self.kod:
            messagebox.showwarning("Ошибка", "Неверный код")
            return
        self.pokazat_reg_login()

    def pokazat_reg_login(self):
        self.ochistit()
        tk.Label(self.ramka, text="Создайте профиль").pack(pady=5)
        tk.Label(self.ramka, text="Логин").pack()
        self.pole_new_login = tk.Entry(self.ramka, width=30)
        self.pole_new_login.pack(pady=3)
        tk.Label(self.ramka, text="Пароль").pack()
        self.pole_new_parol = tk.Entry(self.ramka, width=30, show="*")
        self.pole_new_parol.pack(pady=3)
        tk.Label(self.ramka, text="Повтор пароля").pack()
        self.pole_new_parol2 = tk.Entry(self.ramka, width=30, show="*")
        self.pole_new_parol2.pack(pady=3)
        tk.Label(self.ramka, text="Email").pack()
        self.pole_email = tk.Entry(self.ramka, width=30)
        self.pole_email.pack(pady=3)
        tk.Button(self.ramka, text="Сохранить", command=self.sohranit_prof).pack(
            pady=8
        )

    def sohranit_prof(self):
        login = self.pole_new_login.get().strip()
        p1 = self.pole_new_parol.get()
        p2 = self.pole_new_parol2.get()
        email = self.pole_email.get().strip()
        if login == "" or p1 == "":
            messagebox.showwarning("Ошибка", "Заполните логин и пароль")
            return
        if p1 != p2:
            messagebox.showwarning("Ошибка", "Пароли не совпадают")
            return
        h_login = hash_text(login)
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("SELECT id FROM Admins WHERE username=?", (h_login,))
        if cur.fetchone():
            con.close()
            variant = login + str(random.randint(10, 99))
            messagebox.showwarning(
                "Ошибка",
                "Логин занят. Попробуйте: " + variant,
            )
            return
        cur.execute(
            "UPDATE Admins SET username=?, password=?, email=? WHERE fsp=?",
            (h_login, hash_text(p1), email, self.fsp),
        )
        con.commit()
        con.close()
        messagebox.showinfo("Готово", "Регистрация завершена")
        self.pokazat_vhod()

    def pokazat_uspeshno(self, fio):
        self.ochistit()
        tk.Label(self.ramka, text="Вы вошли").pack(pady=10)
        tk.Label(self.ramka, text=fio).pack(pady=5)
        tk.Button(self.ramka, text="Выход", command=self.pokazat_vhod).pack(pady=10)

    def run(self):
        self.okno.mainloop()


if __name__ == "__main__":
    App().run()
