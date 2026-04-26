"""Operacoes de leitura, renderizacao e merge de PDFs."""
import logging
import os

import fitz
import pikepdf
from PyQt6.QtGui import QImage, QPixmap


logger = logging.getLogger(__name__)


def get_thumbnail(pdf_path: str, page_index: int = 0, width: int = 180) -> QPixmap | None:
    """Renderiza a pagina informada como thumbnail."""
    try:
        doc = fitz.open(pdf_path)
        if page_index >= len(doc):
            page_index = 0
        page = doc[page_index]
        scale = width / page.rect.width
        mat = fitz.Matrix(scale, scale)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        doc.close()

        image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(image)
    except Exception:
        logger.warning("Falha ao renderizar thumbnail do PDF.", exc_info=True)
        return None


def render_page(pdf_path: str, page_index: int = 0, zoom: float = 1.0) -> QPixmap | None:
    """Renderiza uma pagina do PDF."""
    try:
        doc = fitz.open(pdf_path)
        if page_index >= len(doc):
            page_index = 0
        page = doc[page_index]
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        doc.close()

        image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(image)
    except Exception:
        logger.warning("Falha ao renderizar pagina do PDF.", exc_info=True)
        return None


def get_page_count(pdf_path: str) -> int:
    """Retorna o total de paginas do PDF."""
    try:
        doc = fitz.open(pdf_path)
        page_count = len(doc)
        doc.close()
        return page_count
    except Exception:
        return 0


def get_file_size_str(path: str) -> str:
    size = os.path.getsize(path)
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size / 1024 / 1024:.1f} MB"


def merge_pdfs(pdf_paths: list[str], output_path: str, progress_callback=None) -> bool:
    try:
        writer = pikepdf.Pdf.new()
        total = len(pdf_paths)

        for index, path in enumerate(pdf_paths):
            try:
                src = pikepdf.open(path)
                writer.pages.extend(src.pages)
                src.close()
            except Exception:
                logger.warning("PDF ignorado durante o merge.", exc_info=True)

            if progress_callback:
                progress_callback(int((index + 1) / total * 100))

        writer.save(output_path)
        writer.close()
        return True
    except Exception:
        logger.exception("Falha ao combinar PDFs.")
        return False
