# -*- coding: utf-8 -*-
# @Time    : 18-11-12 下午2:37
# @Author  : 张帆
# @Site    : 
# @File    : enquiryRequestModel.py
# @Software: PyCharm
'''
{
    "purpose":"询价或直播",
    "fvcode":"期货品种代码",
    "trade_type":"开仓或平仓",
    "option_type":"期权类型",
    "detail":[
        {
            "contract_code":"合约代码",
            "peprice":"主执行价",
            "days_remaining":"剩余天数"
        },
        {
            "contract_code":"合约代码",
            "peprice":"主执行价",
            "days_remaining":"剩余天数"
        }
    ]
}
'''
import json

from UIModel.model import Model


class EnquiryRequestModel(Model):
    '''询价请求数据包'''


    @classmethod
    def from_json(cls):
        raise NotImplemented

    def __init__(self, fvcode, option_type, mainForm, contract_code, peprice, days_remaining,
                 contract_code_2=None, peprice_2=None, days_remaining_2=None):
        self.fvcode = fvcode
        self.option_type = option_type
        self.mainForm = mainForm
        self.contract_code = contract_code
        self.peprice = peprice
        self.days_remaining = days_remaining
        self.contract_code_2 = contract_code_2
        self.peprice_2 = peprice_2
        self.days_remaining_2 = days_remaining_2

    def get_json(self):
        '''询价请求数据json包，平仓询价请求只有一个合约'''
        return json.dumps({
            "purpose": "询价",
            "fvcode": self.fvcode,
            "trade_type": "平仓",
            "option_type": self.option_type,
            "detail": [
                {
                    "contract_code": self.contract_code,
                    "peprice": self.peprice,
                    "days_remaining": self.days_remaining
                },
                {

                }
            ]
        })

if __name__ == '__main__':
    x = EnquiryRequestModel()