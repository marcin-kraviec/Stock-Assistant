import csv
import yfinance as yf
import plotly.graph_objs as go
import plotly.express as px
import database_connector
from datetime import date
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtWebEngineWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow
from PyQt5.uic import loadUi
from numpy import double


class PortfolioForm(QMainWindow):
    stocks = {}
    database_connector = database_connector.DatabaseConnector()

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
        self.fill_combo_box(PortfolioForm.stocks, self.stocks_combobox)

        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        # update latest company price
        self.amount_spinbox.valueChanged.connect(self.label_update)
        self.stocks_combobox.activated.connect(self.label_update)
        self.value_label.setText(str(round(
            yf.Ticker(str(self.stocks_combobox.currentText())).history(period='1d')['Close'][0] * (
                self.amount_spinbox.value()), 2)))

        # save formed portfolio in the database
        self.save_button.clicked.connect(self.save_it)

    # update value_label with the spinbox value
    def label_update(self):
        value = round(double(
            yf.Ticker(str(self.stocks_combobox.currentText())).history(period='1d')['Close'][
                0]) * self.amount_spinbox.value(), 2)
        self.value_label.setText(str(value))
        self.stocks_combobox.activated[str].connect(lambda: self.value_label.setText(str(value)))

    # add stock to the table
    def add_it(self):
        # spinBox value must be positive and multiple choice of the same company is not allowed
        if (self.amount_spinbox.value() > 0 and not self.portfolio_table.findItems(str(self.stocks_combobox.currentText()),
                                                                            Qt.MatchContains)):
            item = QTableWidgetItem(str(self.stocks_combobox.currentText()))
            item2 = QTableWidgetItem(str(self.amount_spinbox.value()))
            item3 = QTableWidgetItem(str(self.value_label.text()))
            # item4 = QTableWidgetItem(str(date.today()))
            row_position = self.portfolio_table.rowCount()
            self.portfolio_table.insertRow(row_position)
            self.portfolio_table.setItem(row_position, 0, item)
            self.portfolio_table.setItem(row_position, 1, item2)
            self.portfolio_table.setItem(row_position, 2, item3)
            # self.portfolio_table.setItem(row_position, 3, item4)
            self.amount_spinbox.setValue(0)

        elif self.amount_spinbox.value() == 0:
            self.alert_window("Increase the number of the selected item.", "Alert window")

    def save_it(self):
        self.database_connector.create_table(self.textEdit.toPlainText())

        past_values = []
        if self.portfolio_table.rowCount() == 0:
            self.alert_window("Portfolio is empty!", "Alert window")
            print('Portfolio is empty!')
        else:
            for i in range(self.analyse_portfolio_window.combobox.count()):
                if self.analyse_portfolio_window.combobox.itemText(i) == self.textEdit.toPlainText():
                    self.alert_window("Portfolio with this name already exists!", "Alert window")
                    # print('Portfolio exists')
                    break
            else:
                for row in range(self.portfolio_table.rowCount()):
                    stock = '\'' + self.portfolio_table.item(row, 0).text() + '\''
                    amount = self.portfolio_table.item(row, 1).text()
                    value = self.portfolio_table.item(row, 2).text()
                    self.database_connector.insert_into(self.textEdit.toPlainText(), stock, amount, value,
                                                        '\'' + str(date.today()) + '\'')
                    past_values.append(
                        int(amount) * round(
                            yf.Ticker(self.portfolio_table.item(row, 0).text()).history(period='1d')['Close'][0], 2))
                self.analyse_portfolio_window.combobox.addItem(self.textEdit.toPlainText())
                self.portfolio_edit_window.portfolio_combobox.addItem(self.textEdit.toPlainText())
                self.textEdit.clear()
                self.clear()
                self.show_pie_plot()

                # show alert window if portfolio saved successfully
                self.alert_window("Portfolio has been saved successfully.", "Alert window")

    # remove chosen row from the table
    def delete_it(self):
        clicked = self.portfolio_table.currentRow()
        if clicked == -1:
            clicked += 1
        self.portfolio_table.removeRow(clicked)

    # clear the content of the table
    def clear(self):
        for i in reversed(range(self.portfolio_table.rowCount())):
            self.portfolio_table.removeRow(i)

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

        for row in range(self.portfolio_table.rowCount()):
            stocks.append(self.portfolio_table.item(row, 0).text())
            values.append(float(self.portfolio_table.item(row, 2).text()))

        # fig = go.Figure(data=[go.Pie(values=values, labels=stocks, hole=.4)])
        fig = px.pie(values=values, names=stocks, hole=.4, color_discrete_sequence=px.colors.sequential.Viridis)

        if self.portfolio_table.rowCount() >= 1:
            self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
        else:
            self.browser.setHtml(None)

    def alert_window(self, text, window_title):

        # initialise alert window
        m = QMessageBox(self)

        # customise confirmation window
        m.setWindowIcon(QtGui.QIcon("static/alert.png"))
        m.setText(text)
        m.setWindowTitle(window_title)

        # provide options for user
        m.addButton(QMessageBox.Ok)
        m.setStyleSheet("QPushButton {min-width:70px;\
                        min-height: 30px;}")
        m.exec()
