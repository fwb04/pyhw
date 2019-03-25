#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import re
import PIL.Image as img
import qtawesome
import cv2 as cv
import numpy as np
import requests
from PyQt5.QtGui import QImage, QPixmap, QIcon, QFont, QPalette
from PyQt5.QtCore import QCoreApplication, Qt
# from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog,
    QGridLayout, QLabel, QPushButton, QWidget, QToolTip, QMessageBox,
    QInputDialog, QLineEdit, QComboBox)
import base64
import urllib
import urllib.request
import os, base64
import json

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
        # self.setGeometry(300, 300, 1000, 800)
        # self.setFixedSize(960, 700)
        self.resize(1600, 1200)
        # self.setMaximumSize(1600, 1200)
        self.setMinimumSize(1600, 1200)
        self.setWindowTitle('Adding successfully')
        self.setWindowIcon(QIcon('pic.png'))

        # self.main_widget = QWidget()  # 创建窗口主部件
        # self.main_layout = QGridLayout()  # 创建主部件的网格布局
        # self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        #
        # self.left_widget = QWidget()  # 创建左侧部件
        # self.left_widget.setObjectName('left_widget')
        # self.left_layout = QGridLayout()  # 创建左侧部件的网格布局层
        # self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格
        #
        # self.right_widget = QWidget()  # 创建右侧部件
        # self.right_widget.setObjectName('right_widget')
        # self.right_layout = QGridLayout()
        # self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格
        #
        # self.main_layout.addWidget(self.left_widget, 0, 0, 12, 10)  # 左侧部件在第0行第0列，占8行3列
        # self.main_layout.addWidget(self.right_widget, 0, 10, 12, 2)  # 右侧部件在第0行第3列，占8行9列
        # # self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        # 创建图像处理功能按钮
        self.la = QLabel()
        self.textlabel = QLabel(self)
        self.lrbtn = QPushButton('左旋', self)
        self.rrbtn = QPushButton('右旋', self)
        self.mabtn = QPushButton('放大', self)
        self.shbtn = QPushButton('缩小', self)
        self.mbtn = QPushButton('无损放大', self)
        self.dfbtn = QPushButton('去雾', self)
        self.libtn = QPushButton('增艳', self)
        self.sabtn = QPushButton('另存为', self)

        # 创建quit按钮
        self.qbtn = QPushButton('Quit', self)
        self.qbtn.setToolTip('Quit this app')
        self.qbtn.clicked.connect(QCoreApplication.instance().quit)

        self.la.setStyleSheet("QLabel{background:white;}")
        self.textlabel.setStyleSheet("QLabel{background:white;}"
                           "QLabel{color:rgb(100,100,100,250);font-size:20px;font-weight:bold;font-family:宋体;}"
                           "QLabel:hover{color:rgb(100,100,100,120);}")


        self.mabtn.clicked.connect(self.magnify_img)
        self.shbtn.clicked.connect(self.shrink_img)
        self.mbtn.clicked.connect(self.magnify2)
        self.lrbtn.clicked.connect(self.leftrotation)
        self.rrbtn.clicked.connect(self.rightrotation)
        self.sabtn.clicked.connect(self.saveImg)
        self.libtn.clicked.connect(self.color)
        self.dfbtn.clicked.connect(self.defog)

        combo = QComboBox(self)  # 创建一个下拉列表框并填充了五个列表项
        combo.addItem("花卉识别")
        combo.addItem("菜品识别")
        combo.addItem("动物识别")
        combo.addItem("植物识别")
        combo.addItem("地标识别")
        combo.activated[str].connect(self.onActivated)
        # 一旦列表项被选中，会调用onActivated()方法

        # 布局设定
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.la, 0, 0, 16, 10)
        self.layout.addWidget(self.lrbtn, 0, 10, 2, 1)
        self.layout.addWidget(self.rrbtn, 1, 10, 2, 1)
        self.layout.addWidget(self.mabtn, 2, 10, 2, 1)
        self.layout.addWidget(self.shbtn, 3, 10, 2, 1)
        self.layout.addWidget(self.mbtn, 4, 10, 2, 1)
        self.layout.addWidget(self.dfbtn, 5, 10, 2, 1)
        self.layout.addWidget(self.libtn, 6, 10, 2, 1)
        self.layout.addWidget(self.sabtn, 7, 10, 2, 1)
        self.layout.addWidget(combo, 9, 10, 1, 1)
        self.layout.addWidget(self.textlabel, 10, 10, 2, 2)
        self.layout.addWidget(self.qbtn, 12, 10, 2, 1)

    def onActivated(self, text):
        if text == "花卉识别":
            self.leftrotation()
        elif text == "动物识别":
            self.animalread()
        # elif text == "菜品识别":
        #     self.dishread()

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

    def saveImg(self):
        # 调用存储文件dialog
        fileName, tmp = QFileDialog.getSaveFileName(
            self, 'Save Image', './__data', '*.png *.jpg *.bmp', '*.png')

        if fileName is '':
            return
        if self.img.size == 1:
            return

        # 调用opencv写入图像
        cv.imwrite(fileName, self.img)

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

    def magnify_img(self):

        self.img = cv.resize(self.img, (0, 0), fx=1.1, fy=1.1,
                             interpolation=cv.INTER_NEAREST)
        # print(self.img.shape[1])
        # r = 100.0 / self.img.shape[1]
        # dim = (100, int(self.img.shape[0] * r))
        # self.img = cv.resize(self.img, dim, interpolation=cv.INTER_AREA)
        self.refreshShow1()

    def magnify2(self):
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/image_quality_enhance"

        # 二进制方式打开图片文件
        # f = open('杨幂.jpg', 'rb')
        # img = base64.b64encode(self.img.read())

        img = cv.imencode('.jpg', self.img)[1]
        img = str(base64.b64encode(img))[2:-1]
        params = {"image": img}

        params = urllib.parse.urlencode(params).encode("utf-8")

        access_token = '24.d66d45b666d64c58d4597c26018f195d.2592000.1555499580.282335-15777373'
        request_url = request_url + "?access_token=" + access_token
        request = urllib.request.Request(url=request_url, data=params)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urllib.request.urlopen(request)
        content = response.read().decode("utf-8")

        i = content.find("image")
        code = content[i + 9:-2]
        imgdata = base64.b64decode(code)

        img_array = np.fromstring(imgdata, np.uint8)
        self.img = cv.imdecode(img_array, cv.COLOR_BGR2RGB)

        self.refreshShow1()

    def shrink_img(self):
        # height, width = self.img.shape[:2]
        # size = (int(width * 0.3), int(height * 0.5))
        # self.img = cv.resize(self.img, size, interpolation=cv.INTER_AREA)
        self.img = cv.resize(self.img, (0, 0), fx=0.9, fy=0.9,
                             interpolation=cv.INTER_NEAREST)
        self.refreshShow1()

    def leftrotation(self):

        # rows, cols = self.img.shape
        # print(rows, cols)
        # 90度旋转
        # M = cv.getRotationMatrix2D((cols / 2, rows / 2), 90, 1)
        # self.img = cv.warpAffine(self.img, M, (cols, rows))

        self.img = np.rot90(self.img)
        # self.img = img.transpose(img.ROTATE_270)
        self.img = cv.resize(self.img, (0, 0), fx=1, fy=1,
                             interpolation=cv.INTER_NEAREST)
        self.refreshShow1()

    def rightrotation(self):
        self.img = np.rot90(self.img)
        self.img = np.rot90(self.img)
        self.img = np.rot90(self.img)
        self.img = cv.resize(self.img, (0, 0), fx=1, fy=1,
                             interpolation=cv.INTER_NEAREST)
        self.refreshShow1()

    def color(self):
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/contrast_enhance"

        img = cv.imencode('.jpg', self.img)[1]
        img = str(base64.b64encode(img))[2:-1]
        params = {"image": img}

        params = urllib.parse.urlencode(params).encode("utf-8")

        access_token = '24.d66d45b666d64c58d4597c26018f195d.2592000.1555499580.282335-15777373'
        request_url = request_url + "?access_token=" + access_token
        request = urllib.request.Request(url=request_url, data=params)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urllib.request.urlopen(request)
        content = response.read().decode("utf-8")

        i = content.find("image")
        code = content[i + 9:-2]
        imgdata = base64.b64decode(code)

        img_array = np.fromstring(imgdata, np.uint8)
        self.img = cv.imdecode(img_array, cv.COLOR_BGR2RGB)

        self.refreshShow1()

    def defog(self):
        request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/dehaze"

        img = cv.imencode('.jpg', self.img)[1]
        img = str(base64.b64encode(img))[2:-1]
        params = {"image": img}

        params = urllib.parse.urlencode(params).encode("utf-8")

        access_token = '24.d66d45b666d64c58d4597c26018f195d.2592000.1555499580.282335-15777373'
        request_url = request_url + "?access_token=" + access_token
        request = urllib.request.Request(url=request_url, data=params)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urllib.request.urlopen(request)
        content = response.read().decode("utf-8")

        i = content.find("image")
        code = content[i + 9:-2]
        imgdata = base64.b64decode(code)

        img_array = np.fromstring(imgdata, np.uint8)
        self.img = cv.imdecode(img_array, cv.COLOR_BGR2RGB)

        self.refreshShow1()

    def animalread(self):
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/animal"

        img = cv.imencode('.jpg', self.img)[1]
        img = str(base64.b64encode(img))[2:-1]
        params = {"image": img}

        params = urllib.parse.urlencode(params).encode("utf-8")

        access_token = '24.d66d45b666d64c58d4597c26018f195d.2592000.1555499580.282335-15777373'
        request_url = request_url + "?access_token=" + access_token
        request = urllib.request.Request(url=request_url, data=params)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urllib.request.urlopen(request)
        content = response.read().decode("utf-8")

        line = content.strip()
        p2 = re.compile('[^\u4e00-\u9fa5]')  # 中文的编码范围是：\u4e00到\u9fa5
        zh = " ".join(p2.split(line)).strip()
        zh = "\n".join(zh.split())
        outStr = zh
        self.textlabel.setText(outStr)

        # print(content)
        # self.textlabel.setText(content)
        # self.textlabel.adjustSize()