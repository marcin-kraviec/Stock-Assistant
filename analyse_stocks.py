from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from chart_windowss.chart_window import ChartWindow
import os
from config.definitions import ROOT_DIR


# inheritance form ChartWindow
class AnalyseStocks(ChartWindow):

    # dict stores data from static csv file
    stocks = {}

    def __init__(self):
        super().__init__()

        # read the window layout from file
        ui_path = os.path.join(ROOT_DIR, 'static', 'ui_files', 'analyse_stocks.ui')
        loadUi(ui_path, self)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # setup a webengine for plots
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        # fill combobox with data from static csv file
        self.read_csv_file('../static/csv_files/stocks.csv', AnalyseStocks.stocks)
        self.fill_combo_box(AnalyseStocks.stocks, self.stocks_combobox)

        # default state
        self.stock_info_label.setText(AnalyseStocks.stocks[self.stocks_combobox.currentText()])
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
            lambda: self.stock_info_label.setText(self.stocks[self.stocks_combobox.currentText()]))