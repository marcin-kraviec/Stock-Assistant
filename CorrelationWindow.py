from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
import data_analysis
import plotly.graph_objs as go
from AnalysePortfolio import AnalysePortfolio

class CorrelationWindow(QMainWindow):
    data_analysis = data_analysis.DataAnalysis()

    def __init__(self):
        super().__init__()
        # read the window layout from file
        loadUi("static/portfolio_charts.ui", self)

        # setup a webengine for plots
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        self.show_correlation_plot()

    def show_correlation_plot(self):
        # getting a current stock from combobox
        data = self.data_analysis.correlation(AnalysePortfolio.stocks)
        (corr, extremes) = data

        def df_to_plotly(df):
            return {'z': df.values.tolist(),
                    'x': df.columns.tolist(),
                    'y': df.index.tolist(),
                    'zmin':0, 'zmax':1}

        fig = go.Figure(data=go.Heatmap(df_to_plotly(corr), colorscale='Viridis'))
        #fig = go.Figure(data=ff.create_annotated_heatmap(corr))
        # initialise line plot

        # changing plot into html file so that it can be displayed with webengine
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))


