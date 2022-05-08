from datetime import date
from PyQt5.QtCore import Qt
from portfolio_form import PortfolioForm
from PyQt5 import QtWebEngineWidgets, QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import yfinance as yf
import logging

# inheritance from Portfolio Form
class PortfolioEdit(PortfolioForm):

    # store info about portfolio
    current_portfolio = ''
    portfolio_length = 0

    # list that store components that would be given to database queries
    components_to_drop = []
    components_to_add = []

    def __init__(self, analyse_portfolio_window, portfolio_edit_window):
        super().__init__(analyse_portfolio_window, portfolio_edit_window)

        # read the window layout from file
        loadUi("static/ui_files/portfolio_edit.ui", self)
        self.setWindowFlags(Qt.FramelessWindowHint)

        try:
            self.fill_portfolio_combo_box()
        except (TypeError, IndexError) as e:
            logging.error(str(e))

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
        self.read_csv_file('static/csv_files/stocks.csv', PortfolioForm.stocks)
        self.fill_combo_box(PortfolioForm.stocks, self.stocks_combobox)

        # setup a webengine for plots
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        # update portfolio component value
        self.amount_spinbox.valueChanged.connect(self.label_update)
        self.stocks_combobox.activated.connect(self.label_update)
        self.value_label.setText(str(round(
            yf.Ticker(str(self.stocks_combobox.currentText())).history(period='1d')['Close'][0] * (
                self.amount_spinbox.value()),
            2)))

        self.save_button.clicked.connect(self.save_it)

    def add_it(self):
        # check if table is empty
        if self.portfolio_table.rowCount() == 0:
            self.alert_window("Load your portfolio first!\t", "Alert window")
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
                stock = self.portfolio_table.item(row_position, 0).text()
                amount = self.portfolio_table.item(row_position, 1).text()
                value = self.portfolio_table.item(row_position, 2).text()
                edit_date = self.portfolio_table.item(row_position, 3).text()
                component = (stock, amount, value, edit_date)
                self.components_to_add.append(component)


            elif self.amount_spinbox.value() == 0:
                self.alert_window("Increase the number of the selected item.\t", "Alert window")

            elif not b:
                self.alert_window("You have bought this today.\t", "Alert window")

    def save_it(self):
        if self.portfolio_table.rowCount() >= 2:
            # delete components from database that had been dropped from table
            for i in range(len(self.components_to_drop)):
                # tuple unpacking
                (stock, edit_date) = self.components_to_drop[i]
                self.database_connector.delete_from(self.portfolio_combobox.currentText(), '\'' + stock + '\'', '\'' + edit_date + '\'')

            # insert components into database that had been added to the table
            for i in range(len(self.components_to_add)):
                # tuple unpacking
                (stock, amount, value, edit_date) = self.components_to_add[i]
                self.database_connector.insert_into(self.portfolio_combobox.currentText(), '\'' + stock + '\'', amount, value, '\'' + edit_date + '\'')

            self.clear()
            # clear list of components to drop and components to add after saving portfolio
            self.components_to_drop = []
            self.components_to_add = []
            self.show_pie_plot()
            self.alert_window("Portfolio saved successfully!", "Alert window")
        else:
            self.alert_window("There are too few items in your portfolio!", "Alert window")

    # fill combobox with portfolio names
    def fill_portfolio_combo_box(self):
        names = self.database_connector.show_tables()
        for name in names:
            x = self.database_connector.select_from(name)[0][0]
            if x in PortfolioForm.stocks:
                self.portfolio_combobox.addItem(name)

    def load_portfolio(self):
        # clear list of components to drop and components to add while load portfolio
        self.components_to_drop = []
        self.components_to_add = []

        PortfolioEdit.current_portfolio = ''

        # load portfolio data from database
        data = self.database_connector.select_from(self.portfolio_combobox.currentText())

        # fill the table with portfolio data
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
            self.alert_window("Please, load Your portfolio!\t", "Alert window")
        else:
            # initialise confirmation window
            m = QMessageBox(self)

            # customise confirmation window
            m.setWindowIcon(QtGui.QIcon("static/images/alert.png"))
            m.setText("Are you sure you want to delete this portfolio?\t")
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

                # When combobox is empty clear the table
                try:
                    self.load_portfolio()
                except:
                    self.clear()

                # show alert window when portfolio has been deleted
                self.alert_window("Portfolio has been deleted successfully.\t", "Alert window")

    # delete chosen row from the table
    def delete_it(self):
        clicked = self.portfolio_table.currentRow()
        if clicked == -1:
            clicked += 1
        stock = self.portfolio_table.item(clicked, 0).text()
        edit_date = self.portfolio_table.item(clicked, 3).text()
        self.portfolio_table.removeRow(clicked)
        component = (stock, edit_date)
        # add components data to components_to_drop list
        self.components_to_drop.append(component)

