"""Janela principal do Axiel PDF."""
import os
from pathlib import Path

from PyQt6.QtCore import QSize, Qt, QUrl
from PyQt6.QtGui import QAction, QDesktopServices, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.config import read_provider_credentials
from app.paths import resource_path
from app.version import APP_NAME, APP_VERSION
from core.pdf_engine import get_file_size_str, get_page_count
from core.pdf_item import PdfItem
from core.workers import MergeWorker
from modules.ai.features import AI_PROVIDERS
from modules.features import FutureFeature
from modules.ocr.features import OCR_FEATURE
from ui.components.buttons import build_top_button
from ui.components.pdf_preview_dialog import PdfPreviewDialog
from ui.pdf_list import PdfListWidget
from ui.preview_panel import PreviewPanel

BG = "#0e0e14"
SURFACE = "#16161f"
SURFACE2 = "#1e1e2a"
SURFACE3 = "#252532"
BORDER = "#2c2c3e"
BORDER2 = "#38384f"
ACCENT = "#7c7eff"
TEXT = "#e2e2ee"
TEXT2 = "#8888a8"
TEXT3 = "#4a4a62"
DANGER = "#ff4f6a"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(900, 600)
        self.resize(1120, 700)
        self._merge_worker = None
        self._setup_ui()
        self._apply_global_style()

    def _apply_global_style(self):
        self.setStyleSheet(f"""
            QMainWindow {{ background: {BG}; }}
            QWidget {{ font-family: 'DM Sans', 'Segoe UI', sans-serif; }}
            QToolTip {{
                background: {SURFACE2};
                color: {TEXT};
                border: 1px solid {BORDER2};
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 11px;
            }}
        """)

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_topbar())

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        self.pdf_list = PdfListWidget()
        self.pdf_list.selection_changed.connect(self._on_selection)
        self.pdf_list.list_changed.connect(self._update_merge_btn)

        self.preview = PreviewPanel()
        self.preview.setFixedWidth(230)
        self.preview.preview_open_requested.connect(self._open_preview_dialog)

        body.addWidget(self.pdf_list, stretch=1)

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.VLine)
        divider.setStyleSheet(f"color: {BORDER};")
        body.addWidget(divider)
        body.addWidget(self.preview)

        body_widget = QWidget()
        body_widget.setLayout(body)
        root.addWidget(body_widget, stretch=1)
        root.addWidget(self._build_bottombar())

    def _build_topbar(self) -> QWidget:
        bar = QWidget()
        bar.setFixedHeight(54)
        bar.setStyleSheet(f"background: {SURFACE}; border-bottom: 1px solid {BORDER};")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(10)

        logo_txt = QLabel(APP_NAME)
        logo_txt.setStyleSheet(f"""
            color: {TEXT};
            font-size: 15px;
            font-weight: 700;
        """)

        badge = QLabel()
        badge.setFixedSize(34, 34)
        badge.setPixmap(
            QPixmap(resource_path("assets/pdf_badge.svg")).scaled(
                34,
                34,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

        layout.addWidget(logo_txt)
        layout.addWidget(badge)
        layout.addStretch()

        self.lbl_count = QLabel("0 arquivos")
        self.lbl_count.setStyleSheet(f"color: {TEXT3}; font-size: 12px;")
        layout.addWidget(self.lbl_count)

        sep = QLabel("-")
        sep.setStyleSheet(f"color: {TEXT3};")
        layout.addWidget(sep)

        self.lbl_pages = QLabel("0 paginas totais")
        self.lbl_pages.setStyleSheet(f"color: {TEXT3}; font-size: 12px;")
        layout.addWidget(self.lbl_pages)

        layout.addSpacing(20)

        self.btn_ai = self._top_btn("Use IA para editar", primary=False)
        self.btn_ai.setMenu(self._build_ai_menu())

        self.btn_ocr = self._top_btn("Extrair com OCR", primary=False)
        self.btn_ocr.setIcon(QIcon(resource_path(OCR_FEATURE.icon_path)))
        self.btn_ocr.setIconSize(QSize(18, 18))
        self.btn_ocr.clicked.connect(lambda: self._show_future_feature(OCR_FEATURE))

        self.btn_add = self._top_btn("Adicionar PDFs", primary=False)
        self.btn_add.setIcon(QIcon(resource_path("assets/pdf_badge.svg")))
        self.btn_add.setIconSize(QSize(18, 18))
        self.btn_add.clicked.connect(self._add_files)

        self.btn_clear = self._top_btn("Limpar tudo", primary=False)
        self.btn_clear.clicked.connect(self._clear_all)
        self.btn_clear.setStyleSheet(
            self.btn_clear.styleSheet()
            + f"QPushButton:hover {{ color: {DANGER}; border-color: {DANGER}; }}"
        )

        self.btn_about = self._top_btn("Sobre", primary=False)
        self.btn_about.clicked.connect(self._show_about)

        self.btn_merge = self._top_btn("Juntar PDFs", primary=True)
        self.btn_merge.clicked.connect(self._merge)
        self.btn_merge.setEnabled(False)

        layout.addWidget(self.btn_ai)
        layout.addWidget(self.btn_ocr)
        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_clear)
        layout.addWidget(self.btn_about)
        layout.addSpacing(8)
        layout.addWidget(self.btn_merge)

        return bar

    def _build_ai_menu(self) -> QMenu:
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{
                background: {SURFACE2};
                color: {TEXT};
                border: 1px solid {BORDER2};
                padding: 6px;
            }}
            QMenu::item {{
                padding: 7px 28px 7px 8px;
            }}
            QMenu::item:selected {{
                background: {SURFACE3};
            }}
        """)
        for provider in AI_PROVIDERS:
            action = QAction(QIcon(resource_path(provider.icon_path)), provider.name, self)
            action.triggered.connect(lambda checked=False, item=provider: self._show_future_feature(item))
            menu.addAction(action)
        return menu

    def _build_bottombar(self) -> QWidget:
        bar = QWidget()
        bar.setFixedHeight(36)
        bar.setStyleSheet(f"background: {SURFACE}; border-top: 1px solid {BORDER};")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(12)

        self.status_label = QLabel("Pronto")
        self.status_label.setStyleSheet(f"color: {TEXT3}; font-size: 11px;")
        layout.addWidget(self.status_label)

        layout.addStretch()

        self.footer_label = QLabel("Axiel PDF © 2026 Axiel. Open source under GPLv3.")
        self.footer_label.setStyleSheet(f"color: {TEXT3}; font-size: 10px;")
        layout.addWidget(self.footer_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(200)
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background: {SURFACE2};
                border-radius: 2px;
                border: none;
            }}
            QProgressBar::chunk {{
                background: {ACCENT};
                border-radius: 2px;
            }}
        """)
        layout.addWidget(self.progress_bar)

        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet(f"color: {ACCENT}; font-size: 11px; font-weight: 500;")
        self.progress_label.setVisible(False)
        layout.addWidget(self.progress_label)

        return bar

    def _top_btn(self, text: str, primary: bool) -> QPushButton:
        return build_top_button(text, primary, {
            "accent": ACCENT,
            "surface2": SURFACE2,
            "border2": BORDER2,
            "text": TEXT,
            "text2": TEXT2,
            "text3": TEXT3,
        })

    def _show_future_feature(self, feature: FutureFeature):
        credential_lines = []
        if feature.api_key_env:
            credential_lines.append(f"Chave API: {feature.api_key_env}")
        if feature.api_token_env:
            credential_lines.append(f"Token: {feature.api_token_env}")

        provider_credentials = read_provider_credentials(feature.api_key_env, feature.api_token_env)
        configured = bool(provider_credentials.api_key or provider_credentials.api_token)
        credentials = "\n".join(credential_lines) if credential_lines else "Credenciais: nao aplicavel nesta etapa"
        capabilities = "\n".join(f"- {item}" for item in feature.capabilities)

        QMessageBox.information(
            self,
            f"{feature.name} - planejado",
            (
                "Funcionalidade planejada.\n\n"
                f"{credentials}\n"
                f"Configurado no ambiente: {'sim' if configured else 'nao'}\n\n"
                f"Preparado para:\n{capabilities}"
            ),
        )

    def _show_about(self):
        github_url = "https://github.com/axielhq/axiel-pdf"
        msg = QMessageBox(self)
        msg.setWindowTitle(f"Sobre {APP_NAME}")
        msg.setIconPixmap(
            QPixmap(resource_path("assets/pdf_badge.svg")).scaled(
                48,
                48,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        msg.setText(APP_NAME)
        msg.setInformativeText(
            "Automacao de PDFs com inteligencia artificial para fluxos de trabalho "
            "de documentos de alto volume.\n\n"
            "Criado pela Axiel.\n"
            "Codigo aberto sob a Licenca Publica Geral GNU v3.0.\n\n"
            f"Versao: {APP_VERSION}\n"
            f"GitHub: {github_url}"
        )
        github_button = msg.addButton("GitHub", QMessageBox.ButtonRole.ActionRole)
        msg.addButton(QMessageBox.StandardButton.Ok)
        msg.exec()
        if msg.clickedButton() == github_button:
            QDesktopServices.openUrl(QUrl(github_url))

    def _add_files(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecionar PDFs",
            "",
            "Arquivos PDF (*.pdf)",
        )
        if not paths:
            return

        self.status_label.setText(f"Carregando {len(paths)} arquivo(s)...")
        QApplication.processEvents()

        new_items = []
        for path in paths:
            item = PdfItem(path=path)
            item.page_count = get_page_count(path)
            item.file_size = get_file_size_str(path)
            new_items.append(item)

        self.pdf_list.add_items(new_items)
        self._update_stats()
        self.status_label.setText(f"{len(new_items)} arquivo(s) adicionado(s)")

    def _clear_all(self):
        if not self.pdf_list.items:
            return
        reply = QMessageBox.question(
            self,
            "Confirmar",
            "Remover todos os documentos da lista?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.pdf_list.clear_all()
            self._update_stats()
            self.status_label.setText("Lista limpa")

    def _merge(self):
        paths = self.pdf_list.get_paths()
        if not paths:
            return

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar PDF combinado",
            "axiel_pdf_combinado.pdf",
            "Arquivo PDF (*.pdf)",
        )
        if not output_path:
            return

        self.btn_merge.setEnabled(False)
        self.btn_add.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_label.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText(f"Combinando {len(paths)} arquivos...")

        self._merge_worker = MergeWorker(paths, output_path)
        self._merge_worker.progress.connect(self._on_progress)
        self._merge_worker.finished.connect(self._on_merge_done)
        self._merge_worker.start()

    def _on_progress(self, value: int):
        self.progress_bar.setValue(value)
        self.progress_label.setText(f"{value}%")

    def _on_merge_done(self, success: bool, output_path: str):
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        self.btn_merge.setEnabled(True)
        self.btn_add.setEnabled(True)

        if success:
            size = get_file_size_str(output_path)
            filename = Path(output_path).name
            self.status_label.setText(f"Salvo em: {filename} ({size})")

            msg = QMessageBox(self)
            msg.setWindowTitle("Concluido")
            msg.setText(f"PDF combinado gerado com sucesso.\n\nArquivo: {filename}\nTamanho: {size}")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStandardButtons(QMessageBox.StandardButton.Open | QMessageBox.StandardButton.Ok)
            msg.button(QMessageBox.StandardButton.Open).setText("Abrir arquivo")

            if msg.exec() == QMessageBox.StandardButton.Open:
                self._open_file(output_path)
        else:
            self.status_label.setText("Erro ao combinar PDFs")
            QMessageBox.critical(
                self,
                "Erro",
                "Falha ao combinar os PDFs. Verifique se os arquivos estao acessiveis.",
            )

    def _open_file(self, output_path: str):
        import subprocess
        import sys

        if sys.platform == "darwin":
            subprocess.run(["open", output_path], check=False)
        elif sys.platform == "win32":
            os.startfile(output_path)
        else:
            subprocess.run(["xdg-open", output_path], check=False)

    def _on_selection(self, item: PdfItem | None):
        self.preview.show_item(item)

    def _open_preview_dialog(self, item: PdfItem | None):
        if item is None:
            return
        dialog = PdfPreviewDialog(item.path, item.display_name, self)
        dialog.exec()

    def _update_merge_btn(self):
        has_items = len(self.pdf_list.items) >= 2
        self.btn_merge.setEnabled(has_items)
        self._update_stats()

    def _update_stats(self):
        total_files = len(self.pdf_list.items)
        total_pages = sum(item.page_count for item in self.pdf_list.items)
        self.lbl_count.setText(f"{total_files} arquivo{'s' if total_files != 1 else ''}")
        self.lbl_pages.setText(f"{total_pages} pagina{'s' if total_pages != 1 else ''} totais")
