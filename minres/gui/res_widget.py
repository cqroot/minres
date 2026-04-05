#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from minres.core.logger import logger
from minres.core.res_manager import ResManager
from minres.gui.filter_proxy_model import FilterProxyModel
from minres.gui.table_model import TableModel
from minres.gui.table_view import TableView


class ResWidget(QWidget):
    def __init__(self):
        super().__init__()
        logger.debug("Initializing ResWidget")

        self.setup_ui()
        self.setup_models()

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.setup_filter_ui()
        self.main_layout.addLayout(self.filter_row_layout)

        self.table_view = TableView()
        self.main_layout.addWidget(self.table_view)

        self.setLayout(self.main_layout)

    def setup_models(self):
        keys = ResManager().get_keys()
        if keys:
            self.source_model = TableModel(keys[0])
        else:
            self.source_model = TableModel()

        # Proxy model (for filtering)
        self.proxy_model = FilterProxyModel()
        self.proxy_model.setSourceModel(self.source_model)

        # Set sorting role for proxy model
        self.proxy_model.setSortRole(Qt.ItemDataRole.DisplayRole)

        # Set proxy model to table view
        self.table_view.setModel(self.proxy_model)

        # Enable sorting
        self.table_view.setSortingEnabled(True)

    def setup_filter_ui(self):
        self.filter_row_layout = QHBoxLayout()
        self.filter_row_layout.addWidget(QLabel("Filter:"))

        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText("Enter filter keyword...")
        self.filter_row_layout.addWidget(self.filter_edit)

        self.filter_combo = QComboBox()
        self.filter_row_layout.addWidget(self.filter_combo)

    def change_profile(self, name: str):
        logger.info(f"Changing profile to: {name}")
        self.filter_combo.clear()

        self.filter_combo.addItem("All")
        cols = ResManager().get_res_columns(name)
        for _, col in enumerate(cols):
            self.filter_combo.addItem(col)

        self.filter_edit.clear()

        new_source_model = TableModel(name)

        self.proxy_model.beginResetModel()
        self.proxy_model.setSourceModel(new_source_model)
        self.source_model = new_source_model
        self.proxy_model.endResetModel()
        self.table_view.setColumnHidden(0, True)
        self.table_view.set_equal_column_widths()

    def clear_filter(self):
        """Clear filter conditions"""
        logger.debug("Clearing filter")
        self.filter_edit.clear()
