#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import cv2 as cv
import numpy as np
from PyQt5.QtGui import QImage, QPixmap, QIcon, QFont
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog,
    QGridLayout, QLabel, QPushButton, QWidget, QToolTip, QMessageBox)

# window类继承于QWidget
class pwindow(QWidget):

    def __init__(self):
        super().__init__()
        # self.init_show()
        self.initUI()

        # self.initButton()

    # def show(self):
    #     self.setWindowTitle('photo processing tool')
    #     self.resize(1000,800)

    # 初始化窗口函数
    def initUI(self):

        # 窗口大小，位置，名称，图标
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('photo processing tool')
        self.setWindowIcon(QIcon('pic.png'))
        self.show()

        # 为tooltip设置了10px的Sanserif字体
        QToolTip.setFont(QFont('SansSerif', 20))

        # 创建按钮和提示消息
        abtn = QPushButton('Add', self)
        abtn.setToolTip('Add a picture from your labtap')
        # abtn.clicked.connect(self.openSlot)
        abtn.resize(abtn.sizeHint())

        # 创建quit按钮
        qbtn = QPushButton('Quit', self)
        qbtn.setToolTip('Quit this app')
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())

        # 设定按钮布局
        layout = QGridLayout(self)
        layout.addWidget(abtn, 4, 1, 1, 1)
        layout.addWidget(qbtn, 4, 2, 1, 1)
        # layout.addWidget(abtn, 4, 1, 1, 1)

        self.show()

    # 二次确认是否退出
    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

