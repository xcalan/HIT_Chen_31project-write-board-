#!/usr/bin/env python3
# encoding: utf-8
"""
@Time    : 2020/3/29 21:59
@Author  : Xie Cheng
@File    : demo.py
@Software: PyCharm
@desc: 鼠标移动跟踪轨迹(模拟手势操作)
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QPlainTextEdit,QLabel
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, pyqtSlot


class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.resize(800, 500)  # resize设置宽高，move设置位置
        # self.move(100, 100)  # 窗口移动
        self.setWindowTitle("轨迹跟踪示例demo")

        # 在窗体内创建button_clear(清空痕迹)
        self.button_clear = QPushButton("清空", self)
        self.button_clear.setToolTip("清空当前痕迹")  # 鼠标在按钮悬浮显示消息
        self.button_clear.move(200, 50)
        self.button_clear.clicked.connect(self.on_click_clear)  # 按钮与鼠标点击事件相关联

        # 在窗体内创建button_show_points(显示线上的点)
        self.button_show_points = QPushButton("隐藏点", self)
        self.button_show_points.setToolTip("显示线上的所有点")
        self.button_show_points.move(500, 50)
        self.button_show_points.clicked.connect(self.on_click_show_points)

        # setMouseTracking设置为False，否则不按下鼠标时也会跟踪鼠标事件
        self.setMouseTracking(False)

        self.pos_xy = []  # 保存所有移动过的点

        self.show_line_points_flag = 1  # 显示线上所有点标志位 0为隐藏 1为显示

        # 文本框
        self.plainTextEdit = QPlainTextEdit(self)
        self.plainTextEdit.resize(600, 100)
        self.plainTextEdit.move(100, 350)
        self.plainTextEdit.setReadOnly(True)


        # 标签1
        self.label1 = QLabel(self)
        self.label1.setText('绘图区域')
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.move(360, 200)

        # 标签2
        self.label2 = QLabel(self)
        self.label2.setText('线上各点坐标')
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.move(350, 330)

    def paintEvent(self, event):
        # 画线
        painter = QPainter()
        painter.begin(self)
        pen_line = QPen(Qt.black, 5, Qt.SolidLine)  # 痕迹颜色，宽度，样式
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
        painter_point = QPainter()
        if self.show_line_points_flag == 1:
            painter_point.begin(self)
            self.drawPoints(painter_point)
            painter_point.end()

    def drawPoints(self, qp):
        qp.setPen(QPen(Qt.red, 3))
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
            QMessageBox.about(self, "警告", "请点击清空按钮清空当前痕迹")
        else:
            # 中间变量pos_tmp提取当前点
            pos_tmp = (event.pos().x(), event.pos().y())
            # pos_tmp添加到self.pos_xy中
            self.pos_xy.append(pos_tmp)
            self.update()

    def mouseReleaseEvent(self, event):
        """
        重写鼠标按住后松开的事件
        输出所有pos_xy
        """

        pos_test = (-1, -1)
        if self.pos_xy != [] and self.pos_xy[-1] != (-1, -1):
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
            self.button_show_points.setText("隐藏点")
            self.update()  # 调用paintEvent()函数
        else:
            self.show_line_points_flag = 0
            self.button_show_points.setText("显示点")
            self.update()  # 调用paintEvent()函数


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pyqt_learn = Example()
    pyqt_learn.show()
    sys.exit(app.exec_())
