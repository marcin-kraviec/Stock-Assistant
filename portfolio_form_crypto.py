from datetime import date
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import yfinance as yf
from portfolio_form import PortfolioForm

# inheritance from Portfolio Form
class PortfolioFormCrypto(PortfolioForm):

    # store info for combobox
    cryptos = {}

    def __init__(self, analyse_portfolio_window, portfolio_edit_window, portfolio_edit_crypto_window):

        super().__init__(analyse_portfolio_window, portfolio_edit_window)
        self.portfolio_edit_crypto_window = portfolio_edit_crypto_window

        # read the window layout from file
        loadUi("static/portfolio_form_crypto.ui", self)
        self.setWindowFlags(Qt.FramelessWindowHint)

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
        self.fill_combo_box(PortfolioFormCrypto.cryptos, self.stocks_combobox)

        # setup a webengine for plots
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        # update portfolio component value
        self.amount_spinbox.valueChanged.connect(self.label_update)
        self.stocks_combobox.activated.connect(self.label_update)
        self.value_label.setText(str(round(
            yf.Ticker(str(self.stocks_combobox.currentText())).history(period='1d')['Close'][0] * (self.amount_spinbox.value()),
            2)))

        # save portfolio in the database
        self.save_button.clicked.connect(self.save_it)

    def save_it(self):
        
        # create a table for portfolio in database
        self.database_connector.create_table(self.textEdit.toPlainText())

        past_values = []

        # check if table is empty
        if self.portfolio_table.rowCount() == 0:
            self.alert_window("Portfolio is empty!", "Alert window")
            print('Portfolio is empty!')
        else:

            for i in range(self.analyse_portfolio_window.portfolio_combobox.count()):
                # check if portfolio already exists
                if self.analyse_portfolio_window.portfolio_combobox.itemText(i) == self.textEdit.toPlainText():
                    self.alert_window("Portfolio with this name already exists!", "Alert window")
                    break
            else:
                # insert components to database table row by row
                for row in range(self.portfolio_table.rowCount()):
                    stock = '\'' + self.portfolio_table.item(row, 0).text() + '\''
                    amount = self.portfolio_table.item(row, 1).text()
                    value = self.portfolio_table.item(row, 2).text()
                    self.database_connector.insert_into(self.textEdit.toPlainText(), stock, amount, value,
                                                    '\'' + str(date.today()) + '\'')
                    past_values.append(
                        float(amount) * round(
                            yf.Ticker(self.portfolio_table.item(row, 0).text()).history(period='1d')['Close'][0], 2))

                # add portfolio name to comoboxes from different windows
                self.analyse_portfolio_window.portfolio_combobox.addItem(self.textEdit.toPlainText())
                self.portfolio_edit_crypto_window.portfolio_combobox.addItem(self.textEdit.toPlainText())

                # clear the layout elements
                self.textEdit.clear()
                self.clear()
                self.show_pie_plot()

                # show alert window if portfolio saved successfully
                self.alert_window("Portfolio has been saved successfully.", "Alert window")
