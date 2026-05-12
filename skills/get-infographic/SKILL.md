---
name: get-infographic
description: Generate professional infographics from text descriptions using Nano Banana Pro (Gemini 3 Pro Image).
homepage: https://ai.google.dev/
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["uv"], "env": ["GEMINI_API_KEY"] },
        "primaryEnv": "GEMINI_API_KEY",
        "install":
          [
            {
              "id": "uv-brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
          ],
      },
  }
---

# Get Infographic

Use this skill to generate professional infographics from text descriptions. The skill uses Nano Banana Pro (Gemini 3 Pro Image) and adds infographic-specific prompting (clean layouts, color-coded sections, icons).

Generate

```bash
uv run {baseDir}/scripts/generate_infographic.py --prompt "your infographic description" [--resolution 1K|2K|4K] [--aspect-ratio RATIO]
```

Output

- Saved to: `results/get-infographic/` in the workspace
- Automatically sent to Telegram via OpenClaw's MEDIA attachment

Examples

```bash
uv run {baseDir}/scripts/generate_infographic.py --prompt "population growth by continent from 1950 to 2050" --resolution 2K
```

Notes

- Resolution: default `2K` (good balance of quality and speed). Use `1K` for quick drafts, `4K` for print-quality.
- Aspect ratios: `1:1`, `16:9`, `9:16`, etc. Without `--aspect-ratio`, the model picks freely.
- The script enhances your prompt with infographic-specific instructions automatically.
- You must have `GEMINI_API_KEY` set in your environment or OpenClaw config.
