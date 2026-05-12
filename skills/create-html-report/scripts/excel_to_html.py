#!/usr/bin/env python3
"""
excel_to_html.py — Read an xlsx file and dump structured data as JSON.
Usage: python3 excel_to_html.py <file.xlsx> [--sheet NAME]
"""
import json, sys, datetime
try:
    import openpyxl
except ImportError:
    print("ERROR: openpyxl not installed. Run: uv pip install openpyxl --python /tmp/excelenv/bin/python3")
    sys.exit(1)

def col_letter(n):
    s = ""
    while n >= 0:
        s = chr(65 + n % 26) + s
        n = n // 26 - 1
    return s

def fmt(v):
    if v is None:
        return ""
    if isinstance(v, datetime.datetime):
        return v.strftime("%d %b %Y")
    if isinstance(v, datetime.time):
        return v.strftime("%H:%M")
    if isinstance(v, float):
        if v == int(v):
            return str(int(v))
        return f"{v:.2f}"
    return str(v)

wb = openpyxl.load_workbook(sys.argv[1], data_only=True)

sheet_name = None
if "--sheet" in sys.argv:
    idx = sys.argv.index("--sheet")
    sheet_name = sys.argv[idx+1]
    ws = wb[sheet_name]
else:
    ws = wb.active

print(f"Sheet: {ws.title}", file=sys.stderr)
print(f"Dimensions: {ws.dimensions}", file=sys.stderr)

rows = []
for i, row in enumerate(ws.iter_rows(values_only=True)):
    non_none = {j: fmt(v) for j, v in enumerate(row) if v is not None}
    if non_none:
        rows.append({"row": i+1, "cols": non_none})

print(json.dumps({"sheet": ws.title, "rows": rows}, indent=2, default=str))