from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from AnalysePortfolio import AnalysePortfolio
import data_analysis
import plotly.graph_objs as go
import plotly.express as px


class SharpeWindow(QMainWindow):
    data_analysis = data_analysis.DataAnalysis()

    def __init__(self):
        super().__init__()
        # read the window layout from file
        loadUi("static/portfolio_charts.ui", self)

        # setup a webengine for plots
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        self.show_plot()

    def show_plot(self):
        # getting a current stock from combobox
        data = self.data_analysis.optimise(AnalysePortfolio.stocks, AnalysePortfolio.values)
        (p_risk, p_returns, p_sharpe, p_weights, max_ind) = data
        print(p_risk[max_ind])
        print(p_returns[max_ind])
        #fig = go.Figure()
        #fig.add_trace(go.Scatter(x=dates, y=data, name='Cumulative return'))
        #fig.add_trace(go.Scatter(x=p_risk, y=p_returns, color=p_sharpe))
        fig = px.scatter(x=p_risk, y=p_returns, color=p_sharpe)
        fig.add_trace(go.Scatter(x=[p_risk[max_ind]], y=[p_returns[max_ind]], mode='markers',marker_symbol='x-thin', marker_size=10, marker_color="green"))
        #fig.add_trace(go.Scatter(x=[p_risk[max_ind]], y=[p_returns[max_ind]], mode='markers', marker_symbol='x-thin', marker_size=10, marker_color="blue"))
        #plt.scatter(p_risk[max_ind], p_returns[max_ind], color='r', marker='*', s=500)

        # changing plot into html file so that it can be displayed with webengine
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
