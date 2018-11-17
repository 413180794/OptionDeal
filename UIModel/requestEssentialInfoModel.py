# -*- coding: utf-8 -*-
# @Time    : 18-11-13 上午10:54
# @Author  : 张帆
# @Site    : 
# @File    : requsetEssentialInfoModel.py
# @Software: PyCharm
import json
import time

from UIModel.model import Model


class RequestEssentialInfoModel(Model):
    '''请求期权基本信息数据包模型,发送给签约服务器'''

    @classmethod
    def from_json(cls, mainFormControl, json):
        raise NotImplemented

    def __init__(self, mainFormControl):
        self.mainFormControl = mainFormControl
        self.purpose = "req_ess_info"
        self.furthest_date_due = self.str_to_time_stamp(self.mainFormControl.furthest_date_due_dateEdit.text())
        self.fvcode = self.mainFormControl.fvcode_lineEdit.text()
        print(self.furthest_date_due)

    def get_json(self):
        return json.dumps(
            {
                "purpose": self.purpose,
                "fvcode": self.fvcode,
                "furthest_date_due": self.furthest_date_due,
            }
        )

    def str_to_time_stamp(self, date_str):
        '''2018/12/12 ---> 转化为时间戳'''
        time_now = time.mktime(time.strptime(date_str, '%Y/%m/%d'))
        return time_now

    def send_json_to_signing_server(self):
        '''发送json给签约服务器'''
        self.mainFormControl.send_to_signing_server(self.get_json())

    def __repr__(self):
        return f'''
            mainForm:{self.mainFormControl},
            purpose:{self.purpose},
            fvcode:{self.fvcode},
            furthest_date_due:{self.furthest_date_due}
        '''
