import database
from PyQt5 import QtGui, QtWebEngineWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow, QHeaderView
from PyQt5.uic import loadUi
from numpy import double
import yfinance as yf
import plotly.graph_objs as go
import plotly.express as px

import data_analysis


class BondReturns(QMainWindow):

    #rates = {'OTS':0.015, 'DOS':0.02, 'TOZ':0.021, 'COI':0.023, 'EDO':0.027}

    def __init__(self):
        super().__init__()
        loadUi("static/bond_returns.ui", self)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.info_button.clicked.connect(lambda: self.alert_window(self.info_text(), self.comboBox.currentText()))
        self.current_bond=self.comboBox.currentText()

    def alert_window(self, text, window_title):
        m = QMessageBox(self)
        # m.setIcon(QMessageBox.Information)
        m.setWindowIcon(QtGui.QIcon("static/alert.png"))
        m.setText(text)
        m.setWindowTitle(window_title)
        m.addButton(QMessageBox.Close)
        # m.setStandardButtons(QMessageBox.Ok | QMessageBox.Close)
        m.exec()

    def info_text(self):

        number_of_cycles = ''
        cycle_duration = ''
        rate_of_interest = ''
        rate_of_interest_2 = ''
        capitalisation_of_interest = ''
        payment_of_interest = ''

        if self.comboBox.currentText() == 'OTS':
            number_of_cycles = '3'
            cycle_duration = '1 month'
            rate_of_interest = '1.25% per year'
            rate_of_interest_2 = '1.25% per year'
            capitalisation_of_interest = 'No'
            payment_of_interest = 'After each cycle'
        elif self.comboBox.currentText() == 'DOS':
            number_of_cycles = '2'
            cycle_duration = '1 year'
            rate_of_interest = '2% per year'
            rate_of_interest_2 = '2% per year'
            capitalisation_of_interest = 'Yes'
            payment_of_interest = 'Upon redemption'
        elif self.comboBox.currentText() == 'TOZ':
            number_of_cycles = '6'
            cycle_duration = '6 months'
            rate_of_interest = '2.1% per year'
            rate_of_interest_2 = '1 x WIBOR6M '
            capitalisation_of_interest = 'No'
            payment_of_interest = 'After each cycle'
        elif self.comboBox.currentText() == 'COI':
            number_of_cycles = '4'
            cycle_duration = '1 year'
            rate_of_interest = '2.3% per year'
            rate_of_interest_2 = '1% + inflation per year'
            capitalisation_of_interest = 'No'
            payment_of_interest = 'After each cycle'
        elif self.comboBox.currentText() == 'EDO':
            number_of_cycles = '4'
            cycle_duration = '1 year'
            rate_of_interest = '2.7% per year'
            rate_of_interest_2 = '1.25% + inflation per year'
            capitalisation_of_interest = 'Yes'
            payment_of_interest = 'Upon redemption'

        text = """
            Nominal bond value: 100 PLN\t\t\n
            Number of cycles: {a}\t\t\n
            Cycle duration: {b}\t\t\n
            Rate of interest (first cycle): {c}\t\t\n
            Rate of interest (further cycles): {d}\t\n
            Capitalisation of interest: {e}\t\t\n
            Payment of interest: {f}\t\t\n
            Capital Gains Tax: 19%
            """.format(
            a=number_of_cycles,
            b=cycle_duration,
            c=rate_of_interest,
            d=rate_of_interest_2,
            e=capitalisation_of_interest,
            f=payment_of_interest)

        return text

    def fill_table(self, bond):
        for i in range(3):
            pass
        #TODO: Filling the table with data

