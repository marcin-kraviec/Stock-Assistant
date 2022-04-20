# add new requirement to requirements.txt by executing: pipreqs --force [project_path]

import sys

import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.express as px
from PyQt5 import QtWidgets, QtGui, QtWebEngineWidgets, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QWidget, QTableWidgetItem, QPushButton, \
    QGraphicsColorizeEffect, QMessageBox
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
        self.create_portfolio_crypto_button.clicked.connect(self.go_to_portfolio_form_crypto)
        self.edit_portfolio_crypto_button.clicked.connect(self.go_to_portfolio_edit_crypto)


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

    def go_to_portfolio_form_crypto(self):
        widget.setCurrentIndex(widget.currentIndex() + 10)

    def go_to_portfolio_edit_crypto(self):
        widget.setCurrentIndex(widget.currentIndex() + 11)

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
        trace = go.Candlestick(x=data['Date'], open=data['Open'], close=data['Close'], low=data['Low'], high=data['High'])
        data = [trace]
        layout = dict(
            title='Time series with range slider and selectors',
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6m',
                             step='month',
                             stepmode='backward'),
                        dict(count=1,
                             label='YTD',
                             step='year',
                             stepmode='todate'),
                        dict(count=1,
                             label='1y',
                             step='year',
                             stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date'
            )
        )

        fig = go.FigureWidget(data=data, layout=layout)
        fig.update_yaxes(fixedrange=False)
        fig.update_layout(hovermode="x unified")

        #fig.update_xaxes(showspikes=True, spikecolor="grey", spikesnap="cursor", spikemode="across", spikethickness=1)
        #fig.update_yaxes(showspikes=True, spikecolor="grey", spikethickness=1)

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

        trace = go.Scatter(x=data['Date'], y=data['Open'], name='Open')
        trace2 = go.Scatter(x=data['Date'], y=data['Close'], name='Close')
        data = [trace, trace2]
        layout = dict(
            title='Time series with range slider and selectors',
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6m',
                             step='month',
                             stepmode='backward'),
                        dict(count=1,
                             label='YTD',
                             step='year',
                             stepmode='todate'),
                        dict(count=1,
                             label='1y',
                             step='year',
                             stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date'
            )
        )

        fig = go.FigureWidget(data=data, layout=layout)
        fig.update_yaxes(fixedrange=False)
        fig.update_layout(hovermode="x unified")
        # changing plot into html file so that it can be displayed with webengine
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def show_cumulative_return_plot(self):
        # getting a current stock from combobox
        stock = self.stocks_combobox.currentText()

        # downloading data of stock from yfinance
        data = yf.download(stock, '2021-01-01', interval="1d")
        # data = yf.download(stock,'2022-04-01',interval="1h")
        data.reset_index(inplace=True)

        x = data['Close'].pct_change()
        returns = (x + 1).cumprod()

        # initialise line plot

        trace = go.Scatter(x=data['Date'], y=returns, name='Cumulative return')
        data = [trace]
        layout = dict(
            title='Time series with range slider and selectors',
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6m',
                             step='month',
                             stepmode='backward'),
                        dict(count=1,
                             label='YTD',
                             step='year',
                             stepmode='todate'),
                        dict(count=1,
                             label='1y',
                             step='year',
                             stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date'
            )
        )

        fig = go.FigureWidget(data=data, layout=layout)
        fig.layout.update(title_text=stock, xaxis_rangeslider_visible=True)
        fig.update_yaxes(fixedrange=False)
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
        font = QtGui.QFont("Sora")
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
            past_values.append(round(float(amount) * (yf.Ticker(self.my_table.item(row,0).text()).history(period='1d')['Close'][0]), 2))

        for i in range(analyse_portfolio_window.combobox.count()):
            if (analyse_portfolio_window.combobox.itemText(i) == self.textEdit.toPlainText()):
                self.alert_window("Portfolio with this name already exists!", "Alert window")
                print('Portfolio exists')
                break
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

    def alert_window(self, text, window_title):
        m = QMessageBox(self)
        # m.setIcon(QMessageBox.Information)
        m.setWindowIcon(QtGui.QIcon("static/alert.png"))
        m.setText(text)
        m.setWindowTitle(window_title)
        m.setStandardButtons(QMessageBox.Ok)
        m.exec()


class PortfolioFormCrypto(PortfolioForm):

    cryptos = {}

    def __init__(self):
        super().__init__()

        # read the window layout from file
        loadUi("static/portfolio_form_crypto.ui", self)

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
        self.read_csv_file('static/cryptos.csv', PortfolioFormCrypto.cryptos)
        self.fill_combo_box(PortfolioFormCrypto.cryptos, self.comboBox_3)

        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        # update latest company price
        self.spinBox_4.valueChanged.connect(self.label_update)
        self.comboBox_3.activated.connect(self.label_update)
        self.label_5.setText(str(round(yf.Ticker(str(self.comboBox_3.currentText())).history(period='1d')['Close'][0]*(self.spinBox_4.value()), 2)))

        self.save_button.clicked.connect(self.save_it)

    def go_to_home(self):
        widget.setCurrentIndex(widget.currentIndex() - 10)

    def save_it(self):
        database_connector.create_table(self.textEdit.toPlainText())

        past_values = []

        for row in range(self.my_table.rowCount()):
            stock = '\''+self.my_table.item(row, 0).text()+'\''
            amount = (self.my_table.item(row, 1).text())
            print(amount)
            value = self.my_table.item(row, 2).text()
            database_connector.insert_into(self.textEdit.toPlainText(), stock, amount, value, '\''+str(date.today())+'\'')
            past_values.append(round(float(amount) * (yf.Ticker(self.my_table.item(row,0).text()).history(period='1d')['Close'][0]), 2))

        for i in range(analyse_portfolio_window.combobox.count()):
            if (analyse_portfolio_window.combobox.itemText(i) == self.textEdit.toPlainText()):
                self.alert_window("Portfolio with this name already exists!", "Alert window")
                print('Portfolio exists')
                break
        else:
            analyse_portfolio_window.combobox.addItem(self.textEdit.toPlainText())
            portfolio_edit_crypto_window.portfolio_combobox.addItem(self.textEdit.toPlainText())
            self.textEdit.clear()
            self.clear()
            self.show_pie_plot()


class PortfolioEdit(PortfolioForm):

    current_portfolio = ''
    portfolio_length = 0

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

    #TODO: repair saving
    def save_it(self):
        for row in range(PortfolioEdit.portfolio_length, self.my_table.rowCount()):
            stock = '\''+self.my_table.item(row, 0).text()+'\''
            amount = self.my_table.item(row, 1).text()
            value = self.my_table.item(row, 2).text()
            database_connector.insert_into(PortfolioEdit.current_portfolio, stock, amount, value, '\''+str(date.today())+'\'')
        self.clear()
        self.alert_window("Portfolio saved succesfully!", "Alert window")

    def go_to_home(self):
        widget.setCurrentIndex(widget.currentIndex() - 5)

    def fill_portfolio_combo_box(self):
        names = database_connector.show_tables()
        for name in names:
            x = database_connector.select_from(name)[0][0]
            for stock in PortfolioForm.stocks:
                if (stock==x):
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
        PortfolioEdit.portfolio_length = self.my_table.rowCount()
        self.show_pie_plot()

    def delete_portfolio(self):
        #TODO: Alert box with confirmation
        portfolio_to_drop = self.portfolio_combobox.currentText()
        index = self.portfolio_combobox.findText(portfolio_to_drop)
        index2 = analyse_portfolio_window.combobox.findText(portfolio_to_drop)
        print('DROPING:' + portfolio_to_drop)
        database_connector.drop_table(portfolio_to_drop)
        self.portfolio_combobox.removeItem(index)
        analyse_portfolio_window.combobox.removeItem(index2)
        #Error when combobox is clear
        #TODO: Specify an exception
        try:
            self.load_portfolio()
        except:
            self.clear()

    def delete_it(self):
        clicked = self.my_table.currentRow()
        if (clicked == -1):
            clicked += 1
        stock = self.my_table.item(clicked, 0).text()
        date = self.my_table.item(clicked, 3)
        #TODO: deleting from database when save button clicked !!!
        self.my_table.removeRow(clicked)
        database_connector.delete_from(self.portfolio_combobox.currentText(), stock, date)

class PortfolioEditCrypto(PortfolioEdit):

    current_portfolio = ''
    portfolio_length = 0

    def __init__(self):
        super().__init__()

        # read the window layout from file
        loadUi("static/portfolio_edit_crypto.ui", self)

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
        self.read_csv_file('static/cryptos.csv', PortfolioFormCrypto.cryptos)
        self.fill_combo_box(PortfolioFormCrypto.cryptos, self.comboBox_3)

        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        # update latest company price
        self.spinBox_4.valueChanged.connect(self.label_update)
        self.comboBox_3.activated.connect(self.label_update)
        self.label_5.setText(str(round(yf.Ticker(str(self.comboBox_3.currentText())).history(period='1d')['Close'][0]*(self.spinBox_4.value()), 2)))

        self.save_button.clicked.connect(self.save_it)

    def go_to_home(self):
        widget.setCurrentIndex(widget.currentIndex() - 11)

    def fill_portfolio_combo_box(self):
        names = database_connector.show_tables()
        for name in names:
            x = database_connector.select_from(name)[0][0]
            for crypto in PortfolioFormCrypto.cryptos:
                if (crypto==x):
                    self.portfolio_combobox.addItem(name)

    def load_portfolio(self):
        data = database_connector.select_from(self.portfolio_combobox.currentText())

        if PortfolioEditCrypto.current_portfolio != self.portfolio_combobox.currentText():
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

        PortfolioEditCrypto.current_portfolio = self.portfolio_combobox.currentText()
        PortfolioEditCrypto.portfolio_length = self.my_table.rowCount()
        self.show_pie_plot()

class AnalysePortfolio(QMainWindow):

    current_portfolio = ''
    stocks = []
    values = []
    past_values = []

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

        self.portfolio_returns_button.clicked.connect(self.go_to_portfolio_charts)
        self.analyse_corr_button.clicked.connect(self.go_to_correlation_charts)
        self.analyse_sharpe_button.clicked.connect(self.go_to_sharpe_charts)


    def go_to_home(self):
        widget.setCurrentIndex(widget.currentIndex() - 6)

    def go_to_portfolio_charts(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)
        portfolio_charts_window.show_plot()

    def go_to_correlation_charts(self):
        widget.setCurrentIndex(widget.currentIndex() + 2)
        correlation_charts_window.show_plot()

    def go_to_sharpe_charts(self):
        widget.setCurrentIndex(widget.currentIndex() + 3)
        sharpe_charts_window.show_plot()


    def load_portfolio(self):
        data = database_connector.select_from(self.combobox.currentText())

        AnalysePortfolio.stocks = []
        AnalysePortfolio.values = []
        AnalysePortfolio.past_values = []

        for i in range(len(data)):
            if data[i][0] in AnalysePortfolio.stocks:
                stock_index = AnalysePortfolio.stocks.index(data[i][0])
                AnalysePortfolio.values[stock_index] += round(float(data[i][1])*yf.Ticker(data[i][0]).history(period='1d')['Close'][0], 2)
                AnalysePortfolio.past_values[stock_index] += float(data[i][2])
            else:
                AnalysePortfolio.stocks.append(data[i][0])
                AnalysePortfolio.values.append(round(float(data[i][1])*yf.Ticker(data[i][0]).history(period='1d')['Close'][0], 2))
                AnalysePortfolio.past_values.append(float(data[i][2]))

        fig = go.Figure(data=[go.Pie(values=AnalysePortfolio.values, labels=AnalysePortfolio.stocks, hole=.4)])
        #fig.layout.template = 'plotly_dark'
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

        self.value.setText(str(round(sum(AnalysePortfolio.values),2)) + ' $')

        # creating a color effect
        color_effect = QGraphicsColorizeEffect()

        #TODO: Compering the current value with the value from the date of portfolio last edit
        change = round(sum(AnalysePortfolio.values) - sum(AnalysePortfolio.past_values), 2)
        percentage_change = round((change/sum(AnalysePortfolio.past_values)) * 100, 2)
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
            item2 = QTableWidgetItem(str(round(float(data[i][1])*(yf.Ticker(data[i][0]).history(period='1d')['Close'][0]), 2)) + ' $')
            item3 = QTableWidgetItem(str(data[i][3]))
            component_change = round(float(data[i][1])*(yf.Ticker(data[i][0]).history(period='1d')['Close'][0]) - data[i][2], 2)
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
            component_percentage_change = round(((float(data[i][1])*(yf.Ticker(data[i][0]).history(period='1d')['Close'][0]) - data[i][2])/data[i][2])*100, 2)
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
            sharpe_ratio = data_analysis.sharpe_ratio(AnalysePortfolio.stocks, AnalysePortfolio.values)
            self.sharpe.setText('Sharpe ratio: ' + str(round(sharpe_ratio, 2)))
        except Exception as e:
            print('DUPA: ')
            print(e)

        corr_data = data_analysis.correlation(AnalysePortfolio.stocks)
        (corr, extremes) = corr_data
        keys = list(extremes)
        if len(keys) == 1:
            (a, b) = keys[0]
            self.corr.setText('Correletion between ' + a + ' and ' + b + ': ' + str(round(extremes[keys[0]], 2)))
        else:
            (a, b) = keys[0]
            (c, d) = keys[1]
            self.corr.setText('Highest correletion between ' + a + ' and ' + b +': '+ str(round(extremes[keys[0]], 2)) + '\n' + 'Lowest correletion between ' + c + ' and ' + d +': '+str(round(extremes[keys[1]], 2)))

        vol_data = data_analysis.volatility(AnalysePortfolio.stocks, AnalysePortfolio.values)
        (annual, daily) = vol_data
        self.risk.setText('Daily volatility: ' + str(round(daily*100, 2)) + ' %\n' + 'Annual volatility: ' + str(round(annual*100, 2)) + ' %' )

    # fill combobox with stock names
    def fill_combo_box(self):
        for name in database_connector.show_tables():
            if name == 'portfolio_names':
                continue
            self.combobox.addItem(name)

    def clear(self):
        for i in reversed(range(self.my_table.rowCount())):
            self.my_table.removeRow(i)

class PortfolioChart(QMainWindow):

    def __init__(self):
        super().__init__()
        # read the window layout from file
        loadUi("static/portfolio_charts.ui", self)

        # move to home window after clicking a button
        self.back_button.clicked.connect(self.go_to_analyse_portfolio)

        # setup a webengine for plots
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        self.show_plot()

    def show_plot(self):
        # getting a current stock from combobox
        y = AnalysePortfolio.stocks
        (data, dates) = data_analysis.cumulative_returns(AnalysePortfolio.stocks, AnalysePortfolio.values)

        # initialise line plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=data, name='Cumulative return'))
        fig.layout.update(title_text='Returns', xaxis_rangeslider_visible=True)
        fig.update_layout(hovermode="x unified")

        # changing plot into html file so that it can be displayed with webengine
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def go_to_analyse_portfolio(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)

class CorrelationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # read the window layout from file
        loadUi("static/portfolio_charts.ui", self)

        # move to home window after clicking a button
        self.back_button.clicked.connect(self.go_to_analyse_portfolio)

        # setup a webengine for plots
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        self.show_plot()

    def show_plot(self):
        # getting a current stock from combobox
        data = data_analysis.correlation(AnalysePortfolio.stocks)
        (corr, extremes) = data

        def df_to_plotly(df):
            return {'z': df.values.tolist(),
                    'x': df.columns.tolist(),
                    'y': df.index.tolist()}

        fig = go.Figure(data=go.Heatmap(df_to_plotly(corr)))
        #fig = go.Figure(data=ff.create_annotated_heatmap(corr))
        # initialise line plot

        # changing plot into html file so that it can be displayed with webengine
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def go_to_analyse_portfolio(self):
        widget.setCurrentIndex(widget.currentIndex() - 2)

class SharpeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # read the window layout from file
        loadUi("static/portfolio_charts.ui", self)

        # move to home window after clicking a button
        self.back_button.clicked.connect(self.go_to_analyse_portfolio)

        # setup a webengine for plots
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        self.show_plot()

    def show_plot(self):
        # getting a current stock from combobox
        data = data_analysis.optimise(AnalysePortfolio.stocks, AnalysePortfolio.values)
        (p_risk, p_returns, p_sharpe, p_weights, max_ind) = data
        print(p_risk[max_ind])
        print(p_returns[max_ind])
        #fig = go.Figure()
        #fig.add_trace(go.Scatter(x=dates, y=data, name='Cumulative return'))
        #fig.add_trace(go.Scatter(x=p_risk, y=p_returns, color=p_sharpe))
        fig = px.scatter(x=p_risk, y=p_returns, color=p_sharpe)
        fig.add_trace(go.Scatter(x=[p_risk[max_ind]], y=[p_returns[max_ind]], mode='markers',marker_symbol='x-thin', marker_size=10, marker_color="green"))
        #fig.add_trace(go.Scatter(x=[p_risk[max_ind]], y=[p_returns[max_ind]], mode='markers', marker_symbol='x-thin', marker_size=10, marker_color="blue"))
        #plt.scatter(p_risk[max_ind], p_returns[max_ind], color='r', marker='*', s=500)

        # changing plot into html file so that it can be displayed with webengine
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def go_to_analyse_portfolio(self):
        widget.setCurrentIndex(widget.currentIndex() - 3)


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
    portfolio_charts_window = PortfolioChart()
    correlation_charts_window = CorrelationWindow()
    sharpe_charts_window = SharpeWindow()
    portfolio_form_crypto_window = PortfolioFormCrypto()
    portfolio_edit_crypto_window = PortfolioEditCrypto()


    # add main window to stack
    widget.addWidget(home_window)

    # customise the app with css styling
    with open('static/style.css', 'r') as file:
        stylesheet = file.read()
    app.setStyleSheet(stylesheet)
    QtGui.QFontDatabase.addApplicationFont("static/Sora/Sora-Regular.ttf")

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
    widget.addWidget(portfolio_charts_window)
    widget.addWidget(correlation_charts_window)
    widget.addWidget(sharpe_charts_window)
    widget.addWidget(portfolio_form_crypto_window)
    widget.addWidget(portfolio_edit_crypto_window)


    # open in full screen
    widget.showMaximized()

    sys.exit(app.exec_())