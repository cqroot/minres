#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PySide6.QtWidgets import QApplication

from minres.core.logger import logger
from minres.core.res_manager import ResManager
from minres.gui.main_window import MainWindow


def main() -> None:
    logger.info("Starting minres application.")
    try:
        ResManager().load_config("./minres.yaml")
        logger.info("Configuration loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        sys.exit(1)

    app = QApplication(sys.argv)
    app.setApplicationName("minres")
    app.setOrganizationName("minres")

    window = MainWindow()
    window.show()
    logger.info("Main window displayed")

    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(f"Unhandled exception in main: {e}")
        sys.exit(1)
