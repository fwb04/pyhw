#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import cv2 as cv
import numpy as np
from selfpackage import pwindow
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog,
    QGridLayout, QLabel, QPushButton, QWidget, QToolTip)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    p = pwindow()
    # w.initUI()
    sys.exit(app.exec_())
