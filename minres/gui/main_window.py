#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtCore import QStringListModel, Qt
from PySide6.QtWidgets import (
    QListView,
    QMainWindow,
    QSplitter,
    QWidget,
    QVBoxLayout,
    QLabel,
)

from minres.core.logger import logger
from minres.core.res_manager import ResManager
from minres.gui.res_widget import ResWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.info("Initializing MainWindow")
        self.setWindowTitle("minres")
        self.setGeometry(100, 100, 900, 600)

        self.setup_ui()

    def setup_ui(self):
        """Setup UI interface"""
        logger.debug("Setting up UI components")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.setup_left_widgets()
        self.setup_res_widgets()

        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.addWidget(self.list_view)
        self.main_splitter.addWidget(self.res_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(self.main_splitter)

        self.main_splitter.setSizes([50, 1])

        self.status_label = QLabel("Ready")
        self.statusBar().addWidget(self.status_label)

        index = self.list_view.model().index(0, 0)
        self.list_view.setCurrentIndex(index)
        self.on_item_clicked(index)

    def setup_left_widgets(self):
        self.list_view = QListView()
        self.model = QStringListModel()
        self.model.setStringList(ResManager().get_keys())
        self.list_view.setModel(self.model)
        self.list_view.clicked.connect(self.on_item_clicked)

    def setup_res_widgets(self):
        self.res_widget = ResWidget()
        self.res_widget.filter_edit.textChanged.connect(self.on_filter_text_changed)
        self.res_widget.filter_combo.currentIndexChanged.connect(
            self.on_filter_column_changed
        )

    def on_item_clicked(self, index):
        profile_name = self.model.data(index)
        logger.info(f"Profile selected: {profile_name}")

        self.res_widget.change_profile(profile_name)

        self.update_status()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            logger.debug("Escape key pressed, clearing filter")
            self.clear_filter()
        super().keyPressEvent(event)

    def update_status(self):
        total_rows = self.res_widget.source_model.rowCount()
        filtered_rows = self.res_widget.proxy_model.rowCount()

        if filtered_rows == total_rows:
            self.status_label.setText(f"Total rows: {total_rows}")
        else:
            self.status_label.setText(
                f"Showing: {filtered_rows} / Total rows: {total_rows}"
            )

    def clear_filter(self):
        self.res_widget.clear_filter()
        self.update_status()

    def on_filter_text_changed(self, text):
        logger.debug(f"Filter text changed: '{text}'")
        self.res_widget.proxy_model.setFilterText(text)
        self.update_status()

    def on_filter_column_changed(self, index):
        logger.debug(f"Filter column changed to index: {index}")
        self.res_widget.proxy_model.setFilterColumn(index - 1)
