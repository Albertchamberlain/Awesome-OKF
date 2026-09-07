#!/usr/bin/env python3
"""Convert various formats to OKF knowledge bundles.

Supported inputs:
  - Markdown awesome-xx lists (link-list items → OKF entries)
  - JSON arrays of {title, url, description} objects
  - Plain text URL lists

Output: a directory of Markdown files with YAML frontmatter ready for myokf validate.
"""

import json
import re
import sys
from argparse import ArgumentParser
from pathlib import Path
from textwrap import dedent
from datetime import datetime, timezone

TEMPLATE = """\
---
type: {type}
title: {title}
description: {description}
resource: {resource}
tags: [{tags}]
generated:
  by: convert-to-okf
  at: {generated_at}
---

# {title}

{body}
"""


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def parse_markdown_links(text: str) -> list[dict]:
    """Parse markdown list items of the form `- [Title](URL) — Description.`"""
    entries = []
    pattern = re.compile(r"^\s*[-*]\s+\[([^\]]+)]\(([^)]+)\)\s*(?:—\s*(.+))?", re.MULTILINE)
    for m in pattern.finditer(text):
        title = m.group(1).strip()
        url = m.group(2).strip()
        desc = (m.group(3) or title).strip()
        entries.append({"title": title, "url": url, "description": desc})
    return entries


def parse_json(text: str) -> list[dict]:
    data = json.loads(text)
    if isinstance(data, dict):
        data = [data]
    return [{"title": d.get("title", ""), "url": d.get("url", ""), "description": d.get("description", "")} for d in data]


def build_bundle(entries: list[dict], output_dir: Path, *, entry_type: str = "concept") -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for e in entries:
        slug = slugify(e["title"]) or "entry"
        filename = output_dir / f"{slug}.md"
        tags = slugify(e["title"]).replace("-", ", ")
        content = TEMPLATE.format(
            type=entry_type,
            title=e["title"],
            description=e["description"],
            resource=e["url"],
            tags=tags,
            generated_at=now,
            body=e["description"],
        )
        filename.write_text(dedent(content), encoding="utf-8")
    return output_dir


def main() -> None:
    p = ArgumentParser(description="Convert various formats to OKF bundles")
    p.add_argument("input", help="Input file (markdown, json, or text)")
    p.add_argument("-o", "--output", default="./okf-bundle", help="Output directory")
    p.add_argument("-t", "--type", default="concept", help="OKF entry type (default: concept)")
    p.add_argument("--format", choices=["auto", "markdown", "json"], default="auto", help="Input format")
    args = p.parse_args()

    text = Path(args.input).read_text(encoding="utf-8")
    fmt = args.format
    if fmt == "auto":
        fmt = "json" if args.input.endswith(".json") else "markdown"

    entries = parse_json(text) if fmt == "json" else parse_markdown_links(text)
    if not entries:
        print("No entries found in input.", file=sys.stderr)
        sys.exit(1)

    out = build_bundle(entries, Path(args.output), entry_type=args.type)
    print(f"OKF bundle: {len(entries)} entries → {out.resolve()}")
    print("Next: myokf validate", out.name)


if __name__ == "__main__":
    main()