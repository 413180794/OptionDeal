# -*- coding: utf-8 -*-
# @Time    : 18-11-15 下午9:19
# @Author  : 张帆
# @Site    : 
# @File    : enquiryFeasibilityRequestModel.py
# @Software: PyCharm
import json

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

        self.all_date = self.mainFormControl.dateEdit_dict
        self.main_tract_code = self.mainFormControl.main_contract_code_label.text()
        self.main_all_price = self.mainFormControl.main_lineEdit_dict
        self.second_contract_code = self.mainFormControl.second_contract_code_label.text()
        self.second_all_price = self.mainFormControl.second_lineEdit_dict

        # print("all_date", self.all_date)
        # print("main_all_price", self.main_all_price)
        # print("second_all_price", self.second_all_price)

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
            "all_date": {

            },
            "detail": [
                {
                    "contract_code": self.main_tract_code,
                    "all_price": {

                    }
                },
                {
                    "contract_code": self.second_contract_code,
                    "all_price": {

                    }
                }
            ]

        }
        # 扩展 all_date 的内容
        for variable_name in self.all_date.values():
            result_json.get('all_date').update({variable_name[:-9]: self.str_to_time_stamp(getattr(self.mainFormControl, variable_name).text())})

        # 扩展主力合约all_price    main_strike_price_lineEdit 去头去尾
        for variable_name in self.main_all_price.values():
            result_json.get("detail")[0].get('all_price').update(
                {variable_name[5:][:-9]: getattr(self.mainFormControl, variable_name).text()})
        # 扩展主力合约 all_price
        for variable_name in self.second_all_price.values():
            result_json.get("detail")[1].get('all_price').update(
                {variable_name[7:][:-9]: getattr(self.mainFormControl, variable_name).text()})

        return json.dumps(result_json)


