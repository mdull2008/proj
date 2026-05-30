from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from admin_win import AdminWindow
from db import proverit_admin, proverit_user
from user_win import UserWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход")
        self.resize(350, 180)

        self.login = QLineEdit()
        self.parol = QLineEdit()
        self.parol.setEchoMode(QLineEdit.Password)

        self.knopka = QPushButton("Войти")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Логин"))
        layout.addWidget(self.login)
        layout.addWidget(QLabel("Пароль"))
        layout.addWidget(self.parol)
        layout.addWidget(self.knopka)
        self.setLayout(layout)

        self.knopka.clicked.connect(self.vhod)
        self.admin_okno = None
        self.user_okno = None

    def vhod(self):
        log = self.login.text().strip()
        pas = self.parol.text().strip()
        if log == "" or pas == "":
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return
        if proverit_admin(log, pas):
            self.admin_okno = AdminWindow()
            self.admin_okno.show()
            self.close()
            return
        user = proverit_user(log, pas)
        if user:
            self.user_okno = UserWindow(user)
            self.user_okno.show()
            self.close()
            return
        QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
