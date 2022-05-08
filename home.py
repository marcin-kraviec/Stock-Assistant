from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi


class Home(QMainWindow):
    def __init__(self):
        super().__init__()

        # read the window layout from file
        loadUi("static/ui_files/home.ui", self)

        # show confirmation window when exit button is clicked
        self.exit_button.clicked.connect(self.app_exit)

        # minimize window when minimize button is clicked
        self.minimize_button.clicked.connect(lambda: self.showMinimized())

        self.setWindowFlags(Qt.FramelessWindowHint)


    def app_exit(self):

        # initialise confirmation window
        m = QMessageBox(self)

        # customise confirmation window
        m.setWindowIcon(QtGui.QIcon("static/images/alert.png"))
        m.setText("Are you sure you want to exit?\t")
        m.setWindowTitle("Confirmation window")

        # provide options for user
        m.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        m.setStyleSheet("QPushButton {min-width:70px;\
                        min-height: 30px;}")
        btn = m.exec()
        # exit app when yes option is chosen
        if btn == QMessageBox.Yes:
            QCoreApplication.instance().quit()
