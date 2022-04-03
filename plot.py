from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
import plotly.express as px
import yfinance as yf


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button = QtWidgets.QPushButton('Plot', self)
        self.browser = QtWebEngineWidgets.QWebEngineView(self)

        vlayout = QtWidgets.QVBoxLayout(self)
        vlayout.addWidget(self.button, alignment=QtCore.Qt.AlignHCenter)
        vlayout.addWidget(self.browser)

        self.button.clicked.connect(self.show_graph)
        self.resize(1000,800)

    def show_graph(self):

        stock = 'TSLA'
        data = yf.Ticker(stock)
        data = data.history()['Close']
        fig = px.line(data)
        fig.layout.update(xaxis_rangeslider_visible=True)
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

        '''
        df = px.data.tips()
        fig = px.box(df, x="day", y="total_bill", color="smoker")
        fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
        '''

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Widget()
    widget.show()
    app.exec()
    '''
    stock = 'TSLA'
    data = yf.Ticker(stock)
    data = data.history()['Close']
    fig = px.line(data)
    fig.layout.update(xaxis_rangeslider_visible=True)
    fig.show()
    '''