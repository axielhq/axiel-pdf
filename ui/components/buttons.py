"""Fabrica de botoes padronizados da interface."""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton


def build_top_button(text: str, primary: bool, palette: dict[str, str]) -> QPushButton:
    btn = QPushButton(text)
    btn.setFixedHeight(34)
    btn.setMinimumWidth(110)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)

    if primary:
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {palette["accent"]}; color: white;
                border: none; border-radius: 7px;
                padding: 0 16px; font-size: 13px; font-weight: 600;
            }}
            QPushButton:hover {{ background: #6a6cee; }}
            QPushButton:disabled {{ background: #2a2a3a; color: {palette["text3"]}; }}
        """)
    else:
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {palette["surface2"]}; color: {palette["text2"]};
                border: 1px solid {palette["border2"]}; border-radius: 7px;
                padding: 0 14px; font-size: 13px;
            }}
            QPushButton:hover {{ color: {palette["text"]}; border-color: {palette["accent"]}; }}
        """)

    return btn
