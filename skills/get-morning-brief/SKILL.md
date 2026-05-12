---
name: get-morning-brief
description: "Comprehensive morning brief with weather (Ampang, Selangor), next 3 days agenda from Claw_Calendar, latest news (Malaysia/global/Iran-US/tech), saved to file and sent to chat. Triggered by phrases like 'good morning', 'morning brief', 'get morning brief'."
---

# Get Morning Brief

## Overview
This skill assembles a personalized morning briefing for Fahmi. It fetches:
- Weather for Ampang, Selangor (current and forecast)
- Agenda: tasks/events from Claw_Calendar Notion database within the next 3 days
- News: latest 24-hour updates in 4 categories (Malaysia, global, Iran-US conflict, technology/AI)
- A motivational quote to start the day

The brief is formatted in structured markdown, saved to `~/.openclaw/workspace/results/get-morning-brief/morning-brief-YYYY-MM-DD.md`, and sent as a reply.

## When to Use This Skill
- User explicitly requests a morning brief (e.g., "good morning", "give me my morning brief", "get morning brief")
- Can be set to run automatically via cron (see notes)

## Required Setup
- Notion integration with access to Claw_Calendar database. API key stored at `~/.config/notion/api_key`.
- Weather skill installed (uses wttr.in, no API key needed).
- get-news skill installed.
- The Claw_Calendar database `data_source_id` must be `31ce1fb7-4ad2-801d-a816-000b09abdd18`.

## Workflow

When invoked, follow these steps precisely:

1. **Get today's date** in YYYY-MM-DD. Also compute `three_days_later` = today + 3 days (date only).

2. **Fetch Weather**
   - Use the wrapper script: `bash /home/fahmibakeri/.openclaw/workspace/scripts/get_weather_ampang.sh`
   - This script implements:
     - Up to 3 retries with exponential backoff (1s, 2s, 3s)
     - Fallback to simplified format (`?format=%C+%t`) if full format throttled
     - Fallback to "Ampang" location if "+Selangor" causes issues
     - Clear error message if all attempts fail
   - Capture stdout. If the script exits with non-zero, note error and indicate service is temporarily unavailable.
   - Keep output as a code block in the brief.

3. **Fetch Agenda from Claw_Calendar**
   - Read Notion API key: `cat ~/.config/notion/api_key`
   - If key missing, produce error message.
   - Build JSON query:
     ```json
     {
       "filter": {
         "property": "Date",
         "date": {
           "on_or_after": "YYYY-MM-DD",
           "on_or_before": "YYYY-MM-DD"
         }
       },
       "sorts": [{"property": "Date", "direction": "ascending"}]
     }
     ```
   - POST to `https://api.notion.com/v1/data_sources/31ce1fb7-4ad2-801d-a816-000b09abdd18/query`
   - Headers: `Authorization: Bearer <api_key>`, `Notion-Version: 2025-09-03`, `Content-Type: application/json`
   - For each page in results, extract:
     - Task: title plain_text
     - Date: date start (YYYY-MM-DD)
     - Priority: select name (if present)
     - Status: status name (if present)
   - Format each as: `- YYYY-MM-DD: Task text (Priority: X, Status: Y)`
   - If no entries, say "No tasks or events scheduled in the next 3 days."

4. **Fetch News**
   - Invoke the `get-news` skill for all categories (do not specify any specific category).
   - Collect its output. It will provide sections for Malaysia, Global, Iran-US, Technology/AI.

5. **Assemble the Brief**
   - Header:
     ```
     Good morning, Fahmi!

     *<full date>*
     ```
   - Weather section: `**Weather (Ampang, Selangor):**` followed by code block
   - Agenda section: `**Agenda (next 3 days):**` followed by bullet list or "No tasks..."
   - News section: `**News (last 24 hours):**` followed by the get-news output (likely already sectioned)
   - Footer: pick a random motivational quote from this list (cycle by day of month):
     - "The only way to do great work is to love what you do. – Steve Jobs"
     - "Believe you can and you're halfway there. – Theodore Roosevelt"
     - "Your limitation—it's only your imagination."
     - "Push yourself, because no one else is going to do it for you."
     - "Great things never come from comfort zones."
     - "Dream it. Wish it. Do it."
     - "Success doesn’t just find you. You have to go out and get it."
     - "The harder you work for something, the greater you’ll feel when you achieve it."
     - "Don’t stop when you’re tired. Stop when you’re done."
     - "If it’s important to you, you’ll find a way. If not, you’ll find an excuse."
   - Format: `— <quote>`
   - Ensure the sections are separated by blank lines.

6. **Save to File**
   - Create directory `~/.openclaw/workspace/results/get-morning-brief/` if not exists.
   - File name: `morning-brief-<YYYY-MM-DD>.md`
   - Write the full markdown content.

7. **Send to Telegram**
   - Output the full markdown as your reply in this chat.

## Error Handling
- If any source fails (weather curl error, Notion query error, get-news unavailable), include a clear message in that section: `**[Source] Error:** <details>` and continue with other sources.
- If the brief cannot be assembled due to multiple critical failures, inform the user and suggest checking setup.

## Notes
- Dates are handled in Asia/Kuala_Lumpur timezone (default system timezone).
- The weather location is fixed as Ampang, Selangor, Malaysia.
- Motivational quotes cycle based on the day of the month to provide variety.

## Automation
To receive this brief automatically every day at 7:00 AM Asia/Kuala_Lumpur, set up a cron job that sends a message to this chat via Telegram Bot API:

```
0 7 * * * curl -s -X POST "https://api.telegram.org/bot<BOT_TOKEN>/sendMessage" -d chat_id=6191189810 -d text="get-morning-brief" >/dev/null 2>&1
```

Replace `<BOT_TOKEN>` with your bot's token (from BotFather). The chat ID is `6191189810`. This will trigger the skill and the brief will be sent as a reply.

## Examples
User: "good morning"
Assistant: (after running this skill) provides the full brief with weather, agenda, news, and quote.

User: "get my morning brief"
Assistant: same as above.