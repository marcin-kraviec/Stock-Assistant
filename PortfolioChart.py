from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from AnalysePortfolio import AnalysePortfolio
import data_analysis
import plotly.graph_objs as go
from datetime import date

class PortfolioChart(QMainWindow):

    data_analysis = data_analysis.DataAnalysis()

    def __init__(self):
        super().__init__()
        # read the window layout from file
        loadUi("static/portfolio_charts.ui", self)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # setup a webengine for plots
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        self.show_plot()

    def show_plot(self):
        # getting a current stock from combobox
        y = AnalysePortfolio.stocks
        initial_date = min(AnalysePortfolio.dates)
        data = self.data_analysis.cumulative_returns(AnalysePortfolio.stocks, AnalysePortfolio.values, str(initial_date))

        fig = go.Figure(data= go.Scatter(x=data.index,y=data, marker_color='#1f9e89'))

        fig.update_yaxes(fixedrange=False)
        fig.update_layout( xaxis=dict(rangeslider=dict(visible=True)))
        fig.add_hline(y=1, line_dash="dot")
        #fig.update_xaxes(range=[dates[0], str(date.today())], tick0=0)
        fig.update_layout(hovermode="x unified")

        # changing plot into html file so that it can be displayed with webengine
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
