# add new requirement to requirements.txt by executing: pipreqs --force [project_path]
import sys
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import plotly.express as px
from PyQt5 import QtWidgets, QtGui, QtWebEngineWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QWidget, QTableWidgetItem, QPushButton
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
import csv
import ctypes
from numpy import double

# tell the window that this is my own registered application, so I will decide the icon of it
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

    def go_to_analyse_stocks(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_analyse_crypto(self):
        widget.setCurrentIndex(widget.currentIndex() + 2)

    def go_to_analyse_currencies(self):
        widget.setCurrentIndex(widget.currentIndex() + 3)

    def go_to_portfolio_form(self):
        widget.setCurrentIndex(widget.currentIndex() + 4)


class AnalyseStocks(QMainWindow):
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
        widget.setCurrentIndex(widget.currentIndex() - 1)

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


# Inheritance form AnalyseStocks
class AnalyseCrypto(AnalyseStocks):
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
        widget.setCurrentIndex(widget.currentIndex() - 2)


# Inheritance form AnalyseStocks
class AnalyseCurrencies(AnalyseStocks):
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
        widget.setCurrentIndex(widget.currentIndex() - 3)


class PortfolioForm(QMainWindow):

    stocks = {}

    def __init__(self):
        super().__init__()

        # read the window layout from file
        loadUi("static/portfolio_form.ui", self)

        try:
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
        except Exception as e:
            print(e)

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
            row_position = self.my_table.rowCount()
            self.my_table.insertRow(row_position)
            self.my_table.setItem(row_position, 0, item)
            self.my_table.setItem(row_position, 1, item2)
            self.my_table.setItem(row_position, 2, item3)
            self.spinBox_4.setValue(0)

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
            values.append(float(self.my_table.item(row, 2).text()) * int(self.my_table.item(row, 1).text()))


        data = {'stocks': stocks, 'values': values}

        df = pd.DataFrame(data)

        fig = px.pie(df, values='values', names='stocks')

        if self.my_table.rowCount() >= 1:
            self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
        else:
            self.browser.setHtml(None)


# run GUI
if __name__ == "__main__":
    # setup the app
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()

    # initialise all the windows
    home_window = Home()
    analyse_stocks_window = AnalyseStocks()
    analyse_crypto_window = AnalyseCrypto()
    analyse_currencies_window = AnalyseCurrencies()
    portfolio_form_window = PortfolioForm()

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

    # open in full screen
    widget.showMaximized()

    sys.exit(app.exec_())
