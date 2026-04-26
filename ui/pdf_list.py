"""
Lista de PDFs com visual em linhas, acoes e reordenacao.
"""
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget
)

from app.paths import resource_path
from core.pdf_item import PdfItem

BG = "#0e0e14"
SURFACE = "#171821"
SURFACE2 = "#212537"
SURFACE3 = "#2a3045"
SURFACE4 = "#24385a"
SURFACE5 = "#14151d"
BORDER = "#303449"
BORDER2 = "#474d66"
ACCENT = "#7c7eff"
ACCENT_DIM = "#324d86"
TEXT = "#e2e2ee"
TEXT2 = "#8888a8"
TEXT3 = "#4a4a62"
DANGER = "#ff4f6a"
SUCCESS = "#3ecf8e"
ROW_EVEN = "#171821"
ROW_ODD = "#202535"


class PdfRowWidget(QWidget):
    """Linha visual de um documento na lista."""

    remove_requested = pyqtSignal(int)

    def __init__(
        self,
        item: PdfItem,
        index: int,
        alternate: bool,
        moved: bool = False,
        parent=None,
    ):
        super().__init__(parent)
        self.pdf_item = item
        self.index = index
        self.alternate = alternate
        self.moved = moved
        self._editing = False
        self._setup_ui()

    def _setup_ui(self):
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedHeight(64)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        order_box = QWidget()
        order_box.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        order_box.setFixedWidth(56)
        order_box.setStyleSheet("background: transparent; border: none;")
        order_layout = QHBoxLayout(order_box)
        order_layout.setContentsMargins(0, 0, 0, 0)

        self.num_label = QLabel(f"{self.index + 1:02d}")
        self.num_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.num_label.setStyleSheet(f"""
            background: transparent; border: none;
            color: {TEXT2}; font-family: 'DM Mono', monospace;
            font-size: 11px; font-weight: 600;
        """)
        order_layout.addWidget(self.num_label)
        root.addWidget(order_box)

        icon_box = QWidget()
        icon_box.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        icon_box.setFixedWidth(52)
        icon_box.setStyleSheet("background: transparent; border: none;")
        icon_layout = QHBoxLayout(icon_box)
        icon_layout.setContentsMargins(0, 0, 0, 0)

        self.icon_label = QLabel()
        self.icon_label.setFixedSize(20, 24)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("background: transparent; border: none;")
        icon = QPixmap(resource_path("assets/pdf_badge.svg"))
        if not icon.isNull():
            self.icon_label.setPixmap(
                icon.scaled(
                    20,
                    24,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        icon_layout.addWidget(self.icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
        root.addWidget(icon_box)

        info_box = QWidget()
        info_box.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        info_box.setStyleSheet("background: transparent; border: none;")
        info = QVBoxLayout(info_box)
        info.setContentsMargins(12, 8, 12, 8)
        info.setSpacing(2)

        self.name_label = QLabel(self.pdf_item.display_name)
        self.name_label.setStyleSheet(
            f"background: transparent; border: none; color: {TEXT}; font-size: 12px; font-weight: 600;"
        )
        self.name_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        self.name_edit = QLineEdit(self.pdf_item.label)
        self.name_edit.setVisible(False)
        self.name_edit.setStyleSheet(f"""
            QLineEdit {{
                background: {SURFACE3};
                border: 1px solid {ACCENT};
                border-radius: 4px;
                padding: 2px 6px;
                color: {TEXT};
                font-size: 11px;
            }}
        """)
        self.name_edit.returnPressed.connect(self._finish_edit)
        self.name_edit.editingFinished.connect(self._finish_edit)

        self.meta = QLabel(f"{self.pdf_item.page_count} pag  |  {self.pdf_item.file_size}")
        self.meta.setStyleSheet(f"background: transparent; border: none; color: {TEXT2}; font-size: 11px;")
        self.meta.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        info.addWidget(self.name_label)
        info.addWidget(self.name_edit)
        info.addWidget(self.meta)
        root.addWidget(info_box, stretch=1)

        actions_box = QWidget()
        actions_box.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        actions_box.setFixedWidth(238)
        actions_box.setStyleSheet("background: transparent; border: none;")
        actions_layout = QHBoxLayout(actions_box)
        actions_layout.setContentsMargins(12, 0, 12, 0)
        actions_layout.setSpacing(12)
        actions_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.move_badge = QLabel("Movido")
        self.move_badge.setVisible(self.moved)
        self.move_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.move_badge.setFixedHeight(20)
        self.move_badge.setFixedWidth(62)
        self.move_badge.setStyleSheet(f"""
            background: rgba(62, 207, 142, 0.14);
            color: {SUCCESS};
            border: 1px solid rgba(62, 207, 142, 0.35);
            border-radius: 10px;
            padding: 0 8px;
            font-size: 9px;
            font-weight: 700;
        """)
        actions_layout.addWidget(self.move_badge)

        self.btn_rename = self._action_btn("Editar", "Renomear")
        self.btn_rename.clicked.connect(self.start_edit)
        self.btn_remove = self._action_btn("Remover", "Remover")
        self.btn_remove.setStyleSheet(
            self.btn_remove.styleSheet()
            + f"QPushButton:hover {{ color: {DANGER}; border-color: {DANGER}; }}"
        )
        self.btn_remove.clicked.connect(lambda: self.remove_requested.emit(self.index))

        actions_layout.addWidget(self.btn_rename)
        actions_layout.addWidget(self.btn_remove)
        root.addWidget(actions_box)

        self._apply_state(selected=False)

    def _action_btn(self, text: str, tip: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setFixedSize(88, 30)
        btn.setToolTip(tip)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: 1px solid {BORDER};
                border-radius: 5px;
                color: {TEXT2};
                font-size: 11px;
            }}
            QPushButton:hover {{
                background: {SURFACE3};
                border-color: {BORDER2};
                color: {TEXT};
            }}
        """)
        return btn

    def start_edit(self):
        self._editing = True
        self.name_label.setVisible(False)
        self.name_edit.setVisible(True)
        self.name_edit.setText(self.pdf_item.label)
        self.name_edit.selectAll()
        self.name_edit.setFocus()

    def _finish_edit(self):
        if not self._editing:
            return
        self._editing = False
        new_name = self.name_edit.text().strip()
        if new_name:
            self.pdf_item.label = new_name
            self.name_label.setText(new_name)
        self.name_edit.setVisible(False)
        self.name_label.setVisible(True)

    def set_index(self, idx: int):
        self.index = idx
        self.num_label.setText(f"{idx + 1:02d}")

    def set_selected(self, selected: bool):
        self._apply_state(selected)

    def _apply_state(self, selected: bool):
        if selected:
            background = ACCENT_DIM
            left_border = f"border-left: 3px solid {ACCENT};"
        elif self.moved:
            background = SURFACE4
            left_border = f"border-left: 3px solid {SUCCESS};"
        else:
            background = ROW_ODD if self.alternate else ROW_EVEN
            left_border = "border-left: 3px solid transparent;"

        hover = SURFACE3 if not selected else ACCENT_DIM
        self.setStyleSheet(f"""
            PdfRowWidget {{
                background: {background};
                border-top: none;
                border-bottom: none;
                {left_border}
            }}
            PdfRowWidget:hover {{
                background: {hover};
            }}
            PdfRowWidget > QWidget {{
                background: transparent;
            }}
        """)


class PdfListWidget(QWidget):
    """Lista completa com sinais para o app."""

    selection_changed = pyqtSignal(object)
    list_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.items: list[PdfItem] = []
        self._selected_index: int = -1
        self._moved_index: int = -1
        self._row_widgets: list[PdfRowWidget] = []
        self._move_clear_timer = QTimer(self)
        self._move_clear_timer.setSingleShot(True)
        self._move_clear_timer.timeout.connect(self._clear_move_highlight)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        topbar = QWidget()
        topbar.setFixedHeight(42)
        topbar.setStyleSheet(f"background: {SURFACE}; border-bottom: 1px solid {BORDER};")
        tl = QHBoxLayout(topbar)
        tl.setContentsMargins(12, 0, 8, 0)

        self.count_label = QLabel("0 documentos")
        self.count_label.setStyleSheet(f"color: {TEXT2}; font-size: 12px; font-weight: 500;")
        tl.addWidget(self.count_label)
        tl.addStretch()

        btn_up = self._ctrl_btn("Subir", "Mover para cima")
        btn_up.clicked.connect(self._move_up)
        btn_dn = self._ctrl_btn("Descer", "Mover para baixo")
        btn_dn.clicked.connect(self._move_down)
        btn_top = self._ctrl_btn("Inicio", "Mover para o inicio")
        btn_top.clicked.connect(self._move_top)
        btn_bot = self._ctrl_btn("Final", "Mover para o final")
        btn_bot.clicked.connect(self._move_bottom)

        for btn in [btn_up, btn_dn, btn_top, btn_bot]:
            tl.addWidget(btn)

        layout.addWidget(topbar)

        header = QWidget()
        header.setFixedHeight(38)
        header.setStyleSheet(f"background: {SURFACE5}; border-bottom: none;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(0)

        marker = QLabel("")
        marker.setFixedWidth(56)
        hl.addWidget(marker)

        icon_header = QLabel("PDF")
        icon_header.setFixedWidth(52)
        icon_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_header.setStyleSheet(f"color: {TEXT2}; font-size: 11px; font-weight: 700;")
        hl.addWidget(icon_header)

        name_header = QLabel("Documento")
        name_header.setContentsMargins(12, 0, 12, 0)
        name_header.setStyleSheet(f"color: {TEXT2}; font-size: 11px; font-weight: 700;")
        hl.addWidget(name_header, stretch=1)

        action_header = QLabel("Acoes")
        action_header.setFixedWidth(238)
        action_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        action_header.setStyleSheet(f"color: {TEXT2}; font-size: 11px; font-weight: 700;")
        hl.addWidget(action_header)

        layout.addWidget(header)

        self.stack = QWidget()
        self.stack_layout = QVBoxLayout(self.stack)
        self.stack_layout.setContentsMargins(0, 0, 0, 0)
        self.stack_layout.setSpacing(0)

        self.drop_zone = self._make_drop_zone()
        self.stack_layout.addWidget(self.drop_zone)

        from PyQt6.QtWidgets import QScrollArea

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setVisible(False)
        self.scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background: {SURFACE}; }}
            QScrollBar:vertical {{
                background: {SURFACE2}; width: 6px; margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background: {BORDER2}; border-radius: 3px; min-height: 30px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
        """)

        self.list_container = QWidget()
        self.list_container.setStyleSheet(f"background: {SURFACE5};")
        self.list_inner = QVBoxLayout(self.list_container)
        self.list_inner.setContentsMargins(0, 0, 0, 0)
        self.list_inner.setSpacing(0)
        self.list_inner.addStretch()

        self.scroll.setWidget(self.list_container)
        self.stack_layout.addWidget(self.scroll)
        layout.addWidget(self.stack, stretch=1)

        self.setAcceptDrops(True)

    def _make_drop_zone(self) -> QWidget:
        zone = QFrame()
        zone.setStyleSheet(f"""
            QFrame {{
                background: {SURFACE};
                border: 2px dashed {BORDER2};
                border-radius: 12px;
                margin: 24px;
            }}
        """)
        vl = QVBoxLayout(zone)
        vl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vl.setSpacing(8)

        title = QLabel("Arraste PDFs aqui")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {TEXT}; font-size: 15px; font-weight: 600; border: none;")

        sub = QLabel("ou use o botao Adicionar acima")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet(f"color: {TEXT3}; font-size: 12px; border: none;")

        vl.addWidget(title)
        vl.addWidget(sub)
        return zone

    def _ctrl_btn(self, text: str, tip: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setFixedSize(58, 26)
        btn.setToolTip(tip)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: 1px solid {BORDER};
                border-radius: 4px;
                color: {TEXT2};
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: {SURFACE3};
                color: {TEXT};
                border-color: {BORDER2};
            }}
        """)
        return btn

    def add_items(self, new_items: list[PdfItem]):
        existing = {i.path for i in self.items}
        added = [i for i in new_items if i.path not in existing]
        self.items.extend(added)
        self._rebuild()
        self.list_changed.emit()

    def remove_item(self, index: int):
        if 0 <= index < len(self.items):
            was_selected = self._selected_index == index
            self.items.pop(index)
            if was_selected:
                self._selected_index = -1
                self.selection_changed.emit(None)
            self._moved_index = -1
            self._rebuild()
            self.list_changed.emit()

    def clear_all(self):
        self.items.clear()
        self._selected_index = -1
        self._moved_index = -1
        self.selection_changed.emit(None)
        self._rebuild()
        self.list_changed.emit()

    def get_paths(self) -> list[str]:
        return [i.path for i in self.items]

    def _move_up(self):
        i = self._selected_index
        if i > 0:
            self.items[i], self.items[i - 1] = self.items[i - 1], self.items[i]
            self._selected_index = i - 1
            self._mark_moved(self._selected_index)
            self._rebuild()
            self.list_changed.emit()

    def _move_down(self):
        i = self._selected_index
        if 0 <= i < len(self.items) - 1:
            self.items[i], self.items[i + 1] = self.items[i + 1], self.items[i]
            self._selected_index = i + 1
            self._mark_moved(self._selected_index)
            self._rebuild()
            self.list_changed.emit()

    def _move_top(self):
        i = self._selected_index
        if i > 0:
            self.items.insert(0, self.items.pop(i))
            self._selected_index = 0
            self._mark_moved(self._selected_index)
            self._rebuild()
            self.list_changed.emit()

    def _move_bottom(self):
        i = self._selected_index
        if 0 <= i < len(self.items) - 1:
            self.items.append(self.items.pop(i))
            self._selected_index = len(self.items) - 1
            self._mark_moved(self._selected_index)
            self._rebuild()
            self.list_changed.emit()

    def _mark_moved(self, index: int):
        self._moved_index = index
        self._move_clear_timer.start(1200)

    def _clear_move_highlight(self):
        self._moved_index = -1
        for idx, row in enumerate(self._row_widgets):
            row.moved = False
            row.alternate = idx % 2 == 1
            row.set_selected(idx == self._selected_index)

    def _rebuild(self):
        for w in self._row_widgets:
            self.list_inner.removeWidget(w)
            w.deleteLater()
        self._row_widgets.clear()

        empty = len(self.items) == 0
        self.drop_zone.setVisible(empty)
        self.scroll.setVisible(not empty)

        self.count_label.setText(
            f"{len(self.items)} documento{'s' if len(self.items) != 1 else ''}"
        )

        for idx, item in enumerate(self.items):
            row = PdfRowWidget(
                item=item,
                index=idx,
                alternate=(idx % 2 == 1),
                moved=(idx == self._moved_index),
            )
            row.remove_requested.connect(self.remove_item)
            row.mousePressEvent = lambda e, i=idx: self._select(i)
            self.list_inner.insertWidget(self.list_inner.count() - 1, row)
            self._row_widgets.append(row)

        for idx, row in enumerate(self._row_widgets):
            row.set_selected(idx == self._selected_index)

    def _select(self, index: int):
        self._selected_index = index
        for idx, row in enumerate(self._row_widgets):
            row.set_selected(idx == index)
        self.selection_changed.emit(self.items[index] if 0 <= index < len(self.items) else None)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        from core.pdf_engine import get_file_size_str, get_page_count

        paths = [
            u.toLocalFile()
            for u in event.mimeData().urls()
            if u.toLocalFile().lower().endswith(".pdf")
        ]
        if paths:
            new_items = []
            for p in paths:
                item = PdfItem(path=p)
                item.page_count = get_page_count(p)
                item.file_size = get_file_size_str(p)
                new_items.append(item)
            self.add_items(new_items)
