#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import cv2 as cv
import numpy as np
from selfpackage import pwindow, cwindow
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog,
    QGridLayout, QLabel, QPushButton, QWidget, QToolTip)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 定义父窗口和子窗口
    c = cwindow()
    p = pwindow()

    c.addbtn.clicked.connect(p.show)

    p.abtn.clicked.connect(c.openImg)

    p.adbtn.clicked.connect(c.download_img)

    # 隐藏父窗口
    p.abtn.clicked.connect(p.hide)
    p.adbtn.clicked.connect(p.hide)
    # c.qbtn.clicked.connect(p.show)

    sys.exit(app.exec_())
