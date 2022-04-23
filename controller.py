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
    QGraphicsColorizeEffect, QMessageBox, QDesktopWidget, QLayout
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QPoint
from datetime import date
import database
import data_analysis

import csv
# from temporery import *
from AnalyseCurrencies import AnalyseCurrencies
from AnalyseStocks import AnalyseStocks
from AnalyseCrypto import AnalyseCrypto
from Home import Home
from AnalysePortfolio import AnalysePortfolio
from PortfolioEdit import PortfolioEdit
from PortfolioForm import PortfolioForm
from PortfolioEditCrypto import PortfolioEditCrypto
from PortfolioFormCrypto import PortfolioFormCrypto
from CorrelationWindow import CorrelationWindow
from PortfolioChart import PortfolioChart
from SharpeWindow import SharpeWindow
from LoadingWindow import LoadingWindow
# tell the window that this is my own registered application, so I will decide the icon of it
import ctypes

from numpy import double

myappid = 'stock_asisstant.1.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class CreateGui:
    def __init__(self):
        self.home_window = Home()
        self.analyse_stocks_window = AnalyseStocks()
        self.analyse_crypto_window = AnalyseCrypto()
        self.analyse_currencies_window = AnalyseCurrencies()
        self.analyse_portfolio_window = AnalysePortfolio()
        self.portfolio_edit_window = PortfolioEdit(self.analyse_portfolio_window, self)
        self.portfolio_form_window = PortfolioForm(self.analyse_portfolio_window, self.portfolio_edit_window)
        self.portfolio_edit_crypto_window = PortfolioEditCrypto(self.analyse_portfolio_window, self)
        self.portfolio_form_crypto_window = PortfolioFormCrypto(self.analyse_portfolio_window,
                                                                self.portfolio_edit_window,
                                                                self.portfolio_edit_crypto_window)
        self.correlation_charts_window = CorrelationWindow()
        self.portfolio_charts_window = PortfolioChart()
        self.sharpe_charts_window = SharpeWindow()
        self.loading_window = LoadingWindow()

        self.home_window.analyse_stocks_button.clicked.connect(self.go_to_analyse_stocks)
        self.home_window.analyse_crypto_button.clicked.connect(self.go_to_analyse_crypto)
        self.home_window.analyse_currencies_button.clicked.connect(self.go_to_analyse_currencies)
        self.home_window.create_portfolio_button.clicked.connect(self.go_to_create_portfolio)
        self.home_window.analyse_portfolio_button.clicked.connect(self.go_to_analyse_portfolio)
        self.home_window.edit_portfolio_button.clicked.connect(self.go_to_edit_portfolio)
        self.home_window.create_portfolio_crypto_button.clicked.connect(self.go_to_portfolio_form_crypto)
        self.home_window.edit_portfolio_crypto_button.clicked.connect(self.go_to_portfolio_edit_crypto)

        self.analyse_stocks_window.back_button.clicked.connect(lambda: self.go_to_home(self.analyse_stocks_window))
        self.analyse_crypto_window.back_button.clicked.connect(lambda: self.go_to_home(self.analyse_crypto_window))
        self.analyse_currencies_window.back_button.clicked.connect(
            lambda: self.go_to_home(self.analyse_currencies_window))
        self.portfolio_form_window.back_button.clicked.connect(lambda: self.go_to_home(self.portfolio_form_window))
        self.analyse_portfolio_window.back_button.clicked.connect(
            lambda: self.go_to_home(self.analyse_portfolio_window))
        self.portfolio_edit_window.back_button.clicked.connect(lambda: self.go_to_home(self.portfolio_edit_window))
        self.portfolio_form_crypto_window.back_button.clicked.connect(
            lambda: self.go_to_home(self.portfolio_form_crypto_window))
        self.portfolio_edit_crypto_window.back_button.clicked.connect(
            lambda: self.go_to_home(self.portfolio_edit_crypto_window))

        self.analyse_portfolio_window.portfolio_returns_button.clicked.connect(
            lambda: self.go_to_portfolio_chart(self.analyse_portfolio_window))
        self.portfolio_charts_window.back_button.clicked.connect(
            lambda: self.go_to_analyse_portfolio_2(self.portfolio_charts_window))
        self.analyse_portfolio_window.analyse_corr_button.clicked.connect(
            lambda: self.go_to_correlation_window(self.analyse_portfolio_window))
        self.correlation_charts_window.back_button.clicked.connect(
            lambda: self.go_to_analyse_portfolio_2(self.correlation_charts_window))
        self.analyse_portfolio_window.analyse_sharpe_button.clicked.connect(
            lambda: self.go_to_sharpe_window(self.analyse_portfolio_window))
        self.sharpe_charts_window.back_button.clicked.connect(
            lambda: self.go_to_analyse_portfolio_2(self.sharpe_charts_window))

    def go_to_analyse_stocks(self):
        self.home_window.close()
        self.analyse_stocks_window.show()

    def go_to_analyse_crypto(self):
        self.home_window.close()
        self.analyse_crypto_window.show()

    def go_to_analyse_currencies(self):
        self.home_window.close()
        self.analyse_currencies_window.show()

    def go_to_create_portfolio(self):
        self.home_window.close()
        self.portfolio_form_window.show()

    def go_to_analyse_portfolio(self):
        self.home_window.close()
        self.analyse_portfolio_window.show()

    def go_to_edit_portfolio(self):
        self.home_window.close()
        self.portfolio_edit_window.show()

    def go_to_portfolio_edit_crypto(self):
        self.home_window.close()
        self.portfolio_edit_crypto_window.show()

    def go_to_portfolio_form_crypto(self):
        self.home_window.close()
        self.portfolio_form_crypto_window.show()

    def go_to_home(self, window):
        window.close()
        self.home_window.show()

    def go_to_portfolio_chart(self, window):
        window.close()
        self.portfolio_charts_window.show()
        self.portfolio_charts_window.show_plot()

    def go_to_analyse_portfolio_2(self, window):
        window.close()
        self.analyse_portfolio_window.show()

    def go_to_sharpe_window(self, window):
        window.close()
        self.sharpe_charts_window.show()
        self.sharpe_charts_window.show_optimase_plot()

    def go_to_correlation_window(self, window):
        window.close()
        self.correlation_charts_window.show()
        self.correlation_charts_window.show_correlation_plot()


# run GUI
if __name__ == "__main__":
    # setup the app
    app = QApplication(sys.argv)

    loading_window = LoadingWindow()
    loading_window.setGeometry(730,405,460,270)
    loading_window.show()
    loading_window.run()

    database_connector = database.DatabaseConnector()
    data_analysis = data_analysis.DataAnalysis()
    # initialise all the windows

    controller = CreateGui()

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

    controller.home_window.show()
    loading_window.finish(controller.home_window)

    sys.exit(app.exec_())
