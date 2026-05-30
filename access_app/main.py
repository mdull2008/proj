import sys

from PySide6.QtWidgets import QApplication

from db import init_db
from login_win import LoginWindow


def main():
    init_db()
    app = QApplication(sys.argv)
    okno = LoginWindow()
    okno.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
