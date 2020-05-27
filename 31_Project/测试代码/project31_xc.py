# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'project31_xc.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QPlainTextEdit
# from PyQt5.QtGui import QPainter, QPen
# from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtCore import pyqtSlot


class Ui_Form(QtWidgets.QWidget):

    def __init__(self):

        super(Ui_Form, self).__init__()

        # setMouseTracking设置为False，否则不按下鼠标时也会跟踪鼠标事件
        self.setMouseTracking(False)

        self.pos_xy = []  # 保存所有移动过的点

        self.show_line_points_flag = 0  # 显示线上所有点标志位 0为隐藏 1为显示


    def setupUi(self, Form):

        Form.setObjectName("Form")
        Form.resize(872, 522)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(240, 10, 381, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # 在窗体内创建pushButton_2(显示线上的点)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.on_click_show_points)
        self.horizontalLayout.addWidget(self.pushButton_2)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        # 在窗体内创建pushButton(清空痕迹)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.on_click_clear)
        self.horizontalLayout.addWidget(self.pushButton)

        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 410, 861, 89))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget_2)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayout_2.addWidget(self.plainTextEdit)
        spacerItem2 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(360, 389, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(381, 230, 81, 20))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "轨迹跟踪示例demo"))
        self.pushButton_2.setText(_translate("Form", "显示点"))
        self.pushButton.setText(_translate("Form", "清空痕迹"))
        self.label.setText(_translate("Form", "线上各点坐标"))
        self.label_2.setText(_translate("Form", "绘图区域"))

    def paintEvent(self, event):
        # 画线
        painter = QtGui.QPainter()
        painter.begin(self)
        pen_line = QtGui.QPen(QtCore.Qt.black, 5, QtCore.Qt.SolidLine)  # 痕迹颜色，宽度，样式
        painter.setPen(pen_line)

        '''
            首先判断pos_xy列表中是不是至少有两个点了
            然后将pos_xy中第一个点赋值给point_start
            利用中间变量pos_tmp遍历整个pos_xy列表
                point_end = pos_tmp
                画point_start到point_end之间的线
                point_start = point_end
            这样，不断地将相邻两个点之间画线，就能留下鼠标移动轨迹了
        '''

        if len(self.pos_xy) > 1:
            point_start = self.pos_xy[0]
            for pos_tmp in self.pos_xy:
                point_end = pos_tmp

                # 添加下面这段代码可以解决二次点击时出现一条（-1，-1）为终点的线的bug
                if point_end == (-1, -1):
                    point_start = (-1, -1)
                    continue
                if point_start == (-1, -1):
                    point_start = point_end
                    continue

                painter.drawLine(point_start[0], point_start[1], point_end[0], point_end[1])
                point_start = point_end

        painter.end()

        # 画点
        painter_point = QtGui.QPainter()
        if self.show_line_points_flag == 1:
            painter_point.begin(self)
            self.drawPoints(painter_point)
            painter_point.end()

    def drawPoints(self, qp):
        qp.setPen(QtGui.QPen(QtCore.Qt.red, 3))
        for v in self.pos_xy:
            x = v[0]
            y = v[1]
            qp.drawPoint(x, y)

    def mouseMoveEvent(self, event):

        """
        按住鼠标移动事件：将当前点添加到pos_xy列表中
        调用update()函数在这里相当于调用paintEvent()函数
        每次update()时，之前调用的paintEvent()留下的痕迹都会清空
        """
        if self.pos_xy != [] and self.pos_xy[-1] == (-1, -1):
            QtWidgets.QMessageBox.about(self, "警告", "请点击清空按钮清空当前痕迹")
        else:
            # 中间变量pos_tmp提取当前点
            pos_tmp = (event.pos().x(), event.pos().y())
            # pos_tmp添加到self.pos_xy中
            print(pos_tmp)
            self.pos_xy.append(pos_tmp)
            self.update()

    def mouseReleaseEvent(self, event):
        """
        重写鼠标按住后松开的事件
        输出所有pos_xy
        """
        pos_test = (-1, -1)
        self.pos_xy.append(pos_test)
        print('length:', len(self.pos_xy))
        print(self.pos_xy)
        self.plainTextEdit.setPlainText(str(self.pos_xy[0:len(self.pos_xy)-1]))

    # 创建button清空点击事件
    @pyqtSlot()
    def on_click_clear(self):
        self.pos_xy = []
        self.update()
        self.plainTextEdit.setPlainText("")

    # 创建button显示线上的所有点
    @pyqtSlot()
    def on_click_show_points(self):
        if self.show_line_points_flag == 0:
            self.show_line_points_flag = 1
            self.pushButton_2.setText("隐藏点")
            self.update()  # 调用paintEvent()函数
        else:
            self.show_line_points_flag = 0
            self.pushButton_2.setText("显示点")
            self.update()  # 调用paintEvent()函数
