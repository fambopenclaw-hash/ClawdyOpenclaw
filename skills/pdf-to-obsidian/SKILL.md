---
name: pdf-to-obsidian
description: Workflow skill that processes PDF files shared via Telegram, extracts and summarizes text, extracts embedded figures/images, creates a rich markdown note in Obsidian with YAML frontmatter and embedded figures, uploads the PDF to Google Drive organized by topic, and embeds the Gdrive link in the note. Triggered when user shares a PDF file and asks to save it to Obsidian and Gdrive.
---

# pdf-to-obsidian

Extract text + figures from a PDF, create a rich Obsidian note, upload PDF to Gdrive, embed link.

## Config (from memory)

| Item | Value |
|------|-------|
| Obsidian vault | `\\wsl.localhost\Ubuntu\home\fahmibakeri\famb vault` |
| Gdrive base folder | `03 RESOURCE OPENCLAW` (create in root if not exists) |
| Upload method | rclone CLI (`/home/fahmibakeri/bin/rclone`) |
| PDF extraction | pymupdf (via `scripts/pdf-extract-assets.py`) |

## Workflow

```
PDF shared → Duplicate check (vault + Gdrive)
                ↓
         Topic inference (filename + LLM)
                ↓
         Confirm topic with user
                ↓
         Extract text + images (pymupdf)
                ↓
         Summarize + infer title + tags (LLM reads text)
                ↓
         Create .md in Obsidian vault
                ↓
         Upload PDF to Gdrive "03 RESOURCE OPENCLAW/<topic>/"
         (reuse existing subfolder if similar)
                ↓
         Get Gdrive link → embed in .md
```

## Step-by-Step

### 1. Duplicate Check
Before anything else:
- **Vault:** check if a `.md` file matching the slugified title already exists in `\\wsl.localhost\Ubuntu\home\fahmibakeri\famb vault`
- **Gdrive:** run `rclone lsf "gdrive:03 RESOURCE OPENCLAW/" --directories` and check if a file with the same original filename already exists in any topic subfolder
- If duplicate found → show user: `"⚠️ [filename] already exists in [vault/Gdrive location]. Skip, overwrite, or rename?"`
- If user says skip → stop and return the existing link

### 2. Smart Topic Inference
Two-step approach:
1. **Filename parsing** — strip leading numbers, split on `_`, `-`, `.`, and camelCase boundaries; filter stop words; join first 1-2 meaningful parts with `_`
2. **LLM refinement** — read first 500 chars of extracted text + filename; ask LLM to propose:
   - A clean topic folder name (1-2 words, machine-readable)
   - A 1-sentence title for the document
   - 3-5 relevant Obsidian tags (lowercase, hyphenated)

Show user all three for confirmation: `"Topic: [topic] | Title: [title] | Tags: [#tag1] [#tag2] — confirm or edit?"`

### 3. Extract Text + Images
- Run: `python3 scripts/pdf-extract-assets.py <pdf_path> <temp_dir>`
- Extracts text page-by-page and all embedded images using **pymupdf**
- Image output dir: a dedicated temp folder passed as `<temp_dir>`
- Text output: `<pdf_path>.txt` (updated to include page markers)
- If no text extracted → warn user ("PDF appears scanned/image-based")

### 4. Summarize + Tag
- Read the `.txt` file (or up to the first 4,000 characters if very long)
- Produce:
  - **Summary:** 3-8 sentences or 1-2 short paragraphs
  - **Title:** extracted or inferred document title (override LLM suggestion if better)
  - **Tags:** 3-5 relevant Obsidian tags
- Use the title, tags, and summary from the confirmed LLM output

### 5. Create .md in Obsidian
- **Vault path:** `\\wsl.localhost\Ubuntu\home\fahmibakeri\famb vault`
- **Filename:** slugified title + `.md`
- **YAML frontmatter format:**
```markdown
---
title: "{title}"
date: {YYYY-MM-DD}
tags: [{tag1}, {tag2}, {tag3}]
source: "{original_filename}"
---

# {Title}

## Summary

{summary text}

## Key Figures

{! embed images here if present !}

## Source

[📄 {original_filename}]({gdrive_link})
```
- **Images:** Copy all extracted images to vault root. Then select the **top 6 by file size** (or fewer if the document yielded less). Embed these as `![]({filename})` under `## Key Figures`, each with a caption derived from the nearest figure reference in the text (e.g., `*Figure X — [caption text from paper]*`). Discard the rest.
- Save to vault root — no subdirectory sorting
- If file already exists → append timestamp to filename

### 6. Upload to Gdrive (rclone)
- **Base folder:** `03 RESOURCE OPENCLAW`
- Ensure base folder exists: `rclone mkdir "gdrive:03 RESOURCE OPENCLAW"` (no-op if already exists)
- **Topic subfolder:**
  1. List: `rclone lsf "gdrive:03 RESOURCE OPENCLAW/" --directories`
  2. Compare existing folder names against derived topic (case-insensitive, Levenshtein distance ≤ 2 or same first word = match)
  3. If match found → use existing subfolder; otherwise create `rclone mkdir "gdrive:03 RESOURCE OPENCLAW/<topic>"`
- Upload PDF: `rclone copy "<pdf_path>" "gdrive:03 RESOURCE OPENCLAW/<topic>/"` (include trailing `/`)

### 7. Get Share Link & Finalize .md
- Get share link: `rclone link "gdrive:03 RESOURCE OPENCLAW/<topic>/<filename>.pdf"`
- Embed in .md: replace placeholder `## Source` line with the actual link
- If link retrieval fails → use `⚠️ Gdrive link pending — add manually`
- Clean up temp files: remove `<pdf_path>.txt` and `<temp_dir>` after processing

## Error Handling
- Duplicate found → pause and ask user before proceeding
- Text extraction empty → warn user, still create note with `summary = "[Extraction failed — review PDF manually]"`
- Gdrive upload fails → create .md without link, alert user to upload manually
- File already exists in vault → append timestamp to filename
- Image extraction fails → continue without images, do not block the note

## Resources
- `scripts/pdf-extract-assets.py` — text + image extraction (pymupdf, auto-installs on first run)
- `scripts/levenshtein.py` — string similarity helper for topic folder matching (optional, embedded in SKILL.md)
