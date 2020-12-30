#
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class TableModel(QTableWidget):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self.data = data
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        # print(self.data)

    def setData(self):
        headers = []
        for n, k in enumerate(self.data.items()):
            print("TUPLE :: {}) {} -- {}".format(n, k[0], k[1])) if isinstance(k[1], tuple) else print("{}) {} -- {}".format(n, k[0], k[1])) 
            headers.append(k[0])
            item = QTableWidgetItem(k[1]) if not isinstance(k[1], tuple) else QTableWidgetItem("{} - {}".format(k[1][0], k[1][0]))
            print(item)
            self.setItem(1, n, item)
        print(headers)
        self.setHorizontalHeaderLabels(headers)

    # def data(self, index, role):
        # if role == Qt.DisplayRole:
            # return self.data[index.column()][index.row()]
            # for k,v in enumerate(self.data.items()):
                # print(self.data[index])
                # return self.data[index]

    # def headerData(self, section, orientation, role):
        # if role != Qt.DisplayRole 

    # def rowCount(self, index):
        # return 1
        # pass
        # return len(self)

    # def columnCount(self, index):
        # return 8
        