from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

from ChartWindow import ChartWindow
# Inheritance form ChartWindow
class AnalyseCrypto(ChartWindow):
    # Dict stores data from static csv file
    cryptos = {}

    def __init__(self):
        super().__init__()

        # read the window layout from file
        loadUi("static/analyse_stocks.ui", self)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # move to home window after clicking a button

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
        self.rsi_plot_button.toggled.connect(lambda: self.set_plot_type(self.rsi_plot_button))
        self.correlation_plot_button.toggled.connect(lambda: self.set_plot_type(self.correlation_plot_button))

        # make elements of layout dependent from combobox value
        self.stocks_combobox.activated[str].connect(lambda: self.set_plot_type(self.line_plot_button))
        self.stocks_combobox.activated[str].connect(lambda: self.set_plot_type(self.candlestick_plot_button))
        self.stocks_combobox.activated[str].connect(lambda: self.set_plot_type(self.rsi_plot_button))
        self.stocks_combobox.activated[str].connect(lambda: self.set_plot_type(self.correlation_plot_button))
        self.stocks_combobox.activated[str].connect(
            lambda: self.stock_info_label.setText(self.cryptos[self.stocks_combobox.currentText()]))
