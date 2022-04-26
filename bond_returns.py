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
        self.spinBox.valueChanged.connect(self.fill_table)

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
            number_of_cycles = '10'
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

    def fill_table(self):

        self.clear()

        N = 4
        n = self.spinBox.value()
        r = 0.00125
        f = 0.0
        self.tableWidget.insertRow(0)
        self.tableWidget.setItem(0, 0, QTableWidgetItem(str(0)))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(str(n * 100) + ' PLN'))
        for i in range(1, N):
            item = QTableWidgetItem(str(i))
            item2 = QTableWidgetItem(str(n*100)+' PLN')
            item3 = QTableWidgetItem(str(r*100)+'%')
            item4 = QTableWidgetItem(str(r * n * 100)+' PLN')
            item5 = QTableWidgetItem(str(i * r * n * 100)+' PLN')
            item6 = QTableWidgetItem(str(f) + ' PLN')
            item7 = QTableWidgetItem(str(r * n * 100 * 0.19) + ' PLN')
            item8 = QTableWidgetItem(str((i * r * n * 100) - (i * r * n * 100 * 0.19)) + ' PLN')
            item9 = QTableWidgetItem(str(self.wibor_spinbox.value())+ '%')
            item10 = QTableWidgetItem(str(self.inflation_spinbox.value()) + '%')
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, item)
            self.tableWidget.setItem(i, 1, item2)
            self.tableWidget.setItem(i, 2, item3)
            self.tableWidget.setItem(i, 3, item4)
            self.tableWidget.setItem(i, 4, item5)
            self.tableWidget.setItem(i, 5, item6)
            self.tableWidget.setItem(i, 6, item7)
            self.tableWidget.setItem(i, 7, item8)
            self.tableWidget.setItem(i, 8, item9)
            self.tableWidget.setItem(i, 9, item10)

    def clear(self):
        for i in reversed(range(self.tableWidget.rowCount())):
            self.tableWidget.removeRow(i)


        #TODO: Filling the table with data

