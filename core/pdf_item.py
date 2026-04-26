"""Modelo de dado para PDFs carregados na lista."""
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PdfItem:
    path: str
    label: str = ""
    page_count: int = 0
    file_size: str = ""

    def __post_init__(self):
        if not self.label:
            self.label = Path(self.path).stem

    @property
    def filename(self) -> str:
        return Path(self.path).name

    @property
    def display_name(self) -> str:
        return self.label
