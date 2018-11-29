# -*- coding: utf-8 -*-
# @Time    : 18-11-29 上午9:44
# @Author  : 张帆
# @Site    : 
# @File    : resetSecretDialogControl.py
# @Software: PyCharm
import json

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QMessageBox

from UIModel.resetSecretModel import ResetSecretModel
from UIView.resetSecretDialog import Ui_resetSecretDialog


class ResetSecretDialogControl(QDialog, Ui_resetSecretDialog):
    update_password_failed_signal = pyqtSignal(dict)
    update_password_success_signal = pyqtSignal(dict)

    def __init__(self, mainFormControl):
        super(ResetSecretDialogControl, self).__init__()
        self.setupUi(self)
        self.mainFormControl = mainFormControl
        self.client_type = self.mainFormControl.client_type
        self.user_name = self.mainFormControl.user_name
        self.userid = self.user_name + "_" + self.client_type
        self.update_password_failed_signal.connect(self.on_update_password_failed_signal)
        self.update_password_success_signal.connect(self.on_update_password_success_signal)

    def on_update_password_failed_signal(self, json):
        QMessageBox.critical(self, "修改失败",
                             self.tr(json['failure_reason']))

    def on_update_password_success_signal(self, json):
        QMessageBox.information(self, "修改成功", "修改成功")

    @pyqtSlot()
    def on_submit_pushButton_clicked(self):
        reset_secret_model = ResetSecretModel(self)
        if reset_secret_model.check():
            # 检查确认密码与新密码是否相同
            self.mainFormControl.send_to_signing_server(reset_secret_model.get_json())
        else:
            QMessageBox.critical(self, "错误!",
                                 self.tr("两次输入密码不相同!"))
