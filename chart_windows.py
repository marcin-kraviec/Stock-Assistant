# add new requirement to requirements.txt by executing: pipreqs --force [project_path]

import sys

import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from PyQt5 import QtWidgets, QtGui, QtWebEngineWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QWidget, QTableWidgetItem, QPushButton, \
    QGraphicsColorizeEffect
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from datetime import date
import database

import csv



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

    # switching between plot types
    def set_plot_type(self, button):
        if button.isChecked():
            if button.text() == 'Line':
                self.show_line_plot()
            elif button.text() == 'Candlestick':
                self.show_candlestick_plot()

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

        # make elements of layout dependent from combobox value
        self.stocks_combobox.activated[str].connect(lambda: self.set_plot_type(self.line_plot_button))
        self.stocks_combobox.activated[str].connect(lambda: self.set_plot_type(self.candlestick_plot_button))
        self.stocks_combobox.activated[str].connect(
            lambda: self.stock_info_label.setText(self.stocks[self.stocks_combobox.currentText()]))

    def go_to_home(self):
        from app_gui import widget
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

        # make elements of layout dependent from combobox value
        self.stocks_combobox.activated[str].connect(lambda: self.set_plot_type(self.line_plot_button))
        self.stocks_combobox.activated[str].connect(lambda: self.set_plot_type(self.candlestick_plot_button))
        self.stocks_combobox.activated[str].connect(
            lambda: self.stock_info_label.setText(self.cryptos[self.stocks_combobox.currentText()]))

    def go_to_home(self):
        from app_gui import widget
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

        # make elements of layout dependent from combobox value
        self.stocks_combobox.activated[str].connect(lambda: self.set_plot_type(self.line_plot_button))
        self.stocks_combobox.activated[str].connect(lambda: self.set_plot_type(self.candlestick_plot_button))
        self.stocks_combobox.activated[str].connect(lambda: self.stock_info_label.setText(self.currencies[self.stocks_combobox.currentText()]))

    def go_to_home(self):
        from app_gui import widget
        widget.setCurrentIndex(widget.currentIndex() - 3)

