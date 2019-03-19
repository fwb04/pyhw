#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import cv2 as cv
import numpy as np
from selfpackage import window
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QGridLayout, QLabel, QPushButton)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = window()
    a.show()
    app.exec()