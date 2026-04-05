#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QHeaderView, QTableView

from minres.core.logger import logger
from minres.core.res_manager import open_file_with_default_app


class TableView(QTableView):
    def __init__(self):
        super().__init__()

        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.verticalHeader().hide()

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.horizontalHeader().setStretchLastSection(True)

        self.doubleClicked.connect(self.on_item_double_clicked)

    def set_equal_column_widths(self):
        model = self.model()
        if model is None:
            return

        visible_columns = [
            col
            for col in range(model.columnCount())
            if not self.isColumnHidden(col)
        ]
        if not visible_columns:
            return

        total_width = self.viewport().width() or self.width() or 1
        width = total_width // len(visible_columns)
        if width <= 0:
            width = 120

        for column in visible_columns:
            self.setColumnWidth(column, width)
            self.horizontalHeader().setSectionResizeMode(
                column, QHeaderView.ResizeMode.Interactive
            )

    def on_item_double_clicked(self, index: QModelIndex):
        file_path_index = index.sibling(index.row(), 0)
        file_path = file_path_index.data()

        if not file_path:
            logger.warning("Unable to get file path from table index")
            return

        logger.info(f"Attempting to open file: {file_path}")
        success = open_file_with_default_app(file_path)
        if not success:
            logger.error(f"Failed to open file: {file_path}")
