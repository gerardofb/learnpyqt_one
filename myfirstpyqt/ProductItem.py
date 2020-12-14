# This Python file uses the following encoding: utf-8
from PySide2.QtCore import *

class ProductItem(QAbstractTableModel):
    def __init__(self):
        self.productos = [""]
        self.precios = [0.00]
    def rowCount(self,index = QModelIndex()):
        return len(self.productos)
    def columnCount(self, index = QModelIndex()):
        return 2
    def data(self, index, role = Qt.displayRole):
        product = self.productos[index.row()]
        return product

    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.ships.insert(position + row,Ship(" Unknown", " Unknown", " Unknown"))

    self.endInsertRows()

    self.dirty = True return True
