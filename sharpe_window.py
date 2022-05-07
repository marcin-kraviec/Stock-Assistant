from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from analyse_portfolio import AnalysePortfolio
import data_analysis
import plotly.graph_objs as go
import plotly.express as px
import logging


class SharpeWindow(QMainWindow):

    # initialise data_analysis to provide methods for calculations
    data_analysis = data_analysis.DataAnalysis()

    def __init__(self):
        super().__init__()

        # read the window layout from file
        loadUi("static/portfolio_charts.ui", self)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # setup a webengine for plots
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        # switching between plot types with radio buttons
        self.a_button.toggled.connect(lambda: self.set_plot_type(self.a_button))
        self.b_button.toggled.connect(lambda: self.set_plot_type(self.b_button))

        # default state
        try:
            self.show_optimise_plot()
        except ValueError as e:
            logging.error(str(e))

    def show_optimise_plot(self):

        # optimise portfolio with monte carlo method
        data = self.data_analysis.optimise(AnalysePortfolio.stocks, AnalysePortfolio.values)
        (p_risk, p_returns, p_sharpe, p_weights, max_ind) = data

        # initialise figure (plot)
        fig = px.scatter(x=p_risk, y=p_returns, color=p_sharpe, color_continuous_scale=px.colors.sequential.Viridis, labels={
                     'x': "Risk",
                     'y': "Returns",
                     'color': 'Sharpe'
                 },)
        # add optimal portfolio marker
        fig.add_trace(go.Scatter(x=[p_risk[max_ind]], y=[p_returns[max_ind]], mode='markers', marker_size=10, marker_color="#EF553B", name='Optimal'))
        # add current portfolio marker
        fig.add_trace(go.Scatter(x=[p_risk[0]], y=[p_returns[0]], mode='markers', marker_size=10, marker_color="grey", name='Current'))
        fig.update_layout(showlegend=False)

        # changing plot into html file so that it can be displayed with webengine
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def show_weights_plot(self):

        # optimise portfolio with monte carlo method
        data = self.data_analysis.optimise(AnalysePortfolio.stocks, AnalysePortfolio.values)
        (p_risk, p_returns, p_sharpe, p_weights, max_ind) = data

        # initialise figure (bar with 2 set of weights)
        fig = go.Figure(data=[
            go.Bar(name='Optimal: ' + str(round(p_sharpe[max_ind], 2)), x=AnalysePortfolio.stocks, y=p_weights[max_ind], marker_color='#EF553B'),
            go.Bar(name='Current: ' + str(round(p_sharpe[0], 2)), x=AnalysePortfolio.stocks, y=p_weights[0], marker_color='grey')
        ])

        # Change the bar mode
        fig.update_layout(barmode='group')
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    # switching between plot types
    def set_plot_type(self, button):
        if button.isChecked():
            if button.text() == 'A':
                self.show_optimise_plot()
            elif button.text() == 'B':
                self.show_weights_plot()

