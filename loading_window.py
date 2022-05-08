import time
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget, QSplashScreen
from PyQt5.uic import loadUi


class LoadingWindow(QSplashScreen):

    def __init__(self):
        super(QSplashScreen, self).__init__()

        # add google font
        _id = QtGui.QFontDatabase.addApplicationFont("static/Sora/Sora-Bold.ttf")

        # read the window layout from file
        loadUi("static/ui_files/loading_window.ui", self)

        # customise font style for labels in this window
        font = QtGui.QFont("Sora")
        self.name_label.setFont(font)
        self.version_label.setFont(font)


class myThread(QThread):

    def __init__(self, loading_window):
        super().__init__()

        # create an loading window instance
        self.loading_window = loading_window
        self.setTerminationEnabled(True)

    # start loading progressbar when thread starts
    def run(self):
        cnt = 0
        while cnt < 100:
            cnt += 1
            time.sleep(0.1)

            # set increasing value of progressbar
            self.loading_window.loading_progressbar.setValue(cnt)
