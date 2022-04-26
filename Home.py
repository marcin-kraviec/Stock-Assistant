import sys

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class Home(QMainWindow):
    def __init__(self):
        super().__init__()

        # read the window layout from file
        loadUi("static/home.ui", self)
        self.exit_button.clicked.connect(QCoreApplication.instance().quit)
        self.minimize_button.clicked.connect(lambda: self.showMinimized())
        self.setWindowFlags(Qt.FramelessWindowHint)
