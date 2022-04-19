# add new requirement to requirements.txt by executing: pipreqs --force [project_path]

import sys

import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from PyQt5 import QtWidgets, QtGui, QtWebEngineWidgets, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QWidget, QTableWidgetItem, QPushButton, \
    QGraphicsColorizeEffect
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from datetime import date
import database
import data_analysis

import csv


# tell the window that this is my own registered application, so I will decide the icon of it
import ctypes

from numpy import double

myappid = 'stock_asisstant.1.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class Home(QMainWindow):
    def __init__(self):
        super().__init__()

        # read the window layout from file
        loadUi("static/home.ui", self)

        # move between windows after clicking a button
        self.analyse_stocks_button.clicked.connect(self.go_to_analyse_stocks)
        self.analyse_crypto_button.clicked.connect(self.go_to_analyse_crypto)
        self.analyse_currencies_button.clicked.connect(self.go_to_analyse_currencies)
        self.create_portfolio_button.clicked.connect(self.go_to_portfolio_form)
        self.analyse_portfolio_button.clicked.connect(self.go_to_analyse_portfolio)
        self.edit_portfolio_button.clicked.connect(self.go_to_portfolio_edit)

    def go_to_analyse_stocks(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_analyse_crypto(self):
        widget.setCurrentIndex(widget.currentIndex() + 2)

    def go_to_analyse_currencies(self):
        widget.setCurrentIndex(widget.currentIndex() + 3)

    def go_to_portfolio_form(self):
        widget.setCurrentIndex(widget.currentIndex() + 4)

    def go_to_portfolio_edit(self):
        widget.setCurrentIndex(widget.currentIndex() + 5)

    def go_to_analyse_portfolio(self):
        widget.setCurrentIndex(widget.currentIndex() + 6)

class ChartWindow(QMainWindow):

    def __init__(self):
        super().__init__()

    def show_candlestick_plot(self):
        # getting a current stock from combobox
        stock = self.stocks_combobox.currentText()
        templates = ['ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white', 'plotly_dark', 'presentation',
                     'xgridoff', 'ygridoff', 'gridon', 'none']
        # downloading data of stock from yfinance
        data = yf.download(stock, '2021-01-01', interval="1d")
        # data = yf.download(stock,'2022-04-01',interval="1h")
        data.reset_index(inplace=True)

        # initialise candlestick plot
        fig = go.Figure()
        fig.add_trace(
            go.Candlestick(x=data['Date'], open=data['Open'], close=data['Close'], low=data['Low'], high=data['High']))
        # fig.add_trace(go.Candlestick(x=data['index'], open=data['Open'], close=data['Close'], low=data['Low'], high=data['High']))
        fig.layout.update(title_text=stock, xaxis_rangeslider_visible=True)
        fig.update_layout(hovermode="x unified")
        fig.layout.template = templates[3]

        # changing plot into html file so that it can be displayed with webengine
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def show_line_plot(self):
        # getting a current stock from combobox
        stock = self.stocks_combobox.currentText()

        # downloading data of stock from yfinance
        data = yf.download(stock, '2021-01-01', interval="1d")
        # data = yf.download(stock,'2022-04-01',interval="1h")
        data.reset_index(inplace=True)

        # initialise line plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='Open'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Close'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Low'], name='Low'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['High'], name='High'))
        fig.layout.update(title_text=stock, xaxis_rangeslider_visible=True)
        fig.update_layout(hovermode="x unified")

        # changing plot into html file so that it can be displayed with webengine
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def show_cumulative_return_plot(self):
        # getting a current stock from combobox
        stock = self.stocks_combobox.currentText()

        '''
        After understanding how the returns are distributed, we can calculate the returns from an investment.
        For that, we need to calculate the cumulative returns, which can be done using the cumprod() function:
        '''

        # downloading data of stock from yfinance
        data = yf.download(stock, '2021-01-01', interval="1d")
        # data = yf.download(stock,'2022-04-01',interval="1h")
        data.reset_index(inplace=True)

        x = data['Close'].pct_change()
        returns = (x + 1).cumprod()

        # initialise line plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=returns, name='Cumulative return'))
        fig.layout.update(title_text=stock, xaxis_rangeslider_visible=True)
        fig.update_layout(hovermode="x unified")

        # changing plot into html file so that it can be displayed with webengine
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    # switching between plot types
    def set_plot_type(self, button):
        if button.isChecked():
            if button.text() == 'Line':
                self.show_line_plot()
            elif button.text() == 'Candlestick':
                self.show_candlestick_plot()
            elif button.text() == 'Cumulative returns':
                self.show_cumulative_return_plot()

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

# Inheritance form ChartWindow
class AnalyseStocks(ChartWindow):
    # Dict stores data from static csv file
    stocks = {}

    def __init__(self):
        super().__init__()

        # read the window layout from file
        loadUi("static/analyse_stocks.ui", self)

        # move to home window after clicking a button
        self.back_button.clicked.connect(self.go_to_home)

        # setup a webengine for plots
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        # fill combobox with data from static csv file
        self.read_csv_file('static/stocks.csv', AnalyseStocks.stocks)
        self.fill_combo_box(AnalyseStocks.stocks, self.stocks_combobox)

        # default state
        self.stock_info_label.setText(AnalyseStocks.stocks[self.stocks_combobox.currentText()])
        self.show_line_plot()

        # Example of custom font
        font = QtGui.QFont("Roboto")
        self.stock_info_label.setFont(font)

        # switching between plot types with radio buttons
        self.line_plot_button.toggled.connect(lambda: self.set_plot_type(self.line_plot_button))
        self.candlestick_plot_button.toggled.connect(lambda: self.set_plot_type(self.candlestick_plot_button))
        self.cumulative_returns_plot_button.toggled.connect(lambda: self.set_plot_type(self.cumulative_returns_plot_button))

        # make elements of layout dependent from combobox value
        self.stocks_combobox.activated[str].connect(lambda: self.set_plot_type(self.line_plot_button))
        self.stocks_combobox.activated[str].connect(lambda: self.set_plot_type(self.candlestick_plot_button))
        self.stocks_combobox.activated[str].connect(lambda: self.set_plot_type(self.cumulative_returns_plot_button))
        self.stocks_combobox.activated[str].connect(
            lambda: self.stock_info_label.setText(self.stocks[self.stocks_combobox.currentText()]))

    def go_to_home(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)


# Inheritance form ChartWindow
class AnalyseCrypto(ChartWindow):
    # Dict stores data from static csv file
    cryptos = {}

    def __init__(self):
        super().__init__()

        # read the window layout from file
        loadUi("static/analyse_stocks.ui", self)

        # move to home window after clicking a button
        self.back_button.clicked.connect(self.go_to_home)

        # setup a webengine for plots
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        # fill combobox with data from static csv file
        self.read_csv_file('static/cryptos.csv', AnalyseCrypto.cryptos)
        self.fill_combo_box(AnalyseCrypto.cryptos, self.stocks_combobox)

        # default state
        self.stock_info_label.setText(AnalyseCrypto.cryptos[self.stocks_combobox.currentText()])
        self.show_line_plot()

        # switching between plot types with radio buttons
        self.line_plot_button.toggled.connect(lambda: self.set_plot_type(self.line_plot_button))
        self.candlestick_plot_button.toggled.connect(lambda: self.set_plot_type(self.candlestick_plot_button))
        self.cumulative_returns_plot_button.toggled.connect(lambda: self.set_plot_type(self.cumulative_returns_plot_button))

        # make elements of layout dependent from combobox value
        self.stocks_combobox.activated[str].connect(lambda: self.set_plot_type(self.line_plot_button))
        self.stocks_combobox.activated[str].connect(lambda: self.set_plot_type(self.candlestick_plot_button))
        self.stocks_combobox.activated[str].connect(lambda: self.set_plot_type(self.cumulative_returns_plot_button))
        self.stocks_combobox.activated[str].connect(
            lambda: self.stock_info_label.setText(self.cryptos[self.stocks_combobox.currentText()]))

    def go_to_home(self):
        widget.setCurrentIndex(widget.currentIndex() - 2)


# Inheritance form ChartWindow
class AnalyseCurrencies(ChartWindow):
    # Dict stores data from static csv file
    currencies = {}

    def __init__(self):
        super().__init__()
        # read the window layout from file
        loadUi("static/analyse_stocks.ui", self)
        # move to home window after clicking a button
        self.back_button.clicked.connect(self.go_to_home)

        # setup a webengine for plots
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        # fill combobox with data from static csv file
        self.read_csv_file('static/currencies.csv', AnalyseCurrencies.currencies)
        self.fill_combo_box(AnalyseCurrencies.currencies, self.stocks_combobox)

        # default state
        # self.stock_info_label.setText(AnalyseCurrencies.currencies[self.stocks_combobox.currentText()])
        self.show_line_plot()

        # switching between plot types with radio buttons
        self.line_plot_button.toggled.connect(lambda: self.set_plot_type(self.line_plot_button))
        self.candlestick_plot_button.toggled.connect(lambda: self.set_plot_type(self.candlestick_plot_button))
        self.cumulative_returns_plot_button.toggled.connect(lambda: self.set_plot_type(self.cumulative_returns_plot_button))
        # make elements of layout dependent from combobox value
        self.stocks_combobox.activated[str].connect(lambda: self.set_plot_type(self.line_plot_button))
        self.stocks_combobox.activated[str].connect(lambda: self.set_plot_type(self.candlestick_plot_button))
        self.stocks_combobox.activated[str].connect(lambda: self.set_plot_type(self.cumulative_returns_plot_button))
        self.stocks_combobox.activated[str].connect(lambda: self.stock_info_label.setText(self.currencies[self.stocks_combobox.currentText()]))

    def go_to_home(self):
        widget.setCurrentIndex(widget.currentIndex() - 3)


class PortfolioForm(QMainWindow):

    stocks = {}

    def __init__(self):
        super().__init__()

        # read the window layout from file
        loadUi("static/portfolio_form.ui", self)

        # move to home window after clicking a button
        self.back_button.clicked.connect(self.go_to_home)

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
        self.label_5.setText(str(round(yf.Ticker(str(self.comboBox_3.currentText())).history(period='1d')['Close'][0]*(self.spinBox_4.value()), 2)))

        self.save_button.clicked.connect(self.save_it)

    def label_update(self):
        value = round(double(yf.Ticker(str(self.comboBox_3.currentText())).history(period='1d')['Close'][0])*self.spinBox_4.value(), 2)
        self.label_5.setText(str(value))
        self.comboBox_3.activated[str].connect(lambda: self.label_5.setText(str(value)))


    def add_it(self):
        # spinBox value must be postive and multiple choice of the same company is not allowed
        if (self.spinBox_4.value() > 0 and not self.my_table.findItems(str(self.comboBox_3.currentText()), Qt.MatchContains)):
            item = QTableWidgetItem(str(self.comboBox_3.currentText()))
            item2 = QTableWidgetItem(str(self.spinBox_4.value()))
            item3 = QTableWidgetItem(str(self.label_5.text()))
            #item4 = QTableWidgetItem(str(date.today()))
            row_position = self.my_table.rowCount()
            self.my_table.insertRow(row_position)
            self.my_table.setItem(row_position, 0, item)
            self.my_table.setItem(row_position, 1, item2)
            self.my_table.setItem(row_position, 2, item3)
            #self.my_table.setItem(row_position, 3, item4)
            self.spinBox_4.setValue(0)

    def save_it(self):
        database_connector.create_table(self.textEdit.toPlainText())

        past_values = []

        for row in range(self.my_table.rowCount()):
            stock = '\''+self.my_table.item(row, 0).text()+'\''
            amount = self.my_table.item(row, 1).text()
            value = self.my_table.item(row, 2).text()
            database_connector.insert_into(self.textEdit.toPlainText(), stock, amount, value, '\''+str(date.today())+'\'')
            past_values.append(int(amount) * round(yf.Ticker(self.my_table.item(row,0).text()).history(period='1d')['Close'][0], 2))


        for i in range(analyse_portfolio_window.combobox.count()):
            if (analyse_portfolio_window.combobox.itemText(i) == self.textEdit.toPlainText()):

                #TODO: Add alert window here
                print('Portfolio exists')
        else:
            analyse_portfolio_window.combobox.addItem(self.textEdit.toPlainText())
            portfolio_edit_window.portfolio_combobox.addItem(self.textEdit.toPlainText())
            self.textEdit.clear()
            self.clear()
            self.show_pie_plot()


    def delete_it(self):
        clicked = self.my_table.currentRow()
        if (clicked == -1):
            clicked += 1
        self.my_table.removeRow(clicked)

    def clear(self):
        for i in reversed(range(self.my_table.rowCount())):
            self.my_table.removeRow(i)


    def go_to_home(self):
        widget.setCurrentIndex(widget.currentIndex() - 4)

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

        fig = go.Figure(data=[go.Pie(values=values, labels=stocks, hole=.4)])

        if self.my_table.rowCount() >= 1:
            self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
        else:
            self.browser.setHtml(None)

class PortfolioEdit(PortfolioForm):

    current_portfolio = ''
    portfolio_lenght = 0

    def __init__(self):
        super().__init__()

        # read the window layout from file
        loadUi("static/portfolio_edit.ui", self)

        # move to home window after clicking a button
        self.back_button.clicked.connect(self.go_to_home)

        self.fill_portfolio_combo_box()
        self.load_button.clicked.connect(self.load_portfolio)
        self.delete_portfolio_button.clicked.connect(self.delete_portfolio)

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
        self.label_5.setText(str(round(yf.Ticker(str(self.comboBox_3.currentText())).history(period='1d')['Close'][0]*(self.spinBox_4.value()), 2)))

        self.save_button.clicked.connect(self.save_it)

    def add_it(self):
        # spinBox value must be postive and multiple choice of the same company is not allowed
        x = (self.my_table.findItems(str(self.comboBox_3.currentText()), Qt.MatchContains))
        rows = []
        b = True

        for i in range(len(x)):
            rows.append(self.my_table.row(x[i]))

        for j in range(len(rows)):
            print(self.my_table.item(rows[j], 3).text())
            if (str(date.today()) == self.my_table.item(rows[j], 3).text()):
                b = False

        #TODO: Additional check for date:
        if (self.spinBox_4.value() > 0 and (len(x) == 0 or b)):
            item = QTableWidgetItem(str(self.comboBox_3.currentText()))
            item2 = QTableWidgetItem(str(self.spinBox_4.value()))
            item3 = QTableWidgetItem(str(self.label_5.text()))
            item4 = QTableWidgetItem(str(date.today()))
            row_position = self.my_table.rowCount()
            self.my_table.insertRow(row_position)
            self.my_table.setItem(row_position, 0, item)
            self.my_table.setItem(row_position, 1, item2)
            self.my_table.setItem(row_position, 2, item3)
            self.my_table.setItem(row_position, 3, item4)
            self.spinBox_4.setValue(0)

    def save_it(self):

        for row in range(PortfolioEdit.portfolio_lenght, self.my_table.rowCount()):
            stock = '\''+self.my_table.item(row, 0).text()+'\''
            amount = self.my_table.item(row, 1).text()
            value = self.my_table.item(row, 2).text()
            database_connector.insert_into(PortfolioEdit.current_portfolio, stock, amount, value, '\''+str(date.today())+'\'')
        self.clear()


        #TODO: Alert window
        '''
        for i in range(analyse_portfolio_window.combobox.count()):
            if (analyse_portfolio_window.combobox.itemText(i) == self.textEdit.toPlainText()):

                #TODO: Add alert window here
                print('Portfolio exists')
        else:
            analyse_portfolio_window.combobox.addItem(self.textEdit.toPlainText())
            portfolio_edit_window.portfolio_combobox.addItem(self.textEdit.toPlainText())
            self.textEdit.clear()
            self.clear()
            self.show_pie_plot()
        '''

    def go_to_home(self):
        widget.setCurrentIndex(widget.currentIndex() - 5)

    def fill_portfolio_combo_box(self):
        names = database_connector.show_tables()
        for name in names:
            self.portfolio_combobox.addItem(name)

    def load_portfolio(self):

        data = database_connector.select_from(self.portfolio_combobox.currentText())

        if PortfolioEdit.current_portfolio != self.portfolio_combobox.currentText():
            self.clear()
            for i in range(len(data)):
                item = QTableWidgetItem(str(data[i][0]))
                item2 = QTableWidgetItem(str(data[i][1]))
                item3 = QTableWidgetItem(str(data[i][2]))
                item4 = QTableWidgetItem(str(data[i][3]))
                row_position = self.my_table.rowCount()
                self.my_table.insertRow(row_position)
                self.my_table.setItem(row_position, 0, item)
                self.my_table.setItem(row_position, 1, item2)
                self.my_table.setItem(row_position, 2, item3)
                self.my_table.setItem(row_position, 3, item4)

        PortfolioEdit.current_portfolio = self.portfolio_combobox.currentText()
        PortfolioEdit.portfolio_lenght = self.my_table.rowCount()
        self.show_pie_plot()

    def delete_portfolio(self):
        #TODO: Alert box with confirmation
        portfolio_to_drop = self.portfolio_combobox.currentText()
        index = self.portfolio_combobox.findText(portfolio_to_drop)
        print('DROPING:' + portfolio_to_drop)
        database_connector.drop_table(portfolio_to_drop)
        self.portfolio_combobox.removeItem(index)
        #Error when combobox is clear
        #TODO: Specify an exception
        try:
            self.load_portfolio()
        except:
            self.clear()


class AnalysePortfolio(QMainWindow):

    current_portfolio = ''

    def __init__(self):
        super().__init__()

        # read the window layout from file
        loadUi("static/analyse_portfolio.ui", self)

        # move to home window after clicking a button
        self.back_button.clicked.connect(self.go_to_home)

        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        self.fill_combo_box()

        try:
            self.load_portfolio()
        except Exception as e:
            print('Preventing from crashing as there is no portfolio in database')
            print(e)

        self.load_button.clicked.connect(self.load_portfolio)


    def go_to_home(self):
        widget.setCurrentIndex(widget.currentIndex() - 6)

    def load_portfolio(self):
        data = database_connector.select_from(self.combobox.currentText())

        stocks = []
        values = []
        past_values = []

        for i in range(len(data)):
            if data[i][0] in stocks:
                stock_index = stocks.index(data[i][0])
                values[stock_index] += int(data[i][1])*round(yf.Ticker(data[i][0]).history(period='1d')['Close'][0], 2)
                past_values[stock_index] += float(data[i][2])
            else:
                stocks.append(data[i][0])
                values.append(int(data[i][1])*round(yf.Ticker(data[i][0]).history(period='1d')['Close'][0], 2))
                past_values.append(float(data[i][2]))

        fig = go.Figure(data=[go.Pie(values=values, labels=stocks, hole=.4)])
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

        self.value.setText(str(round(sum(values),2)) + ' $')

        # creating a color effect
        color_effect = QGraphicsColorizeEffect()

        #TODO: Compering the current value with the value from the date of portfolio last edit
        change = round(sum(values) - sum(past_values), 2)
        percentage_change = round((change/sum(past_values)) * 100, 2)
        if change > 0.0:
            profit = '+' + str(change) + ' $' + '       +' + str(percentage_change) + ' %'
            # setting color to color effect
            color_effect.setColor(Qt.darkGreen)
        elif change == 0.0:
            profit = str(abs(change)) + ' $' + '       ' + str(percentage_change) + ' %'
            color_effect.setColor(Qt.gray)
        else:
            profit = str(change) + ' $' + '       ' + str(percentage_change) + ' %'
            # setting color to color effect
            color_effect.setColor(Qt.red)

        self.change.setText(profit)
        # adding color effect to the label
        self.change.setGraphicsEffect(color_effect)

        #TODO: Make the same thing with all components

        self.clear()

        for i in range(len(data)):
            item = QTableWidgetItem(str(data[i][0]))
            item2 = QTableWidgetItem(str(round(int(data[i][1])*(yf.Ticker(data[i][0]).history(period='1d')['Close'][0]), 2)) + ' $')
            item3 = QTableWidgetItem(str(data[i][3]))
            component_change = round(int(data[i][1])*(yf.Ticker(data[i][0]).history(period='1d')['Close'][0]) - data[i][2], 2)
            font = QFont()
            font.setBold(True)
            if component_change > 0.0:
                component_change = '+'+str(component_change)+' $'
                color = Qt.darkGreen
            elif component_change == 0.0:
                component_change = str(abs(component_change)) + ' $'
                color = Qt.gray
            else:
                component_change = str(component_change) + ' $'
                color = Qt.red
            item4 = QTableWidgetItem(component_change)
            #item4.setBackground(color)
            item4.setForeground(color)
            item4.setFont(font)
            component_percentage_change = round(((int(data[i][1])*(yf.Ticker(data[i][0]).history(period='1d')['Close'][0]) - data[i][2])/data[i][2])*100, 2)
            if component_percentage_change > 0.0:
                component_percentage_change = '+'+str(component_percentage_change)+' %'
            elif component_percentage_change == 0.0:
                component_percentage_change = str(abs(component_percentage_change)) + ' %'
                color = Qt.gray
            else:
                component_percentage_change = str(component_percentage_change) + ' %'
            item5 = QTableWidgetItem(component_percentage_change)
            #item5.setBackground(color)
            item5.setForeground(color)
            item5.setFont(font)
            row_position = self.my_table.rowCount()
            self.my_table.insertRow(row_position)
            self.my_table.setItem(row_position, 0, item)
            self.my_table.setItem(row_position, 1, item2)
            self.my_table.setItem(row_position, 2, item3)
            self.my_table.setItem(row_position, 3, item4)
            self.my_table.setItem(row_position, 4, item5)

        try:
            sharpe_ratio = data_analysis.sharpe_ratio(stocks, values)
            self.sharpe.setText('Sharpe ratio: ' + str(round(sharpe_ratio, 2)))
        except Exception as e:
            print('DUPA: ')
            print(e)

        corr_data = data_analysis.correlation(stocks)
        (corr, extremes) = corr_data
        keys = list(extremes)
        (a,b) = keys[0]
        (c,d) = keys[1]


        self.corr.setText('Highest correletion between ' + a + ' and ' + b +': '+ str(round(extremes[keys[0]], 2)) + '\n' + 'Lowest correletion between ' + c + ' and ' + d +': '+str(round(extremes[keys[1]], 2)))

    # fill combobox with stock names
    def fill_combo_box(self):
        for name in database_connector.show_tables():
            if name == 'portfolio_names':
                continue
            self.combobox.addItem(name)

    def clear(self):
        for i in reversed(range(self.my_table.rowCount())):
            self.my_table.removeRow(i)


# run GUI
if __name__ == "__main__":
    # setup the app
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    database_connector = database.DatabaseConnector()
    data_analysis = data_analysis.DataAnalysis()
    # initialise all the windows
    home_window = Home()
    analyse_stocks_window = AnalyseStocks()
    analyse_crypto_window = AnalyseCrypto()
    analyse_currencies_window = AnalyseCurrencies()
    portfolio_form_window = PortfolioForm()
    portfolio_edit_window = PortfolioEdit()
    analyse_portfolio_window = AnalysePortfolio()


    # add main window to stack
    widget.addWidget(home_window)

    # customise the app with css styling
    with open('static/style.css', 'r') as file:
        stylesheet = file.read()
    app.setStyleSheet(stylesheet)
    QtGui.QFontDatabase.addApplicationFont("static/Roboto-Regular.ttf")

    # customise the app with icon and title
    app_icon = QSystemTrayIcon(QtGui.QIcon('static/icon.png'), parent=app)
    app_icon.show()
    icon = QtGui.QIcon("static/icon.png")
    app.setWindowIcon(icon)
    widget.setWindowTitle("Stock Assistant")

    # add the rest of the windows to stack
    widget.addWidget(analyse_stocks_window)
    widget.addWidget(analyse_crypto_window)
    widget.addWidget(analyse_currencies_window)
    widget.addWidget(portfolio_form_window)
    widget.addWidget(portfolio_edit_window)
    widget.addWidget(analyse_portfolio_window)

    # open in full screen
    widget.showMaximized()

    sys.exit(app.exec_())
