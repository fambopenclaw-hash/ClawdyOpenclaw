---
name: get-news
description: Fetches and summarizes recent news from Malaysia (local), global, Iran-US conflict, and technology/AI categories within the last 24 hours. Use when the user requests news updates or summaries in any of these domains. Provides a standardized approach to gathering timely news with consistent formatting and category-specific search strategies.
---

# Get News

## Overview

The get-news skill enables Codex to retrieve and summarize the latest news from four key categories: Malaysia local news, global news, Iran-US war developments, and technology/AI news. It ensures fresh content (within 24 hours) and presents it in a clear, categorized format.

## When to Use This Skill

Trigger the skill when the user:
- Asks for news updates or current events
- Requests summaries of recent happenings in Malaysia, globally, regarding the Iran-US conflict, or in technology/AI
- Wants to stay informed about developments in any of these four categories

## Capabilities

The skill supports fetching news for the following categories:

1. **Malaysia Local News**
   - Focus: National and regional events within Malaysia
   - Query approach: "Malaysia news" or specific topics like "Malaysia politics", "Malaysia economy"
   - Freshness: last 24 hours

2. **Global News**
   - Focus: Major world events and international developments
   - Query approach: "global news", "world news", "international news"
   - Freshness: last 24 hours

3. **Iran-US War**
   - Focus: Latest developments in the conflict between Iran and the United States
   - Query approach: "Iran US war", "Iran-US conflict", "Iran United States tensions"
   - Freshness: last 24 hours

4. **Technology & AI**
   - Focus: Recent advancements, product releases, and research in technology and artificial intelligence
   - Query approach: "technology news", "AI news", "artificial intelligence latest"
   - Freshness: last 24 hours

## How to Use

When the user requests news:

1. Identify which categories are needed. If none are specified, fetch all four.
2. For each category, call `web_search` with:
   - `query`: appropriate search terms for the category
   - `count`: default 5 (adjustable based on user preference)
   - `freshness`: "day" to restrict to last 24 hours
3. Collect the results and format them under clear category headings.
4. If a category yields no results, note that appropriately.
5. Present the compiled news summary to the user.

### Optional Parameters

- `count`: Number of results to fetch per category (default: 5)
- `specific_categories`: A list limiting which categories to fetch (if user specifies)

### Example Interactions

**User:** "Get me the latest news"
**Codex:** Fetches all four categories and presents a combined summary.

**User:** "What's happening in Malaysia?"
**Codex:** Fetches only Malaysia local news.

**User:** "Tell me about the Iran-US situation and any new AI developments."
**Codex:** Fetches Iran-US war and Technology & AI categories.

## Notes

- Always use `freshness: 'day'` to ensure recency.
- Prefer broad queries for each category to capture a range of news sources.
- If the user wants more depth on a specific topic, consider follow-up searches within that category.
- The skill does not currently support historical news beyond 24 hours.

---

## Generate HTML Report from News

After compiling the news summary, automatically generate a self-contained HTML report and publish it to GitHub Pages. This step leverages the `create-html-report` skill infrastructure.

### When This Happens

Automatically triggered at the end of every news fetch — no additional user input needed.

### Step 1 — Structure the News Data

Organize the compiled news into a JSON-friendly structure with:

- **Title**: e.g. "Latest News Summary — 15 May 2026"
- **Categories**: Malaysia, Global, Iran-US, Technology/AI
- **Items per category**: headline, source, time, summary, url (if available)
- **Generated timestamp**

### Step 2 — Generate the HTML

Build a self-contained HTML file using the news-friendly layout below. Save to:

`~/.openclaw/workspace/skills/create-html-report/output/news-<YYYY-MM-DD>.html`

**HTML Layout Reference:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>News Summary — DD MMM YYYY</title>
  <style>
    :root {
      --dark: #0f1b2d; --blue: #0032A0; --light: #e8edf5;
      --mid: #c5d0e6; --green: #1a7a4a; --amber: #d4820a;
      --red: #c0392b; --text: #1a1a2e; --muted: #5a6a7a;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', Calibri, sans-serif; background: var(--light); color: var(--text); font-size: 14px; }

    .header {
      background: var(--dark);
      background-image: linear-gradient(135deg, #0f1b2d 0%, #1a2f4e 100%);
      color: #fff; padding: 28px 36px 24px;
      border-bottom: 4px solid var(--blue);
    }
    .header-top { display: flex; align-items: center; gap: 14px; margin-bottom: 6px; }
    .badge { background: var(--blue); color: #fff; font-size: 10px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; padding: 4px 10px; border-radius: 4px; }
    .header h1 { font-size: 22px; font-weight: 700; }
    .header-meta { font-size: 12px; color: var(--mid); margin-top: 4px; }

    .body { padding: 28px 36px 48px; max-width: 1100px; }

    /* Category Sections */
    .news-category { background: #fff; border-radius: 12px; padding: 20px 24px; box-shadow: 0 1px 4px rgba(0,0,0,.08); margin-bottom: 16px; }
    .category-title {
      font-size: 13px; font-weight: 700; color: #fff; margin-bottom: 14px;
      padding: 8px 14px; border-radius: 8px;
      display: flex; align-items: center; gap: 8px;
    }
    .category-title.malaysia { background: linear-gradient(135deg, #0032A0, #0050c8); }
    .category-title.global   { background: linear-gradient(135deg, #1a7a4a, #22a86a); }
    .category-title.iranus  { background: linear-gradient(135deg, #c0392b, #e74c3c); }
    .category-title.tech    { background: linear-gradient(135deg, #6c3483, #9b59b6); }

    .news-item { border-left: 3px solid var(--mid); padding: 10px 14px; margin-bottom: 10px; background: #f4f7fc; border-radius: 6px; }
    .news-item:last-child { margin-bottom: 0; }
    .news-headline { font-size: 14px; font-weight: 700; color: var(--dark); margin-bottom: 4px; line-height: 1.4; }
    .news-meta { font-size: 11px; color: var(--muted); margin-bottom: 6px; }
    .news-summary { font-size: 13px; color: var(--text); line-height: 1.6; }
    .news-source { font-size: 11px; font-weight: 700; color: var(--blue); margin-top: 4px; }

    /* Stats row */
    .stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 24px; }
    .stat-card { background: #fff; border-radius: 10px; padding: 16px 18px; box-shadow: 0 1px 4px rgba(0,0,0,.08); border-top: 4px solid var(--blue); }
    .stat-card.g { border-top-color: var(--green); }
    .stat-card.a { border-top-color: var(--amber); }
    .stat-card.r { border-top-color: var(--red); }
    .stat-label { font-size: 10px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: var(--muted); margin-bottom: 4px; }
    .stat-value { font-size: 20px; font-weight: 700; color: var(--dark); }

    @media (max-width: 700px) { .stat-grid { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 600px) { .header { padding: 20px 20px 16px; } .body { padding: 20px 20px 36px; } }
  </style>
</head>
<body>

<div class="header">
  <div style="margin-bottom:10px">
    <a href="index.html" style="color:#fff;font-size:12px;font-weight:700;text-decoration:none;background:var(--blue);padding:5px 12px;border-radius:6px;">← Back to Index</a>
  </div>
  <div class="header-top">
    <span class="badge">NEWS</span>
    <h1>News Summary — DD MMM YYYY</h1>
  </div>
  <div class="header-meta">Auto-generated from get-news skill · Last 24 hours</div>
</div>

<div class="body">

  <!-- Stats row: total items per category -->
  <div class="stat-grid">
    <div class="stat-card">
      <div class="stat-label">🇲🇾 Malaysia</div>
      <div class="stat-value" id="cnt-my">N</div>
    </div>
    <div class="stat-card g">
      <div class="stat-label">🌍 Global</div>
      <div class="stat-value" id="cnt-gl">N</div>
    </div>
    <div class="stat-card a">
      <div class="stat-label">⚔️ Iran-US</div>
      <div class="stat-value" id="cnt-iran">N</div>
    </div>
    <div class="stat-card r">
      <div class="stat-label">🤖 Tech/AI</div>
      <div class="stat-value" id="cnt-tech">N</div>
    </div>
  </div>

  <!-- Malaysia Section -->
  <div class="news-category">
    <div class="category-title malaysia">🇲🇾 Malaysia</div>
    <div id="news-malaysia"><!-- filled by script --></div>
  </div>

  <!-- Global Section -->
  <div class="news-category">
    <div class="category-title global">🌍 Global</div>
    <div id="news-global"><!-- filled by script --></div>
  </div>

  <!-- Iran-US Section -->
  <div class="news-category">
    <div class="category-title iranus">⚔️ Iran-US Conflict</div>
    <div id="news-iranus"><!-- filled by script --></div>
  </div>

  <!-- Tech/AI Section -->
  <div class="news-category">
    <div class="category-title tech">🤖 Technology & AI</div>
    <div id="news-tech"><!-- filled by script --></div>
  </div>

  <!-- Footer -->
  <div style="text-align:center;padding:20px 36px;font-size:12px;color:var(--muted);border-top:1px solid var(--mid);margin-top:8px">
    Generated by OpenClaw get-news skill · <span id="gen-time"></span>
  </div>
</div>

<script>
  // Inject counts
  document.getElementById('gen-time').textContent = new Date().toLocaleString('en-MY', {timeZone:'Asia/Kuala_Lumpur'});
</script>
</body>
</html>
```

Fill in the `<div>` slots for each category with `news-item` blocks, and update the stat counts via the `id` elements.

### Step 3 — Push to GitHub Pages

```bash
# Clone the repo
gh repo clone fahmiamni/reports /tmp/gh-pages-news 2>/dev/null || git clone https://github.com/fahmiamni/reports.git /tmp/gh-pages-news

# Copy the HTML file
cp ~/.openclaw/workspace/skills/create-html-report/output/news-<YYYY-MM-DD>.html /tmp/gh-pages-news/news-<YYYY-MM-DD>.html

# Commit and push
cd /tmp/gh-pages-news
git config user.email "clawdius@openclaw.ai"
git config user.name "Clawdius"
git config credential.helper "!gh auth git-credential"
git add news-<YYYY-MM-DD>.html
git commit -m "Update news summary: <YYYY-MM-DD>"
git push origin main
```

### Step 4 — Update index.html

Read `/tmp/gh-pages-news/index.html`, add a new card BEFORE the closing `</div>` of `.card-grid`:

```html
<a class="card" href="news-<YYYY-MM-DD>.html">
  <div class="card-title">📰 News Summary — DD MMM YYYY</div>
  <div class="card-desc">Malaysia · Global · Iran-US · Tech/AI</div>
  <div class="card-tag">News</div>
</a>
```

Commit and push the updated `index.html`.

### Live URL

`https://fahmiamni.github.io/reports/news-<YYYY-MM-DD>.html`

Share this link with the user after publishing.
