# Axiel PDF

Axiel PDF is a local desktop application for combining PDF files.

The current implementation is written in Python with PyQt6. Selected files stay on the user's machine; the app does not send documents to external services.

## Status

Current app version: `1.0.2`.

AI and OCR entries are present in the interface as planned capabilities. They do not call external APIs or process documents yet.

## Current Features

- Add PDFs through a file picker.
- Add PDFs by external drag and drop.
- Reorder documents with buttons.
- Rename the label shown in the list.
- Remove documents from the list.
- Preview the first page of a selected PDF.
- Open an enlarged preview with zoom.
- Merge PDFs with progress feedback.

## Planned Capabilities

- OCR text extraction.
- AI-assisted organization and renaming.
- Duplicate and blank-page detection.
- Document intelligence workflows.

See `ROADMAP.md` for the broader project direction.

## Requirements

- Python 3.11 or newer.
- Dependencies listed in `requirements.txt`.

## Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
python main.py
```

## Build

`build.sh` uses PyInstaller to create a desktop executable:

```bash
./build.sh
```

The executable is created in `dist/`.

## Project Structure

```text
app/           bootstrap, paths, configuration and version
core/          PDF reading, preview and merge logic
ui/            PyQt6 interface
ui/components/ reusable UI components
modules/       manifests for current and planned capabilities
integrations/  planned provider registry
assets/        images and icons
```

## Privacy

Axiel PDF works with local files. Before publishing logs, screenshots or examples, check that they do not contain personal data, document content or private file paths.

## License

This project is licensed under the GNU General Public License v3.0. See `LICENSE` for the full terms.

## About Axiel

Axiel is an open source ecosystem for AI, automation, bots, document workflows and developer tools.

Main profile: [axielhq](https://github.com/axielhq)
