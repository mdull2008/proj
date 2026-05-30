from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListView,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from db import RAZDELY, sohranit_prava, vse_polzovateli

PRAVA = ["полный", "просмотр", "запрещен"]

NAZV = {
    "buh": "Бухгалтерия",
    "kadry": "Кадры",
    "upr": "Управление",
    "proiz": "Производство",
}


class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Админ - права")
        self.resize(700, 500)

        self.spisok = QListView()
        self.model = QStandardItemModel()
        self.spisok.setModel(self.model)

        self.combos = {}
        for key in RAZDELY:
            cb = QComboBox()
            for p in PRAVA:
                cb.addItem(p)
            self.combos[key] = cb

        self.knopka_save = QPushButton("Сохранить")

        prava_layout = QVBoxLayout()
        for key in RAZDELY:
            row = QHBoxLayout()
            row.addWidget(QLabel(NAZV[key]))
            row.addWidget(self.combos[key])
            prava_layout.addLayout(row)

        right = QVBoxLayout()
        right.addWidget(QLabel("Права пользователя"))
        right.addLayout(prava_layout)
        right.addWidget(self.knopka_save)

        main = QHBoxLayout()
        main.addWidget(self.spisok, 2)
        main.addLayout(right, 1)
        self.setLayout(main)

        self.users = []
        self.zagruzit_spisok()
        self.spisok.selectionModel().selectionChanged.connect(self.vybor)
        self.knopka_save.clicked.connect(self.sohranit)

    def zagruzit_spisok(self):
        self.model.clear()
        self.users = vse_polzovateli()
        for row in self.users:
            uid, fio, dolzh, buh, kadry, upr, proiz = row
            text = fio + " - " + dolzh
            item = QStandardItem(text)
            item.setData(uid, Qt.UserRole)
            self.model.appendRow(item)

    def vybor(self):
        indexes = self.spisok.selectedIndexes()
        if not indexes:
            return
        uid = indexes[0].data(Qt.UserRole)
        for row in self.users:
            if row[0] == uid:
                _, fio, dolzh, buh, kadry, upr, proiz = row
                self.combos["buh"].setCurrentText(buh)
                self.combos["kadry"].setCurrentText(kadry)
                self.combos["upr"].setCurrentText(upr)
                self.combos["proiz"].setCurrentText(proiz)
                break

    def sohranit(self):
        indexes = self.spisok.selectedIndexes()
        if not indexes:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя")
            return
        uid = indexes[0].data(Qt.UserRole)
        buh = self.combos["buh"].currentText()
        kadry = self.combos["kadry"].currentText()
        upr = self.combos["upr"].currentText()
        proiz = self.combos["proiz"].currentText()
        sohranit_prava(uid, buh, kadry, upr, proiz)
        self.zagruzit_spisok()
        QMessageBox.information(self, "Готово", "Права сохранены")
