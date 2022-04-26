import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget, QSplashScreen
from PyQt5.uic import loadUi


class LoadingWindow(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()
        # read the window layout from file
        loadUi("static/loading_window.ui", self)


class myThread(QThread):
    def __init__(self, loading_window):
        super().__init__()
        self.loading_window = loading_window
        self.setTerminationEnabled(True)

    def run(self):
        cnt = 0
        while cnt < 100:
            cnt += 1
            time.sleep(0.06)
            self.loading_window.progressBar.setValue(cnt)
            self.loading_window.counter.setText(str(cnt) + "%")


