#!/usr/bin/env python3
"""
pdf-extract-assets.py
Extracts text AND images from a PDF for the pdf-to-obsidian workflow.
Usage: python3 pdf-extract-assets.py <pdf_path> <output_dir>
"""

import sys
import os
import shutil

def install_deps():
    import subprocess
    result = subprocess.run(
        ['uv', 'venv', '/tmp/pdf-venv', '--python', '3.12'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"uv venv failed:\n{result.stderr}")
    result = subprocess.run(
        ['uv', 'pip', 'install', '--python', '/tmp/pdf-venv/bin/python', 'pymupdf', 'pdfplumber'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"uv pip install failed:\n{result.stderr}")

def extract(pdf_path: str, output_dir: str) -> dict:
    venv_python = '/tmp/pdf-venv/bin/python'
    if not os.path.exists(venv_python):
        install_deps()

    import subprocess, json

    script = f"""
import fitz
import os
import json

pdf_path = {repr(pdf_path)}
output_dir = {repr(output_dir)}
os.makedirs(output_dir, exist_ok=True)

doc = fitz.open(pdf_path)
results = {{"text": "", "images": [], "page_count": len(doc)}}

# Extract text
text_parts = []
for i, page in enumerate(doc, 1):
    t = page.get_text()
    text_parts.append(t if t else f"[Page {{i}} — no text]")

results["text"] = "\\n\\n".join(text_parts)

# Extract images (filter out tiny artifacts and oversized background renders)
img_count = 0
MIN_SIZE = 5_000   # bytes — discard anything smaller (logo/icon noise)
MAX_SIZE = 4_000_000  # bytes — discard anything suspiciously large (full-page renders)
for i, page in enumerate(doc, 1):
    for img_index, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        base_image = doc.extract_image(xref)
        img_bytes = base_image["image"]
        img_ext = base_image["ext"]
        # Skip if size suggests artifact or full-page background render
        if len(img_bytes) < MIN_SIZE or len(img_bytes) > MAX_SIZE:
            continue
        img_filename = f"page{{i}}_img{{img_index+1}}.{{img_ext}}"
        img_path = os.path.join(output_dir, img_filename)
        with open(img_path, "wb") as f:
            f.write(img_bytes)
        results["images"].append({{"filename": img_filename, "page": i}})
        img_count += 1

results["images_filtered"] = f"kept {{img_count}} of {{len(results['images'])}} raw, top 6 selected for vault"

print(json.dumps(results))
"""
    result = subprocess.run(
        [venv_python, '-c', script],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"pymupdf extraction failed:\n{result.stderr}")
    return json.loads(result.stdout)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 pdf-extract-assets.py <pdf_path> <output_dir>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(pdf_path):
        print(f"[!] File not found: {pdf_path}")
        sys.exit(1)

    print(f"[*] Extracting text and images from {pdf_path}...")
    results = extract(pdf_path, output_dir)

    print(f"[*] Extracted {len(results['text']):,} characters of text.")
    print(f"[*] Found {len(results['images'])} images.")
    print(f"[*] Images saved to: {output_dir}")
    print(f"[*] Done.")
