from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class Home(QMainWindow):
    def __init__(self):
        super().__init__()

        # read the window layout from file
        loadUi("static/home.ui", self)
        # self.setWindowFlags(Qt.FramelessWindowHint)
