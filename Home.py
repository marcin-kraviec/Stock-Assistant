import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi


class Home(QMainWindow):
    def __init__(self):
        super().__init__()

        # read the window layout from file
        loadUi("static/home.ui", self)
        self.exit_button.clicked.connect(self.exit)
        self.minimize_button.clicked.connect(lambda: self.showMinimized())
        self.setWindowFlags(Qt.FramelessWindowHint)

    def exit(self):
        m = QMessageBox(self)
        # m.setIcon(QMessageBox.Information)
        m.setWindowIcon(QtGui.QIcon("static/alert.png"))
        m.setText("Are you sure you want to exit?")
        m.setWindowTitle("Confirmation window")
        m.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        m.setStyleSheet("QPushButton {min-width:70px;\
                        min-height: 30px;}")
        btn = m.exec()
        if btn == QMessageBox.Yes:
            QCoreApplication.instance().quit()
