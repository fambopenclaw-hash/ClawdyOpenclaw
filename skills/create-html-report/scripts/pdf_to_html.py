#!/usr/bin/env python3
"""
pdf_to_html.py — Read a PDF file and dump structured data as JSON.
Usage: python3 pdf_to_html.py <file.pdf>
"""
import json, sys
try:
    import pdfplumber
except ImportError:
    print("ERROR: pdfplumber not installed. Run: uv pip install pdfplumber --python /tmp/pdfenv/bin/python3")
    sys.exit(1)

pages_data = []
with pdfplumber.open(sys.argv[1]) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text() or ""
        tables = page.extract_tables()
        pages_data.append({
            "page": i + 1,
            "text": text.strip(),
            "tables": [table for table in tables if table]
        })

result = {
    "num_pages": len(pages_data),
    "pages": pages_data
}

print(json.dumps(result, indent=2, default=str))