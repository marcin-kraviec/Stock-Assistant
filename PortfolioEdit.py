from datetime import date

from PyQt5.QtCore import Qt

from PortfolioForm import PortfolioForm
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

        self.fill_portfolio_combo_box()
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
        self.fill_combo_box(PortfolioForm.stocks, self.comboBox_3)

        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        # update latest company price
        self.spinBox_4.valueChanged.connect(self.label_update)
        self.comboBox_3.activated.connect(self.label_update)
        self.label_5.setText(str(round(
            yf.Ticker(str(self.comboBox_3.currentText())).history(period='1d')['Close'][0] * (self.spinBox_4.value()),
            2)))

        self.save_button.clicked.connect(self.save_it)

    def add_it(self):
        # spinBox value must be postive and multiple choice of the same company is not allowed
        x = (self.my_table.findItems(str(self.comboBox_3.currentText()), Qt.MatchContains))
        rows = []
        b = True

        for i in range(len(x)):
            rows.append(self.my_table.row(x[i]))

        for j in range(len(rows)):
            print(self.my_table.item(rows[j], 3).text())
            if (str(date.today()) == self.my_table.item(rows[j], 3).text()):
                b = False

        # TODO: Additional check for date:
        if (self.spinBox_4.value() > 0 and (len(x) == 0 or b)):
            item = QTableWidgetItem(str(self.comboBox_3.currentText()))
            item2 = QTableWidgetItem(str(self.spinBox_4.value()))
            item3 = QTableWidgetItem(str(self.label_5.text()))
            item4 = QTableWidgetItem(str(date.today()))
            row_position = self.my_table.rowCount()
            self.my_table.insertRow(row_position)
            self.my_table.setItem(row_position, 0, item)
            self.my_table.setItem(row_position, 1, item2)
            self.my_table.setItem(row_position, 2, item3)
            self.my_table.setItem(row_position, 3, item4)
            self.spinBox_4.setValue(0)

    # TODO: repair saving
    def save_it(self):
        for row in range(PortfolioEdit.portfolio_length, self.my_table.rowCount()):
            stock = '\'' + self.my_table.item(row, 0).text() + '\''
            amount = self.my_table.item(row, 1).text()
            value = self.my_table.item(row, 2).text()
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
                row_position = self.my_table.rowCount()
                self.my_table.insertRow(row_position)
                self.my_table.setItem(row_position, 0, item)
                self.my_table.setItem(row_position, 1, item2)
                self.my_table.setItem(row_position, 2, item3)
                self.my_table.setItem(row_position, 3, item4)

        PortfolioEdit.current_portfolio = self.portfolio_combobox.currentText()
        PortfolioEdit.portfolio_length = self.my_table.rowCount()
        self.show_pie_plot()

    def delete_portfolio(self):
        if self.my_table.rowCount()==0:
            self.alert_window("Please, load Your portfolio!", "Alert window")
        else:
            m = QMessageBox(self)
            # m.setIcon(QMessageBox.Information)
            m.setWindowIcon(QtGui.QIcon("static/alert.png"))
            m.setText("Are you sure you want to delete this portfolio?")
            m.setWindowTitle("Confirmation window")
            m.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            btn = m.exec()
            if btn == QMessageBox.Yes:
                portfolio_to_drop = self.portfolio_combobox.currentText()
                index = self.portfolio_combobox.findText(portfolio_to_drop)
                index2 = self.analyse_portfolio_window.combobox.findText(portfolio_to_drop)
                print('DROPING:' + portfolio_to_drop)
                self.database_connector.drop_table(portfolio_to_drop)
                self.portfolio_combobox.removeItem(index)
                self.analyse_portfolio_window.combobox.removeItem(index2)
                # Error when combobox is clear
                # TODO: Specify an exception
                try:
                    self.load_portfolio()
                except:
                    self.clear()
                self.alert_window("Portfolio has been deleted succesfully.", "Alert window")





    def delete_it(self):
        clicked = self.my_table.currentRow()
        if (clicked == -1):
            clicked += 1
        stock = self.my_table.item(clicked, 0).text()
        date = self.my_table.item(clicked, 3)
        # TODO: deleting from database when save button clicked !!!
        self.my_table.removeRow(clicked)
        self.database_connector.delete_from(self.portfolio_combobox.currentText(), stock, date)
