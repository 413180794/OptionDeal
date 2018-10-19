# -*- coding: utf-8 -*-
# @Time    : 18-10-17 下午3:36
# @Author  : 张帆
# @Site    : 
# @File    : main.py
# @Software: PyCharm



import sys

from PyQt5.QtWidgets import QApplication

from UIControl.mainWindowControl import MainFormControl


def main():
    app = QApplication(sys.argv)
    mainwindow = MainFormControl()
    mainwindow.show()


    sys.exit(app.exec_())

if __name__ == '__main__':
    main()