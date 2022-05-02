from datetime import date
from PyQt5.QtCore import Qt
from portfolio_form import PortfolioForm
from PyQt5 import QtWebEngineWidgets, QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import yfinance as yf


class PortfolioEdit(PortfolioForm):
    current_portfolio = ''
    portfolio_length = 0

    def __init__(self, analyse_portfolio_window, portfolio_edit_window):
        super().__init__(analyse_portfolio_window, portfolio_edit_window)

        # read the window layout from file
        loadUi("static/portfolio_edit.ui", self)
        self.setWindowFlags(Qt.FramelessWindowHint)

        try:
            self.fill_portfolio_combo_box()
        except TypeError as e:
            print(e)

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
        self.read_csv_file('static/stocks.csv', PortfolioForm.stocks)
        self.fill_combo_box(PortfolioForm.stocks, self.stocks_combobox)

        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        # update latest company price
        self.amount_spinbox.valueChanged.connect(self.label_update)
        self.stocks_combobox.activated.connect(self.label_update)
        self.value_label.setText(str(round(
            yf.Ticker(str(self.stocks_combobox.currentText())).history(period='1d')['Close'][0] * (
                self.amount_spinbox.value()),
            2)))

        self.save_button.clicked.connect(self.save_it)

    def add_it(self):
        if self.portfolio_table.rowCount() == 0:
            self.alert_window("Load your portfolio first!", "Alert window")
        else:
            # spinBox value must be positive and multiple choice of the same company is not allowed
            x = (self.portfolio_table.findItems(str(self.stocks_combobox.currentText()), Qt.MatchContains))
            rows = []
            b = True

            for i in range(len(x)):
                rows.append(self.portfolio_table.row(x[i]))

            for j in range(len(rows)):
                print(self.portfolio_table.item(rows[j], 3).text())
                if str(date.today()) == self.portfolio_table.item(rows[j], 3).text():
                    b = False

            if self.amount_spinbox.value() > 0 and (len(x) == 0 or b):
                item = QTableWidgetItem(str(self.stocks_combobox.currentText()))
                item2 = QTableWidgetItem(str(self.amount_spinbox.value()))
                item3 = QTableWidgetItem(str(self.value_label.text()))
                item4 = QTableWidgetItem(str(date.today()))
                row_position = self.portfolio_table.rowCount()
                self.portfolio_table.insertRow(row_position)
                self.portfolio_table.setItem(row_position, 0, item)
                self.portfolio_table.setItem(row_position, 1, item2)
                self.portfolio_table.setItem(row_position, 2, item3)
                self.portfolio_table.setItem(row_position, 3, item4)
                self.amount_spinbox.setValue(0)

            elif self.amount_spinbox.value() == 0:
                self.alert_window("Increase the number of the selected item.", "Alert window")

            elif not b:
                self.alert_window("You have bought this today.", "Alert window")

    # TODO: repair saving
    def save_it(self):
        for row in range(PortfolioEdit.portfolio_length, self.portfolio_table.rowCount()):
            stock = '\'' + self.portfolio_table.item(row, 0).text() + '\''
            amount = self.portfolio_table.item(row, 1).text()
            value = self.portfolio_table.item(row, 2).text()
            self.database_connector.insert_into(PortfolioEdit.current_portfolio, stock, amount, value,
                                                '\'' + str(date.today()) + '\'')
        self.clear()
        self.alert_window("Portfolio saved succesfully!", "Alert window")

    def fill_portfolio_combo_box(self):
        names = self.database_connector.show_tables()
        for name in names:
            x = self.database_connector.select_from(name)[0][0]
            if x in PortfolioForm.stocks:
                self.portfolio_combobox.addItem(name)

    def load_portfolio(self):

        data = self.database_connector.select_from(self.portfolio_combobox.currentText())

        if PortfolioEdit.current_portfolio != self.portfolio_combobox.currentText():
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

        PortfolioEdit.current_portfolio = self.portfolio_combobox.currentText()
        PortfolioEdit.portfolio_length = self.portfolio_table.rowCount()
        self.show_pie_plot()

    def delete_portfolio(self):
        if self.portfolio_table.rowCount() == 0:
            self.alert_window("Please, load Your portfolio!", "Alert window")
        else:
            # initialise confirmation window
            m = QMessageBox(self)

            # customise confirmation window
            m.setWindowIcon(QtGui.QIcon("static/alert.png"))
            m.setText("Are you sure you want to delete this portfolio?")
            m.setWindowTitle("Confirmation window")

            # provide options for user
            m.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            m.setStyleSheet("QPushButton {min-width:70px;\
                            min-height: 30px;}")
            btn = m.exec()

            # delete portfolio when yes option is chosen
            if btn == QMessageBox.Yes:
                portfolio_to_drop = self.portfolio_combobox.currentText()
                index = self.portfolio_combobox.findText(portfolio_to_drop)
                index2 = self.analyse_portfolio_window.combobox.findText(portfolio_to_drop)
                # print('DROPPING:' + portfolio_to_drop)
                self.database_connector.drop_table(portfolio_to_drop)
                self.portfolio_combobox.removeItem(index)
                self.analyse_portfolio_window.combobox.removeItem(index2)

                # Error when combobox is clear
                # TODO: Specify an exception
                try:
                    self.load_portfolio()
                except:
                    self.clear()

                # show alert window when portfolio has been deleted
                self.alert_window("Portfolio has been deleted successfully.", "Alert window")

    # delete chosen row from the table
    def delete_it(self):
        clicked = self.portfolio_table.currentRow()
        if clicked == -1:
            clicked += 1
        self.portfolio_table.removeRow(clicked)
        # stock = self.portfolio_table.item(clicked, 0).text()
        # date = self.portfolio_table.item(clicked, 3)
        # TODO: deleting from database when save button clicked !!!
        # self.database_connector.delete_from(self.portfolio_combobox.currentText(), stock, date)
