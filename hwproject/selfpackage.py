#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import re
import PIL.Image as img
# import qtawesome
import cv2 as cv
import numpy as np
import requests
from PyQt5.QtGui import QImage, QPixmap, QIcon, QFont, QPalette
from PyQt5.QtCore import QCoreApplication, Qt
# from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog,
    QGridLayout, QLabel, QPushButton, QWidget, QToolTip, QMessageBox,
    QInputDialog, QLineEdit, QComboBox, QScrollArea, QTabWidget, QMainWindow)
import urllib
import urllib.request
import os, base64
import json

# pwindow类继承于QWidget
class pwindow(QWidget):

    # 窗口初始化
    def __init__(self):
        super().__init__()
        self.initUI()

    # 初始化窗口函数
    def initUI(self):

        # 窗口大小，位置，名称，图标
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('photo processing tool')
        self.setWindowIcon(QIcon('pic.png'))
        # self.show()

        # 为tooltip设置了10px的Sanserif字体
        QToolTip.setFont(QFont('SansSerif', 15))

        # 创建添加按钮1和提示消息
        self.abtn = QPushButton('Add1', self)
        self.abtn.setToolTip('Add a picture from your labtap')
        # self.abtn.clicked.connect(self.openImg)
        # self.abtn.clicked.connect(self.hide)
        self.abtn.resize(self.abtn.sizeHint())

        # 创建添加按钮2和提示消息
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

    # 二次确认是否退出
    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class cwindow(QMainWindow):

    def __init__(self):
        # 初始化一个img的ndarray, 用于存储图像
        self.img = np.ndarray(())
        super().__init__()
        self.initUI()

    # 初始化窗口函数
    def initUI(self):

        # 窗口大小，位置，名称，图标
        self.resize(1024, 768)
        # self.setMaximumSize(1600, 1200)
        self.setMinimumSize(1024, 768)
        self.setWindowTitle('photo processing tool')
        self.setWindowIcon(QIcon('pic.png'))

        self.main_widget = QWidget()  # 创建窗口主部件
        self.main_layout = QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        self.right_widget = QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        self.main_layout.addWidget(self.left_widget, 0, 0, 16, 10)  # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget, 0, 10, 16, 2)  # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        # 创建图像显示label
        self.la = QLabel(self)
        self.scrollarea = QScrollArea(self)

        # 文字显示label
        self.textlabel = QLabel(self)
        self.scrollarea2 = QScrollArea(self)
        self.text1 = QLabel(self)
        self.text2 = QLabel(self)
        self.text1.setText("基本图像处理")
        self.text2.setText("图像识别")

        # 创建图像处理功能按钮
        self.lrbtn = QPushButton('左旋', self)
        self.rrbtn = QPushButton('右旋', self)
        self.mabtn = QPushButton('放大', self)
        self.shbtn = QPushButton('缩小', self)
        self.mbtn = QPushButton('无损放大', self)
        self.dfbtn = QPushButton('去雾', self)
        self.libtn = QPushButton('增艳', self)
        self.sabtn = QPushButton('另存为', self)
        self.pickbtn = QPushButton('确定', self)
        self.addbtn = QPushButton('添加', self)

        # 创建quit按钮
        self.qbtn = QPushButton('Quit', self)
        self.qbtn.setToolTip('Quit this app')

        # 设置图像显示和文字显示label背景
        self.la.setStyleSheet("QLabel{background:white;}")
        # self.la.setAlignment(Qt.AlignCenter)
        # self.la.setScaledContents(True)
        self.scrollarea.setWidget(self.la)
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setMinimumSize(800, 600)
        self.scrollarea.setAlignment(Qt.AlignCenter)
        # self.tab.addTab(self.scrollarea, "page 1")
        # self.tab.show()

        self.scrollarea2.setWidget(self.textlabel)
        self.scrollarea2.setWidgetResizable(True)
        self.scrollarea2.setAlignment(Qt.AlignCenter)
        self.textlabel.setStyleSheet("QLabel{background:white;}"
                           "QLabel{color:rgb(100,100,100,250);font-size:20px;font-weight:bold;font-family:宋体;}")
                           # "QLabel:hover{color:rgb(100,100,100,120);}")

        # 创建按钮的信号与槽的连接
        self.mabtn.clicked.connect(self.magnify_img)
        self.shbtn.clicked.connect(self.shrink_img)
        self.mbtn.clicked.connect(self.magnify2)
        self.lrbtn.clicked.connect(self.leftrotation)
        self.rrbtn.clicked.connect(self.rightrotation)
        self.sabtn.clicked.connect(self.saveImg)
        self.qbtn.clicked.connect(QCoreApplication.instance().quit)
        self.libtn.clicked.connect(self.color)
        self.dfbtn.clicked.connect(self.defog)

        # 创建一个下拉列表框并填充了7个列表项
        self.combo = QComboBox(self)
        self.combo.addItem("菜品识别")
        self.combo.addItem("动物识别")
        self.combo.addItem("植物识别")
        self.combo.addItem("地标识别")
        self.combo.addItem("logo识别")
        self.combo.addItem("车型识别")
        self.combo.addItem("通用物体识别")
        self.combo.activated[str].connect(self.onActivated)
        # self.pickbtn.clicked.connect(self.activate)
        # 一旦列表项被选中，会调用onActivated()方法

        # 布局设定
        # self.layout = QGridLayout(self)
        # self.left_layout.addWidget(self.la, 0, 0, 16, 10)
        self.left_layout.addWidget(self.scrollarea, 0, 0, 16, 10)
        self.right_layout.addWidget(self.text1, 0, 10, 1, 2)
        self.right_layout.addWidget(self.lrbtn, 1, 10, 1, 1)
        self.right_layout.addWidget(self.rrbtn, 2, 10, 1, 1)
        self.right_layout.addWidget(self.mabtn, 3, 10, 1, 1)
        self.right_layout.addWidget(self.shbtn, 4, 10, 1, 1)
        self.right_layout.addWidget(self.mbtn, 5, 10, 1, 1)
        self.right_layout.addWidget(self.dfbtn, 6, 10, 1, 1)
        self.right_layout.addWidget(self.libtn, 7, 10, 1, 1)
        self.right_layout.addWidget(self.text2, 8, 10, 1, 2)
        self.right_layout.addWidget(self.combo, 9, 10, 1, 2)
        self.right_layout.addWidget(self.scrollarea2, 10, 10, 4, 2)
        self.right_layout.addWidget(self.addbtn, 14, 10, 1, 1)
        self.right_layout.addWidget(self.sabtn, 15, 10, 1, 1)
        self.right_layout.addWidget(self.qbtn, 16, 10, 1, 1)

        self.show()

    def activate(self):
        self.combo.activated[str].connect(self.onActivated)

    # 列表项选中连接方法
    def onActivated(self, text):
        if text == "动物识别":
            self.animalread()
        elif text == "菜品识别":
            self.dishread()
        elif text == "植物识别":
            self.plantread()
        elif text == "logo识别":
            self.logoread()
        elif text == "地标识别":
            self.landmarkread()
        elif text == "车型识别":
            self.carread()
        elif text == "通用物体识别":
            self.anythingread()

    def handle_click(self):
        if not self.isVisible():
            self.show()

    # 提示框获取输入网址
    def getWeb(self):
        self.web, okPressed = QInputDialog.getText(self, "Get text", "Web site:", QLineEdit.Normal, "")
        if okPressed and self.web != '':
            return self.web

    # 提示框获取输入名称
    def getName(self):
        self.name, okPressed = QInputDialog.getText(self, "Get text", "Img name:", QLineEdit.Normal, "")
        if okPressed and self.name != '':
            return self.name

    # 打开本地图像方法
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

    # 将图像保存到本地方法
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

    # 图像显示方法
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

    # 从网络下载图片
    def download_img(self):
        web = self.getWeb()
        name = self.getName()

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

    # 放大图片
    def magnify_img(self):

        # 将图像两个方向拉伸1.1倍
        self.img = cv.resize(self.img, (0, 0), fx=1.1, fy=1.1,
                             interpolation=cv.INTER_NEAREST)

        self.refreshShow1()

    # 调用无损放大图片api
    def magnify2(self):
        # 网址
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/image_quality_enhance"

        # 图像进行base64编码
        img = cv.imencode('.jpg', self.img)[1]
        img = str(base64.b64encode(img))[2:-1]
        params = {"image": img}

        params = urllib.parse.urlencode(params).encode("utf-8")

        # 调用api，获取返回内容
        access_token = '24.d66d45b666d64c58d4597c26018f195d.2592000.1555499580.282335-15777373'
        request_url = request_url + "?access_token=" + access_token
        request = urllib.request.Request(url=request_url, data=params)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urllib.request.urlopen(request)
        content = response.read().decode("utf-8")

        # 获取返回图片的base64编码并进行解码
        i = content.find("image")
        code = content[i + 9:-2]
        imgdata = base64.b64decode(code)

        # 将解码后的图像放入gui中显示
        img_array = np.fromstring(imgdata, np.uint8)
        self.img = cv.imdecode(img_array, cv.COLOR_BGR2RGB)

        self.refreshShow1()

    # 缩小图像
    def shrink_img(self):
        # 将图像两个方向压缩0.9倍
        self.img = cv.resize(self.img, (0, 0), fx=0.9, fy=0.9,
                             interpolation=cv.INTER_NEAREST)
        self.refreshShow1()

    # 图像左旋
    def leftrotation(self):

        # 使用numpy中的方法将图像向左旋转90度
        self.img = np.rot90(self.img)

        self.img = cv.resize(self.img, (0, 0), fx=1, fy=1,
                             interpolation=cv.INTER_NEAREST)
        self.refreshShow1()

    # 图像右旋
    def rightrotation(self):
        # 将图像右旋90度即左旋270度
        self.img = np.rot90(self.img)
        self.img = np.rot90(self.img)
        self.img = np.rot90(self.img)
        self.img = cv.resize(self.img, (0, 0), fx=1, fy=1,
                             interpolation=cv.INTER_NEAREST)
        self.refreshShow1()

    # 图像对比度增强API
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

    # 图像去雾处理API
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

    # 识别图像中的动物API
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

        # 对返回的字符串进行排版并显示出来
        hjson = json.loads(content)
        js = json.dumps(hjson, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False)
        self.textlabel.setText(js)

    # 识别图像中的植物
    def plantread(self):
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/plant"

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

        hjson = json.loads(content)
        js = json.dumps(hjson, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False)
        self.textlabel.setText(js)

    # 识别图像中的菜品
    def dishread(self):
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/dish"

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

        hjson = json.loads(content)
        js = json.dumps(hjson, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False)
        self.textlabel.setText(js)

    # 识别图像中的地标
    def landmarkread(self):
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/landmark"

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

        hjson = json.loads(content)
        js = json.dumps(hjson, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False)
        self.textlabel.setText(js)

    # 识别图像中的车型
    def carread(self):
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/car"

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

        hjson = json.loads(content)
        js = json.dumps(hjson, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False)
        self.textlabel.setText(js)

    # 识别图像中的商标
    def logoread(self):
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/logo"

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

        hjson = json.loads(content)
        js = json.dumps(hjson, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False)
        self.textlabel.setText(js)

    # 识别图像中的物体信息
    def anythingread(self):
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"

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

        hjson = json.loads(content)
        js = json.dumps(hjson, sort_keys=True, indent=4, separators=(',', ';'), ensure_ascii=False)
        self.textlabel.setText(js)