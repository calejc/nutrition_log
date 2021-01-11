#!/usr/bin/env python3
import sys, sqlite3, datetime, data
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from day import Day
from week import Week
from layout import Ui_MainWindow


class GridWidget(QLabel):

    def __init__(self, label):
        super(GridWidget, self).__init__()
        self.label = QLabel(label)



class HeaderWidget(QWidget):

    def __init__(self, label, parent=None):
        super(HeaderWidget, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.label = QLabel("{}".format(label))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFrameShape(QFrame.Panel)
        self.label.setFrameShadow(QFrame.Sunken)
        self.label.setLineWidth(1)
        self.setStyleSheet("background-color:red;font-weight:bold;")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
