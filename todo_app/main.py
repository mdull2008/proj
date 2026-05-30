import sys

from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

STATUSES = [
    "Новая",
    "Принята в работу",
    "выполнена на 50%",
    "Закрыта",
]


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список дел")
        self.resize(750, 450)

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("tasks.db")
        self.db.open()

        zapros = QSqlQuery()
        zapros.exec(
            "CREATE TABLE IF NOT EXISTS tasks "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, status TEXT)"
        )

        self.model = QSqlTableModel()
        self.model.setTable("tasks")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()

        self.model.setHeaderData(0, Qt.Horizontal, "№")
        self.model.setHeaderData(1, Qt.Horizontal, "Задача")
        self.model.setHeaderData(2, Qt.Horizontal, "Статус")

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setColumnHidden(0, True)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)

        self.pole = QLineEdit()
        self.pole.setPlaceholderText("Новая задача")

        self.knopka_dobavit = QPushButton("Добавить")
        self.knopka_udalit = QPushButton("Удалить")
        self.knopka_ochistit = QPushButton("Очистить всё")

        self.status = QComboBox()
        for s in STATUSES:
            self.status.addItem(s)

        self.knopka_status = QPushButton("Сменить статус")

        verh = QHBoxLayout()
        verh.addWidget(self.pole)
        verh.addWidget(self.knopka_dobavit)

        niz = QHBoxLayout()
        niz.addWidget(self.status)
        niz.addWidget(self.knopka_status)
        niz.addWidget(self.knopka_udalit)
        niz.addWidget(self.knopka_ochistit)

        layout = QVBoxLayout()
        layout.addLayout(verh)
        layout.addWidget(self.table)
        layout.addLayout(niz)
        self.setLayout(layout)

        self.knopka_dobavit.clicked.connect(self.dobavit)
        self.knopka_udalit.clicked.connect(self.udalit)
        self.knopka_ochistit.clicked.connect(self.ochistit)
        self.knopka_status.clicked.connect(self.smenit_status)
        self.pole.returnPressed.connect(self.dobavit)

    def dobavit(self):
        text = self.pole.text().strip()
        if text == "":
            return
        q = QSqlQuery()
        q.prepare("INSERT INTO tasks (text, status) VALUES (?, ?)")
        q.addBindValue(text)
        q.addBindValue("Новая")
        q.exec()
        self.model.select()
        self.pole.clear()

    def udalit(self):
        row = self.table.currentIndex().row()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите задачу")
            return
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()

    def ochistit(self):
        otvet = QMessageBox.question(
            self,
            "Вопрос",
            "Удалить все задачи?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if otvet == QMessageBox.Yes:
            QSqlQuery().exec("DELETE FROM tasks")
            self.model.select()

    def smenit_status(self):
        row = self.table.currentIndex().row()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите задачу")
            return
        noviy = self.status.currentText()
        self.model.setData(self.model.index(row, 2), noviy)
        self.model.submitAll()
        self.model.select()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    okno = MainWindow()
    okno.show()
    sys.exit(app.exec())
