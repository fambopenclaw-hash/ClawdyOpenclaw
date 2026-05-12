---
name: create-markdown
description: Extract detailed analysis from PDF files and generate comprehensive reports in Markdown format, saved to Obsidian vault and Google Drive, with a clickable link back to the original file embedded in the note. Triggers when user provides a PDF and asks to analyze it, create a report, or convert it to markdown. Handles both text-based and image-based (scanned) PDFs.
---

# Create Markdown from PDF

Extract content from a PDF → generate a structured Markdown report → save to Obsidian vault → upload PDF to Google Drive → embed a clickable Gdrive link in the note as a source reference.

## Config

| Item | Value |
|------|-------|
| Obsidian vault | `/home/fahmibakeri/famb vault` |
| Gdrive base folder | `03 RESOURCE OPENCLAW` |
| Upload method | rclone CLI (`/home/fahmibakeri/bin/rclone`) |

## Workflow

```
PDF in inbound folder
  → Extract text (pdfplumber or PyMuPDF + Tesseract OCR)
  → Analyze content — infer title, tags, structure
  → Generate structured Markdown report
  → Save .md to Obsidian vault
  → Upload PDF to Gdrive "03 RESOURCE OPENCLAW/<topic>/"
  → Get Gdrive share link
  → Append source link to the Obsidian note
```

## Step-by-Step

### 1. Locate the PDF
Check `/home/fahmibakeri/.openclaw/media/inbound/` for the most recent PDF file (sorted by modification time).

### 2. Extract Text
Run `python3 scripts/extract_pdf.py <pdf_path>` to extract text. Falls back to OCR (Tesseract) for scanned/image-based PDFs.

**What it does:**
1. Tries `pdfplumber` (fast, text-layer aware) — if text is found, returns it
2. Falls back to **PyMuPDF** (`get_pixmap`) to render PDF pages as images, then runs **Tesseract OCR** via `pytesseract` (for scanned/image PDFs)
3. Wraps each page in `--- Page N ---` separators for structure

> **Note:** The script auto-detects `.venv` alongside the skill folder. If not found, it falls back to the current interpreter.

### 3. Analyze Content
Identify:
- **Document type** (paper, report, book, form, etc.)
- **Title** — extracted from the PDF or inferred from filename/content
- **Tags** — 3-5 relevant lowercase tags (e.g. `pdf`, `analysis`, `research`)
- **Key sections** — breakdown of major headings and content areas
- **Key takeaways** — 3-5 bullet points of the most important points
- **Raw excerpts** — 2-3 notable quotes or passages

### 4. Generate Markdown Report

```markdown
---
title: <Document Title>
source: <original_filename.pdf>
date: <YYYY-MM-DD>
tags: [pdf, analysis, <category>]
gdrive_link: <link>
---

# <Document Title>

## Overview
<1-2 paragraph summary of the document>

## Key Sections

### <Section 1>
<Detailed notes on this section>

### <Section 2>
<Detailed notes on this section>

## Key Takeaways
- <Bullet point 1>
- <Bullet point 2>
- <Bullet point 3>

## Raw Excerpts
> <Noteworthy quote or excerpt 1>

> <Noteworthy quote or excerpt 2>

---

## Source

[📄 View original PDF on Google Drive](<gdrive_link>)
```

### 5. Save to Obsidian Vault
- **Vault path:** `\\wsl.localhost\Ubuntu\home\fahmibakeri\famb vault`
- **Filename:** slugified title + `.md`
- **Images:** copy extracted images to vault root if any; embed top 6 by file size under `## Key Figures` with captions
- Prepend to vault index if applicable
- If file already exists → append timestamp to filename

### 6. Upload PDF to Google Drive (rclone)

**Base folder:** `03 RESOURCE OPENCLAW`

1. Ensure base folder exists:
   ```bash
   rclone mkdir "gdrive:03 RESOURCE OPENCLAW"
   ```
2. **Topic subfolder:** List existing subfolders and match by filename/topic similarity (Levenshtein ≤ 2 or same first word); reuse existing or create new:
   ```bash
   rclone lsf "gdrive:03 RESOURCE OPENCLAW/" --directories
   rclone mkdir "gdrive:03 RESOURCE OPENCLAW/<topic>"
   ```
3. Upload PDF:
   ```bash
   rclone copy "<pdf_path>" "gdrive:03 RESOURCE OPENCLAW/<topic>/"
   ```

### 7. Get Share Link & Finalize Note
1. Get share link:
   ```bash
   rclone link "gdrive:03 RESOURCE OPENCLAW/<topic>/<filename>.pdf"
   ```
2. Update the Obsidian `.md` file:
   - Set `gdrive_link:` in YAML frontmatter to the returned link
   - Replace the `## Source` placeholder section with the real link
3. If link retrieval fails → use `⚠️ Gdrive link pending — add manually`

### 8. Cleanup
Remove `<pdf_path>.txt` and any temp directories after processing.

## Setup (One-Time)

Before first use, install Python dependencies:

```bash
cd ~/.openclaw/workspace/skills/create-markdown
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python pdfplumber pillow pytesseract pymupdf
```

> **Note:** `pymupdf` is already installed alongside `pdfplumber` in the current venv.

## Error Handling
- **Text extraction empty** → warn user, still create note with `summary = "[Extraction failed — review PDF manually]"`
- **Gdrive upload fails** → create .md without link, alert user to upload manually
- **Link retrieval fails** → use `⚠️ Gdrive link pending — add manually` as placeholder
- **File already exists in vault** → append timestamp to filename

## Scripts

### extract_pdf.py

Extracts text from a PDF file. Uses `pdfplumber` for text-based PDFs; falls back to **PyMuPDF + Tesseract OCR** for image-based PDFs.

```bash
source .venv/bin/activate
python3 scripts/extract_pdf.py <path_to_pdf>
```

**Why PyMuPDF instead of pdf2image:** PyMuPDF has zero external binary dependencies (no poppler needed), making it the reliable choice across WSL, Windows, and macOS without extra system-level installs.

**Output:** Plain text to stdout; errors and diagnostics to stderr.
