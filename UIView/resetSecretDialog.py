# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resetSecretDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_resetSecretDialog(object):
    def setupUi(self, resetSecretDialog):
        resetSecretDialog.setObjectName("resetSecretDialog")
        resetSecretDialog.resize(365, 170)
        self.horizontalLayout = QtWidgets.QHBoxLayout(resetSecretDialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.Label = QtWidgets.QLabel(resetSecretDialog)
        self.Label.setObjectName("Label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Label)
        self.old_password_LineEdit = QtWidgets.QLineEdit(resetSecretDialog)
        self.old_password_LineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.old_password_LineEdit.setObjectName("old_password_LineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.old_password_LineEdit)
        self.Label_2 = QtWidgets.QLabel(resetSecretDialog)
        self.Label_2.setObjectName("Label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.Label_2)
        self.new_password_LineEdit = QtWidgets.QLineEdit(resetSecretDialog)
        self.new_password_LineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.new_password_LineEdit.setObjectName("new_password_LineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.new_password_LineEdit)
        self.Label_3 = QtWidgets.QLabel(resetSecretDialog)
        self.Label_3.setObjectName("Label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.Label_3)
        self.new_password_again_LineEdit = QtWidgets.QLineEdit(resetSecretDialog)
        self.new_password_again_LineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.new_password_again_LineEdit.setObjectName("new_password_again_LineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.new_password_again_LineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.submit_pushButton = QtWidgets.QPushButton(resetSecretDialog)
        self.submit_pushButton.setObjectName("submit_pushButton")
        self.verticalLayout.addWidget(self.submit_pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(resetSecretDialog)
        QtCore.QMetaObject.connectSlotsByName(resetSecretDialog)

    def retranslateUi(self, resetSecretDialog):
        _translate = QtCore.QCoreApplication.translate
        resetSecretDialog.setWindowTitle(_translate("resetSecretDialog", "Dialog"))
        self.Label.setText(_translate("resetSecretDialog", "原密码"))
        self.Label_2.setText(_translate("resetSecretDialog", "新密码"))
        self.Label_3.setText(_translate("resetSecretDialog", "确认密码"))
        self.submit_pushButton.setText(_translate("resetSecretDialog", "提交更改"))

