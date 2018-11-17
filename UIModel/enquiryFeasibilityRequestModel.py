# -*- coding: utf-8 -*-
# @Time    : 18-11-15 下午9:19
# @Author  : 张帆
# @Site    : 
# @File    : enquiryFeasibilityRequestModel.py
# @Software: PyCharm
from UIModel.model import Model


class EnquiryFeasibilityRequest(Model):
    '''询价可行性请求数据包--->发送给签约服务器,签约服务器对
    这笔交易进行可行性验证,并且回复一些东西'''

    def __init__(self, mainFormControl, enquiry_type, trade_type, option_type, all_date: dict,
                 main_tract_code, main_all_price: dict, second_contract_code, second_all_price: dict):
        self.mainFormControl = mainFormControl
        self.purpose = "enquiry_feasible_req"
        self.fvcode = self.mainFormControl.show_fvcode_label.text()
        self._enquiry_type = enquiry_type
        self._trade_type = trade_type
        self.option_type = self.mainFormControl.option_type_comboBox.currentText()

        self.all_date = self.mainFormControl.main_dateEdit_dict
        self.main_tract_code = self.mainFormControl.main_contract_code_label.text()
        self.main_all_price = self.mainFormControl.main_lineEdit_dict
        self.second_contract_code = self.mainFormControl.second_contract_code_label.text()
        self.second_all_price = self.mainFormControl.second_lineEdit_dict

        print("all_date", self.all_date)
        print("main_all_price", self.main_all_price)
        print("second_all_price", self.second_all_price)

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

        }

        pass

    @classmethod
    def from_json(cls, mainFormControl, json):
        pass
