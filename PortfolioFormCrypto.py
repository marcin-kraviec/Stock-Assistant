from datetime import date

from PyQt5 import QtWebEngineWidgets
from PyQt5.uic import loadUi
import yfinance as yf
from PortfolioForm import PortfolioForm


class PortfolioFormCrypto(PortfolioForm):

    cryptos = {}

    def __init__(self, analyse_portfolio_window, portfolio_edit_window, portfolio_edit_crypto_window):
        super().__init__(analyse_portfolio_window, portfolio_edit_window)
        self.portfolio_edit_crypto_window = portfolio_edit_crypto_window
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

    def save_it(self):
        self.database_connector.create_table(self.textEdit.toPlainText())

        past_values = []
        if self.my_table.rowCount() == 0:
            self.alert_window("Portfolio is empty!", "Alert window")
            print('Portfolio is empty!')
        else:
            for i in range(self.analyse_portfolio_window.combobox.count()):
                if (self.analyse_portfolio_window.combobox.itemText(i) == self.textEdit.toPlainText()):
                    self.alert_window("Portfolio with this name already exists!", "Alert window")
                    print('Portfolio exists')
                    break
            else:
                for row in range(self.my_table.rowCount()):
                    stock = '\'' + self.my_table.item(row, 0).text() + '\''
                    amount = self.my_table.item(row, 1).text()
                    value = self.my_table.item(row, 2).text()
                    self.database_connector.insert_into(self.textEdit.toPlainText(), stock, amount, value,
                                                        '\'' + str(date.today()) + '\'')
                    past_values.append(
                        float(amount) * round(
                            yf.Ticker(self.my_table.item(row, 0).text()).history(period='1d')['Close'][0], 2))
                self.analyse_portfolio_window.combobox.addItem(self.textEdit.toPlainText())
                self.portfolio_edit_crypto_window.portfolio_combobox.addItem(self.textEdit.toPlainText())
                self.textEdit.clear()
                self.clear()
                self.show_pie_plot()
                self.alert_window("Portfolio has been saved succesfully.", "Alert window")
