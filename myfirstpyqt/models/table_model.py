from PySide2.QtCore import QAbstractTableModel
from PySide2.QtGui import Qt

class TableModel(QAbstractTableModel):
    def __init__(self, data, header_data):
        super(TableModel, self).__init__()
        self._data = data
        self.header_data = header_data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def header_data(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headerdata[col]
        return None
