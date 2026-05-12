#!/usr/bin/env python3
"""
pdf-to-obsidian.py
Extracts text from a PDF and caches it to <pdf_path>.txt for agent consumption.
Usage: python3 pdf-to-obsidian.py <pdf_path>
"""

import sys
import os

def run(cmd):
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{result.stderr}")
    return result.stdout.strip()

def install_deps():
    import subprocess
    result = subprocess.run(
        ['uv', 'venv', '/tmp/pdf-venv', '--python', '3.12'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"uv venv failed:\n{result.stderr}")
    result = subprocess.run(
        ['uv', 'pip', 'install', '--python', '/tmp/pdf-venv/bin/python', 'pdfplumber'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"uv pip install failed:\n{result.stderr}")

def extract_text_from_pdf(pdf_path: str) -> str:
    venv_python = '/tmp/pdf-venv/bin/python'
    if not os.path.exists(venv_python):
        install_deps()
    import subprocess
    result = subprocess.run(
        [venv_python, '-c', f"""
import pdfplumber
text_parts = []
with pdfplumber.open('{pdf_path}') as pdf:
    for i, page in enumerate(pdf.pages, 1):
        t = page.extract_text()
        text_parts.append(t if t else f'[Page {{i}} — no text extracted]')
print('\\n\\n'.join(text_parts))
"""],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"pdfplumber extraction failed:\n{result.stderr}")
    return result.stdout

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 pdf-to-obsidian.py <pdf_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    if not os.path.exists(pdf_path):
        print(f"[!] File not found: {pdf_path}")
        sys.exit(1)

    print(f"[*] Extracting text from {pdf_path}...")
    text = extract_text_from_pdf(pdf_path)
    total_chars = len(text)

    if total_chars == 0:
        print("[!] Warning: No text extracted. PDF may be scanned/image-based.")
    else:
        print(f"[*] Extracted {total_chars:,} characters.")

    out_path = pdf_path + ".txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"[*] Text saved to: {out_path}")
    print("[*] Done.")
