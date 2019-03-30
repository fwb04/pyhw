#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from selfpackage import pwindow, cwindow
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog,
    QGridLayout, QLabel, QPushButton, QWidget, QToolTip)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 定义父窗口和子窗口
    p = pwindow()
    c = cwindow()

    # 点击pwindow添加按钮显示cwindow
    p.addbtn.clicked.connect(c.show)
    # 点击cwindow的add1按钮从本地添加图片
    c.abtn.clicked.connect(p.openImg)
    # 点击cwindow的add2按钮从网络添加图片
    c.adbtn.clicked.connect(p.download_img)

    # 添加图片后隐藏cwindow
    c.abtn.clicked.connect(c.hide)
    c.adbtn.clicked.connect(c.hide)

    sys.exit(app.exec_())
