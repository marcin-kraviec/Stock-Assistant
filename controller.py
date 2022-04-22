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
from temporery import *

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
        self.portfolio_form_window = PortfolioForm()
        self.portfolio_edit_window = PortfolioEdit()
        self.analyse_portfolio_window = AnalysePortfolio()
        '''
        self.portfolio_charts_window = PortfolioChart()
        self.correlation_charts_window = CorrelationWindow()
        self.sharpe_charts_window = SharpeWindow()
        '''
        self.portfolio_form_crypto_window = PortfolioFormCrypto()
        self.portfolio_edit_crypto_window = PortfolioEditCrypto()

        self.home_window.analyse_stocks_button.clicked.connect(self.go_to_analyse_stocks)
        self.home_window.analyse_crypto_button.clicked.connect(self.go_to_analyse_crypto)

        self.analyse_stocks_window.back_button.clicked.connect(lambda: self.go_to_home(self.analyse_stocks_window))
        self.analyse_crypto_window.back_button.clicked.connect(lambda: self.go_to_home(self.analyse_crypto_window))

        '''
        self.home_window.analyse_currencies_button.clicked.connect(self.go_to_analyse_currencies)
        self.home_window.create_portfolio_button.clicked.connect(self.go_to_portfolio_form)
        self.home_window.analyse_portfolio_button.clicked.connect(self.go_to_analyse_portfolio)
        self.home_window.edit_portfolio_button.clicked.connect(self.go_to_portfolio_edit)
        self.home_window.create_portfolio_crypto_button.clicked.connect(self.go_to_portfolio_form_crypto)
        self.home_window.edit_portfolio_crypto_button.clicked.connect(self.go_to_portfolio_edit_crypto)
        '''

    def go_to_analyse_stocks(self):
        self.home_window.close()
        self.analyse_stocks_window.show()
        ##
    def go_to_analyse_crypto(self):
        self.home_window.close()
        self.analyse_crypto_window.show()

    def go_to_home(self, window):
        window.close()
        self.home_window.show()
'''
    def login_to_kasta_or_otp(self):
        if self.main_page.login_page.logged_in and self.main_page.login_page.validAccount == 'True':
            self.main_page.login_page.close()
            self.kasta_page.show()
        elif self.main_page.login_page.logged_in and self.main_page.login_page.validAccount == 'False':
            self.otp_page.email_in_otp = self.main_page.login_page.email  # PRZEKAZANIE MAILA
            self.main_page.login_page.close()
            self.otp_page.show()

    
        def login_to_otp(self):
        if self.main_page.login_page.logged_in and self.main_page.login_page.validAccount == 'False':
            self.otp_page.email_in_otp = self.main_page.login_page.email # PRZEKAZANIE MAILA
            self.main_page.login_page.close()
            self.otp_page.show()


    def register_to_login(self):
        self.register_page.close()
        self.main_page.login_page.show()
        ##
        self.empty_error_labels()
        self.empty_text_fields()

    def register_to_otp(self):
        if self.register_page.successfully_registered:
            self.register_page.close()
            self.otp_page.email_in_otp = self.register_page.email # PRZEKAZANIE MAILA
            self.otp_page.show()

    def confirmation_to_login(self):
        self.confirmation_page.close()
        self.main_page.login_page.show()
        self.confirmation_page.close()
        self.main_page.login_page.show()
        ##
        self.empty_error_labels()
        self.empty_text_fields()
        self.empty_otp_field()
        self.timer.stop()

    def otp_to_login(self):
        if self.otp_page.is_confirmed:
            self.otp_page.close()
            self.confirmation_page.show()
            self.timer.start(5000)
'''

# run GUI
if __name__ == "__main__":
    # setup the app
    app = QApplication(sys.argv)
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



    sys.exit(app.exec_())
