from PyQt5 import QtWebEngineWidgets
from PyQt5.uic import loadUi
import yfinance as yf
from PortfolioForm import PortfolioForm



class PortfolioFormCrypto(PortfolioForm):
    cryptos = {}

    def __init__(self, analyse_portfolio_window, portfolio_edit_window):
        super().__init__(analyse_portfolio_window, portfolio_edit_window)

        # read the window layout from file
        loadUi("static/portfolio_form_crypto.ui", self)

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
        self.label_5.setText(str(round(
            yf.Ticker(str(self.comboBox_3.currentText())).history(period='1d')['Close'][0] * (self.spinBox_4.value()),
            2)))

        self.save_button.clicked.connect(self.save_it)