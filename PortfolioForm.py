import csv
from datetime import date

from PyQt5.QtCore import Qt

import database
from PyQt5 import QtGui, QtWebEngineWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow
from PyQt5.uic import loadUi
from numpy import double
import yfinance as yf
import plotly.graph_objs as go
import plotly.express as px


class PortfolioForm(QMainWindow):
    stocks = {}
    database_connector = database.DatabaseConnector()

    def __init__(self, analyse_portfolio_window, portfolio_edit_window):
        self.analyse_portfolio_window = analyse_portfolio_window
        self.portfolio_edit_window = portfolio_edit_window
        super().__init__()

        # read the window layout from file
        loadUi("static/portfolio_form.ui", self)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # add, delete, clear elements in portfolio form
        self.add_button.clicked.connect(self.add_it)
        self.delete_it_button.clicked.connect(self.delete_it)
        self.clear_button.clicked.connect(self.clear)

        # update plot
        self.add_button.clicked.connect(self.show_pie_plot)
        self.delete_it_button.clicked.connect(self.show_pie_plot)
        self.clear_button.clicked.connect(self.show_pie_plot)

        # fill combobox with data from static csv file
        self.read_csv_file('static/stocks.csv', PortfolioForm.stocks)
        self.fill_combo_box(PortfolioForm.stocks, self.comboBox_3)

        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        # update latest company price
        self.spinBox_4.valueChanged.connect(self.label_update)
        self.comboBox_3.activated.connect(self.label_update)
        self.label_5.setText(str(round(
            yf.Ticker(str(self.comboBox_3.currentText())).history(period='1d')['Close'][0] * (self.spinBox_4.value()),
            2)))

        self.save_button.clicked.connect(self.save_it)

    def label_update(self):
        value = round(double(
            yf.Ticker(str(self.comboBox_3.currentText())).history(period='1d')['Close'][0]) * self.spinBox_4.value(), 2)
        self.label_5.setText(str(value))
        self.comboBox_3.activated[str].connect(lambda: self.label_5.setText(str(value)))

    def add_it(self):
        # spinBox value must be postive and multiple choice of the same company is not allowed
        if (self.spinBox_4.value() > 0 and not self.my_table.findItems(str(self.comboBox_3.currentText()),
                                                                       Qt.MatchContains)):
            item = QTableWidgetItem(str(self.comboBox_3.currentText()))
            item2 = QTableWidgetItem(str(self.spinBox_4.value()))
            item3 = QTableWidgetItem(str(self.label_5.text()))
            # item4 = QTableWidgetItem(str(date.today()))
            row_position = self.my_table.rowCount()
            self.my_table.insertRow(row_position)
            self.my_table.setItem(row_position, 0, item)
            self.my_table.setItem(row_position, 1, item2)
            self.my_table.setItem(row_position, 2, item3)
            # self.my_table.setItem(row_position, 3, item4)
            self.spinBox_4.setValue(0)

    def save_it(self):
        self.database_connector.create_table(self.textEdit.toPlainText())

        past_values = []
        if self.my_table.rowCount() == 0:
            self.alert_window("Portfolio is empty!", "Alert window")
            print('Portfolio is empty!')
        else:
            for i in range(self.analyse_portfolio_window.combobox.count()):
                if (self.analyse_portfolio_window.combobox.itemText(i) == self.textEdit.toPlainText()):
                    self.alert_window("Portfolio with this name already exists!", "Alert window")
                    print('Portfolio exists')
                    break
            else:
                for row in range(self.my_table.rowCount()):
                    stock = '\'' + self.my_table.item(row, 0).text() + '\''
                    amount = self.my_table.item(row, 1).text()
                    value = self.my_table.item(row, 2).text()
                    self.database_connector.insert_into(self.textEdit.toPlainText(), stock, amount, value,
                                                        '\'' + str(date.today()) + '\'')
                    past_values.append(
                        int(amount) * round(
                            yf.Ticker(self.my_table.item(row, 0).text()).history(period='1d')['Close'][0], 2))
                self.analyse_portfolio_window.combobox.addItem(self.textEdit.toPlainText())
                self.portfolio_edit_window.portfolio_combobox.addItem(self.textEdit.toPlainText())
                self.textEdit.clear()
                self.clear()
                self.show_pie_plot()
                self.alert_window("Portfolio has been saved succesfully.", "Alert window")

    def delete_it(self):
        clicked = self.my_table.currentRow()
        if (clicked == -1):
            clicked += 1
        self.my_table.removeRow(clicked)

    def clear(self):
        for i in reversed(range(self.my_table.rowCount())):
            self.my_table.removeRow(i)

    # fill combobox with stock names
    def fill_combo_box(self, dict, combobox):
        for key in dict.keys():
            combobox.addItem(key)

    # read the data from static csv file and fill stocks dict
    def read_csv_file(self, file_path, dict):
        with open(file_path) as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                dict[row[0]] = row[1]

    def show_pie_plot(self):
        stocks = []
        values = []

        for row in range(self.my_table.rowCount()):
            stocks.append(self.my_table.item(row, 0).text())
            values.append(float(self.my_table.item(row, 2).text()))

        #fig = go.Figure(data=[go.Pie(values=values, labels=stocks, hole=.4)])
        fig = px.pie(values=values, names=stocks, hole=.4,color_discrete_sequence=px.colors.sequential.Viridis)

        if self.my_table.rowCount() >= 1:
            self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
        else:
            self.browser.setHtml(None)

    def alert_window(self, text, window_title):
        m = QMessageBox(self)
        # m.setIcon(QMessageBox.Information)
        m.setWindowIcon(QtGui.QIcon("static/alert.png"))
        m.setText(text)
        m.setWindowTitle(window_title)
        m.addButton(QMessageBox.Ok)
        # m.setStandardButtons(QMessageBox.Ok | QMessageBox.Close)
        m.exec()