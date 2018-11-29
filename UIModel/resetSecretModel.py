# -*- coding: utf-8 -*-
# @Time    : 18-11-29 上午10:34
# @Author  : 张帆
# @Site    : 
# @File    : resetSecretModel.py
# @Software: PyCharm
import hashlib
import json

from UIModel.model import Model


class ResetSecretModel(Model):
    def __init__(self, resetSecretDialogControl):
        self.resetSecretDialogControl = resetSecretDialogControl
        self.client_type = self.resetSecretDialogControl.client_type
        self.user_name = self.resetSecretDialogControl.user_name
        self.userid = self.user_name + "_" + self.client_type
        self.old_password = self.resetSecretDialogControl.old_password_LineEdit.text()
        self.new_password = self.resetSecretDialogControl.new_password_LineEdit.text()
        self.new_password_again = self.resetSecretDialogControl.new_password_again_LineEdit.text()



    def check(self):
        '''检查新密码与确认密码是否一样'''
        return True if self.new_password == self.new_password_again else False

    def get_json(self):
        return json.dumps({
            "purpose": "update_user_password",
            "client_type": self.client_type,
            "user_name": self.user_name,
            "old_password": self.get_password(self.old_password),
            "new_password": self.get_password(self.new_password),
            "userid": self.userid
        })

    def __repr__(self):
        return str(self.get_json())
