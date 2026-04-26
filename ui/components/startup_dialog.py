"""Tela inicial do aplicativo."""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout

from app.paths import resource_path
from app.version import APP_NAME


BG = "#000000"
ACCENT = "#1976ff"
TEXT = "#ffffff"
TEXT2 = "#aeb8d6"


class StartupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(APP_NAME)
        self.setModal(True)
        self.setFixedSize(760, 520)
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"""
            QDialog {{
                background: {BG};
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(42, 42, 42, 34)
        layout.setSpacing(18)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()

        logo = QLabel()
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap(resource_path("assets/axiel_pdf_logo.png"))
        if not pixmap.isNull():
            logo.setPixmap(
                pixmap.scaled(
                    560,
                    320,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            logo.setText(APP_NAME)
            logo.setStyleSheet(f"color: {TEXT}; font-size: 34px; font-weight: 700;")
        layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Automacao de PDFs com inteligencia artificial")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"color: {TEXT2}; font-size: 14px;")
        layout.addWidget(subtitle)

        layout.addStretch()

        btn = QPushButton("Entrar")
        btn.setFixedSize(150, 38)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self.accept)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {ACCENT};
                color: white;
                border: none;
                border-radius: 7px;
                font-size: 13px;
                font-weight: 700;
            }}
            QPushButton:hover {{
                background: #2f86ff;
            }}
        """)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
