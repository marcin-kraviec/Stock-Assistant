import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("static/home.ui", self)
        self.analyse_stocks_button.clicked.connect(self.go_to_analyse_stocks)

    def go_to_analyse_stocks(self):
        widget.setCurrentIndex(widget.currentIndex()+1)


class AnalyseStocks(QMainWindow):
    def __init__(self):
        super(AnalyseStocks, self).__init__()
        loadUi("static/analyse_stocks.ui", self)

if __name__=="__main__":
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    main_window = MainWindow()
    analyse_stocks_window = AnalyseStocks()
    widget.addWidget(main_window)
    widget.setWindowTitle("Stock Assistant")
    widget.setWindowIcon(QtGui.QIcon("static/icon.png"))
    widget.addWidget(analyse_stocks_window)
    widget.showMaximized()
    sys.exit(app.exec_())