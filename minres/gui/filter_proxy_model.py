#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtCore import QSortFilterProxyModel


class FilterProxyModel(QSortFilterProxyModel):
    ALL_COLUMNS = -1

    def __init__(self):
        super().__init__()
        self._filter_column = self.ALL_COLUMNS
        self._filter_text = ""

    def setFilterColumn(self, column):
        self._filter_column = column
        self.invalidateFilter()

    def setFilterText(self, text):
        self._filter_text = text.lower()
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        if not self._filter_text:
            return True

        source_model = self.sourceModel()
        if not source_model:
            return False

        # If a specific column is specified, only check that column
        if self._filter_column >= 0:
            index = source_model.index(source_row, self._filter_column)
            data = source_model.data(index)
            return self._filter_text in str(data).lower()

        # Otherwise check all columns
        for col in range(source_model.columnCount()):
            index = source_model.index(source_row, col)
            data = source_model.data(index)
            if self._filter_text in str(data).lower():
                return True

        return False
