#!/usr/bin/env python3
"""Convert various formats to OKF knowledge bundles.

Supported inputs:
  - Markdown awesome-xx lists (link-list items → OKF entries)
  - JSON arrays of {title, url, description} objects
  - Plain text URL lists
  - GitHub repo URLs (metadata + README fetched via GitHub API, no auth)
  - Obsidian vaults, Notion exports, Feishu exports, Typora notes (Markdown files/dirs)
  - YAML lists/mappings of {title, url, description} (via pyyaml when installed)
  - CSV tables with title/url/description columns (first column falls back to title)
  - Generic key: value blocks (frontmatter, properties files, custom formats)
  - Text-layer PDFs (via pymupdf when installed; scanned PDFs print an OCR recipe)
  - Scans / images (no bundled OCR — prints a ready-to-run PaddleOCR recipe)

Output: a directory of Markdown files with YAML frontmatter ready for myokf validate.
"""

import json
import re
import sys
import urllib.error
import urllib.request
from argparse import ArgumentParser
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

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


def parse_url_list(text: str) -> list[dict]:
    """Parse plain text lines that are bare URLs."""
    entries = []
    for line in text.splitlines():
        m = re.match(r"^\s*(https?://\S+)\s*$", line)
        if not m:
            continue
        url = m.group(1)
        title = url.rstrip("/").split("/")[-1] or url
        entries.append({"title": title, "url": url, "description": url})
    return entries


def fetch_github(repo_url: str) -> dict:
    """Fetch repo metadata + README from GitHub (public repos, no auth needed)."""
    m = re.match(r"https?://github\.com/([^/\s]+)/([^/\s]+?)(?:/.*)?$", repo_url.strip())
    if not m:
        raise SystemExit(f"Not a GitHub repo URL: {repo_url}")
    owner, repo = m.group(1), m.group(2).removesuffix(".git")

    def api(path: str, raw: bool = False) -> str:
        headers = {"User-Agent": "awesome-okf-converter"}
        if raw:
            headers["Accept"] = "application/vnd.github.raw"
        req = urllib.request.Request(f"https://api.github.com/{path}", headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8")

    try:
        meta = json.loads(api(f"repos/{owner}/{repo}"))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"GitHub API error {e.code} for {owner}/{repo} (repo may be private)") from e
    except urllib.error.URLError as e:
        raise SystemExit(f"Network error fetching {owner}/{repo}: {e.reason}") from e

    readme = ""
    try:
        readme = api(f"repos/{owner}/{repo}/readme", raw=True)
    except (urllib.error.HTTPError, urllib.error.URLError):
        pass  # no README — entry still stands on metadata

    tags = list(meta.get("topics") or [])
    if not tags and meta.get("language"):
        tags = [meta["language"].lower()]

    return {
        "title": meta.get("full_name", f"{owner}/{repo}"),
        "url": meta.get("html_url", repo_url),
        "description": meta.get("description") or meta.get("full_name", repo_url),
        "tags": tags,
        "body": readme,
    }


def parse_markdown_dir(input_path: Path, *, variant: str) -> list[dict]:
    """Obsidian vault / Notion export / Feishu export / Typora notes → one entry per Markdown file."""
    if input_path.is_file():
        files = [input_path]
    else:
        files = sorted(
            p for p in input_path.rglob("*.md")
            if not any(part.startswith(".") for part in p.relative_to(input_path).parts)
        )

    entries = []
    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace").strip()
        if not text:
            continue
        # drop the note's own YAML frontmatter (Obsidian notes carry one)
        if text.startswith("---") and len(text.split("---", 2)) == 3:
            text = text.split("---", 2)[2].strip()
        if variant == "obsidian":
            # [[Note]] → Note, [[Note|alias]] → alias
            text = re.sub(r"!?\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", lambda m: m.group(2) or m.group(1), text)
        title_m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        title = title_m.group(1).strip() if title_m else f.stem
        body = re.sub(r"^#\s+.+(\r?\n)", "", text, count=1, flags=re.MULTILINE) if title_m else text
        desc = title
        for line in body.splitlines():
            line = line.strip()
            if line and not line.startswith(("#", "```")):
                desc = line
                break
        entries.append({"title": title, "url": str(f), "description": desc, "body": body})
    return entries


def parse_yaml(text: str) -> list[dict]:
    """YAML list (or mapping) of {title, url, description} — needs pyyaml (optional)."""
    try:
        import yaml
    except ImportError:
        raise SystemExit(
            "YAML conversion needs pyyaml:\n"
            "  pip install pyyaml\n"
            "  python scripts/convert-to-okf.py data.yaml --format yaml -o kb/"
        ) from None
    data = yaml.safe_load(text)
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        raise SystemExit("YAML must be a list of {title, url, description} (or a single mapping)")
    return [
        {
            "title": str(d.get("title", "")),
            "url": str(d.get("url", "")),
            "description": str(d.get("description") or d.get("title", "")),
        }
        for d in data
        if isinstance(d, dict)
    ]


def parse_csv(text: str) -> list[dict]:
    """CSV with title/url/description columns; without a title column, the first
    three columns are used positionally as title, url, description."""
    import csv as _csv
    import io

    reader = _csv.DictReader(io.StringIO(text))
    rows = list(reader)
    if not rows:
        return []
    entries = []
    if "title" in (reader.fieldnames or []):
        for r in rows:
            title = (r.get("title") or "").strip()
            if not title:
                continue
            entries.append({
                "title": title,
                "url": (r.get("url") or "").strip(),
                "description": (r.get("description") or title).strip(),
            })
    else:
        for r in rows:
            vals = [str(v).strip() for v in r.values()]
            title = vals[0] if vals else ""
            if not title:
                continue
            entries.append({
                "title": title,
                "url": vals[1] if len(vals) > 1 else "",
                "description": vals[2] if len(vals) > 2 else title,
            })
    return entries


def parse_keyvalue(text: str) -> list[dict]:
    """Generic key: value blocks — YAML frontmatter, properties files, custom formats.

    One entry per block of consecutive `key: value` lines that has a title.
    A blank line or `---` starts a new entry. Key aliases: title/name,
    url/link/resource, description/desc/summary. Unknown keys are ignored.
    """
    entries = []
    current: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped == "---":
            if current:
                entry = _kv_entry(current)
                if entry:
                    entries.append(entry)
                current = {}
            continue
        m = re.match(r"^([A-Za-z_][\w .-]*)\s*[:=]\s*(.+)$", stripped)
        if m:
            current[m.group(1).strip().lower().replace(" ", "_")] = m.group(2).strip().strip("\"'")
    if current:
        entry = _kv_entry(current)
        if entry:
            entries.append(entry)
    return entries


def _kv_entry(kv: dict[str, str]) -> dict | None:
    title = kv.get("title") or kv.get("name") or ""
    if not title:
        return None
    return {
        "title": title,
        "url": kv.get("url") or kv.get("link") or kv.get("resource") or "",
        "description": kv.get("description") or kv.get("desc") or kv.get("summary") or title,
    }


def parse_anything(text: str) -> list[dict]:
    """The OKF Anything fallback chain: list → JSON → key-value → URLs → line-per-row."""
    for parser in (parse_markdown_links, parse_json, parse_keyvalue, parse_url_list):
        try:
            entries = parser(text)
        except (ValueError, TypeError):
            continue
        if entries and entries[0].get("title"):
            return entries
    # last resort: every non-empty line becomes one entry
    return [
        {"title": line.strip(), "url": "", "description": line.strip()}
        for line in text.splitlines()
        if line.strip()
    ]


def parse_pdf(input_path: Path) -> list[dict]:
    """Text-layer PDF → one entry per page. Scanned PDFs need OCR (recipe printed)."""
    try:
        import fitz  # pymupdf — optional, text extraction only
    except ImportError:
        raise SystemExit(
            "PDF conversion needs pymupdf for the text layer:\n"
            "  pip install pymupdf\n"
            "Scanned/image-only PDFs need OCR first — PaddleOCR recipe:\n"
            "  pip install paddleocr paddlepaddle\n"
            f"  paddleocr ppocr -i {input_path} --type ocr --lang en -o ocr-text/\n"
            "  python scripts/convert-to-okf.py ocr-text/ --format notion -o kb/"
        ) from None
    doc = fitz.open(input_path)
    entries = []
    for i, page in enumerate(doc, 1):
        text = page.get_text().strip()
        if not text:
            continue
        first_line = next((ln for ln in text.splitlines() if ln.strip()), input_path.stem)
        entries.append({
            "title": f"{input_path.stem} — page {i}",
            "url": str(input_path),
            "description": first_line[:200],
            "body": text,
        })
    if not entries:
        raise SystemExit(
            f"No text layer found in {input_path} — it is a scanned PDF. OCR first:\n"
            "  pip install paddleocr paddlepaddle\n"
            f"  paddleocr ppocr -i {input_path} --type ocr --lang en -o ocr-text/\n"
            "  python scripts/convert-to-okf.py ocr-text/ --format notion -o kb/"
        )
    return entries


def parse_image(input_path: Path) -> list[dict]:
    """Scans / images — OCR is intentionally not bundled. Print the canonical recipe."""
    raise SystemExit(
        f"OCR is not bundled — convert {input_path} with a local OCR engine first:\n"
        "  pip install paddleocr paddlepaddle\n"
        f"  paddleocr ppocr -i {input_path} --type ocr --lang en -o ocr-text/\n"
        "  python scripts/convert-to-okf.py ocr-text/ --format notion -o kb/"
    )


def build_bundle(entries: list[dict], output_dir: Path, *, entry_type: str = "concept") -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    seen: dict[str, int] = {}
    for e in entries:
        slug = slugify(e["title"]) or "entry"
        n = seen.get(slug, 0) + 1
        seen[slug] = n
        filename = output_dir / (f"{slug}.md" if n == 1 else f"{slug}-{n}.md")
        tags = ", ".join(e.get("tags") or []) or slugify(e["title"]).replace("-", ", ")
        content = TEMPLATE.format(
            type=entry_type,
            title=e["title"],
            description=e["description"],
            resource=e["url"],
            tags=tags,
            generated_at=now,
            body=e.get("body") or e["description"],
        )
        filename.write_text(dedent(content), encoding="utf-8")
    return output_dir


def main() -> None:
    p = ArgumentParser(description="Convert various formats to OKF bundles")
    p.add_argument("input", help="Input file, directory, or GitHub repo URL")
    p.add_argument("-o", "--output", default="./okf-bundle", help="Output directory")
    p.add_argument("-t", "--type", default="concept", help="OKF entry type (default: concept)")
    p.add_argument("--format", choices=["auto", "anything", "markdown", "json", "yaml", "csv", "kv", "urls", "github", "obsidian", "notion", "feishu", "typora", "pdf", "image"], default="auto", help="Input format")
    args = p.parse_args()

    fmt = args.format
    if fmt == "auto":
        if args.input.endswith(".json"):
            fmt = "json"
        elif args.input.lower().endswith((".yaml", ".yml")):
            fmt = "yaml"
        elif args.input.lower().endswith(".csv"):
            fmt = "csv"
        elif args.input.endswith(".txt"):
            fmt = "urls"
        elif re.match(r"https?://github\.com/", args.input):
            fmt = "github"
        elif Path(args.input).is_dir():
            fmt = "obsidian"
        elif args.input.lower().endswith(".pdf"):
            fmt = "pdf"
        elif re.search(r"\.(png|jpe?g|tiff?|bmp|webp)$", args.input, re.IGNORECASE):
            fmt = "image"
        else:
            fmt = "anything"

    if fmt == "github":
        entries = [fetch_github(args.input)]
    elif fmt == "json":
        entries = parse_json(Path(args.input).read_text(encoding="utf-8"))
    elif fmt == "yaml":
        entries = parse_yaml(Path(args.input).read_text(encoding="utf-8"))
    elif fmt == "csv":
        entries = parse_csv(Path(args.input).read_text(encoding="utf-8"))
    elif fmt == "kv":
        entries = parse_keyvalue(Path(args.input).read_text(encoding="utf-8"))
    elif fmt == "urls":
        entries = parse_url_list(Path(args.input).read_text(encoding="utf-8"))
    elif fmt in {"obsidian", "notion", "feishu", "typora"}:
        entries = parse_markdown_dir(Path(args.input), variant=fmt)
    elif fmt == "pdf":
        entries = parse_pdf(Path(args.input))
    elif fmt == "image":
        parse_image(Path(args.input))
        entries = []  # unreachable — parse_image always exits with the recipe
    elif fmt == "anything":
        entries = parse_anything(Path(args.input).read_text(encoding="utf-8"))
    else:
        entries = parse_markdown_links(Path(args.input).read_text(encoding="utf-8"))

    if not entries:
        print("No entries found in input.", file=sys.stderr)
        sys.exit(1)

    out = build_bundle(entries, Path(args.output), entry_type=args.type)
    print(f"OKF bundle: {len(entries)} entries → {out.resolve()}")
    print("Next: myokf validate", out.name)


if __name__ == "__main__":
    main()
