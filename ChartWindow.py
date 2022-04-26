import csv

import yfinance as yf
from PyQt5.QtWidgets import QMainWindow
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

import data_analysis


class ChartWindow(QMainWindow):

    data_analysis = data_analysis.DataAnalysis()

    def __init__(self):
        super().__init__()

    def show_candlestick_plot(self):

        # getting a current stock from combobox
        stock = self.stocks_combobox.currentText()
        # downloading data of stock from yfinance
        #data = yf.download(stock, '2021-01-01', interval="1d")
        data = yf.download(stock, interval="1d")
        df = data[['Close']]
        data.reset_index(inplace=True)

        #data.index = data.index.strftime("%Y/%m/%d %H:%M")

        sma = df.rolling(window=20).mean().dropna()
        rstd = df.rolling(window=20).std().dropna()

        upper_band = sma + 2 * rstd
        lower_band = sma - 2 * rstd

        upper_band = upper_band.rename(columns={'Close': 'upper'})
        lower_band = lower_band.rename(columns={'Close': 'lower'})

        sma.drop(sma.loc[sma.index < '2021-01-01 00:00:00'].index, inplace=True)
        upper_band.drop(upper_band.loc[upper_band.index < '2021-01-01 00:00:00'].index, inplace=True)
        lower_band.drop(lower_band.loc[lower_band.index < '2021-01-01 00:00:00'].index, inplace=True)
        data.drop(data.loc[data['Date'] < '2021-01-01 00:00:00'].index, inplace=True)


        # Plotting
        trace2 = go.Scatter(x=lower_band.index, y=lower_band['lower'], name='Lower Band', line_color='rgba(173,204,255,0.2)')
        trace3 = go.Scatter(x=upper_band.index, y=upper_band['upper'], name='Upper Band', fill='tonexty', fillcolor='rgba(173,204,255,0.2)', line_color='rgba(173,204,255,0.2)')
        trace4 = go.Candlestick(x=data['Date'], open=data['Open'], close=data['Close'], low=data['Low'], high=data['High'])
        trace5 = go.Scatter(x=sma.index, y=sma['Close'], name='SMA', line_color='#FECB52')

        data = [ trace2, trace3, trace4, trace5]
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
        '''
        fig.update_xaxes(
            rangeslider_visible=True,
            rangebreaks=[
                # NOTE: Below values are bound (not single values), ie. hide x to y
                dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
                dict(values=["2019-12-25", "2020-12-24"])]) # hide holidays (Christmas and New Year's, etc)
        # changing plot into html file so that it can be displayed with webengine
        '''
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))


    def show_line_plot(self):
        # getting a current stock from combobox
        stock = self.stocks_combobox.currentText()
        #data = yf.download(stock, '2021-01-01', interval="1d")
        data = yf.download(stock, interval="1d")
        # downloading data of stock from yfinance
        df = data[['Close']]
        data.reset_index(inplace=True)

        sma = df.rolling(window=20).mean().dropna()
        rstd = df.rolling(window=20).std().dropna()

        upper_band = sma + 2 * rstd
        lower_band = sma - 2 * rstd

        upper_band = upper_band.rename(columns={'Close': 'upper'})
        lower_band = lower_band.rename(columns={'Close': 'lower'})

        sma.drop(sma.loc[sma.index < '2021-01-01 00:00:00'].index, inplace=True)
        upper_band.drop(upper_band.loc[upper_band.index < '2021-01-01 00:00:00'].index, inplace=True)
        lower_band.drop(lower_band.loc[lower_band.index < '2021-01-01 00:00:00'].index, inplace=True)
        data.drop(data.loc[data['Date'] < '2021-01-01 00:00:00'].index, inplace=True)


        # Plotting
        trace2 = go.Scatter(x=lower_band.index,y=lower_band['lower'],name='Lower Band', line_color='rgba(173,204,255,0.2)')
        trace3 = go.Scatter(x=upper_band.index,y=upper_band['upper'],name='Upper Band',fill='tonexty',fillcolor='rgba(173,204,255,0.2)', line_color='rgba(173,204,255,0.2)')
        trace4 = go.Scatter(x=data['Date'],y=data['Close'],name='Close', line_color='#636EFA')
        trace5 = go.Scatter(x=data['Date'], y=data['Open'], name='Open', line_color='#FF0000')
        trace6 = go.Scatter(x=sma.index,y=sma['Close'],name='SMA', line_color='#FECB52')


        data = [trace2, trace3, trace4, trace5, trace6]
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
                rangeslider = dict(
                    visible=True
                ),
                type='date'
            )
        )

        fig = go.FigureWidget(data=data, layout=layout)
        fig.update_yaxes(fixedrange=False)
        fig.update_layout(hovermode="x unified")

        '''
        fig.update_xaxes(
            rangeslider_visible=True,
            rangebreaks=[
                # NOTE: Below values are bound (not single values), ie. hide x to y
                dict(bounds=["Sat", "Mon"]),  # hide weekends, eg. hide sat to before mon
                dict(values=["2019-12-25", "2020-12-24"])])  # hide holidays (Christmas and New Year's, etc)
        # changing plot into html file so that it can be displayed with webengine
        '''
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))


    def show_rsi_plot(self):
        # getting a current stock from combobox
        stock = self.stocks_combobox.currentText()

        # downloading data of stock from yfinance
        data = yf.download(stock, '2021-01-01', interval="1d")
        # data = yf.download(stock,'2022-04-01',interval="1h")
        data.reset_index(inplace=True)

        df = self.data_analysis.rsi(data, period=13)

        trace1 = go.Scatter(x=df['Date'], y=[70] * len(df['Date']), name='Overbought', marker_color='#109618',line=dict(dash='dot'))
        trace2 = go.Scatter(x=df['Date'], y=df['RSI'], name='RSI', marker_color='#109618')
        trace3 = go.Scatter(x=df['Date'], y=[30] * len(df['Date']),name='Oversold', marker_color='#109618',line=dict(dash='dot'))
        data = [trace1, trace2, trace3]
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
        fig.update_yaxes(fixedrange=False, range=[0, 100], tick0=0)
        fig.update_layout(hovermode="x unified")
        # changing plot into html file so that it can be displayed with webengine
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def show_correlation_plot(self):
        # getting a current stock from combobox
        stock = self.stocks_combobox.currentText()
        stocks = [self.stocks_combobox.itemText(i) for i in range(self.stocks_combobox.count())]

        data = self.data_analysis.correlation(stocks)
        (corr, extremes) = data

        df = corr[stock].abs().sort_values()

        def df_to_plotly(df):
            return {'y': df.values.tolist(),
                    'x': df.index.tolist()}

        #fig = go.Figure(data=go.Heatmap(df_to_plotly(df), colorscale='Viridis'))
        #fig = go.Figure(data=go.Bar(df_to_plotly(df), marker=dict(color = df.values.tolist(),colorscale='viridis')))

        fig = px.bar(x=df.index.tolist(), y=df.values.tolist(), color=df.values.tolist(),  color_continuous_scale=px.colors.sequential.Viridis)
        fig.update_yaxes(range=[0, 1], tick0=0)
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    # switching between plot types
    def set_plot_type(self, button):
        if button.isChecked():
            if button.text() == 'Line':
                self.show_line_plot()
            elif button.text() == 'Candlestick':
                self.show_candlestick_plot()
            elif button.text() == 'RSI':
                self.show_rsi_plot()
            elif button.text() == 'Correlation':
                self.show_correlation_plot()

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