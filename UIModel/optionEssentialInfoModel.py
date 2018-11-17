# -*- coding: utf-8 -*-
# @Time    : 18-11-13 下午9:21
# @Author  : 张帆
# @Site    : 
# @File    : optionEssentialInfoModel.py
# @Software: PyCharm
from UIModel.model import Model


class OptionEssentialInfoModel(Model):
    '''期权基本信息数据包,由签约服务器发送给交易端'''

    def get_json(self):
        pass

    def __init__(self, mainFormControl, purpose, fvcode, main_contract_code, main_lots, second_contract_code="",
                 second_lots=""):
        self.mainFormControl = mainFormControl
        self.purpose = purpose
        self._fvcode = fvcode
        self._main_contract_code = main_contract_code
        self._main_lots = main_lots
        self._second_contract_code = second_contract_code
        self._second_lots = second_lots
        if not self.if_has_second_contract():
            self.hide_second_contract()
    @property
    def fvcode(self):
        return self._fvcode

    @property
    def main_contract_code(self):
        return self._main_contract_code

    @property
    def main_lots(self):
        return self._main_lots

    @property
    def second_contract_code(self):
        return self._second_contract_code

    @property
    def second_lots(self):
        return self._second_lots

    def hide_second_contract(self):
        '''隐藏次主力合约的控件'''
        for second_widget in self.mainFormControl.second_contract_widget:

            second_widget.hide()
    def if_has_second_contract(self):
        '''是否含有次主力合约'''
        return False if self.second_contract_code == "" else True

    def set_show_fvcode_label_text(self):
        '''设置期货合约代码标签的内容'''
        self.mainFormControl.show_fvcode_label.setText(self.fvcode)

    def set_main_max_lots_label_text(self):
        self.mainFormControl.main_max_lots_label.setText(str(self.main_lots))

    def set_secode_max_lots_label_text(self):
        self.mainFormControl.second_max_lots_label.setText(str(self.second_lots))

    @classmethod
    def from_json(cls, mainFormControl, json):
        return cls(mainFormControl, json.get("purpose"),
                   json.get("fvcode"),
                   json.get("detail")[0].get("contract_code"),
                   json.get("detail")[0].get("lots"),
                   json.get("detail")[1].get("contract_code"),
                   json.get("detail")[1].get("lots"))
