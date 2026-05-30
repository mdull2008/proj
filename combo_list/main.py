import sys

from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QListWidget,
    QVBoxLayout,
    QWidget,
)


class Okno(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Combo и список")
        self.resize(320, 400)

        self.combo = QComboBox()
        self.spisok = QListWidget()

        for i in range(1, 11):
            self.combo.addItem("Строка " + str(i))

        layout = QVBoxLayout()
        layout.addWidget(self.combo)
        layout.addWidget(self.spisok)
        self.setLayout(layout)

        self.combo.activated.connect(self.vybor_combo)
        self.spisok.itemClicked.connect(self.vybor_spisok)

    def vybor_combo(self, nomer):
        text = self.combo.itemText(nomer)
        self.spisok.addItem(text)
        self.combo.removeItem(nomer)

    def vybor_spisok(self, element):
        text = element.text()
        self.combo.addItem(text)
        self.spisok.takeItem(self.spisok.row(element))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    okno = Okno()
    okno.show()
    sys.exit(app.exec())
