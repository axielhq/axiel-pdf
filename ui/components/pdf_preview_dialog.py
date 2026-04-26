"""Dialog de visualizacao ampliada de PDF."""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QHBoxLayout, QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget
)

from core.pdf_engine import render_page

BG = "#0e0e14"
SURFACE = "#16161f"
SURFACE2 = "#1e1e2a"
BORDER = "#2c2c3e"
BORDER2 = "#38384f"
ACCENT = "#7c7eff"
TEXT = "#e2e2ee"
TEXT2 = "#8888a8"


class PdfPreviewDialog(QDialog):
    def __init__(self, pdf_path: str, title: str, parent=None):
        super().__init__(parent)
        self._pdf_path = pdf_path
        self._title = title
        self._page_index = 0
        self._zoom = 1.3
        self._setup_ui()
        self._render_page()

    def _setup_ui(self):
        self.setWindowTitle(self._title)
        self.setModal(True)
        self.resize(780, 680)
        self.setMinimumSize(520, 420)
        self.setStyleSheet(f"""
            QDialog {{ background: {BG}; }}
            QWidget {{ color: {TEXT}; font-family: 'DM Sans', 'Segoe UI', sans-serif; }}
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        toolbar = QWidget()
        toolbar.setFixedHeight(52)
        toolbar.setStyleSheet(f"background: {SURFACE}; border-bottom: 1px solid {BORDER};")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(14, 0, 14, 0)
        toolbar_layout.setSpacing(8)

        self.title_label = QLabel(self._title)
        self.title_label.setStyleSheet(f"color: {TEXT}; font-size: 13px; font-weight: 600;")

        self.zoom_out_btn = self._tool_btn("Zoom -")
        self.zoom_out_btn.clicked.connect(self._zoom_out)

        self.zoom_in_btn = self._tool_btn("Zoom +")
        self.zoom_in_btn.clicked.connect(self._zoom_in)

        self.close_btn = self._tool_btn("Fechar", danger=True)
        self.close_btn.clicked.connect(self.close)

        toolbar_layout.addWidget(self.title_label)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.zoom_out_btn)
        toolbar_layout.addWidget(self.zoom_in_btn)
        toolbar_layout.addWidget(self.close_btn)
        root.addWidget(toolbar)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background: {BG}; }}
            QScrollBar:vertical {{
                background: {SURFACE2}; width: 8px; margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background: {BORDER2}; border-radius: 4px; min-height: 30px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
        """)

        self.canvas = QWidget()
        canvas_layout = QVBoxLayout(self.canvas)
        canvas_layout.setContentsMargins(24, 24, 24, 24)
        canvas_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.page_frame = QWidget()
        self.page_frame.setStyleSheet(f"background: #ffffff; border: 1px solid {BORDER};")
        frame_layout = QVBoxLayout(self.page_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)

        self.page_label = QLabel()
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_label.setStyleSheet("background: #ffffff;")
        frame_layout.addWidget(self.page_label)

        self.info_label = QLabel("")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet(f"color: {TEXT2}; font-size: 11px; padding: 10px 0 0 0;")

        canvas_layout.addWidget(self.page_frame)
        canvas_layout.addWidget(self.info_label)
        self.scroll.setWidget(self.canvas)
        root.addWidget(self.scroll, stretch=1)

    def _tool_btn(self, text: str, danger: bool = False) -> QPushButton:
        btn = QPushButton(text)
        btn.setFixedHeight(32)
        btn.setMinimumWidth(74)
        hover_color = "#ff4f6a" if danger else ACCENT
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {SURFACE2};
                color: {TEXT2};
                border: 1px solid {BORDER2};
                border-radius: 7px;
                padding: 0 12px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                color: {TEXT};
                border-color: {hover_color};
            }}
        """)
        return btn

    def _render_page(self):
        pixmap = render_page(self._pdf_path, self._page_index, self._zoom)
        if not pixmap or pixmap.isNull():
            self.info_label.setText("Falha ao renderizar a pagina.")
            return

        self.page_label.setPixmap(pixmap)
        self.page_label.resize(pixmap.size())
        self.page_frame.setFixedSize(pixmap.size())
        self.info_label.setText(f"Pagina 1  |  Zoom {int(self._zoom * 100)}%")

    def _zoom_in(self):
        self._zoom = min(self._zoom + 0.2, 3.0)
        self._render_page()

    def _zoom_out(self):
        self._zoom = max(self._zoom - 0.2, 0.6)
        self._render_page()

    def wheelEvent(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if event.angleDelta().y() > 0:
                self._zoom_in()
            else:
                self._zoom_out()
            event.accept()
            return
        super().wheelEvent(event)
