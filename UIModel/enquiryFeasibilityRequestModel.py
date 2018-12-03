# -*- coding: utf-8 -*-
# @Time    : 18-11-15 下午9:19
# @Author  : 张帆
# @Site    : 
# @File    : enquiryFeasibilityRequestModel.py
# @Software: PyCharm
import json

from PyQt5.QtWidgets import QFormLayout

from UIModel.model import Model


class EnquiryFeasibilityRequestModel(Model):
    '''询价可行性请求数据包--->发送给签约服务器,签约服务器对
    这笔交易进行可行性验证,并且回复一些东西'''

    def __init__(self, mainFormControl, enquiry_type, trade_type):
        self.mainFormControl = mainFormControl
        self.purpose = "enquiry_feasible_req"
        self.fvcode = self.mainFormControl.show_fvcode_label.text()
        self._enquiry_type = enquiry_type
        self._trade_type = trade_type
        self.option_type = self.mainFormControl.option_type_comboBox.currentText()

        self.all_date = []
        self.main_tract_code = self.mainFormControl.main_contract_code_label.text()
        self.main_all_price = []
        self.second_contract_code = self.mainFormControl.second_contract_code_label.text()
        self.second_all_price = []
        self.get_all_date()
        self.get_main_all_price()
        self.get_second_all_price()
        # print("all_date", self.all_date)
        # print("main_all_price", self.main_all_price)
        # print("second_all_price", self.second_all_price)

    def get_all_date(self):
        '''获得所有日期数据'''
        self.all_date.clear()
        for i in range(1,self.mainFormControl.dateEdit_formLayout.rowCount()):
            dateEdit = self.mainFormControl.dateEdit_formLayout.itemAt(i, QFormLayout.FieldRole).widget()
            date_time = dateEdit.text()
            print(date_time)
            self.all_date.append(date_time)
    def get_main_all_price(self):
        self.main_all_price.clear()
        for i in range(1,self.mainFormControl.main_contract_formLayout.rowCount()):
            lineEdit = self.mainFormControl.main_contract_formLayout.itemAt(i, QFormLayout.FieldRole).widget()
            price = lineEdit.text()
            self.main_all_price.append(price)
    def get_second_all_price(self):
        self.second_all_price.clear()
        for i in range(1,self.mainFormControl.second_contract_formLayout.rowCount()):
            lineEdit = self.mainFormControl.second_contract_formLayout.itemAt(i, QFormLayout.FieldRole).widget()
            price = lineEdit.text()
            self.second_all_price.append(price)
    @property
    def trade_type(self):
        return self._trade_type

    @trade_type.setter
    def trade_type(self, type):
        if type not in ['开仓', '平仓']:
            raise ValueError('trade_type 只能设置为开仓或平仓')
        self._trade_type = type

    @property
    def enquiry_type(self):
        return self._enquiry_type

    @enquiry_type.setter
    def enquiry_type(self, type):
        if type not in ['直播', '询价']:
            raise ValueError("enquiry_type只能设置为直播或询价")

    def get_json(self):

        result_json = {
            "purpose": self.purpose,
            "fvcode": self.fvcode,
            "trade_type": self.trade_type,
            "enquiry_type": self.enquiry_type,
            "option_type": self.option_type,
            "all_date": self.all_date,
            "detail": [
                {
                    "contract_code": self.main_tract_code,
                    "all_price": self.main_all_price
                },
                {
                    "contract_code": self.second_contract_code,
                    "all_price": self.second_all_price
                }
            ]

        }
        return json.dumps(result_json)


