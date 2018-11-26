# -*- coding: utf-8 -*-
# @Time    : 18-11-26 下午4:14
# @Author  : 张帆
# @Site    : 
# @File    : udateUsersInfoModel.py
# @Software: PyCharm
from UIModel.model import Model


class UpdateUsersInfoModel(Model):
    def __init__(self, hedge_listWidget, transaction_listWidget, online_users):
        self.purpose = "users_info_update"
        self.online_users = online_users
        self.transaction_listWidget = transaction_listWidget  # 销售组用户列表
        self.hedge_listWidget = hedge_listWidget  # 对冲组用户列表

    @classmethod
    def from_json(cls, mainFormControl, json):
        return UpdateUsersInfoModel(mainFormControl.hedge_listWidget, mainFormControl.transaction_listWidget,
                                    json['online_users'])

    def remove_all_item(self):
        for row in range(1, self.transaction_listWidget.count()):
            # 删除销售组 所有用户
            self.transaction_listWidget.takeItem(row)

        for row in range(1, self.hedge_listWidget.count()):
            # 删除所有对冲组用户
            self.hedge_listWidget.takeItem(row)

    def add_new_item(self):
        '''添加更新的用户名'''
        for user_name_group in self.online_users:
            user_name, group = user_name_group.rsplit("_", 1)
            if group == "Hedge":
                self.hedge_listWidget.addItem(user_name)
            elif group == "Transaction":
                self.transaction_listWidget.addItem(user_name)

