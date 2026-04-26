# Changelog

All important changes to Axiel PDF are documented in this file.

## [Unreleased]

### Planned

- OCR text extraction.
- AI-assisted file organization and renaming.
- Duplicate PDF detection.
- Text validation and document intelligence workflows.
- Automated tests.

## [1.0.2] - 2026-04-26

### Changed

- Set the public application version to `1.0.2`.
- Added the current PyQt6 desktop application source.
- Added the startup dialog, about dialog and institutional footer.
- Added the local Axiel PDF logo and provider icons.
- Added GPLv3 license, project README and Git ignore rules.

## Local Implementation History

The entries below document the local desktop application work that preceded the first public source push.

### Version 2.8 - Institutional Footer

- Added copyright and GPLv3 text to the main window footer.

### Version 2.7 - Startup Screen

- Added a startup dialog shown when opening the application.
- Added the Axiel PDF logo as a local asset.
- Added an `Entrar` button before the main window is shown.

### Version 2.6 - About Dialog

- Added a `Sobre` button to the top bar.
- Added product description, Axiel attribution, GPLv3 notice, version and GitHub link.

### Version 2.5 - Zebra List Cleanup

- Removed boxed backgrounds around document names and metadata.
- Kept row-level zebra backgrounds.

### Version 2.4 - Zebra List Without Grid Lines

- Removed vertical and horizontal grid lines from the PDF list.
- Kept alternating row colors, selection and move highlight states.

### Version 2.3 - Rebuilt List Layout

- Rebuilt the PDF row layout with fixed columns.
- Aligned document information and actions.
- Applied continuous zebra row styling.

### Version 2.2 - List Color Application

- Corrected row background application.
- Improved contrast between alternating rows.

### Version 2.1 - Continuous Grid List

- Adjusted the list to a continuous horizontal row layout.
- Removed card-like spacing between documents.

### Version 2.0 - Horizontal Separation

- Improved visual separation between PDF rows.
- Preserved selection and move highlights.

### Version 1.9 - Light Grid List

- Added a visual column header.
- Applied linear alternating rows.

### Version 1.8 - More Readable Document List

- Added a PDF icon to each row.
- Added a temporary moved-state highlight.

### Version 1.7 - Enlarged Preview

- Added enlarged preview dialog.
- Added scroll and zoom controls.

### Version 1.6 - Modular Foundation

- Added `app/`, `modules/`, `integrations/` and `ui/components/`.
- Centralized asset path resolution.
- Moved product identity and version metadata to `app.version`.
- Prepared environment-based provider credential reads.

### Version 1.5 - Planned AI and OCR Providers

- Added planned AI and OCR capability manifests.
- Added provider icons and environment variable names.
- Added disabled/planned UI entries for AI and OCR.

### Version 1.4 - Add PDF Button Icon

- Added the PDF icon to the `Adicionar PDFs` button.

### Version 1.3 - PDF Visual Identity

- Added `assets/pdf_badge.svg`.
- Updated the application identity assets.
- Updated build asset packaging.

### Version 1.2 - Cleaner Interface

- Removed decorative icons from several UI areas.
- Simplified action button labels.

### Version 1.1 - Axiel PDF Identity

- Set the product name to `Axiel PDF`.
- Updated the application title, organization and default combined PDF filename.

### Version 1.0 - Audited Base

- Desktop PyQt6 app for merging PDFs.
- PDF add, remove, visual rename and button-based ordering.
- First-page preview.
- Page count and file size display.
- Merge through `pikepdf` in a worker thread.
- Progress bar during merge.
