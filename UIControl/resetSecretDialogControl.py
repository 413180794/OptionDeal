# -*- coding: utf-8 -*-
# @Time    : 18-11-29 上午9:44
# @Author  : 张帆
# @Site    : 
# @File    : resetSecretDialogControl.py
# @Software: PyCharm
import json

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QMessageBox

from UIControl.tool import get_password_md5
from UIView.resetSecretDialog import Ui_resetSecretDialog


class ResetSecretDialogControl(QDialog, Ui_resetSecretDialog):
    update_password_failed_signal = pyqtSignal(dict)
    update_password_success_signal = pyqtSignal(dict)

    def __init__(self, client_type,user_name,send_to_server,parent):
        super(ResetSecretDialogControl, self).__init__(parent)
        self.setupUi(self)

        self.client_type =client_type
        self.user_name = user_name
        self.userid = self.user_name + "_" + self.client_type
        self.send_to_server = send_to_server
        self.update_password_failed_signal.connect(self.on_update_password_failed_signal)
        self.update_password_success_signal.connect(self.on_update_password_success_signal)

    def on_update_password_failed_signal(self, json):
        QMessageBox.critical(self, "修改失败",
                             self.tr(json['failure_reason']))

    def on_update_password_success_signal(self, json):
        QMessageBox.information(self, "修改成功", "修改成功")

    @pyqtSlot()
    def on_submit_pushButton_clicked(self):
        old_password = self.old_password_LineEdit.text()
        new_password = self.new_password_again_LineEdit.text()
        new_password_again = self.new_password_again_LineEdit.text()
        if new_password != new_password_again:
            # 如果两次输入的密码不同
            QMessageBox.critical(self, "错误!", "两次输入密码不相同!")
            return
        else:
            msg_json = json.dumps({
            "purpose": "update_user_password",
            "client_type": self.client_type,
            "user_name": self.user_name,
            "old_password": get_password_md5(old_password),
            "new_password": get_password_md5(new_password),
            "userid": self.userid
        })
            self.send_to_server(msg_json)