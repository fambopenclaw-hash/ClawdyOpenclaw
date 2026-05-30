## 📄 Notion Pages & Databases

### Connected Pages (Containers)

| Page Name | Page ID | Purpose |
|-----------|---------|---------|
| `Claw_task` | `318e1fb7-4ad2-8076-89b1-c686864d473b` | Default page for manual to-do blocks |
| `Claw_notes` | `318e1fb7-4ad2-807d-8d9d-dac6766a39f3` | General notes storage |
| `Claw_ideas` | `318e1fb7-4ad2-8032-8df8-e1fa7786bd64` | Ideas and brainstorming |
| `Claw_Infographic` | `4a1e1fb7-4ad2-8299-adb7-015b842e43cc` | Infographics and images |

### Databases (Data Sources)

| Database Name | Database ID | Data Source ID | Purpose |
|---------------|-------------|----------------|---------|
| `Claw_Calendar` | `31ce1fb7-4ad2-80bf-9a33-fcd9fcfe05fc` | Same as DB ID | Default tasks & events |
| `Db_Bonus` | `2a4e1fb7-4ad2-81ed-b82e-e5c55bf0d606` | `2a4e1fb7-4ad2-81a8-ad22-000bdb26a297` | Expense tracking (default for add expense) |

> **Note:** In Notion API v2025-09-03, databases are called "data sources". The `database_id` is used when creating pages; the `data_source_id` is used when querying.

### 📝 Page Mapping Rules

| Input Type | Target Page | Notes |
|------------|-------------|-------|
| Task capture (user says "add task") | `Claw_Calendar` database | Unless explicitly requested otherwise |
| Expense capture (user says "add expense") | `Db_Bonus` database | Default expense tracking database |
| Notes | `Claw_notes` page | Prepend to existing content |
| Ideas | `Claw_ideas` page | Prepend to existing content |
| Infographics/Images | `Claw_Infographic` page | Upload images; avoid text-only entries |
| Manual to-do blocks | `Claw_task` page | Only when specifically mentioned |

### ⚙️ General Notion Rules

- **Auto-save:** Infographics are NOT automatically saved to Notion. Only save when explicitly requested.
- **Content insertion:** Always prepend new content to the TOP of existing page content (never append).
- **Date fields:** When adding tasks/events, always include a `Date` field (default to current date if unspecified).
- **Priority fields:** Always include a `Priority` field (default to "Medium" if unspecified).

### 🔧 Adding New Pages or Databases

To add a new connected page:
1. Create the page in Notion
2. Share it with your integration
3. Add an entry to the **Connected Pages** table above with: Page Name, Page ID, and Purpose

To add a new database:
1. Create the database (with desired properties)
2. Share it with your integration
3. Get both the `database_id` and `data_source_id` (usually the same unless embedded)
4. Add an entry to the **Databases** table above with all four columns

---

### Obsidian Vault

**Vault Path:** `\\wsl.localhost\Ubuntu\home\fahmibakeri\famb vault`

* Use this path when asked to add notes to Obsidian.
* The vault is located in WSL Ubuntu filesystem.

---

### Infographic Preferences

* **Notion saving:** Do NOT automatically save infographics to Notion unless explicitly requested.
* **News infographic style:** Multi-section dashboard with color-coded quadrants, clean layout, professional design, resolution 1200x800.

### Claw_Calendar Database Rules (Reference)

* **Database ID:** `31ce1fb7-4ad2-80bf-9a33-fcd9fcfe05fc`
* **Default database for tasks & events:** When the user asks to "add" a task or event, create it in **Claw_Calendar** (not Claw_task)
* When adding tasks/events:
  * Always include the **Date** field (use current date if not specified by user)
  * Always include **Priority** field (use "Medium" if not specified by user)

### Db_Bonus Database Rules (Reference)

* **Database ID (for creating pages):** `2a4e1fb7-4ad2-81ed-b82e-e5c55bf0d606`
* **Data Source ID (for querying):** `2a4e1fb7-4ad2-81a8-ad22-000bdb26a297`
* **Default database for expenses:** When the user asks to "add expense" or "add expenditure", create it in **Db_Bonus**
* Properties:
  * **Description** (title) - Required: expense description
  * **Date** (date) - Required: when expense occurred (use current date if unspecified)
  * **Amount** (number, MYR) - Required: expense amount
  * **Category** (select) - Optional: one of Balek_kg, Food & Dining, Healthcare, Gadgets, Family, Personal, Others, FunTime, Giving, Productivity
  * **Type** (select) - Optional: Monthly or Bonus
* Note: Year-Month and Month are auto-calculated formulas based on Date

---

### Image Handling Preferences

* When asked to upload/embed an image, **automatically check the inbound folder**: `/home/fahmibakeri/.openclaw/media/inbound/`
* Look for recent images (by modification time) that match the context
* Use the file directly (base64 embed or local path) — do not ask user to create external links or upload elsewhere
* Only ask for alternative source if no suitable image is found in inbound folder

---

### OneNote Integration

**Maton API Gateway** enabled for OneNote access via Microsoft Graph.

#### Connection Details

| Property | Value |
|----------|-------|
| **Connection ID** | `505e760f-51aa-483b-9f7b-618c495d8480` |
| **Status** | ACTIVE |
| **Created** | 2026-03-30 |
| **App** | one-note |
| **Method** | OAUTH2 |

#### Default Notebook

| Field | Value |
|-------|-------|
| **Notebook Name** | `fambopenclaw_notebook` |
| **Notebook ID** | `0-AF179132430EF28E!sb487f5d43c4c46c9a9ae8202166f4107` |
| **Default Section** | `Openclaw_Notebook` |
| **Web Link** | [Open in OneNote](https://onedrive.live.com/redir.aspx?resid=AF179132430EF28E!sb487f5d43c4c46c9a9ae8202166f4107&id=documents&page=edit&cid=af179132430ef28e) |
| **User Role** | Owner |
| **Shared** | Yes |

#### Usage Notes

- All OneNote API calls use Maton gateway: `https://gateway.maton.ai/one-note/v1.0/me/onenote/...`
- Authentication: `Authorization: Bearer $MATON_API_KEY`
- Sections in this notebook: `Openclaw_Notebook` (used for image uploads and notes)
- Connection status and new connections managed at: `https://ctrl.maton.ai`

---

## 🌐 GitHub Pages Reporting

- **Report repo:** `fahmiamni/reports` → GitHub Pages at `https://fahmiamni.github.io/reports/`
- **Pattern for news reports:** `https://fahmiamni.github.io/reports/news-YYYY-MM-DD.html`
- Always use this URL pattern when generating and sharing links from the reports repo.
- Clone to local: `git clone https://github.com/fahmiamni/reports.git /tmp/news-pages`
- Push auth: use `fahmiamni` account token via `gh auth token --hostname github.com --user fahmiamni`

User wants reminders for kid-friendly, watchable milestones only:
- Proximity Operations Demo (manual spacecraft maneuver)
- Trans-Lunar Injection (TLI) burn)
- Lunar Flyby (closest Moon approach)
- Earth Re-entry (plasma fireball)
- Splashdown (Pacific recovery)

Reminders will be sent 15-30 minutes before each event with live stream link. No other notifications.
