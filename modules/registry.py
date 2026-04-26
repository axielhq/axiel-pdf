"""Registro global dos modulos do produto."""
from modules.ai.manifest import AI_MODULE
from modules.merge.manifest import MERGE_MODULE
from modules.ocr.manifest import OCR_MODULE
from modules.settings.manifest import SETTINGS_MODULE


PRODUCT_MODULES = (
    MERGE_MODULE,
    SETTINGS_MODULE,
    AI_MODULE,
    OCR_MODULE,
)
