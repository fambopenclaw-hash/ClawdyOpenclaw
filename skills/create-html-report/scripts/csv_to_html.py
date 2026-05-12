#!/usr/bin/env python3
"""
csv_to_html.py — Read a CSV file and output structured JSON.
Usage: python3 csv_to_html.py <file.csv>
"""
import json, sys, csv

with open(sys.argv[1], newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = [dict(row) for row in reader]

print(json.dumps({"num_rows": len(rows), "headers": list(rows[0].keys()) if rows else [], "rows": rows}, indent=2, default=str))