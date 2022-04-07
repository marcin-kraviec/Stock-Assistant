# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'home.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from analyse_stocks import Ui_Analyse_Stocks_Window

class Ui_MainWindow(object):

    def open_analyse_stocks_window(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Analyse_Stocks_Window()
        self.ui.setupUi(self.window)
        self.window.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(959, 666)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.create_portofio_button = QtWidgets.QPushButton(self.centralwidget)
        self.create_portofio_button.setGeometry(QtCore.QRect(70, 380, 371, 51))
        self.create_portofio_button.setObjectName("create_portofio_button")
        self.analyse_portfolio_button = QtWidgets.QPushButton(self.centralwidget)
        self.analyse_portfolio_button.setGeometry(QtCore.QRect(70, 440, 371, 51))
        self.analyse_portfolio_button.setObjectName("analyse_portfolio_button")
        self.analyse_stocks_button = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.open_analyse_stocks_window())
        self.analyse_stocks_button.setGeometry(QtCore.QRect(460, 380, 371, 51))
        self.analyse_stocks_button.setObjectName("analyse_stocks_button")
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(80, 30, 901, 61))
        self.title_label.setObjectName("title_label")
        self.analyse_crypto_button = QtWidgets.QPushButton(self.centralwidget)
        self.analyse_crypto_button.setGeometry(QtCore.QRect(460, 440, 371, 51))
        self.analyse_crypto_button.setObjectName("analyse_crypto_button")
        self.simulate_bond_returns_button = QtWidgets.QPushButton(self.centralwidget)
        self.simulate_bond_returns_button.setGeometry(QtCore.QRect(70, 500, 371, 51))
        self.simulate_bond_returns_button.setObjectName("simulate_bond_returns_button")
        self.analyse_currencies_button = QtWidgets.QPushButton(self.centralwidget)
        self.analyse_currencies_button.setGeometry(QtCore.QRect(460, 500, 371, 51))
        self.analyse_currencies_button.setObjectName("analyse_currencies_button")
        self.introduction_label = QtWidgets.QLabel(self.centralwidget)
        self.introduction_label.setGeometry(QtCore.QRect(80, 110, 901, 221))
        self.introduction_label.setObjectName("introduction_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 959, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Stock Assistant"))
        MainWindow.setWindowIcon(QtGui.QIcon('static/icon.png'))
        self.create_portofio_button.setText(_translate("MainWindow", "Create Portfolio"))
        self.analyse_portfolio_button.setText(_translate("MainWindow", "Analyse Portfolio"))
        self.analyse_stocks_button.setText(_translate("MainWindow", "Analyse Stocks"))
        self.title_label.setText(_translate("MainWindow", "Welcome to Stock Assistant App!"))
        self.analyse_crypto_button.setText(_translate("MainWindow", "Analyse Crypto"))
        self.simulate_bond_returns_button.setText(_translate("MainWindow", "Simulate Bond Returns"))
        self.analyse_currencies_button.setText(_translate("MainWindow", "Analyse Currencies"))
        self.introduction_label.setText(_translate("MainWindow", "adhuadhuiahidhaisohiashaisoihshhaisdoohidashioashisioasiohhasihdaishashifhaiofohifohaifdhaiafaohi"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.setWindowIcon(QtGui.QIcon("static/icon.png"))
    sys.exit(app.exec_())
