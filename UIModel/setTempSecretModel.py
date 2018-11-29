# -*- coding: utf-8 -*-
# @Time    : 18-11-29 上午11:15
# @Author  : 张帆
# @Site    : 
# @File    : setTempSecretModel.py
# @Software: PyCharm
import json

from UIModel.model import Model


class SetTempSecretModel(Model):
    def __init__(self, setTempSecretDialogControl):
        self.setTempSecretDialogControl = setTempSecretDialogControl
        self.client_type = self.setTempSecretDialogControl.client_type
        self.user_name = self.setTempSecretDialogControl.user_name
        self.userid = self.setTempSecretDialogControl.userid
        self.old_password = self.setTempSecretDialogControl.old_password_LineEdit.text()
        self.temp_password = self.setTempSecretDialogControl.temp_password_LineEdit.text()
        self.temp_password_again = self.setTempSecretDialogControl.temp_password_again_LineEdit.text()
        self.valid_time = self.setTempSecretDialogControl.valid_time_dateEdit.text()

    def check(self):
        '''检查新密码与确认密码是否一样'''
        return True if self.temp_password == self.temp_password_again else False

    def get_json(self):
        return json.dumps({
            "purpose": "set_temp_password",
            "user_name": self.user_name,
            "temp_password": self.get_password(self.temp_password),
            "password":self.get_password(self.old_password),
            "valid_time": self.str_to_time_stamp(self.valid_time),
            "client_type": self.client_type,
            "userid": self.userid
        })
