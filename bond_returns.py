from PyQt5.QtCore import Qt

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

    ots_data = {'cycles': 3, 'rate': 0.00125, 'fee': 0.0, 'capitalisation': False}
    dos_data = {'cycles': 2, 'rate': 0.02, 'fee': 0.7, 'capitalisation': True}
    toz_data = {'cycles': 6, 'rate': 0.0105, 'fee': 0.7, 'capitalisation': False}
    coi_data = {'cycles': 4, 'rate': 0.023, 'fee': 0.7, 'capitalisation': False}
    edo_data = {'cycles': 10, 'rate': 0.027, 'fee': 2, 'capitalisation': False}

    def __init__(self):
        super().__init__()
        loadUi("static/bond_returns.ui", self)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.info_button.clicked.connect(lambda: self.alert_window(self.info_text(), self.comboBox.currentText()))
        self.spinBox.valueChanged.connect(self.set_bond_type)
        self.inflation_spinbox.valueChanged.connect(self.set_bond_type)
        self.wibor_spinbox.valueChanged.connect(self.set_bond_type)
        self.comboBox.activated[str].connect(self.set_bond_type)
        self.info_button.clicked.connect(self.info_text)

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

        bond = self.comboBox.currentText()
        N = 0
        n = self.spinBox.value()
        r1 = 0.0
        r2 = 0.0
        inflation = self.inflation_spinbox.value()
        wibor = self.wibor_spinbox.value()
        fee = 0.0
        capitalisation = False

        if bond == 'OTS':
            N = self.ots_data['cycles']
            r1 = self.ots_data['rate']
            r2 = self.ots_data['rate']
            fee = self.ots_data['fee']
            capitalisation = self.ots_data['capitalisation']
        elif bond == 'DOS':
            N = self.dos_data['cycles']
            r1 = self.dos_data['rate']
            r2 = self.dos_data['rate']
            fee = self.dos_data['fee']
            capitalisation = self.dos_data['capitalisation']

        self.clear()

        self.tableWidget.insertRow(0)
        self.tableWidget.setItem(0, 0, QTableWidgetItem(str(0)))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(str(n * 100) + ' PLN'))

        for i in range(1, N + 1):

            if i == 1:
                self.tableWidget.insertRow(i)
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i)))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(n*100)))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(str(round(r1*100, 2))))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(str(round(r1 * n * 100, 2))))
                self.tableWidget.setItem(i, 4, QTableWidgetItem(str(round(i * r1 * n * 100, 2))))
                self.tableWidget.setItem(i, 5, QTableWidgetItem(str(fee)))
                self.tableWidget.setItem(i, 6, QTableWidgetItem(str(round(r1 * n * 100 * 0.19, 2))))
                self.tableWidget.setItem(i, 7, QTableWidgetItem(str(round(((i * r1 * n * 100) - (i * r1 * n * 100 * 0.19)), 2))))
                self.tableWidget.setItem(i, 8, QTableWidgetItem(str(wibor)))
                self.tableWidget.setItem(i, 9, QTableWidgetItem(str(inflation)))
                self.tableWidget.setItem(i, 10, QTableWidgetItem(str(i * inflation)))
                profit = (float(self.tableWidget.item(i, 1).text()) + float(self.tableWidget.item(i, 7).text())) - (float(self.tableWidget.item(i, 1).text()) + float(self.tableWidget.item(i, 1).text()) * float(self.tableWidget.item(i, 9).text())/100)
                self.tableWidget.setItem(i, 11, QTableWidgetItem(str(round(profit, 2))))
                percentage = profit * 100 / float(self.tableWidget.item(i, 1).text())
                self.tableWidget.setItem(i, 12, QTableWidgetItem(str(round(percentage, 2))))


            else:
                if capitalisation == False:
                    self.tableWidget.insertRow(i)
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i)))
                    self.tableWidget.setItem(i, 1, QTableWidgetItem(str(n * 100)))
                    self.tableWidget.setItem(i, 2, QTableWidgetItem(str(round(r2 * 100, 2))))
                    self.tableWidget.setItem(i, 3, QTableWidgetItem(str(round(r2 * n * 100, 2))))
                    self.tableWidget.setItem(i, 4, QTableWidgetItem(str(round(i * r2 * n * 100, 2))))
                    if i == N:
                        self.tableWidget.setItem(i, 5, QTableWidgetItem(str(0.0)))
                    else:
                        self.tableWidget.setItem(i, 5, QTableWidgetItem(str(fee*n)))
                    self.tableWidget.setItem(i, 6, QTableWidgetItem(str(round(r2 * n * 100 * 0.19, 2))))
                    self.tableWidget.setItem(i, 7, QTableWidgetItem(str(round(((i * r2 * n * 100) - (i * r2 * n * 100 * 0.19)), 2))))
                    self.tableWidget.setItem(i, 8, QTableWidgetItem(str(wibor)))
                    self.tableWidget.setItem(i, 9, QTableWidgetItem(str(inflation)))
                    accumulated_inflation = ((1 + float(self.tableWidget.item(i - 1, 9).text())/100) * (1 + float(self.tableWidget.item(i-1, 10).text())/100) - 1)*100
                    self.tableWidget.setItem(i, 10, QTableWidgetItem(str(round(accumulated_inflation, 2))))
                    profit = (float(self.tableWidget.item(i, 1).text()) + float(self.tableWidget.item(i, 7).text())) - (float(self.tableWidget.item(i, 1).text()) + float(self.tableWidget.item(i, 1).text()) * float(self.tableWidget.item(i, 9).text()) / 100)
                    if profit < 0:
                        self.tableWidget.setItem(i, 11, QTableWidgetItem(str(round(profit + float(self.tableWidget.item(i - 1, 11).text()), 2))))
                        percentage = profit*100/float(self.tableWidget.item(i, 1).text())
                        self.tableWidget.setItem(i, 12, QTableWidgetItem(str(round(percentage + float(self.tableWidget.item(i - 1, 12).text()), 2))))
                    else:
                        self.tableWidget.setItem(i, 11, QTableWidgetItem(str(round(profit, 2))))
                        percentage = profit * 100 / float(self.tableWidget.item(i, 1).text())
                        self.tableWidget.setItem(i, 12, QTableWidgetItem(str(round(percentage, 2))))

                else:
                    self.tableWidget.insertRow(i)
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i)))
                    self.tableWidget.setItem(i, 1, QTableWidgetItem(str(n * 100)))
                    self.tableWidget.setItem(i, 2, QTableWidgetItem(str(round(r1 * 100, 2))))
                    self.tableWidget.setItem(i, 3, QTableWidgetItem(str(round(r1 * n * 100, 2))))
                    self.tableWidget.setItem(i, 4, QTableWidgetItem(str(round(i * r1 * n * 100, 2))))
                    self.tableWidget.setItem(i, 5, QTableWidgetItem(str(fee)))
                    self.tableWidget.setItem(i, 6, QTableWidgetItem(str(round(r1 * n * 100 * 0.19, 2))))
                    self.tableWidget.setItem(i, 7, QTableWidgetItem(str(round(((i * r1 * n * 100) - (i * r1 * n * 100 * 0.19)), 2))))
                    self.tableWidget.setItem(i, 8, QTableWidgetItem(str(wibor)))
                    self.tableWidget.setItem(i, 9, QTableWidgetItem(str(inflation)))
                    accumulated_inflation = ((1 + float(self.tableWidget.item(i - 1, 9).text()) / 100) * (1 + float(self.tableWidget.item(i - 1, 10).text()) / 100) - 1) * 100
                    self.tableWidget.setItem(i, 10, QTableWidgetItem(str(round(accumulated_inflation, 2))))
                    profit = (float(self.tableWidget.item(i, 1).text()) + float(self.tableWidget.item(i, 7).text())) - (float(self.tableWidget.item(i, 1).text()) * float(self.tableWidget.item(i, 1).text()) / 100)
                    self.tableWidget.setItem(i, 11, QTableWidgetItem(str(round(profit + float(self.tableWidget.item(i - 1, 11).text()), 2))))
                    percentage = profit*100/float(self.tableWidget.item(i, 1).text())
                    self.tableWidget.setItem(i, 12, QTableWidgetItem(str(round(percentage  + float(self.tableWidget.item(i - 1, 12).text()), 2))))
        self.show_plot()


    def ots(self):
        self.current_bond = self.comboBox.currentText()
        N = self.ots_data['cycles']
        n = self.spinBox.value()
        r1 = self.ots_data['rate']
        r2 = self.ots_data['rate']
        inflation = self.inflation_spinbox.value()
        wibor = self.wibor_spinbox.value()
        fee = self.ots_data['fee']
        capitalisation = self.ots_data['capitalisation']

        self.clear()

        self.tableWidget.insertRow(0)
        self.tableWidget.setItem(0, 0, QTableWidgetItem(str(0)))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(str(n * 100)))

        for i in range(1, N + 1):

            if i == 1:
                self.tableWidget.insertRow(i)
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i)))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(n * 100)))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(str(round(r1 * 100, 2))))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(str(round(r1 * n * 100, 2))))
                self.tableWidget.setItem(i, 4, QTableWidgetItem(str(round(i * r1 * n * 100, 2))))
                self.tableWidget.setItem(i, 5, QTableWidgetItem(str(fee)))
                self.tableWidget.setItem(i, 6, QTableWidgetItem(str(round(r1 * n * 100 * 0.19, 2))))
                self.tableWidget.setItem(i, 7, QTableWidgetItem(
                    str(round(((i * r1 * n * 100) - (i * r1 * n * 100 * 0.19)), 2))))
                self.tableWidget.setItem(i, 8, QTableWidgetItem(str(wibor)))
                self.tableWidget.setItem(i, 9, QTableWidgetItem(str(inflation)))
                self.tableWidget.setItem(i, 10, QTableWidgetItem(str(i * inflation)))
                profit = (float(self.tableWidget.item(i, 1).text()) + float(self.tableWidget.item(i, 7).text())) - (
                            float(self.tableWidget.item(i, 1).text()) + float(
                        self.tableWidget.item(i, 1).text()) * float(self.tableWidget.item(i, 9).text()) / 100)
                self.tableWidget.setItem(i, 11, QTableWidgetItem(str(round(profit, 2))))
                percentage = profit * 100 / float(self.tableWidget.item(i, 1).text())
                self.tableWidget.setItem(i, 12, QTableWidgetItem(str(round(percentage, 2))))


            else:
                self.tableWidget.insertRow(i)
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i)))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(n * 100)))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(str(round(r2 * 100, 2))))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(str(round(r2 * n * 100, 2))))
                self.tableWidget.setItem(i, 4, QTableWidgetItem(str(round(i * r2 * n * 100, 2))))
                if i == N:
                    self.tableWidget.setItem(i, 5, QTableWidgetItem(str(0.0)))
                else:
                    self.tableWidget.setItem(i, 5, QTableWidgetItem(str(fee * n)))
                self.tableWidget.setItem(i, 6, QTableWidgetItem(str(round(r2 * n * 100 * 0.19, 2))))
                self.tableWidget.setItem(i, 7, QTableWidgetItem(
                    str(round(((i * r2 * n * 100) - (i * r2 * n * 100 * 0.19)), 2))))
                self.tableWidget.setItem(i, 8, QTableWidgetItem(str(wibor)))
                self.tableWidget.setItem(i, 9, QTableWidgetItem(str(inflation)))
                accumulated_inflation = ((1 + float(self.tableWidget.item(i - 1, 9).text()) / 100) * (
                            1 + float(self.tableWidget.item(i - 1, 10).text()) / 100) - 1) * 100
                self.tableWidget.setItem(i, 10, QTableWidgetItem(str(round(accumulated_inflation, 2))))
                profit = (float(self.tableWidget.item(i, 1).text()) + float(self.tableWidget.item(i, 7).text())) - (
                            float(self.tableWidget.item(i, 1).text()) + float(
                        self.tableWidget.item(i, 1).text()) * float(self.tableWidget.item(i, 9).text()) / 100)
                if profit < 0:
                    self.tableWidget.setItem(i, 11, QTableWidgetItem(
                        str(round(profit + float(self.tableWidget.item(i - 1, 11).text()), 2))))
                    percentage = profit * 100 / float(self.tableWidget.item(i, 1).text())
                    self.tableWidget.setItem(i, 12, QTableWidgetItem(
                        str(round(percentage + float(self.tableWidget.item(i - 1, 12).text()), 2))))
                else:
                    self.tableWidget.setItem(i, 11, QTableWidgetItem(str(round(profit, 2))))
                    percentage = profit * 100 / float(self.tableWidget.item(i, 1).text())
                    self.tableWidget.setItem(i, 12, QTableWidgetItem(str(round(percentage, 2))))

        self.show_plot()


    def dos(self):
        self.current_bond = self.comboBox.currentText()
        N = self.dos_data['cycles']
        n = self.spinBox.value()
        r1 = self.dos_data['rate']
        r2 = self.dos_data['rate']
        inflation = self.inflation_spinbox.value()
        wibor = self.wibor_spinbox.value()
        fee = self.dos_data['fee']
        capitalisation = self.dos_data['capitalisation']

        self.clear()

        self.tableWidget.insertRow(0)
        self.tableWidget.setItem(0, 0, QTableWidgetItem(str(0)))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(str(n * 100)))

        for i in range(1, N + 1):

            if i == 1:
                self.tableWidget.insertRow(i)
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i)))
                interest = r1 * n * 100
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(n * 100 + interest)))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(str(round(r1 * 100, 2))))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(str(round(interest, 2))))
                self.tableWidget.setItem(i, 4, QTableWidgetItem(str(round(interest, 2))))
                self.tableWidget.setItem(i, 5, QTableWidgetItem(str(round(fee*n))))
                self.tableWidget.setItem(i, 6, QTableWidgetItem(str(round((interest - fee*n)  * 0.19, 2))))
                self.tableWidget.setItem(i, 7, QTableWidgetItem(
                    str(round(((interest) - (fee*n) - ((interest - fee*n)* 0.19)), 2))))
                self.tableWidget.setItem(i, 8, QTableWidgetItem(str(wibor)))
                self.tableWidget.setItem(i, 9, QTableWidgetItem(str(inflation)))
                self.tableWidget.setItem(i, 10, QTableWidgetItem(str(i * inflation)))
                profit = (float(self.tableWidget.item(i, 1).text()) + float(self.tableWidget.item(i, 7).text())) - (
                            float(self.tableWidget.item(i, 1).text()) + float(
                        self.tableWidget.item(i, 1).text()) * float(self.tableWidget.item(i, 9).text()) / 100)
                self.tableWidget.setItem(i, 11, QTableWidgetItem(str(round(profit, 2))))
                percentage = profit * 100 / float(self.tableWidget.item(i, 1).text())
                self.tableWidget.setItem(i, 12, QTableWidgetItem(str(round(percentage, 2))))


            else:
                self.tableWidget.insertRow(i)
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i)))
                interest = float(r1 * float(self.tableWidget.item(i-1, 1).text()))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(interest + float(self.tableWidget.item(i-1, 1).text()))))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(str(round(r2 * 100, 2))))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(str(round(r2 * (float(self.tableWidget.item(i-1, 1).text())), 2))))
                self.tableWidget.setItem(i, 4, QTableWidgetItem(str(round(interest + float(self.tableWidget.item(i-1, 1).text()) - n*100, 2))))
                self.tableWidget.setItem(i, 5, QTableWidgetItem(str(0.0)))
                self.tableWidget.setItem(i, 6, QTableWidgetItem(str(round(float(self.tableWidget.item(i, 4).text()) * 0.19, 2))))
                self.tableWidget.setItem(i, 7, QTableWidgetItem(
                    str(round(float(self.tableWidget.item(i, 4).text()) - float(self.tableWidget.item(i, 4).text()) * 0.19 , 2))))
                self.tableWidget.setItem(i, 8, QTableWidgetItem(str(wibor)))
                self.tableWidget.setItem(i, 9, QTableWidgetItem(str(inflation)))
                accumulated_inflation = ((1 + float(self.tableWidget.item(i - 1, 9).text()) / 100) * (
                            1 + float(self.tableWidget.item(i - 1, 10).text()) / 100) - 1) * 100
                self.tableWidget.setItem(i, 10, QTableWidgetItem(str(round(accumulated_inflation, 2))))
                profit = (float(self.tableWidget.item(i, 7).text())) - (float(self.tableWidget.item(i, 1).text()) * float(self.tableWidget.item(i, 10).text()) / 100)
                self.tableWidget.setItem(i, 11, QTableWidgetItem(str(round(profit, 2))))
                percentage = profit * 100 / float(self.tableWidget.item(i, 1).text())
                self.tableWidget.setItem(i, 12, QTableWidgetItem(str(round(percentage, 2))))
                '''
                if profit < 0:
                    self.tableWidget.setItem(i, 11, QTableWidgetItem(
                        str(round(profit + float(self.tableWidget.item(i - 1, 11).text()), 2))))
                    percentage = profit * 100 / float(self.tableWidget.item(i, 1).text())
                    self.tableWidget.setItem(i, 12, QTableWidgetItem(
                        str(round(percentage + float(self.tableWidget.item(i - 1, 12).text()), 2))))
                else:
                    self.tableWidget.setItem(i, 11, QTableWidgetItem(str(round(profit, 2))))
                    percentage = profit * 100 / float(self.tableWidget.item(i, 1).text())
                    self.tableWidget.setItem(i, 12, QTableWidgetItem(str(round(percentage, 2))))
                '''
        self.show_plot()


    def toz(self):
        self.current_bond = self.comboBox.currentText()
        N = self.toz_data['cycles']
        n = self.spinBox.value()
        r1 = self.toz_data['rate']
        r2 = 1
        inflation = self.inflation_spinbox.value()
        wibor = self.wibor_spinbox.value()
        fee = self.toz_data['fee']
        capitalisation = self.toz_data['capitalisation']

        self.clear()

        self.tableWidget.insertRow(0)
        self.tableWidget.setItem(0, 0, QTableWidgetItem(str(0)))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(str(n * 100)))

        for i in range(1, N + 1):

            if i == 1:
                self.tableWidget.insertRow(i)
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i)))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(n * 100)))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(str(round(r1 * 100, 2))))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(str(round(r1 * n * 100, 2))))
                self.tableWidget.setItem(i, 4, QTableWidgetItem(str(round(r1 * n * 100, 2))))
                self.tableWidget.setItem(i, 5, QTableWidgetItem(str(round(fee*n, 2))))
                self.tableWidget.setItem(i, 6, QTableWidgetItem(str(round((r1 * n * 100) * 0.19, 2))))
                self.tableWidget.setItem(i, 7, QTableWidgetItem(
                    str(round(((r1 * n * 100) - (fee*n) - ((r1 * n * 100)* 0.19)), 2))))
                self.tableWidget.setItem(i, 8, QTableWidgetItem(str(wibor)))
                self.tableWidget.setItem(i, 9, QTableWidgetItem(str(inflation)))
                self.tableWidget.setItem(i, 10, QTableWidgetItem(str(i * inflation)))
                profit = (float(self.tableWidget.item(i, 1).text()) + float(self.tableWidget.item(i, 7).text())) - (
                            float(self.tableWidget.item(i, 1).text()) + float(
                        self.tableWidget.item(i, 1).text()) * float(self.tableWidget.item(i, 9).text()) / 100)
                self.tableWidget.setItem(i, 11, QTableWidgetItem(str(round(profit, 2))))
                percentage = profit * 100 / float(self.tableWidget.item(i, 1).text())
                self.tableWidget.setItem(i, 12, QTableWidgetItem(str(round(percentage, 2))))


            else:
                self.tableWidget.insertRow(i)
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i)))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(n*100)))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(str(wibor)))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(str(round(wibor * n, 2))))
                self.tableWidget.setItem(i, 4, QTableWidgetItem(str(round(wibor * n + float(self.tableWidget.item(i-1, 4).text()), 2))))
                if i == N:
                    self.tableWidget.setItem(i, 5, QTableWidgetItem(str(0.0)))
                    self.tableWidget.setItem(i, 6, QTableWidgetItem(str(round(float(wibor * n * 0.19), 2))))
                    self.tableWidget.setItem(i, 7, QTableWidgetItem(
                        str(round(float(self.tableWidget.item(i, 4).text()) - float(self.tableWidget.item(i, 6).text()), 2))))
                else:
                    self.tableWidget.setItem(i, 5, QTableWidgetItem(str(round(fee*n, 2))))
                    self.tableWidget.setItem(i, 6, QTableWidgetItem(str(round(float(wibor * n * 0.19), 2))))
                    self.tableWidget.setItem(i, 7, QTableWidgetItem(
                        str(round(float(self.tableWidget.item(i, 4).text()) - (fee*n) - float(self.tableWidget.item(i, 6).text()) , 2))))
                self.tableWidget.setItem(i, 8, QTableWidgetItem(str(wibor)))
                self.tableWidget.setItem(i, 9, QTableWidgetItem(str(inflation)))
                accumulated_inflation = ((1 + float(self.tableWidget.item(i - 1, 9).text()) / 100) * (
                            1 + float(self.tableWidget.item(i - 1, 10).text()) / 100) - 1) * 100
                self.tableWidget.setItem(i, 10, QTableWidgetItem(str(round(accumulated_inflation, 2))))
                profit = (float(self.tableWidget.item(i, 7).text())) - (float(self.tableWidget.item(i, 1).text()) * float(self.tableWidget.item(i, 10).text()) / 100)
                self.tableWidget.setItem(i, 11, QTableWidgetItem(str(round(profit, 2))))
                percentage = profit * 100 / float(self.tableWidget.item(i, 1).text())
                self.tableWidget.setItem(i, 12, QTableWidgetItem(str(round(percentage, 2))))

        self.show_plot()


    # OK
    def coi(self):
        self.current_bond = self.comboBox.currentText()
        N = self.coi_data['cycles']
        n = self.spinBox.value()
        r1 = self.coi_data['rate']
        r2 = 1
        inflation = self.inflation_spinbox.value()
        wibor = self.wibor_spinbox.value()
        fee = self.coi_data['fee']
        capitalisation = self.coi_data['capitalisation']

        self.clear()

        self.tableWidget.insertRow(0)
        self.tableWidget.setItem(0, 0, QTableWidgetItem(str(0)))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(str(n * 100)))

        for i in range(1, N + 1):

            if i == 1:
                self.tableWidget.insertRow(i)
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i)))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(n * 100)))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(str(round(r1 * 100, 2))))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(str(round(r1 * n * 100, 2))))
                self.tableWidget.setItem(i, 4, QTableWidgetItem(str(round(r1 * n * 100, 2))))
                self.tableWidget.setItem(i, 5, QTableWidgetItem(str(round(fee*n, 2))))
                self.tableWidget.setItem(i, 6, QTableWidgetItem(str(round((r1 * n * 100 - fee*n)  * 0.19, 2))))
                self.tableWidget.setItem(i, 7, QTableWidgetItem(
                    str(round(((r1 * n * 100) - (fee*n) - ((r1 * n * 100 - fee*n)* 0.19)), 2))))
                self.tableWidget.setItem(i, 8, QTableWidgetItem(str(wibor)))
                self.tableWidget.setItem(i, 9, QTableWidgetItem(str(inflation)))
                self.tableWidget.setItem(i, 10, QTableWidgetItem(str(i * inflation)))
                profit = (float(self.tableWidget.item(i, 1).text()) + float(self.tableWidget.item(i, 7).text())) - (
                            float(self.tableWidget.item(i, 1).text()) + float(
                        self.tableWidget.item(i, 1).text()) * float(self.tableWidget.item(i, 9).text()) / 100)
                self.tableWidget.setItem(i, 11, QTableWidgetItem(str(round(profit, 2))))
                percentage = profit * 100 / float(self.tableWidget.item(i, 1).text())
                self.tableWidget.setItem(i, 12, QTableWidgetItem(str(round(percentage, 2))))


            else:
                self.tableWidget.insertRow(i)
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i)))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(n*100)))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(str(r2+inflation)))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(str(round((r2+inflation) * n, 2))))
                self.tableWidget.setItem(i, 4, QTableWidgetItem(str(round((r2+inflation) * n + float(self.tableWidget.item(i-1, 4).text()), 2))))
                if i == N:
                    self.tableWidget.setItem(i, 5, QTableWidgetItem(str(0.0)))
                    self.tableWidget.setItem(i, 6, QTableWidgetItem(str(round(float(((r2 + inflation) * n) * 0.19), 2))))
                    self.tableWidget.setItem(i, 7, QTableWidgetItem(
                        str(round((float(self.tableWidget.item(i, 4).text()) - float(
                            self.tableWidget.item(i, 5).text())) * 0.81, 2))))
                else:
                    self.tableWidget.setItem(i, 5, QTableWidgetItem(str(round(fee*n, 2))))
                    self.tableWidget.setItem(i, 6, QTableWidgetItem(str(round(float(((r2+inflation) * n - fee*n)* 0.19), 2))))
                    self.tableWidget.setItem(i, 7, QTableWidgetItem(
                        str(round((float(self.tableWidget.item(i, 4).text()) - float(
                            self.tableWidget.item(i, 5).text())) * 0.81, 2))))
                self.tableWidget.setItem(i, 8, QTableWidgetItem(str(wibor)))
                self.tableWidget.setItem(i, 9, QTableWidgetItem(str(inflation)))
                accumulated_inflation = ((1 + float(self.tableWidget.item(i - 1, 9).text()) / 100) * (
                            1 + float(self.tableWidget.item(i - 1, 10).text()) / 100) - 1) * 100
                self.tableWidget.setItem(i, 10, QTableWidgetItem(str(round(accumulated_inflation, 2))))
                profit = (float(self.tableWidget.item(i, 7).text())) - (float(self.tableWidget.item(i, 1).text()) * float(self.tableWidget.item(i, 10).text()) / 100)
                self.tableWidget.setItem(i, 11, QTableWidgetItem(str(round(profit, 2))))
                percentage = profit * 100 / float(self.tableWidget.item(i, 1).text())
                self.tableWidget.setItem(i, 12, QTableWidgetItem(str(round(percentage, 2))))

        self.show_plot()


    def edo(self):
        self.current_bond = self.comboBox.currentText()
        N = self.edo_data['cycles']
        n = self.spinBox.value()
        r1 = self.edo_data['rate']
        r2 = 1.25
        inflation = self.inflation_spinbox.value()
        wibor = self.wibor_spinbox.value()
        fee = self.edo_data['fee']
        capitalisation = self.edo_data['capitalisation']

        self.clear()

        self.tableWidget.insertRow(0)
        self.tableWidget.setItem(0, 0, QTableWidgetItem(str(0)))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(str(n * 100)))

        for i in range(1, N + 1):

            if i == 1:
                self.tableWidget.insertRow(i)
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i)))
                interest = r1 * n * 100
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(round(n * 100 + interest, 2))))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(str(round(r1 * 100, 2))))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(str(round(interest, 2))))
                self.tableWidget.setItem(i, 4, QTableWidgetItem(str(round(interest, 2))))
                self.tableWidget.setItem(i, 5, QTableWidgetItem(str(round(fee*n))))
                self.tableWidget.setItem(i, 6, QTableWidgetItem(str(round((interest - fee*n)  * 0.19, 2))))
                self.tableWidget.setItem(i, 7, QTableWidgetItem(
                    str(round(((interest) - (fee*n) - ((interest - fee*n)* 0.19)), 2))))
                self.tableWidget.setItem(i, 8, QTableWidgetItem(str(wibor)))
                self.tableWidget.setItem(i, 9, QTableWidgetItem(str(inflation)))
                self.tableWidget.setItem(i, 10, QTableWidgetItem(str(i * inflation)))
                profit = (float(self.tableWidget.item(i, 1).text()) + float(self.tableWidget.item(i, 7).text())) - (
                            float(self.tableWidget.item(i, 1).text()) + float(
                        self.tableWidget.item(i, 1).text()) * float(self.tableWidget.item(i, 9).text()) / 100)
                self.tableWidget.setItem(i, 11, QTableWidgetItem(str(round(profit, 2))))
                percentage = profit * 100 / float(self.tableWidget.item(i, 1).text())
                self.tableWidget.setItem(i, 12, QTableWidgetItem(str(round(percentage, 2))))

            else:
                self.tableWidget.insertRow(i)
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i)))
                interest = float(((r2+inflation)/100) * float(self.tableWidget.item(i-1, 1).text()))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(round(interest + float(self.tableWidget.item(i-1, 1).text()), 2))))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(str(round(r2 + inflation, 2))))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(str(round(((r2+inflation)/100) * (float(self.tableWidget.item(i-1, 1).text())), 2))))
                self.tableWidget.setItem(i, 4, QTableWidgetItem(str(round(interest + float(self.tableWidget.item(i-1, 1).text()) - n*100, 2))))
                #self.tableWidget.setItem(i, 4, QTableWidgetItem(
                #    str(round((r2 + inflation) * n + float(self.tableWidget.item(i - 1, 4).text()), 2))))
                if i == N:
                    '''
                    self.tableWidget.setItem(i, 5, QTableWidgetItem(str(0.0)))
                    self.tableWidget.setItem(i, 6, QTableWidgetItem(str(round(float(self.tableWidget.item(i, 4).text()) * 0.19, 2))))
                    self.tableWidget.setItem(i, 7, QTableWidgetItem(
                        str(round(float(self.tableWidget.item(i, 4).text()) - float(self.tableWidget.item(i, 4).text()) * 0.19 , 2))))
                    '''
                    self.tableWidget.setItem(i, 5, QTableWidgetItem(str(0.0)))
                    self.tableWidget.setItem(i, 6,
                                             QTableWidgetItem(str(round(float(self.tableWidget.item(i, 4).text()) * 0.19, 2))))
                    self.tableWidget.setItem(i, 7, QTableWidgetItem(
                        str(round((float(self.tableWidget.item(i, 4).text()) - float(
                            self.tableWidget.item(i, 5).text())) * 0.81, 2))))
                else:
                    self.tableWidget.setItem(i, 5, QTableWidgetItem(str(round(fee * n, 2))))
                    self.tableWidget.setItem(i, 6, QTableWidgetItem(
                        str(round((float(self.tableWidget.item(i, 4).text()) - fee * n) * 0.19, 2))))
                    self.tableWidget.setItem(i, 7, QTableWidgetItem(
                        str(round((float(self.tableWidget.item(i, 4).text()) - float(
                            self.tableWidget.item(i, 5).text())) * 0.81, 2))))
                self.tableWidget.setItem(i, 8, QTableWidgetItem(str(wibor)))
                self.tableWidget.setItem(i, 9, QTableWidgetItem(str(inflation)))
                accumulated_inflation = ((1 + float(self.tableWidget.item(i - 1, 9).text()) / 100) * (
                            1 + float(self.tableWidget.item(i - 1, 10).text()) / 100) - 1) * 100
                self.tableWidget.setItem(i, 10, QTableWidgetItem(str(round(accumulated_inflation, 2))))
                profit = (float(self.tableWidget.item(i, 7).text())) - (float(self.tableWidget.item(i, 1).text()) * float(self.tableWidget.item(i, 10).text()) / 100)
                self.tableWidget.setItem(i, 11, QTableWidgetItem(str(round(profit, 2))))
                percentage = profit * 100 / float(self.tableWidget.item(i, 1).text())
                self.tableWidget.setItem(i, 12, QTableWidgetItem(str(round(percentage, 2))))


        self.show_plot()

    def set_bond_type(self):
        if self.comboBox.currentText() == 'OTS':
            self.ots()
        elif self.comboBox.currentText() == 'DOS':
            self.dos()
        elif self.comboBox.currentText() == 'TOZ':
            self.toz()
        elif self.comboBox.currentText() == 'COI':
            self.coi()
        elif self.comboBox.currentText() == 'EDO':
            self.edo()

    def clear(self):
        for i in reversed(range(self.tableWidget.rowCount())):
            self.tableWidget.removeRow(i)

    def show_plot(self):

        profit = {}
        real_profit = {}
        for i in range(self.tableWidget.rowCount()):
            key = str(i)
            if i == 0:
                profit[key] = 0.0
                real_profit[key] = 0.0
            else:
                profit[key] = float(self.tableWidget.item(i, 7).text())
                real_profit[key] = float(self.tableWidget.item(i, 11).text())



        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(profit.keys()), y=list(profit.values()),
                                 mode='lines',
                                 name='Profit'))
        fig.add_trace(go.Scatter(x=list(real_profit.keys()), y=list(real_profit.values()),
                                 mode='lines',
                                 name='Real profit'))
        fig.add_hline(y=0, line_dash="dot")
        fig.update_layout(hovermode="x unified")
        fig.update_xaxes(range=[1, len(list(profit.keys())) -1], tick0=0)

        if self.tableWidget.rowCount() >= 1:
            self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
        else:
            self.browser.setHtml(None)

