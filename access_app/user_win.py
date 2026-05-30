from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QMessageBox,
    QStackedWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

RAZDELY = [
    ("Бухгалтерия", "buh"),
    ("Кадры", "kadry"),
    ("Управление", "upr"),
    ("Производство", "proiz"),
]


class UserWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("Пользователь: " + user["fio"])
        self.resize(800, 500)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        self.knopki = {}
        self.labels = {}

        for i, (name, key) in enumerate(RAZDELY):
            page = QWidget()
            label = QLabel()
            label.setWordWrap(True)
            self.labels[key] = label
            lay = QVBoxLayout()
            lay.addWidget(label)
            page.setLayout(lay)
            self.stack.addWidget(page)

            action = QAction(name, self)
            action.triggered.connect(lambda checked=False, n=i: self.otkrit(n))
            self.toolbar.addAction(action)
            self.knopki[key] = action

            pravo = user[key]
            if pravo == "запрещен":
                action.setEnabled(False)
                label.setText(name + "\nДоступ запрещен")
            elif pravo == "просмотр":
                label.setText(
                    name + "\nВам предоставлен доступ только для просмотра"
                )
            else:
                label.setText(name + "\nВам предоставлен полный доступ")

        self.stack.setCurrentIndex(0)

    def otkrit(self, nomer):
        keys = [k for _, k in RAZDELY]
        key = keys[nomer]
        if self.user[key] == "запрещен":
            QMessageBox.warning(self, "Ошибка", "Нет доступа")
            return
        self.stack.setCurrentIndex(nomer)
