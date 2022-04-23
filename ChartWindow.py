import csv

import yfinance as yf
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMainWindow
import plotly.graph_objs as go


class ChartWindow(QMainWindow):

    def __init__(self):
        super().__init__()

    def show_candlestick_plot(self):
        # getting a current stock from combobox
        stock = self.stocks_combobox.currentText()
        templates = ['ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white', 'plotly_dark', 'presentation',
                     'xgridoff', 'ygridoff', 'gridon', 'none']
        # downloading data of stock from yfinance
        data = yf.download(stock, '2021-01-01', interval="1d")
        # data = yf.download(stock,'2022-04-01',interval="1h")
        data.reset_index(inplace=True)

        # initialise candlestick plot
        trace = go.Candlestick(x=data['Date'], open=data['Open'], close=data['Close'], low=data['Low'],
                               high=data['High'])
        data = [trace]
        layout = dict(
            title='Time series with range slider and selectors',
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6m',
                             step='month',
                             stepmode='backward'),
                        dict(count=1,
                             label='YTD',
                             step='year',
                             stepmode='todate'),
                        dict(count=1,
                             label='1y',
                             step='year',
                             stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date'
            )
        )

        fig = go.FigureWidget(data=data, layout=layout)
        fig.update_yaxes(fixedrange=False)
        fig.update_layout(hovermode="x unified")

        # fig.update_xaxes(showspikes=True, spikecolor="grey", spikesnap="cursor", spikemode="across", spikethickness=1)
        # fig.update_yaxes(showspikes=True, spikecolor="grey", spikethickness=1)

        fig.layout.template = templates[3]

        # changing plot into html file so that it can be displayed with webengine
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def show_line_plot(self):
        # getting a current stock from combobox
        stock = self.stocks_combobox.currentText()

        # downloading data of stock from yfinance
        data = yf.download(stock, '2021-01-01', interval="1d")
        # data = yf.download(stock,'2022-04-01',interval="1h")
        data.reset_index(inplace=True)

        trace = go.Scatter(x=data['Date'], y=data['Open'], name='Open')
        trace2 = go.Scatter(x=data['Date'], y=data['Close'], name='Close')
        data = [trace, trace2]
        layout = dict(
            title='Time series with range slider and selectors',
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6m',
                             step='month',
                             stepmode='backward'),
                        dict(count=1,
                             label='YTD',
                             step='year',
                             stepmode='todate'),
                        dict(count=1,
                             label='1y',
                             step='year',
                             stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date'
            )
        )

        fig = go.FigureWidget(data=data, layout=layout)
        fig.update_yaxes(fixedrange=False)
        fig.update_layout(hovermode="x unified")
        # changing plot into html file so that it can be displayed with webengine
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def show_cumulative_return_plot(self):
        # getting a current stock from combobox
        stock = self.stocks_combobox.currentText()

        # downloading data of stock from yfinance
        data = yf.download(stock, '2021-01-01', interval="1d")
        # data = yf.download(stock,'2022-04-01',interval="1h")
        data.reset_index(inplace=True)

        x = data['Close'].pct_change()
        returns = (x + 1).cumprod()

        # initialise line plot

        trace = go.Scatter(x=data['Date'], y=returns, name='Cumulative return')
        data = [trace]
        layout = dict(
            title='Time series with range slider and selectors',
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6m',
                             step='month',
                             stepmode='backward'),
                        dict(count=1,
                             label='YTD',
                             step='year',
                             stepmode='todate'),
                        dict(count=1,
                             label='1y',
                             step='year',
                             stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date'
            )
        )

        fig = go.FigureWidget(data=data, layout=layout)
        fig.layout.update(title_text=stock, xaxis_rangeslider_visible=True)
        fig.update_yaxes(fixedrange=False)
        fig.update_layout(hovermode="x unified")

        # changing plot into html file so that it can be displayed with webengine
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    # switching between plot types
    def set_plot_type(self, button):
        if button.isChecked():
            if button.text() == 'Line':
                self.show_line_plot()
            elif button.text() == 'Candlestick':
                self.show_candlestick_plot()
            elif button.text() == 'Cumulative returns':
                self.show_cumulative_return_plot()

    # fill combobox with stock names
    def fill_combo_box(self, dict, combobox):
        for key in dict.keys():
            combobox.addItem(key)

    # read the data from static csv file and fill stocks dict
    def read_csv_file(self, file_path, dict):
        with open(file_path) as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                dict[row[0]] = row[1]
