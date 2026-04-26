"""Workers usados por operacoes que nao devem bloquear a interface."""
from PyQt6.QtCore import QThread, pyqtSignal
from core.pdf_engine import get_thumbnail


class ThumbnailWorker(QThread):
    thumbnail_ready = pyqtSignal(str, object)

    def __init__(self, path: str, width: int = 180):
        super().__init__()
        self.path = path
        self.width = width
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def run(self):
        if self._cancelled:
            return
        pixmap = get_thumbnail(self.path, 0, self.width)
        if not self._cancelled:
            self.thumbnail_ready.emit(self.path, pixmap)


class MergeWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)

    def __init__(self, paths: list, output: str):
        super().__init__()
        self.paths = paths
        self.output = output

    def run(self):
        from core.pdf_engine import merge_pdfs
        ok = merge_pdfs(self.paths, self.output, self.progress.emit)
        self.finished.emit(ok, self.output)
