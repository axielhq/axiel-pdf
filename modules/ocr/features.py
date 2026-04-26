"""Funcionalidade futura de OCR."""
from modules.features import FutureFeature


OCR_CAPABILITIES = (
    "Extrair texto de imagens em PDFs digitalizados",
    "Identificar dados estruturados a partir do texto extraido",
    "Disponibilizar o texto extraido para as futuras rotinas de IA",
)


OCR_FEATURE = FutureFeature(
    key="ocr",
    name="OCR",
    icon_path="assets/providers/ocr.svg",
    capabilities=OCR_CAPABILITIES,
)
