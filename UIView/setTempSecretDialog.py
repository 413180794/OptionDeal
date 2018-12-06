# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setTempSecretDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_setTempSecretDialog(object):
    def setupUi(self, setTempSecretDialog):
        setTempSecretDialog.setObjectName("setTempSecretDialog")
        setTempSecretDialog.resize(415, 207)
        self.horizontalLayout = QtWidgets.QHBoxLayout(setTempSecretDialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.Label = QtWidgets.QLabel(setTempSecretDialog)
        self.Label.setObjectName("Label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Label)
        self.old_password_LineEdit = QtWidgets.QLineEdit(setTempSecretDialog)
        self.old_password_LineEdit.setObjectName("old_password_LineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.old_password_LineEdit)
        self.Label_4 = QtWidgets.QLabel(setTempSecretDialog)
        self.Label_4.setObjectName("Label_4")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.Label_4)
        self.temp_password_LineEdit = QtWidgets.QLineEdit(setTempSecretDialog)
        self.temp_password_LineEdit.setObjectName("temp_password_LineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.temp_password_LineEdit)
        self.Label_5 = QtWidgets.QLabel(setTempSecretDialog)
        self.Label_5.setObjectName("Label_5")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.Label_5)
        self.temp_password_again_LineEdit = QtWidgets.QLineEdit(setTempSecretDialog)
        self.temp_password_again_LineEdit.setObjectName("temp_password_again_LineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.temp_password_again_LineEdit)
        self.Label_6 = QtWidgets.QLabel(setTempSecretDialog)
        self.Label_6.setObjectName("Label_6")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.Label_6)
        self.valid_time_dateEdit = QtWidgets.QDateEdit(setTempSecretDialog)
        self.valid_time_dateEdit.setObjectName("valid_time_dateEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.valid_time_dateEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.submit_pushButton = QtWidgets.QPushButton(setTempSecretDialog)
        self.submit_pushButton.setObjectName("submit_pushButton")
        self.verticalLayout.addWidget(self.submit_pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(setTempSecretDialog)
        QtCore.QMetaObject.connectSlotsByName(setTempSecretDialog)

    def retranslateUi(self, setTempSecretDialog):
        _translate = QtCore.QCoreApplication.translate
        setTempSecretDialog.setWindowTitle(_translate("setTempSecretDialog", "Dialog"))
        self.Label.setText(_translate("setTempSecretDialog", "原密码"))
        self.Label_4.setText(_translate("setTempSecretDialog", "授权密码"))
        self.Label_5.setText(_translate("setTempSecretDialog", "确认授权密码"))
        self.Label_6.setText(_translate("setTempSecretDialog", "授权截止日"))
        self.submit_pushButton.setText(_translate("setTempSecretDialog", "提交更改"))

