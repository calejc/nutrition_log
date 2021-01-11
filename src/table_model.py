#
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class TableModel(QAbstractTableModel):
    def __init__(self, data, headers, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.data = data
        self.headers = headers

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.data[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headers[col])
        return QVariant()

    def rowCount(self, parent):
        return len(self.data)

    def columnCount(self, parent):
        if len(self.data) > 0: 
            return len(self.data[0]) 
        return 0
        