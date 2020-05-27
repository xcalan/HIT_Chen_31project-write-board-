#!/usr/bin/env python3
# encoding: utf-8
"""
@Time    : 2020/3/31 12:02
@Author  : Xie Cheng
@File    : index.py
@Software: PyCharm
@desc: 主程序入口
"""
import sys
import project31_xc

from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWidget = QWidget()
    ui = project31_xc.Ui_Form()
    ui.setupUi(mainWidget)
    mainWidget.show()
    sys.exit(app.exec_())

