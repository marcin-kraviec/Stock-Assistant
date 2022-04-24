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

        self.a_button.toggled.connect(lambda: self.set_plot_type(self.a_button))
        self.b_button.toggled.connect(lambda: self.set_plot_type(self.b_button))

        self.show_optimase_plot()

    def show_optimase_plot(self):
        # getting a current stock from combobox
        data = self.data_analysis.optimise(AnalysePortfolio.stocks, AnalysePortfolio.values)
        (p_risk, p_returns, p_sharpe, p_weights, max_ind) = data
        print(p_risk[max_ind])
        print(p_returns[max_ind])

        print(p_risk[0])
        print(p_returns[0])
        #fig = go.Figure()
        #fig.add_trace(go.Scatter(x=dates, y=data, name='Cumulative return'))
        #fig.add_trace(go.Scatter(x=p_risk, y=p_returns, color=p_sharpe))
        fig = px.scatter(x=p_risk, y=p_returns, color=p_sharpe, color_continuous_scale=px.colors.sequential.Viridis)
        fig.add_trace(go.Scatter(x=[p_risk[max_ind]], y=[p_returns[max_ind]], mode='markers',marker_symbol='star', marker_size=10, marker_color="green"))
        fig.add_trace(go.Scatter(x=[p_risk[0]], y=[p_returns[0]], mode='markers', marker_symbol='star', marker_size=10, marker_color="blue"))
        #plt.scatter(p_risk[max_ind], p_returns[max_ind], color='r', marker='*', s=500)

        # changing plot into html file so that it can be displayed with webengine
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def show_weights_plot(self):
        data = self.data_analysis.optimise(AnalysePortfolio.stocks, AnalysePortfolio.values)
        (p_risk, p_returns, p_sharpe, p_weights, max_ind) = data

        fig = go.Figure(data=[
            go.Bar(name='Optimal: ' + str(round(p_sharpe[max_ind], 2)), x=AnalysePortfolio.stocks, y=p_weights[max_ind]),
            go.Bar(name='Current: ' + str(round(p_sharpe[0], 2)), x=AnalysePortfolio.stocks, y=p_weights[0])
        ])
        # Change the bar mode
        fig.update_layout(barmode='group')
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    # switching between plot types
    def set_plot_type(self, button):
        if button.isChecked():
            if button.text() == 'A':
                self.show_optimase_plot()
            elif button.text() == 'B':
                self.show_weights_plot()

