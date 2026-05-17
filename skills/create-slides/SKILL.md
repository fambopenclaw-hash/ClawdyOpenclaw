---
name: create-slides
description: Generate PETRONAS-branded Subsurface strategy PowerPoint decks from JSON configuration. Use when the user asks to create, generate, or build a PPTX slide deck for Subsurface strategy reporting. Works with make_slides.py and a JSON config file.
---

# create-slides

Generate a branded 7-slide PowerPoint deck from a JSON config. Built on `python-pptx`.

## Quick Start

1. **Prepare JSON config** — copy and fill in `references/sample_config.json` (see below)
2. **Run the script:**
   ```bash
   python3 scripts/make_slides.py <path/to/config.json>
   ```
3. Output saved to the path in `config.output`

## JSON Config Schema

| Key | Type | Description |
|-----|------|-------------|
| `output` | string | Output .pptx filename |
| `title_slide` | object | Slide 1 content |
| `strategies` | array | Slides 3–6 (one per strategy item) |
| `strategies[].num` | string | "01"–"04", determines which slide builder is used |
| `strategies[].title` | string | Strategy title |
| `strategies[].owner` | string | Owner name |
| `strategies[].objective` | string | Objective text (slides 01–02 only) |
| `strategies[].deliverables` | string[] | Bullet items |
| `strategies[].notes` | string[] | Status/notes bullets |
| `strategies[].plan` | string[] | Activity bullets (slides 02–03) |
| `strategies[].focus` | string | Focus strip text |
| `strategies[].timeline` | string | Timeline strip text (slide 01) |
| `strategies[].emphasis_title` | string | Large callout title (slide 03) |
| `strategies[].emphasis_body` | string | Callout body (slide 03) |
| `strategies[].metrics` | object[] | 3 metric cards {label, title, desc} (slide 03) |
| `strategies[].milestone_title` | string | BCO milestone title (slide 04) |
| `strategies[].milestone_body` | string | BCO milestone body (slide 04) |
| `strategies[].deliverables_text` | string | Deliverables text block (slide 04) |
| `strategies[].notes_text` | string | Notes text block (slide 04) |
| `strategies[].status` | string | Status label (slide 04) |

## Slide Map

| Slide | Content |
|-------|---------|
| 1 | Title — from `title_slide` |
| 2 | Overview — agenda cards from `strategies` |
| 3 | Strategy 01 — ERMAI Log Conditioning Jurassic |
| 4 | Strategy 02 — LWD and ERMAI Introduction |
| 5 | Strategy 03 — ERMAI Interpretation QC |
| 6 | Strategy 04 — ERMAI BCO (M1) |
| 7 | Summary — 4 strategy cards |

## Colour Palette (PETRONAS)

| Token | Hex |
|-------|-----|
| DARK_PURPLE | `#3B1A6B` |
| TEAL | `#00927D` |
| TEAL_LIGHT | `#00B0F0` |
| GOLD | `#F5A623` |
| GREEN | `#00785A` |
| AMBER | `#B05700` |

## Customising

- **Colour constants** are defined at the top of `scripts/make_slides.py`
- **Slide dimensions** — `prs.slide_width = Inches(13.33)`, `prs.slide_height = Inches(7.5)` (16:9 widescreen)
- **Brand badge** — change `"SUBSURFACE"` in `title_slide.category` or pass per-slide via `badge` param