"""Inicializacao da aplicacao desktop."""
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

from app.paths import PROJECT_ROOT
from app.version import APP_NAME, APP_ORGANIZATION


def ensure_project_imports():
    root = str(PROJECT_ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)


def create_application(argv: list[str]) -> QApplication:
    ensure_project_imports()
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(APP_ORGANIZATION)
    app.setFont(QFont("DM Sans", 13))
    return app
