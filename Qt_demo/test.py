#!/usr/bin/env python3
# encoding: utf-8
"""
@Time    : 2020/3/28 22:20
@Author  : Xie Cheng
@File    : test.py
@Software: PyCharm
@desc: PyQt5测试用例
"""
import sys

# # 导入file文件夹下的ttt.py文件
# sys.path.append('file')
# from aaa import ttt

import aaa

from PyQt5.QtWidgets import QApplication, QMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = aaa.Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())


