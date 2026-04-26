"""
Painel de preview lateral com thumbnail e info do PDF selecionado.
"""
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget

from core.pdf_item import PdfItem
from core.workers import ThumbnailWorker

BG = "#0e0e14"
SURFACE = "#16161f"
BORDER = "#2c2c3e"
TEXT = "#e2e2ee"
TEXT2 = "#8888a8"
TEXT3 = "#4a4a62"


class PreviewPanel(QWidget):
    preview_open_requested = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_path = None
        self._current_item = None
        self._worker = None
        self._setup_ui()

    def _setup_ui(self):
        self.setMinimumWidth(220)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QWidget()
        header.setFixedHeight(42)
        header.setStyleSheet(f"background: {SURFACE}; border-bottom: 1px solid {BORDER};")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(14, 0, 14, 0)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Pre-visualizacao")
        title.setStyleSheet(f"color: {TEXT2}; font-size: 12px; font-weight: 500;")
        header_layout.addWidget(title)
        layout.addWidget(header)

        self.content = QWidget()
        self.content.setStyleSheet(f"background: {BG};")
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(16, 20, 16, 20)
        content_layout.setSpacing(14)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.placeholder = QLabel("Selecione um\ndocumento para\nvisualizar")
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder.setStyleSheet(f"""
            color: {TEXT3}; font-size: 12px; line-height: 1.6;
            padding: 40px 10px;
        """)

        self.img_frame = QFrame()
        self.img_frame.setVisible(False)
        self.img_frame.setCursor(Qt.CursorShape.PointingHandCursor)
        self.img_frame.setStyleSheet(f"""
            QFrame {{
                background: #ffffff;
                border-radius: 4px;
                border: 1px solid {BORDER};
            }}
        """)
        img_layout = QVBoxLayout(self.img_frame)
        img_layout.setContentsMargins(0, 0, 0, 0)

        self.img_label = QLabel()
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_label.setScaledContents(False)
        self.img_label.setStyleSheet("background: #ffffff;")
        img_layout.addWidget(self.img_label)

        self.loading_label = QLabel("Carregando...")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setStyleSheet(f"color: {TEXT3}; font-size: 12px;")
        self.loading_label.setVisible(False)

        self.info_frame = QFrame()
        self.info_frame.setVisible(False)
        self.info_frame.setStyleSheet(f"""
            QFrame {{
                background: {SURFACE};
                border: 1px solid {BORDER};
                border-radius: 8px;
                padding: 4px;
            }}
        """)
        info_layout = QVBoxLayout(self.info_frame)
        info_layout.setContentsMargins(12, 10, 12, 10)
        info_layout.setSpacing(6)

        self.info_name = QLabel()
        self.info_name.setWordWrap(True)
        self.info_name.setStyleSheet(f"""
            color: {TEXT}; font-size: 12px; font-weight: 600;
            border: none; background: transparent;
        """)

        self.info_pages = QLabel()
        self.info_pages.setStyleSheet(f"color: {TEXT2}; font-size: 11px; border: none; background: transparent;")

        self.info_size = QLabel()
        self.info_size.setStyleSheet(f"color: {TEXT3}; font-size: 11px; border: none; background: transparent;")

        info_layout.addWidget(self.info_name)
        info_layout.addWidget(self.info_pages)
        info_layout.addWidget(self.info_size)

        content_layout.addWidget(self.placeholder)
        content_layout.addWidget(self.loading_label)
        content_layout.addWidget(self.img_frame)
        content_layout.addWidget(self.info_frame)
        content_layout.addStretch()

        layout.addWidget(self.content, stretch=1)

    def show_item(self, item: PdfItem | None):
        if item is None:
            self._clear()
            return

        if item.path == self._current_path:
            return

        self._current_path = item.path
        self._current_item = item

        if self._worker and self._worker.isRunning():
            self._worker.cancel()
            self._worker.wait(300)

        self.placeholder.setVisible(False)
        self.img_frame.setVisible(False)
        self.loading_label.setVisible(True)
        self.info_frame.setVisible(False)

        self._worker = ThumbnailWorker(item.path, width=self.width() - 40)
        self._worker.thumbnail_ready.connect(self._on_thumbnail)
        self._worker.start()

        self.info_name.setText(item.display_name)
        self.info_pages.setText(f"Paginas: {item.page_count}")
        self.info_size.setText(f"Tamanho: {item.file_size}")

    def _on_thumbnail(self, path: str, pixmap):
        if path != self._current_path:
            return
        self.loading_label.setVisible(False)
        if pixmap and not pixmap.isNull():
            max_w = self.width() - 40
            scaled = pixmap.scaledToWidth(max_w, Qt.TransformationMode.SmoothTransformation)
            self.img_label.setPixmap(scaled)
            self.img_label.setFixedHeight(scaled.height())
            self.img_frame.setVisible(True)
        self.info_frame.setVisible(True)

    def _clear(self):
        self._current_path = None
        self._current_item = None
        self.placeholder.setVisible(True)
        self.img_frame.setVisible(False)
        self.loading_label.setVisible(False)
        self.info_frame.setVisible(False)

    def mousePressEvent(self, event):
        if (
            event.button() == Qt.MouseButton.LeftButton
            and self._current_item is not None
            and self.img_frame.isVisible()
        ):
            local_pos = self.mapFromGlobal(event.globalPosition().toPoint())
            if self.img_frame.geometry().contains(local_pos):
                self.preview_open_requested.emit(self._current_item)
                event.accept()
                return
        super().mousePressEvent(event)
