# -*- coding: utf-8 -*-
# @Time    : 18-12-5 上午11:17
# @Author  : 张帆
# @Site    : 
# @File    : Ship.py
# @Software: PyCharm

class Ship:
    def __init__(self, name: str, owner, country, teu=0, description=""):
        self.name = name

        self.owner = owner
        self.country = country
        self.teu = teu
        self.desciption = description

    def __cmp__(self, other: str):
        return self.name.lower() > other.lower()
