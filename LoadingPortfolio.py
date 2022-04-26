import time

from PyQt5.QtCore import QThread, pyqtSignal, QMutex
from PyQt5.QtWidgets import QMainWindow, QWidget, QSplashScreen
from PyQt5.uic import loadUi


class LoadingPortfolio(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()
        # read the window layout from file
        loadUi("static/loading_portfolio.ui", self)


class myThread(QThread):
    def __init__(self, loading_portfolio):
        super().__init__()
        self.loading_portfolio = loading_portfolio
        self.setTerminationEnabled(True)

    def run(self):
        cnt = 0
        while cnt < 100:
            cnt += 1
            time.sleep(0.03)
            self.loading_portfolio.progressBar.setValue(cnt)
            self.loading_portfolio.counter.setText(str(cnt) + "%")

