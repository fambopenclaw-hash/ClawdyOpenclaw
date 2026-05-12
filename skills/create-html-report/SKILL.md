---
name: create-html-report
description: Analyze a file (Excel .xlsx, PDF, CSV, or other structured document) and generate a comprehensive, self-contained HTML report. Use when the user provides any data file and asks to create an HTML report, dashboard, infographic, or web view from it. Covers: Daily Move Reports (DMR), well dashboards, operational reports, PDF documents, CSV data, and any structured data. Triggers on phrases like "generate HTML from file", "create report from spreadsheet", "convert PDF to HTML dashboard", "convert csv to html", "analyze and report on this file".
---

# create-html-report

Convert an Excel (.xlsx), PDF, CSV, or other structured file into a professional, self-contained HTML report and publish it to GitHub Pages.

## Workflow

### Step 0 — Detect Input Type

Inspect the file extension to determine the extraction approach:

| Extension | Library | Notes |
|-----------|---------|-------|
| `.xlsx` | `openpyxl` | Use `data_only=True` for computed values |
| `.pdf` | `pdfplumber` | Text + tables; fallback OCR for scanned pages |
| `.csv` | built-in `csv` | Parse directly |
| `.pptx` | `python-pptx` | Extract slides, shapes, text, and tables |
| `.docx` | `python-docx` | Extract paragraphs, tables, headings, and text |
| Others | `pdfplumber` or `openpyxl` | Try openpyxl first for unknown formats |

### Step 1 — Extract Data

#### Excel (.xlsx)
```bash
uv venv /tmp/reportenv -q
uv pip install openpyxl pdfplumber --python /tmp/reportenv/bin/python3 -q
/tmp/reportenv/bin/python3 -c "
import openpyxl
wb = openpyxl.load_workbook('path/to/file.xlsx', data_only=True)
..."
```

#### PDF
```bash
/tmp/reportenv/bin/python3 -c "
import pdfplumber
with pdfplumber.open('path/to/file.pdf') as pdf:
    for page in pdf.pages:
        print(page.extract_text())
        print(page.extract_tables())
"
```

#### CSV
```bash
/tmp/reportenv/bin/python3 -c "
import csv, json
with open('path/to/file.csv') as f:
    reader = csv.DictReader(f)
    print(json.dumps([dict(row) for row in reader], indent=2))
"
```

#### PowerPoint (.pptx)
```bash
/tmp/reportenv/bin/python3 -c "
from pptx import Presentation
from pptx.util import Inches, Pt
prs = Presentation('path/to/file.pptx')
for i, slide in enumerate(prs.slides):
    print(f'=== Slide {i+1} ===')
    for shape in slide.shapes:
        if hasattr(shape, 'text'):
            print(shape.text)
        if shape.has_table:
            for row in shape.table.rows:
                print([cell.text for cell in row.cells])
"
```

#### Word (.docx)
```bash
/tmp/reportenv/bin/python3 -c "
from docx import Document
doc = Document('path/to/file.docx')
for para in doc.paragraphs:
    print(para.text)
for table in doc.tables:
    for row in table.rows:
        print([cell.text for cell in row.cells])
"
```

If both libraries are already available, skip the venv step.

### Step 2 — Understand the Structure

Read all content and identify:
- **Source type** — sheet names (xlsx), page count (pdf), column headers (csv)
- **Header rows** — field names (often row 1 or row 2)
- **Data layout** — merged cells, sections, column-spanning
- **Key values** — numbers, dates, metrics that deserve highlight cards
- **Section breaks** — logical groupings of content

### Step 3 — Generate the HTML

Build a self-contained HTML file using a professional report layout:
- Dark navy header with document title and source type badge
- Key metrics as stat cards (color-coded: blue/green/amber/red)
- Sections clearly delineated with bold headers and bordered tables
- All styles inline in a `<style>` block (no external dependencies)
- Responsive design (works on mobile)
- Font: Segoe UI / Calibri / sans-serif fallback

The HTML should be comprehensive — include ALL non-empty data, organized logically by section.

**Every generated HTML page MUST include a "Back to Index" backlink** in the footer section pointing to `index.html` (same directory level on GitHub Pages). Use a clean, minimal link styled consistently with the page. This is non-negotiable.

**Output path:** save as `~/.openclaw/workspace/skills/create-html-report/output/<descriptive-name>.html`

**Template selection:**
- For DMR-style reports: use `references/dmr-template.html`
- For PowerPoint conversions: use `references/slides-template.html` (slide-by-slide layout)
- For Word documents: use `references/doc-template.html` (document-style with headings)
- For general documents (PDF, CSV, mixed): use `references/generic-template.html`
- Fill in the template dynamically with extracted data.

### Step 4 — Push to GitHub Pages

1. Clone the repo:
   ```bash
   gh repo clone fahmiamni/github.io /tmp/gh-pages
   ```
2. Copy the HTML file into the repo:
   ```bash
   cp ~/.openclaw/workspace/skills/create-html-report/output/<file>.html /tmp/gh-pages/<file>.html
   ```
3. Commit and push:
   ```bash
   cd /tmp/gh-pages
   git config user.email "clawdius@openclaw.ai"
   git config user.name "Clawdius"
   git config credential.helper "!gh auth git-credential"
   git add <file>.html
   git commit -m "Add report: <title> $(date)"
   git push origin main
   ```
   If auth fails, fall back to `gh repo clone` + file copy + `gh api` to push.
4. Verify push was accepted.

### Step 5 — Add Back to Index Link

In every generated HTML file, add a back-to-index link **at the TOP of the page** inside the header area:

```html
<div style="margin-bottom:10px">
  <a href="index.html" style="color:#fff;font-size:12px;font-weight:700;text-decoration:none;background:var(--blue);padding:5px 12px;border-radius:6px;">← Back to Index</a>
</div>
```

Place this directly after the opening `<div class="header">` tag, before the `.header-top` div.

### Step 6 — Update index.html

1. Read `/tmp/gh-pages/index.html`
2. Add a new card link for the new HTML file BEFORE the closing `</div>` of `.card-grid`:
   ```html
   <a class="card" href=".html">
     <div class="card-title"><REPORT TITLE></div>
     <div class="card-desc"><SHORT DESCRIPTION></div>
     <div class="card-tag">Report</div>
   </a>
   ```
   Use `accent-green` for financial/cost reports, `accent-amber` for warnings, `accent-red` for critical items.
3. Commit and push the updated `index.html`.

## Key Reference Files

- `references/dmr-template.html` — Full HTML boilerplate for DMR-style spreadsheet reports
- `references/generic-template.html` — Full HTML boilerplate for general documents, PDFs, and CSV data
- `references/slides-template.html` — Full HTML boilerplate for PowerPoint slide decks
- `references/doc-template.html` — Full HTML boilerplate for Word documents
- `scripts/excel_to_html.py` — Python script that reads an xlsx file and extracts structured JSON
- `scripts/pdf_to_html.py` — Python script that reads a PDF file and extracts text + tables as JSON
- `scripts/csv_to_html.py` — Python script that reads a CSV file and outputs structured JSON
- `scripts/pptx_to_html.py` — Python script that reads a .pptx file and extracts slide content as JSON
- `scripts/docx_to_html.py` — Python script that reads a .docx file and extracts paragraphs and tables as JSON

## GitHub Pages Repo

**Repo:** `fahmiamni/github.io`
**Live URL base:** `https://fahmiamni.github.io/`
**HTML file URL:** `https://fahmiamni.github.io/<file>.html`

## Important Notes

- For Excel, always use `data_only=True` to get computed cell values instead of formulas.
- For PDF, use `pdfplumber` for text/table extraction; fall back to `PyPDF2` or `pytesseract` (OCR) for scanned/image PDFs.
- For CSV, use Python's built-in `csv.DictReader` — no extra library needed.
- For PowerPoint (.pptx), use `python-pptx` — extract slide titles, body text, and tables.
- For Word (.docx), use `python-docx` — extract headings, paragraphs, lists, and tables.
- For datetime values, format as `YYYY-MM-DD` or `DD MMM YYYY` for readability.
- The HTML file must be fully self-contained — no external CSS/JS links that could break.
- Commit messages should be descriptive: include the report name and date.
- When multiple input types are present in a single file (e.g., a PDF with embedded tables), treat as PDF and extract everything.