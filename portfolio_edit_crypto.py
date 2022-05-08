from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic import loadUi

from portfolio_edit import PortfolioEdit
from portfolio_form_crypto import PortfolioFormCrypto
import yfinance as yf


class PortfolioEditCrypto(PortfolioEdit):

    # store info about portfolio
    current_portfolio = ''
    portfolio_length = 0

    # list that store components that would be given to database queries
    components_to_drop = []
    components_to_add = []

    def __init__(self, analyse_portfolio_window, portfolio_edit_window):
        super().__init__(analyse_portfolio_window, portfolio_edit_window)

        # read the window layout from file
        loadUi("static/ui_files/portfolio_edit_crypto.ui", self)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # load/delete when right button is clicked
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
        self.read_csv_file('static/csv_files/cryptos.csv', PortfolioFormCrypto.cryptos)
        self.fill_combo_box(PortfolioFormCrypto.cryptos, self.stocks_combobox)

        try:
            self.fill_portfolio_combo_box()
        except (TypeError, IndexError) as e:
            print(e)

        # setup a webengine for plots
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        # update portfolio component value
        self.amount_spinbox.valueChanged.connect(self.label_update)
        self.stocks_combobox.activated.connect(self.label_update)
        self.value_label.setText(str(round(
            yf.Ticker(str(self.stocks_combobox.currentText())).history(period='1d')['Close'][0] * (self.amount_spinbox.value()),
            2)))

        self.save_button.clicked.connect(self.save_it)

    # fill combobox with portfolio names
    def fill_portfolio_combo_box(self):
        names = self.database_connector.show_tables()
        for name in names:
            x = self.database_connector.select_from(name)[0][0]
            if x in PortfolioFormCrypto.cryptos:
                self.portfolio_combobox.addItem(name)

    def load_portfolio(self):
        # clear list of components to drop and components to add while load portfolio
        self.components_to_drop = []
        self.components_to_add = []

        PortfolioEditCrypto.current_portfolio = ''

        # load portfolio data from database
        data = self.database_connector.select_from(self.portfolio_combobox.currentText())

        # fill the table with portfolio data
        if PortfolioEditCrypto.current_portfolio != self.portfolio_combobox.currentText():
            self.clear()
            for i in range(len(data)):
                item = QTableWidgetItem(str(data[i][0]))
                item2 = QTableWidgetItem(str(data[i][1]))
                item3 = QTableWidgetItem(str(data[i][2]))
                item4 = QTableWidgetItem(str(data[i][3]))
                row_position = self.portfolio_table.rowCount()
                self.portfolio_table.insertRow(row_position)
                self.portfolio_table.setItem(row_position, 0, item)
                self.portfolio_table.setItem(row_position, 1, item2)
                self.portfolio_table.setItem(row_position, 2, item3)
                self.portfolio_table.setItem(row_position, 3, item4)

        PortfolioEditCrypto.current_portfolio = self.portfolio_combobox.currentText()
        PortfolioEditCrypto.portfolio_length = self.portfolio_table.rowCount()
        self.show_pie_plot()
