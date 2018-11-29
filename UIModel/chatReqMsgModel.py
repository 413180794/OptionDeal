# -*- coding: utf-8 -*-
# @Time    : 18-11-27 下午3:35
# @Author  : 张帆
# @Site    : 
# @File    : chatReqMsgModel.py
# @Software: PyCharm
import json

from UIModel.model import Model


class ChatReqMsgModel(Model):
    '''聊天请求数据包'''

    def __init__(self, input_msg_textEdit, company_name, user_name, group_list, client_type):
        self.input_msg_textEdit = input_msg_textEdit
        self.company_name = company_name
        self.user_name = user_name
        self.group_list = group_list
        self.client_type = client_type
        self.userid = self.user_name + "_" + self.client_type
        self._message = input_msg_textEdit.document().toPlainText()

    def get_json(self):
        return json.dumps({
            "purpose": "chat_message",
            "user_name": self.user_name,
            "group_list": self.group_list,
            "company_name": self.company_name,
            "userid": self.userid,
            "message": self.message
        })

    @property
    def message(self):
        return self._message

    def __str__(self):
        return str(json.loads(self.get_json()))
