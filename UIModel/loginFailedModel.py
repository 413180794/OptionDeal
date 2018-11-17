# -*- coding: utf-8 -*-
# @Time    : 18-11-14 下午4:53
# @Author  : 张帆
# @Site    : 
# @File    : loginFailedModel.py
# @Software: PyCharm
from UIModel.model import Model


class LoginFailedModel(Model):

    def __init__(self, mainFromControl, purpose, failure_reason):
        self.mainFormControl = mainFromControl
        self.purpose = purpose
        self._failure_reason = failure_reason

    @classmethod
    def from_json(cls, mainFormControl, json):
        return cls(mainFormControl, json['purpose'], json['failure_reason'])

    @property
    def failure_reason(self):
        return self._failure_reason

    def get_json(self):
        raise NotImplemented


if __name__ == '__main__':
    x = LoginFailedModel('123', '123')
