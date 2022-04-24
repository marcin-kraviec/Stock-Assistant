import database
from PyQt5 import QtGui, QtWebEngineWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow
from PyQt5.uic import loadUi
from numpy import double
import yfinance as yf
import plotly.graph_objs as go
import plotly.express as px

import data_analysis


class BondReturns(QMainWindow):
    text = """
    Nominal bond value: 100 PLN\t\t\n
    Number of cycles: N\t\t\n
    Cycle duration: N\t\t\n
    Rate of interest (first cycle): N\t\t\n
    Rate of interest (further cycles): N\t\n
    Capitalisation of interest: N\t\t\n
    Payment of interest: N\t\t\n
    Capital Gains Tax: 19%
    """

    def __init__(self):
        super().__init__()
        loadUi("static/bond_returns.ui", self)
        self.info_button.clicked.connect(lambda: self.alert_window(self.text, self.comboBox.currentText()))

    def alert_window(self, text, window_title):
        m = QMessageBox(self)
        # m.setIcon(QMessageBox.Information)
        m.setWindowIcon(QtGui.QIcon("static/alert.png"))
        m.setText(text)
        m.setWindowTitle(window_title)
        m.addButton(QMessageBox.Close)
        # m.setStandardButtons(QMessageBox.Ok | QMessageBox.Close)
        m.exec()