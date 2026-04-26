"""Resolucao centralizada de caminhos locais e empacotados."""
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def runtime_root() -> Path:
    return Path(getattr(sys, "_MEIPASS", PROJECT_ROOT))


def resource_path(relative_path: str) -> str:
    return str(runtime_root() / relative_path)


def project_path(relative_path: str = "") -> Path:
    return PROJECT_ROOT / relative_path
