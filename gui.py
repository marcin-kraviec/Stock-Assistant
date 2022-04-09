import sys
import yfinance as yf
import plotly.graph_objs as go
from PyQt5 import QtWidgets, QtGui, QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon
from PyQt5.uic import loadUi

# these lines tell the window that this is my own registered application, so I will decide the icon of it
import ctypes
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("static/home.ui", self)
        self.analyse_stocks_button.clicked.connect(self.go_to_analyse_stocks)
        self.analyse_crypto_button.clicked.connect(self.go_to_analyse_crypto)
        self.analyse_currencies_button.clicked.connect(self.go_to_analyse_currencies)

    def go_to_analyse_stocks(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

    def go_to_analyse_crypto(self):
        widget.setCurrentIndex(widget.currentIndex()+2)

    def go_to_analyse_currencies(self):
        widget.setCurrentIndex(widget.currentIndex()+3)

class AnalyseStocks(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("static/analyse_stocks.ui", self)
        self.back_button.clicked.connect(self.go_to_main_window)
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        self.back_button.clicked.connect(self.go_to_main_window)

        self.show_line_plot()
        self.line_plot_button.toggled.connect(lambda: self.set_plot_type(self.line_plot_button))
        self.candlestick_plot_button.toggled.connect(lambda: self.set_plot_type(self.candlestick_plot_button))


    def go_to_main_window(self):
        widget.setCurrentIndex(widget.currentIndex()-1)

    def show_candlestick_plot(self):
        stock = 'TSLA'
        #data = yf.download(stock,'2022-04-01',interval="1h")
        data = yf.download(stock, '2021-01-01', interval="1d")
        data.reset_index(inplace=True)

        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=data['Date'], open=data['Open'], close=data['Close'], low=data['Low'], high=data['High']))
        #fig.add_trace(go.Candlestick(x=data['index'], open=data['Open'], close=data['Close'], low=data['Low'], high=data['High']))
        fig.layout.update(title_text=stock, xaxis_rangeslider_visible=True)
        fig.update_layout(hovermode="x unified")

        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def show_line_plot(self):
        stock = 'TSLA'
        #data = yf.download(stock,'2022-04-01',interval="1h")
        data = yf.download(stock, '2021-01-01', interval="1d")
        data.reset_index(inplace=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='Open'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Close'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Low'], name='Low'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['High'], name='High'))
        fig.layout.update(title_text=stock, xaxis_rangeslider_visible=True)
        fig.update_layout(hovermode="x unified")

        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def set_plot_type(self, button):
        if button.isChecked():
            if button.text() == 'Line':
                self.show_line_plot()
            elif button.text() == 'Candlestick':
                self.show_candlestick_plot()

class AnalyseCrypto(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("static/analyse_crypto.ui", self)
        self.back_button.clicked.connect(self.go_to_main_window)
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        self.show_line_plot()
        self.line_plot_button.toggled.connect(lambda: self.set_plot_type(self.line_plot_button))
        self.candlestick_plot_button.toggled.connect(lambda: self.set_plot_type(self.candlestick_plot_button))

    def go_to_main_window(self):
        widget.setCurrentIndex(widget.currentIndex() - 2)

    def show_candlestick_plot(self):
        stock = 'ETH-USD'
        #data = yf.download(stock,'2022-04-01',interval="1h")
        data = yf.download(stock, '2021-01-01', interval="1d")
        data.reset_index(inplace=True)

        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=data['Date'], open=data['Open'], close=data['Close'], low=data['Low'], high=data['High']))
        #fig.add_trace(go.Candlestick(x=data['index'], open=data['Open'], close=data['Close'], low=data['Low'], high=data['High']))
        fig.layout.update(title_text=stock, xaxis_rangeslider_visible=True)
        fig.update_layout(hovermode="x unified")

        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def show_line_plot(self):
        stock = 'ETH-USD'
        #data = yf.download(stock,'2022-04-01',interval="1h")
        data = yf.download(stock, '2021-01-01', interval="1d")
        data.reset_index(inplace=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='Open'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Close'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Low'], name='Low'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['High'], name='High'))
        fig.layout.update(title_text=stock, xaxis_rangeslider_visible=True)
        fig.update_layout(hovermode="x unified")

        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def set_plot_type(self, button):
        if button.isChecked():
            if button.text() == 'Line':
                self.show_line_plot()
            elif button.text() == 'Candlestick':
                self.show_candlestick_plot()


class AnalyseCurrencies(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("static/analyse_currencies.ui", self)
        self.back_button.clicked.connect(self.go_to_main_window)
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.vlayout.addWidget(self.browser)

        self.show_line_plot()
        self.line_plot_button.toggled.connect(lambda: self.set_plot_type(self.line_plot_button))
        self.candlestick_plot_button.toggled.connect(lambda: self.set_plot_type(self.candlestick_plot_button))

    def go_to_main_window(self):
        widget.setCurrentIndex(widget.currentIndex() - 3)

    def show_candlestick_plot(self):
        stock = 'EURPLN=X'
        #data = yf.download(stock,'2022-04-01',interval="1h")
        data = yf.download(stock, '2021-01-01', interval="1d")
        data.reset_index(inplace=True)

        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=data['Date'], open=data['Open'], close=data['Close'], low=data['Low'], high=data['High']))
        #fig.add_trace(go.Candlestick(x=data['index'], open=data['Open'], close=data['Close'], low=data['Low'], high=data['High']))
        fig.layout.update(title_text=stock, xaxis_rangeslider_visible=True)
        fig.update_layout(hovermode="x unified")

        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def show_line_plot(self):
        stock = 'EURPLN=X'
        #data = yf.download(stock,'2022-04-01',interval="1h")
        data = yf.download(stock, '2021-01-01', interval="1d")
        data.reset_index(inplace=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='Open'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Close'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Low'], name='Low'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['High'], name='High'))
        fig.layout.update(title_text=stock, xaxis_rangeslider_visible=True)
        fig.update_layout(hovermode="x unified")

        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def set_plot_type(self, button):
        if button.isChecked():
            if button.text() == 'Line':
                self.show_line_plot()
            elif button.text() == 'Candlestick':
                self.show_candlestick_plot()

if __name__=="__main__":
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()

    main_window = MainWindow()
    analyse_stocks_window = AnalyseStocks()
    analyse_crypto_window = AnalyseCrypto()
    analyse_currencies_window = AnalyseCurrencies()

    app_icon = QSystemTrayIcon(QtGui.QIcon('static/icon.png'), parent=app)
    app_icon.show()

    widget.addWidget(main_window)
    widget.setWindowTitle("Stock Assistant")
    icon = QtGui.QIcon("static/icon.png")
    app.setWindowIcon(icon)

    widget.addWidget(analyse_stocks_window)
    widget.addWidget(analyse_crypto_window)
    widget.addWidget(analyse_currencies_window)
    widget.showMaximized()

    sys.exit(app.exec_())