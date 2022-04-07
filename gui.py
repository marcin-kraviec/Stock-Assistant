import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("static/home.ui", self)
        self.analyse_stocks_button.clicked.connect(self.go_to_analyse_stocks)
        self.analyse_crypto_button.clicked.connect(self.go_to_analyse_crypto)

    def go_to_analyse_stocks(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

    def go_to_analyse_crypto(self):
        widget.setCurrentIndex(widget.currentIndex()+2)


class AnalyseStocks(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("static/analyse_stocks.ui", self)
        self.back_button.clicked.connect(self.go_to_main_window)

    def go_to_main_window(self):
        widget.setCurrentIndex(widget.currentIndex()-1)

class AnalyseCrypto(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("static/analyse_crypto.ui", self)
        self.back_button.clicked.connect(self.go_to_main_window)

    def go_to_main_window(self):
        widget.setCurrentIndex(widget.currentIndex() - 2)

if __name__=="__main__":
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()

    main_window = MainWindow()
    analyse_stocks_window = AnalyseStocks()
    analyse_crypto_window = AnalyseCrypto()

    widget.addWidget(main_window)
    widget.setWindowTitle("Stock Assistant")
    widget.setWindowIcon(QtGui.QIcon("static/icon.png"))
    widget.addWidget(analyse_stocks_window)
    widget.addWidget(analyse_crypto_window)
    widget.showMaximized()

    sys.exit(app.exec_())