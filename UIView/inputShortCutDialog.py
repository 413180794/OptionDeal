# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inputShortCutDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from UIView.customKeySequenceEdit import CustomKeySequenceEdit


class Ui_inputShortCutDialog(object):
    def setupUi(self, inputShortCutDialog):
        inputShortCutDialog.setObjectName("inputShortCutDialog")
        inputShortCutDialog.resize(389, 149)
        self.verticalLayout = QtWidgets.QVBoxLayout(inputShortCutDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.set_who_label = QtWidgets.QLabel(inputShortCutDialog)
        self.set_who_label.setText("")
        self.set_who_label.setObjectName("set_who_label")
        self.verticalLayout.addWidget(self.set_who_label)
        self.lineEdit = CustomKeySequenceEdit(inputShortCutDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.show_error_label = QtWidgets.QLabel(inputShortCutDialog)
        self.show_error_label.setText("")
        self.show_error_label.setObjectName("show_error_label")
        self.verticalLayout.addWidget(self.show_error_label)
        self.buttonBox = QtWidgets.QDialogButtonBox(inputShortCutDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(inputShortCutDialog)
        self.buttonBox.accepted.connect(inputShortCutDialog.accept)
        self.buttonBox.rejected.connect(inputShortCutDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(inputShortCutDialog)

    def retranslateUi(self, inputShortCutDialog):
        _translate = QtCore.QCoreApplication.translate
        inputShortCutDialog.setWindowTitle(_translate("inputShortCutDialog", "Dialog"))

