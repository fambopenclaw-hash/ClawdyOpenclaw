#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Generate an infographic using the existing nano-banana-pro skill.

This wrapper script:
- Enhances the user prompt for infographic generation
- Builds an output path under results/get-infographic/
- Invokes the nano-banana-pro generate_image.py script
- Forwards the MEDIA output line for OpenClaw attachment
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Generate a professional infographic using Nano Banana Pro"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Infographic description (plain text, e.g., 'climate change statistics')"
    )
    parser.add_argument(
        "--resolution", "-r",
        choices=["1K", "2K", "4K"],
        default="2K",
        help="Output resolution (default: 2K)"
    )
    parser.add_argument(
        "--aspect-ratio", "-a",
        help="Aspect ratio, e.g., 16:9, 9:16, 1:1 (optional)"
    )

    args = parser.parse_args()

    # Use raw prompt without enhancement
    enhanced_prompt = args.prompt

    # Output directory: results/get-infographic in workspace root
    workspace_root = Path("/home/fahmibakeri/.openclaw/workspace")
    output_dir = workspace_root / "results" / "get-infographic"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename: infographic_YYYY-MM-DD-HH-MM-SS_slug.png
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # Slugify first part of prompt
    slug_raw = args.prompt[:30]
    slug = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" for c in slug_raw).rstrip()
    slug = slug.replace(" ", "_")
    filename = f"infographic_{timestamp}_{slug}.png"
    output_path = output_dir / filename

    # Locate the nano-banana-pro generate_image.py script
    # It is installed globally with OpenClaw
    nano_script = Path.home() / ".npm-global" / "lib" / "node_modules" / "openclaw" / "skills" / "nano-banana-pro" / "scripts" / "generate_image.py"
    if not nano_script.exists():
        print(f"Error: Nano Banana Pro script not found at {nano_script}", file=sys.stderr)
        print("Make sure the nano-banana-pro skill is installed correctly.", file=sys.stderr)
        sys.exit(1)

    # Build command
    cmd = [
        "uv", "run", str(nano_script),
        "--prompt", enhanced_prompt,
        "--filename", str(output_path),
        "--resolution", args.resolution
    ]
    if args.aspect_ratio:
        cmd.extend(["--aspect-ratio", args.aspect_ratio])

    # Preserve environment (for GEMINI_API_KEY)
    env = os.environ.copy()

    print(f"Generating infographic with resolution {args.resolution}...")
    print(f"Prompt: {enhanced_prompt[:120]}...")

    # Run subprocess, capture output, but also stream to our stdout/stderr
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)

    # Forward stdout and stderr
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)

    if result.returncode != 0:
        print(f"Error: Nano Banana Pro exited with code {result.returncode}", file=sys.stderr)
        sys.exit(result.returncode)

    # Success: the nano script prints a MEDIA: line which we already forwarded.
    # OpenClaw will pick that up and attach the image to the Telegram message.


if __name__ == "__main__":
    main()
