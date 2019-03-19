#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import cv2 as cv
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget

# window类继承于QWidget
class window(QWidget):

    def __init__(self):
        super().__init__()
        self.init_show()

    def init_show(self):

        self.setWindowTitle('photo processing tool')
        self.resize(800,600)