# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'analyse_stocks.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Analyse_Stocks_Window(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1067, 671)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stocks_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.stocks_combobox.setGeometry(QtCore.QRect(760, 50, 231, 22))
        self.stocks_combobox.setObjectName("stocks_combobox")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(50, 190, 941, 421))
        self.widget.setObjectName("widget")
        self.stock_name_label = QtWidgets.QLabel(self.centralwidget)
        self.stock_name_label.setGeometry(QtCore.QRect(50, 60, 361, 16))
        self.stock_name_label.setText("")
        self.stock_name_label.setObjectName("stock_name_label")
        self.stock_info_label = QtWidgets.QLabel(self.centralwidget)
        self.stock_info_label.setGeometry(QtCore.QRect(50, 120, 47, 13))
        self.stock_info_label.setObjectName("stock_info_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1067, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.stock_info_label.setText(_translate("MainWindow", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Analyse_Stocks_Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
