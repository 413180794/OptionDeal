# -*- coding: utf-8 -*-
# @Time    : 18-11-29 上午9:44
# @Author  : 张帆
# @Site    : 
# @File    : setTempSecretDialogControl.py
# @Software: PyCharm
import json

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QMessageBox

from UIModel.setTempSecretModel import SetTempSecretModel
from UIView.setTempSecretDialog import Ui_setTempSecretDialog


class SetTempSecretDialogControl(QDialog, Ui_setTempSecretDialog):
    def __init__(self, mainFormControl):
        super(SetTempSecretDialogControl, self).__init__()
        self.setupUi(self)
        self.mainFormControl = mainFormControl
        self.client_type = self.mainFormControl.client_type
        self.user_name = self.mainFormControl.user_name
        self.userid = self.user_name + "_" + self.client_type

    @pyqtSlot()
    def on_submit_pushButton_clicked(self):
        set_temp_secret_model = SetTempSecretModel(self)
        if set_temp_secret_model.check():
            # 检查确认密码与新密码是否相同
            self.mainFormControl.send_to_signing_server(set_temp_secret_model.get_json())
        else:
            QMessageBox.critical(self, "错误",
                                 self.tr("两次输入密码不相同"))
