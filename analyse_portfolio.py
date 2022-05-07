from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QGraphicsColorizeEffect, QMessageBox
from PyQt5.uic import loadUi
import yfinance as yf
import database_connector
import data_analysis
import plotly.express as px
import logging


class AnalysePortfolio(QMainWindow):

    # initialise database_connector and establish connection with database
    database_connector = database_connector.DatabaseConnector()

    # initialise data_analysis to provide methods for calculations
    data_analysis = data_analysis.DataAnalysis()

    # store important data about portfolio and allow other classes to access this data
    current_portfolio = ''
    stocks = []
    values = []
    past_values = []
    dates = []

    def __init__(self):
        super().__init__()

        # read the window layout from file
        loadUi("static/analyse_portfolio.ui", self)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # setup a webengine for plots
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        # default state with crashing prevention
        try:
            self.fill_combo_box()
        except TypeError as e:
            logging.error('There are not any portfolios in database: ' + str(e))

        # default state with crashing prevention
        try:
            self.load_portfolio()
        except TypeError as e:
            logging.error(str(e))

        # load window features for chosen portfolio
        self.load_button.clicked.connect(self.load_portfolio)
        self.info_corr_button.clicked.connect(lambda: self.info_window("Correlation",
                                                                       "In finance, correlation measures the degree to which two securities move in relation to each other.\n"
                                                                       "The values are in the range of 0 to 1.\nHigher correlation means that the stocks have returns that are more correlated."))
        self.info_risk_button.clicked.connect(lambda: self.info_window("Volatility",
                                                                       "In finance, volatility is a statistic that is used to measure risk and the instability of stock prices.\nIf a stock is very volatile, you can expect large changes in its price and therefore a higher risk.\n"
                                                                       "The annual volatility is calculated on the basis of all trading days in the year. (252 days)"))
        self.info_sharpe_button.clicked.connect(lambda: self.info_window("Sharpe ratio",
                                                                         "In finance, Sharpe ratio is the measure of the risk-adjusted return of a portfolio.\nA portfolio with a higher Sharpe ratio is considered as a better one.\n"
                                                                         "Sharpe ratios greater than 1 are considered optimal."))

    def load_portfolio(self):

        # get portfolio data from database
        data = self.database_connector.select_from(self.portfolio_combobox.currentText())

        AnalysePortfolio.stocks = []
        AnalysePortfolio.values = []
        AnalysePortfolio.past_values = []
        AnalysePortfolio.dates = []

        # pass the data of current portfolio components to provide this data for other classes
        for i in range(len(data)):
            AnalysePortfolio.dates.append(data[i][3])
            # check if a stock ticker was already added to stocks list
            # if yes add value to the previously calculated value for this ticker
            if data[i][0] in AnalysePortfolio.stocks:
                stock_index = AnalysePortfolio.stocks.index(data[i][0])
                # calculate current value of portfolio component
                AnalysePortfolio.values[stock_index] += float(data[i][1]) * round(
                    yf.Ticker(data[i][0]).history(period='1d')['Close'][0], 2)
                AnalysePortfolio.past_values[stock_index] += float(data[i][2])
            # if not append the value for a ticker
            else:
                AnalysePortfolio.stocks.append(data[i][0])
                AnalysePortfolio.values.append(
                    round(float(data[i][1]) * (yf.Ticker(data[i][0]).history(period='1d')['Close'][0]), 2))
                AnalysePortfolio.past_values.append(round(float(data[i][2]), 2))

        # initialise figure (pie plot)
        fig = px.pie(values=AnalysePortfolio.values, names=AnalysePortfolio.stocks, hole=.4,
                     color_discrete_sequence=px.colors.sequential.Viridis[::-1])

        # changing plot into html file so that it can be displayed with webengine
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

        # show current value of the portfolio
        self.value.setText(str(round(sum(AnalysePortfolio.values), 2)) + ' $')

        # creating a color effect
        color_effect = QGraphicsColorizeEffect()

        # calculate the profit/loss since portfolio creation
        change = round(sum(AnalysePortfolio.values) - sum(AnalysePortfolio.past_values), 2)
        percentage_change = round((change / sum(AnalysePortfolio.past_values)) * 100, 2)

        # setting the color corresponding to the profit/loss
        if change > 0.0:
            profit = '+' + str(change) + ' $' + '       +' + str(percentage_change) + ' %'
            # setting color to color effect
            color_effect.setColor(Qt.darkGreen)
        elif change == 0.0:
            profit = str(abs(change)) + ' $' + '       ' + str(percentage_change) + ' %'
            # setting color to color effect
            color_effect.setColor(Qt.gray)
        else:
            profit = str(change) + ' $' + '       ' + str(percentage_change) + ' %'
            # setting color to color effect
            color_effect.setColor(Qt.red)

        # show profit/loss of the portfolio
        self.change.setText(profit)

        # adding color effect to the label
        self.change.setGraphicsEffect(color_effect)

        # clear the table before adding new components of chosen portfolio
        self.clear()

        # loop responsible for adding portfolio components to the table
        for i in range(len(data)):
            # stock ticker
            item1 = QTableWidgetItem(str(data[i][0]))
            # value
            item2 = QTableWidgetItem(
                str(round(float(data[i][1]) * (yf.Ticker(data[i][0]).history(period='1d')['Close'][0]), 2)) + ' $')
            # date
            item3 = QTableWidgetItem(str(data[i][3]))
            # calculate profit/loss for the component
            component_change = round(
                float(data[i][1]) * (yf.Ticker(data[i][0]).history(period='1d')['Close'][0]) - data[i][2], 2)

            # creating a bold font
            font = QFont()
            font.setBold(True)

            # setting the color corresponding to the profit/loss
            if component_change > 0.0:
                component_change = '+' + str(component_change) + ' $'
                color = Qt.darkGreen
            elif component_change == 0.0:
                component_change = str(abs(component_change)) + ' $'
                color = Qt.gray
            else:
                component_change = str(component_change) + ' $'
                color = Qt.red

            # component profit/loss with corresponding color and bold font
            item4 = QTableWidgetItem(component_change)
            item4.setForeground(color)
            item4.setFont(font)

            # calculate percentage profit/loss for the component
            component_percentage_change = round(((float(data[i][1]) * (
                yf.Ticker(data[i][0]).history(period='1d')['Close'][0]) - data[i][2]) / data[i][2]) * 100, 2)

            # setting the color corresponding to the profit/loss
            if component_percentage_change > 0.0:
                component_percentage_change = '+' + str(component_percentage_change) + ' %'
            elif component_percentage_change == 0.0:
                component_percentage_change = str(abs(component_percentage_change)) + ' %'
                color = Qt.gray
            else:
                component_percentage_change = str(component_percentage_change) + ' %'

            # component profit/loss with corresponding color and bold font
            item5 = QTableWidgetItem(component_percentage_change)
            item5.setForeground(color)
            item5.setFont(font)

            # add components data to right row and cells
            row_position = self.portfolio_table.rowCount()
            self.portfolio_table.insertRow(row_position)
            self.portfolio_table.setItem(row_position, 0, item1)
            self.portfolio_table.setItem(row_position, 1, item2)
            self.portfolio_table.setItem(row_position, 2, item3)
            self.portfolio_table.setItem(row_position, 3, item4)
            self.portfolio_table.setItem(row_position, 4, item5)

        # calculate and show sharpe_ratio
        sharpe_ratio = self.data_analysis.sharpe_ratio(AnalysePortfolio.stocks, AnalysePortfolio.values)
        self.sharpe_label.setText('Sharpe ratio: ')

        sharpe_color = QGraphicsColorizeEffect()

        if round(sharpe_ratio, 2) < 0.8:
            sharpe_color.setColor(Qt.red)
        elif 0.8 <= round(sharpe_ratio, 2) < 1:
            sharpe_color.setColor(Qt.yellow)
        elif 1 <= round(sharpe_ratio, 2) < 1.2:
            sharpe_color.setColor(Qt.green)
        elif round(sharpe_ratio, 2) >= 1.2:
            sharpe_color.setColor(Qt.darkGreen)
        else:
            sharpe_color.setColor(Qt.gray)

        self.sharpe_value_label.setText(str(round(sharpe_ratio, 2)))
        self.sharpe_value_label.setGraphicsEffect(sharpe_color)

        # calculate correlation
        corr_data = self.data_analysis.correlation(AnalysePortfolio.stocks)
        (corr, extremes) = corr_data
        keys = list(extremes)
        # check if portfolio has only 2 components
        if len(keys) == 1:
            (a, b) = keys[0]
            self.corr_label.setText('Correletion between ' + a + ' and ' + b + ': ' + str(round(extremes[keys[0]], 2)))
        else:
            (a, b) = keys[0]
            (c, d) = keys[1]
            self.corr_label.setText('Highest correletion between ' + a + ' and ' + b + ': ' + str(
                round(extremes[keys[0]], 2)) + '\n' + 'Lowest correletion between ' + c + ' and ' + d + ': ' + str(
                round(extremes[keys[1]], 2)))

        # calculate and show daily and annual volatility
        vol_data = self.data_analysis.volatility(AnalysePortfolio.stocks, AnalysePortfolio.values)
        (annual, daily) = vol_data
        self.risk_label.setText(
            'Daily volatility: ' + str(round(daily * 100, 2)) + ' %\n' + 'Annual volatility: ' + str(
                round(annual * 100, 2)) + ' %')

    # fill portfolio_combobox with portfolio names
    def fill_combo_box(self):
        for name in self.database_connector.show_tables():
            if name == 'portfolio_names':
                continue
            self.portfolio_combobox.addItem(name)

    # clear the table
    def clear(self):
        for i in reversed(range(self.portfolio_table.rowCount())):
            self.portfolio_table.removeRow(i)

    def info_window(self, title, text):

        # initialise info window
        m = QMessageBox(self)

        # customise info window
        m.setWindowIcon(QIcon("static/info_icon.png"))
        # m.setText(header)
        m.setText(text)
        m.setWindowTitle(title)

        # provide options for user
        m.addButton(QMessageBox.Close)
        m.setStyleSheet("QPushButton {min-width:70px;\
                        min-height: 30px;}")
        m.exec()
