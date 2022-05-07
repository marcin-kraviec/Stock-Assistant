from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from analyse_portfolio import AnalysePortfolio
import data_analysis
import plotly.graph_objs as go
from datetime import date


class PortfolioChart(QMainWindow):

    # initialise data_analysis to provide methods for calculations
    data_analysis = data_analysis.DataAnalysis()

    def __init__(self):
        super().__init__()

        # read the window layout from file
        loadUi("static/ui_files/portfolio_charts.ui", self)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # setup a webengine for plots
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        # default state
        self.show_plot()
        self.portfolio_charts_title_label.setText('Cumulative returns')
        self.info_label.setText('This window provides a cumulative returns plot. It shows the growth of each 1$ invested into portfolio.')

    def show_plot(self):

        # getting a date of portfolio creation
        initial_date = min(AnalysePortfolio.dates)

        # culculating cumulative returns
        data = self.data_analysis.cumulative_returns(AnalysePortfolio.stocks, AnalysePortfolio.values,
                                                     str(initial_date))
        # initialise figure (plot)
        fig = go.Figure(data=go.Scatter(x=data.index, y=data, marker_color='#1f9e89'))
        fig.update_yaxes(fixedrange=False)
        fig.update_layout(xaxis=dict(rangeslider=dict(visible=True)))
        fig.add_hline(y=1, line_dash="dot")
        fig.update_layout(hovermode="x unified")

        # changing plot into html file so that it can be displayed with webengine
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
