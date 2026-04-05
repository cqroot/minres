#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
from typing import List

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

from minres.core.res_manager import ResManager


class TableModel(QAbstractTableModel):
    def __init__(self, key: str = None):
        super().__init__()

        cols = copy.deepcopy(ResManager().get_res_columns(key))
        if cols:
            cols.insert(0, "Path")
        self._headers = cols if cols else []

        data = ResManager().get_res_data(key)
        self._data = data if data else []

        print(f"TableModel created for key: {key}")
        print(f"  Rows: {len(self._data)}")
        print(f"  Columns: {self._headers}")

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if row < len(self._data) and col < len(self._data[row]):
                return str(self._data[row][col])
            return None

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                if section < len(self._headers):
                    return self._headers[section]
            else:
                return str(section + 1)
        return None
