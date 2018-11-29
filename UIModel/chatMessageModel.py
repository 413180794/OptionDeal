# -*- coding: utf-8 -*-
# @Time    : 18-11-28 上午10:03
# @Author  : 张帆
# @Site    : 
# @File    : chatMessageModel.py
# @Software: PyCharm
import time

from PyQt5.QtWidgets import QTextBrowser

from UIModel.model import Model


class ChatMessageModel(Model):
    '''聊天信息到达数据包(服务器单向传输事件"'''

    def __init__(self, show_msg_textBrowser, to_company_group, html_list, from_user, from_company, message):
        self.from_user = from_user
        self.from_company = from_company
        self.message = message
        self.to_company_group = to_company_group
        self.show_msg_textBrowser = show_msg_textBrowser
        self.html_list = html_list

    @classmethod
    def from_json(cls, mainFormControl, json):
        return ChatMessageModel(mainFormControl.show_msg_textBrowser, mainFormControl.company_name,
                                mainFormControl.html_list, json['from_user'],
                                json['from_company'],
                                json['message'])

    def get_time(self):
        return time.strftime("%H:%M", time.localtime())

    def show_message(self):
        '''将收到的消息添加到文本显示框 对谁可能很多!'''
        print(self.to_company_group)
        self.html_list.append(f'''
                    <div style="margin:20px 10px;">
                    <div style="width:10%; text-align:center; margin:0 auto; background-color:white;
                            border-radius:10%; color:gray;"> {self.get_time()}</div>
                        <div >
                            <div style="margin-right:20px;"> {self.from_user} 对 {self.to_company_group}</div>
                            <div style="float: right;">{self.message}</div>
                        </div>
                    </div>
                       ''')
        self.show_msg_textBrowser.setHtml("".join(self.html_list))
