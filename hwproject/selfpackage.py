#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import cv2 as cv
import numpy as np
import requests
from PyQt5.QtGui import QImage, QPixmap, QIcon, QFont
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog,
    QGridLayout, QLabel, QPushButton, QWidget, QToolTip, QMessageBox,
    QInputDialog, QLineEdit)

# pwindow类继承于QWidget
class pwindow(QWidget):

    def __init__(self):
        super().__init__()
        # self.init_show()
        self.initUI()

    # 初始化窗口函数
    def initUI(self):

        # 窗口大小，位置，名称，图标
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('photo processing tool')
        self.setWindowIcon(QIcon('pic.png'))
        self.show()

        # 为tooltip设置了10px的Sanserif字体
        QToolTip.setFont(QFont('SansSerif', 15))

        # 创建按钮和提示消息
        self.abtn = QPushButton('Add1', self)
        self.abtn.setToolTip('Add a picture from your labtap')
        # self.abtn.clicked.connect(self.openImg)
        # self.abtn.clicked.connect(self.hide)
        self.abtn.resize(self.abtn.sizeHint())

        # 创建按钮和提示消息
        self.adbtn = QPushButton('Add2', self)
        self.adbtn.setToolTip('Add a picture from internet')
        # abtn.clicked.connect(self.openSlot)
        self.adbtn.resize(self.adbtn.sizeHint())

        # 创建quit按钮
        qbtn = QPushButton('Quit', self)
        qbtn.setToolTip('Quit this app')
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())

        # 设定按钮布局
        layout = QGridLayout(self)
        layout.addWidget(self.abtn, 4, 1, 1, 1)
        layout.addWidget(self.adbtn, 4, 2, 1, 1)
        layout.addWidget(qbtn, 4, 3, 1, 1)
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


class cwindow(QWidget):

    def __init__(self):

        # 初始化一个img的ndarray, 用于存储图像
        self.img = np.ndarray(())
        super().__init__()
        self.initUI()

     # 初始化窗口函数
    def initUI(self):

        # 窗口大小，位置，名称，图标
        self.setGeometry(300, 300, 1000, 800)
        self.setWindowTitle('Adding successfully')
        self.setWindowIcon(QIcon('pic.png'))
        # self.show()

        self.la = QLabel()
        self.lrbtn = QPushButton('lr', self)
        self.rrbtn = QPushButton('rr', self)

        # 创建quit按钮
        self.qbtn = QPushButton('Quit', self)
        self.qbtn.setToolTip('Quit this app')
        self.qbtn.clicked.connect(QCoreApplication.instance().quit)

        # 布局设定
        layout = QGridLayout(self)
        layout.addWidget(self.la, 1, 1, 4, 4)
        layout.addWidget(self.lrbtn, 1, 5, 1, 1)
        layout.addWidget(self.rrbtn, 2, 5, 1, 1)
        layout.addWidget(self.qbtn, 4, 5, 1, 1)

    def handle_click(self):
        if not self.isVisible():
            self.show()

    def getWeb(self):
        self.web, okPressed = QInputDialog.getText(self, "Get text", "Web site:", QLineEdit.Normal, "")
        if okPressed and self.web != '':
            return self.web

    def getName(self):
        self.name, okPressed = QInputDialog.getText(self, "Get text", "Img name:", QLineEdit.Normal, "")
        if okPressed and self.name != '':
            return self.name


    def openImg(self):
        # 调用打开文件diglog
        fileName, tmp = QFileDialog.getOpenFileName(
            self, 'Open Image', './__data', '*.png *.jpg *.bmp')

        if fileName is '':
            return

        # 采用opencv函数读取数据
        self.img = cv.imread(fileName, -1)

        if self.img.size == 1:
            return

        self.refreshShow1()

    def refreshShow1(self):

        # 提取图像的尺寸和通道, 用于将opencv下的image转换成Qimage
        height, width, channel = self.img.shape
        bytesPerLine = 3 * width
        self.qImg = QImage(self.img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

        # 将Qimage显示出来
        self.la.setPixmap(QPixmap.fromImage(self.qImg))

    def refreshShow2(self):

        # 提取图像的尺寸和通道, 用于将opencv下的image转换成Qimage
        height, width, channel = self.webimg.shape
        bytesPerLine = 3 * width
        self.qImg = QImage(self.webimg.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

        # 将Qimage显示出来
        self.la.setPixmap(QPixmap.fromImage(self.qImg))

    def download_img(self):
        web = self.getWeb()
        name = self.getName()
        # self.web, okPressed = QInputDialog.getText(self, "Get text", "Web site:", QLineEdit.Normal, "")
        # self.name, okPressed = QInputDialog.getText(self, "Get text", "Img name:", QLineEdit.Normal, "")
        url_info = [web, name]
        if url_info[1]:
            # print("-----------downloading image %s" % (url_info[0]))
            try:
                url = url_info[0]
                response = requests.get(url)
                img = response.content

                # Save Path
                path = '%s' % (url_info[1])
                with open(path, 'wb') as f:
                    f.write(img)

                self.webimg = cv.imread(name, -1)
                if self.webimg.size == 1:
                    return

                self.refreshShow2()

                return (True, path)
            except Exception as ex:
                print("--------Error----")
                pass