# -*- coding: utf-8 -*-
# @Time    : 18-11-26 下午4:14
# @Author  : 张帆
# @Site    : 
# @File    : udateUsersInfoModel.py
# @Software: PyCharm
from UIModel.model import Model


# sam_南华_transaction 用户名_所在公司名_所在组类型


class UpdateUsersInfoModel(Model):
    def __init__(self, hedge_listWidget, transaction_listWidget, online_users):
        self.purpose = "users_info_update"
        self._online_users = online_users
        self.transaction_listWidget = transaction_listWidget  # 销售组用户列表
        self.hedge_listWidget = hedge_listWidget  # 对冲组用户列表

    @classmethod
    def from_json(cls, mainFormControl, json):
        return UpdateUsersInfoModel(mainFormControl.hedge_listWidget, mainFormControl.transaction_listWidget,
                                    json['online_users'])

    @property
    def online_users(self):
        return self._online_users

    def remove_all_item(self):
        # for row in range(0, self.transaction_listWidget.count()):
        #     # 删除销售组 所有用户
        #     self.transaction_listWidget.takeItem(row)
        #
        # for row in range(0, self.hedge_listWidget.count()):
        #     # 删除所有对冲组用户
        #     self.hedge_listWidget.takeItem(row)
        self.transaction_listWidget.clear()
        self.hedge_listWidget.clear()

    def add_all_item(self, hedge_users, transaction_users):
        print(hedge_users)
        print(transaction_users)
        for company_name in hedge_users.keys():
            self.hedge_listWidget.addItem(company_name)
        for company_name in transaction_users.keys():
            self.transaction_listWidget.addItem(company_name)
