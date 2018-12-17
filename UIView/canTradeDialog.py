# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'canTradeDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_canTradeDialog(object):
    def setupUi(self, canTradeDialog):
        canTradeDialog.setObjectName("canTradeDialog")
        canTradeDialog.resize(428, 313)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(canTradeDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(canTradeDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(canTradeDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableView.setAutoScroll(False)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(canTradeDialog)
        QtCore.QMetaObject.connectSlotsByName(canTradeDialog)

    def retranslateUi(self, canTradeDialog):
        _translate = QtCore.QCoreApplication.translate
        canTradeDialog.setWindowTitle(_translate("canTradeDialog", "今日可交易期权"))
        self.label.setText(_translate("canTradeDialog", "最小销量：50手"))

