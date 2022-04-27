# add new requirement to requirements.txt by executing: pipreqs --force [project_path]

import sys
from time import sleep

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
from LoadingWindow import LoadingWindow, myThread
from bond_returns import BondReturns
# tell the window that this is my own registered application, so I will decide the icon of it
import ctypes

from numpy import double

myappid = 'stock_asisstant.1.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class CreateGui:
    def __init__(self):
        self.widget = QtWidgets.QStackedWidget()

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
        self.bond_returns_window = BondReturns()

        self.home_window.analyse_stocks_button.clicked.connect(self.go_to_analyse_stocks)
        self.home_window.analyse_crypto_button.clicked.connect(self.go_to_analyse_crypto)
        self.home_window.analyse_currencies_button.clicked.connect(self.go_to_analyse_currencies)
        self.home_window.create_portfolio_button.clicked.connect(self.go_to_create_portfolio)
        self.home_window.analyse_portfolio_button.clicked.connect(self.go_to_analyse_portfolio)
        self.home_window.edit_portfolio_button.clicked.connect(self.go_to_edit_portfolio)
        self.home_window.create_portfolio_crypto_button.clicked.connect(self.go_to_portfolio_form_crypto)
        self.home_window.edit_portfolio_crypto_button.clicked.connect(self.go_to_portfolio_edit_crypto)
        self.home_window.bond_returns_button.clicked.connect(self.go_to_bond_returns)
        self.home_window.minimize_button.clicked.connect(lambda: self.widget.showMinimized())

        self.analyse_stocks_window.back_button.clicked.connect(lambda: self.go_to_home(1))
        self.analyse_crypto_window.back_button.clicked.connect(lambda: self.go_to_home(2))
        self.analyse_currencies_window.back_button.clicked.connect(
            lambda: self.go_to_home(3))
        self.portfolio_form_window.back_button.clicked.connect(lambda: self.go_to_home(4))
        self.analyse_portfolio_window.back_button.clicked.connect(
            lambda: self.go_to_home(6))
        self.portfolio_edit_window.back_button.clicked.connect(lambda: self.go_to_home(5))
        self.portfolio_form_crypto_window.back_button.clicked.connect(
            lambda: self.go_to_home(10))
        self.portfolio_edit_crypto_window.back_button.clicked.connect(
            lambda: self.go_to_home(11))
        self.bond_returns_window.back_button.clicked.connect(lambda: self.go_to_home(12))

        self.analyse_portfolio_window.portfolio_returns_button.clicked.connect(
            lambda: self.go_to_portfolio_chart())
        self.portfolio_charts_window.back_button.clicked.connect(
            lambda: self.go_to_analyse_portfolio_back(1))
        self.analyse_portfolio_window.analyse_corr_button.clicked.connect(
            lambda: self.go_to_correlation_window())
        self.correlation_charts_window.back_button.clicked.connect(
            lambda: self.go_to_analyse_portfolio_back(2))
        self.analyse_portfolio_window.analyse_sharpe_button.clicked.connect(
            lambda: self.go_to_sharpe_window())
        self.sharpe_charts_window.back_button.clicked.connect(
            lambda: self.go_to_analyse_portfolio_back(3))

        self.widget.setWindowFlags(Qt.FramelessWindowHint)
        self.widget.addWidget(self.home_window)
        self.widget.addWidget(self.analyse_stocks_window)
        self.widget.addWidget(self.analyse_crypto_window)
        self.widget.addWidget(self.analyse_currencies_window)
        self.widget.addWidget(self.portfolio_form_window)
        self.widget.addWidget(self.portfolio_edit_window)
        self.widget.addWidget(self.analyse_portfolio_window)
        self.widget.addWidget(self.portfolio_charts_window)
        self.widget.addWidget(self.correlation_charts_window)
        self.widget.addWidget(self.sharpe_charts_window)
        self.widget.addWidget(self.portfolio_form_crypto_window)
        self.widget.addWidget(self.portfolio_edit_crypto_window)
        self.widget.addWidget(self.bond_returns_window)

    def go_to_analyse_stocks(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def go_to_analyse_crypto(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 2)

    def go_to_analyse_currencies(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 3)

    def go_to_create_portfolio(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 4)

    def go_to_edit_portfolio(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 5)

    def go_to_analyse_portfolio(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 6)

    def go_to_portfolio_form_crypto(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 10)

    def go_to_portfolio_edit_crypto(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 11)

    def go_to_bond_returns(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 12)

    def go_to_home(self, index):
        self.widget.setCurrentIndex(self.widget.currentIndex() - index)

    def go_to_portfolio_chart(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        self.portfolio_charts_window.show_plot()

    def go_to_sharpe_window(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 3)
        self.sharpe_charts_window.show_optimase_plot()

    def go_to_correlation_window(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 2)
        self.correlation_charts_window.show_correlation_plot()

    def go_to_analyse_portfolio_back(self, index):
        self.widget.setCurrentIndex(self.widget.currentIndex() - index)


# run GUI
if __name__ == "__main__":
    # setup the app
    app = QApplication(sys.argv)

    loading_window = LoadingWindow()
    t = myThread(loading_window)
    t.start()
    loading_window.setGeometry(560, 290, 800, 500)
    loading_window.show()

    database_connector = database.DatabaseConnector()
    data_analysis = data_analysis.DataAnalysis()

    controller_2 = CreateGui()

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
    controller_2.widget.showMaximized()
    loading_window.finish(controller_2.widget)
    t.terminate()

    sys.exit(app.exec_())