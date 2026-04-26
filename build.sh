#!/bin/bash
# build.sh - Gera executavel do Axiel PDF com PyInstaller
# Funciona em macOS, Linux e Windows (Git Bash / WSL)

set -e

echo "Instalando dependencias..."
pip install -r requirements.txt
pip install pyinstaller

echo "Gerando executavel..."
pyinstaller \
  --name "Axiel PDF" \
  --windowed \
  --onefile \
  --add-data "ui:ui" \
  --add-data "core:core" \
  --add-data "assets:assets" \
  --hidden-import PyQt6.QtCore \
  --hidden-import PyQt6.QtGui \
  --hidden-import PyQt6.QtWidgets \
  --hidden-import fitz \
  --hidden-import pikepdf \
  main.py

echo ""
echo "Executavel gerado em: dist/Axiel PDF"
echo ""
