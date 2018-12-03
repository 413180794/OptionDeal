# -*- coding: utf-8 -*-
# @Time    : 18-11-12 下午9:09
# @Author  : 张帆
# @Site    : 
# @File    : loginSuccessModel.py
# @Software: PyCharm
from PyQt5 import QtWidgets, QtGui, QtCore

from UIModel.model import Model


class LoginSuccessModel(Model):
    '''收到登录成功数据包'''
    if_add_widget = False

    def __init__(self, mainFormControl, userid, company_name,option_type):
        self.mainFormControl = mainFormControl
        self._user_name, self._client_type = userid.split("_")
        self._company_name = company_name
        self.option_type = option_type
        self.mainFormControl.user_name = self._user_name
        self.mainFormControl.client_type = self._client_type
        self.mainFormControl.company_name = self._company_name
        self.mainFormControl.option_type = self.option_type
        
    @classmethod
    def from_json(cls, mainFormControl, json):
        return cls(mainFormControl, json.get('userid'), json.get("company_name"),json.get('option_type'))

    def change_type_option_combox(self, combox):
        for item in self.option_type.keys():
            combox.addItem(item)



