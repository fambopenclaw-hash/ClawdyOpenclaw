#!/usr/bin/env python3
import sys
import os
import json
import subprocess

def main():
    api_key_path = os.path.expanduser('~/.config/notion/api_key')
    try:
        with open(api_key_path, 'r') as f:
            api_key = f.read().strip()
    except Exception as e:
        print("**Agenda Error:** Notion API key not found or unreadable.")
        sys.exit(1)

    today = "2026-03-25"
    three_days_later = "2026-03-28"

    json_data = {
        "filter": {
            "property": "Date",
            "date": {
                "on_or_after": today,
                "on_or_before": three_days_later
            }
        },
        "sorts": [
            {"property": "Date", "direction": "ascending"}
        ]
    }

    cmd = [
        "curl", "-s", "-f", "-X", "POST",
        "https://api.notion.com/v1/data_sources/31ce1fb7-4ad2-801d-a816-000b09abdd18/query",
        "-H", f"Authorization: Bearer {api_key}",
        "-H", "Notion-Version: 2025-09-03",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(json_data)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        response = result.stdout
    except subprocess.CalledProcessError as e:
        print("**Agenda Error:** Notion API request failed.")
        sys.exit(1)

    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        print("**Agenda Error:** Invalid response from Notion API.")
        sys.exit(1)

    entries = []
    for page in data.get('results', []):
        props = page.get('properties', {})
        # Task: title array (list of rich text)
        task = ''
        if 'Task' in props:
            title_arr = props['Task'].get('title', [])
            if title_arr:
                task = title_arr[0].get('plain_text', '')
        # Date: date start
        date_val = ''
        if 'Date' in props:
            date_info = props['Date'].get('date')
            if date_info:
                date_val = date_info.get('start', '')
        # Priority: select name
        priority = ''
        if 'Priority' in props:
            select_info = props['Priority'].get('select')
            if select_info:
                priority = select_info.get('name', '')
        # Status: status name
        status = ''
        if 'Status' in props:
            status_info = props['Status'].get('status')
            if status_info:
                status = status_info.get('name', '')
        entries.append(f"- {date_val}: {task} (Priority: {priority}, Status: {status})")

    if entries:
        for e in entries:
            print(e)
    else:
        print("No tasks or events scheduled in the next 3 days.")

if __name__ == "__main__":
    main()
