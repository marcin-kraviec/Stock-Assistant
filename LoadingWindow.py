import time

from PyQt5.QtWidgets import QMainWindow, QWidget, QSplashScreen
from PyQt5.uic import loadUi


class LoadingWindow(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()
        # read the window layout from file
        loadUi("static/loading_window.ui", self)

    def run(self):
        for i in range(99):
            time.sleep(0.05)
            self.progressBar.setValue(i + 1)
            self.counter.setText(str(i + 1) + "%")
