import csv
import yfinance as yf
from PyQt5.QtWidgets import QMainWindow
import plotly.graph_objs as go
import plotly.express as px
import data_analysis


class ChartWindow(QMainWindow):

    # initialise data_analysis to provide methods for calculations
    data_analysis = data_analysis.DataAnalysis()

    def __init__(self):
        super().__init__()

    def show_candlestick_plot(self):

        # getting a current stock from combobox
        stock = self.stocks_combobox.currentText()

        # downloading data of stock from yfinance
        data = yf.download(stock, start="2020-10-01", interval="1d")
        df = data['Close']
        data.reset_index(inplace=True)

        # calculating sma and std with 20 days window
        sma = df.rolling(window=20).mean().dropna()
        rstd = df.rolling(window=20).std().dropna()

        # calculating bollinger bands
        upper_band = sma + 2 * rstd
        lower_band = sma - 2 * rstd
        upper_band = upper_band.rename(columns={'Close': 'upper'})
        lower_band = lower_band.rename(columns={'Close': 'lower'})

        # dropping all the data that is before 2021-01-01
        sma.drop(sma.loc[sma.index < '2021-01-01 00:00:00'].index, inplace=True)
        upper_band.drop(upper_band.loc[upper_band.index < '2021-01-01 00:00:00'].index, inplace=True)
        lower_band.drop(lower_band.loc[lower_band.index < '2021-01-01 00:00:00'].index, inplace=True)
        data.drop(data.loc[data['Date'] < '2021-01-01 00:00:00'].index, inplace=True)

        # initialising traces that would be displayed on one plot
        trace1 = go.Scatter(x=lower_band.index, y=lower_band['lower'], name='Lower Band', line_color='rgba(173,204,255,0.2)')
        trace2 = go.Scatter(x=upper_band.index, y=upper_band['upper'], name='Upper Band', fill='tonexty', fillcolor='rgba(173,204,255,0.2)', line_color='rgba(173,204,255,0.2)')
        trace3 = go.Candlestick(x=data['Date'], open=data['Open'], close=data['Close'], low=data['Low'], high=data['High'], name='Value')
        trace4 = go.Scatter(x=sma.index, y=sma['Close'], name='SMA', line_color='#FECB52')

        data = [trace1, trace2, trace3, trace4]

        # providing layout information with time period options
        layout = dict(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1M',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6M',
                             step='month',
                             stepmode='backward'),
                        dict(count=1,
                             label='YTD',
                             step='year',
                             stepmode='todate'),
                        dict(count=1,
                             label='1Y',
                             step='year',
                             stepmode='backward'),
                        dict(count=1,
                             label='ALL',
                             step='all')
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date'
            )
        )

        # initialise figure (plot)
        fig = go.FigureWidget(data=data, layout=layout)
        fig.update_yaxes(fixedrange=False)
        fig.update_layout(hovermode="x unified")

        # change figure type to html so that it can be displayed in QWebEngineView
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))


    def show_line_plot(self):

        # getting a current stock from combobox
        stock = self.stocks_combobox.currentText()

        # downloading data of stock from yfinance
        data = yf.download(stock,start="2020-10-01", interval="1d")
        df = data['Close']
        data.reset_index(inplace=True)

        # calculating sma and std with 20 days window
        sma = df.rolling(window=20).mean().dropna()
        rstd = df.rolling(window=20).std().dropna()

        # calculating bollinger bands
        upper_band = sma + 2 * rstd
        lower_band = sma - 2 * rstd
        upper_band = upper_band.rename(columns={'Close': 'upper'})
        lower_band = lower_band.rename(columns={'Close': 'lower'})

        # dropping all the data that is before 2021-01-01
        sma.drop(sma.loc[sma.index < '2021-01-01 00:00:00'].index, inplace=True)
        upper_band.drop(upper_band.loc[upper_band.index < '2021-01-01 00:00:00'].index, inplace=True)
        lower_band.drop(lower_band.loc[lower_band.index < '2021-01-01 00:00:00'].index, inplace=True)
        data.drop(data.loc[data['Date'] < '2021-01-01 00:00:00'].index, inplace=True)

        # initialising traces that would be displayed on one plot
        trace1 = go.Scatter(x=lower_band.index,y=lower_band['lower'],name='Lower Band', line_color='rgba(173,204,255,0.2)')
        trace2 = go.Scatter(x=upper_band.index,y=upper_band['upper'],name='Upper Band',fill='tonexty',fillcolor='rgba(173,204,255,0.2)', line_color='rgba(173,204,255,0.2)')
        trace3 = go.Scatter(x=data['Date'],y=data['Close'],name='Close', line_color='#636EFA')
        trace4 = go.Scatter(x=data['Date'], y=data['Open'], name='Open', line_color='#FF0000')
        trace5 = go.Scatter(x=sma.index,y=sma['Close'],name='SMA', line_color='#FECB52')

        data = [trace1, trace2, trace3, trace4, trace5]

        # providing layout information with time period options
        layout = dict(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1M',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6M',
                             step='month',
                             stepmode='backward'),
                        dict(count=1,
                             label='YTD',
                             step='year',
                             stepmode='todate'),
                        dict(count=1,
                             label='1Y',
                             step='year',
                             stepmode='backward'),
                        dict(count=1,
                             label='ALL',
                             step='all')
                    ])
                ),
                rangeslider = dict(
                    visible=True
                ),
                type='date'
            )
        )

        # initialise figure (plot)
        fig = go.FigureWidget(data=data, layout=layout)
        fig.update_yaxes(fixedrange=False)
        fig.update_layout(hovermode="x unified")

        # change figure type to html so that it can be displayed in QWebEngineView
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def show_rsi_plot(self):

        # getting a current stock from combobox
        stock = self.stocks_combobox.currentText()

        # downloading data of stock from yfinance
        data = yf.download(stock, start='2021-01-01', interval="1d")
        data.reset_index(inplace=True)

        # calculate rsi
        df = self.data_analysis.rsi(data, period=13)

        # initialising traces that would be displayed on one plot
        trace1 = go.Scatter(x=df['Date'], y=[70] * len(df['Date']), name='Overbought', marker_color='#109618',line=dict(dash='dot'))
        trace2 = go.Scatter(x=df['Date'], y=df['RSI'], name='RSI', marker_color='#109618')
        trace3 = go.Scatter(x=df['Date'], y=[30] * len(df['Date']),name='Oversold', marker_color='#109618',line=dict(dash='dot'))

        data = [trace1, trace2, trace3]

        # providing layout information with time period options
        layout = dict(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1M',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6M',
                             step='month',
                             stepmode='backward'),
                        dict(count=1,
                             label='YTD',
                             step='year',
                             stepmode='todate'),
                        dict(count=1,
                             label='1Y',
                             step='year',
                             stepmode='backward'),
                        dict(count=1,
                             label='ALL',
                             step='all')
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date'
            )
        )

        # initialise figure (plot)
        fig = go.FigureWidget(data=data, layout=layout)
        fig.update_yaxes(fixedrange=False, range=[0, 100], tick0=0)
        fig.update_layout(hovermode="x unified")

        # change figure type to html so that it can be displayed in QWebEngineView
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def show_correlation_plot(self):

        # getting a current stock from combobox
        stock = self.stocks_combobox.currentText()

        # getting all stocks from combobox
        stocks = [self.stocks_combobox.itemText(i) for i in range(self.stocks_combobox.count())]

        # calculating correlation for stock in combobox
        data = self.data_analysis.correlation(stocks)
        (corr, extremes) = data
        df = corr[stock].abs().sort_values()

        # initialise figure (plot)
        fig = px.bar(x=df.index.tolist(), y=df.values.tolist(), color=df.values.tolist(),  color_continuous_scale=px.colors.sequential.Viridis,
                     labels={
                     'x': "Stock",
                     'y': "Correlation",
                     'color': 'Color'
                 },)
        fig.update_yaxes(range=[0, 1], tick0=0)

        # change figure type to html so that it can be displayed in QWebEngineView
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