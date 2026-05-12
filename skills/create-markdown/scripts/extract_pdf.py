#!/usr/bin/env python3
"""
extract_pdf.py — Extract text from PDF files.
Uses pdfplumber for text-based PDFs; falls back to PyMuPDF + Tesseract OCR for image-based PDFs.

Dependencies: pdfplumber, pillow, pytesseract, pymupdf
Install via: uv venv .venv && uv pip install --python .venv/bin/python pdfplumber pillow pytesseract pymupdf
"""

import sys
import os

# Detect Python environment — prefer uv venv over system Python
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHON = os.path.join(SCRIPT_DIR, "..", ".venv", "bin", "python")


def get_python():
    """Return the best available Python interpreter."""
    if os.path.exists(VENV_PYTHON):
        return VENV_PYTHON
    return sys.executable


PYTHON = get_python()


# ── PDFPlumber path ──────────────────────────────────────────────────────────

def extract_with_pdfplumber(pdf_path):
    import pdfplumber
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                text_parts.append(f"--- Page {i+1} ---\n{page_text}")
    return "\n\n".join(text_parts)


# ── PyMuPDF + Tesseract OCR path ─────────────────────────────────────────────

def extract_with_ocr(pdf_path):
    """
    Convert PDF pages to images using PyMuPDF (no external binaries needed),
    then run Tesseract OCR on each rendered image.
    """
    import pytesseract
    from PIL import Image
    import fitz  # PyMuPDF

    text_parts = []
    doc = fitz.open(pdf_path)

    for i, page in enumerate(doc):
        # Render page at 300 DPI equivalent (matrix=2.0 → ~144 DPI, 3.0 → ~216 DPI)
        mat = fitz.Matrix(2.5, 2.5)
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("png")
        from io import BytesIO
        img = Image.open(BytesIO(img_bytes))
        text = pytesseract.image_to_string(img)
        text_parts.append(f"--- Page {i+1} ---\n{text}")

    doc.close()
    return "\n\n".join(text_parts)


# ── Main dispatcher ──────────────────────────────────────────────────────────

def extract_pdf(pdf_path):
    """Main extraction function with fallback chain."""
    if not os.path.exists(pdf_path):
        print(f"ERROR: File not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    # Try pdfplumber first (works for text-based PDFs)
    try:
        text = extract_with_pdfplumber(pdf_path)
        if text and text.strip():
            return text
    except Exception as e:
        print(f"pdfplumber failed: {e}", file=sys.stderr)

    # Fall back to PyMuPDF + Tesseract OCR (for scanned/image-based PDFs)
    try:
        return extract_with_ocr(pdf_path)
    except Exception as e:
        print(f"OCR failed: {e}", file=sys.stderr)

    print("ERROR: No extraction method available. Install pdfplumber.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path_to_pdf>", file=sys.stderr)
        sys.exit(1)

    text = extract_pdf(sys.argv[1])
    print(text)