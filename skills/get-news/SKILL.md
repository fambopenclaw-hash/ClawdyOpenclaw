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
