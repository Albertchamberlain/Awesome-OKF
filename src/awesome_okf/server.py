"""MCP meta-server that exposes the Awesome-OKF catalog to agents."""

from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from .catalog import Catalog, get_catalog

mcp = FastMCP("awesome-okf")


def _entry_to_dict(entry) -> dict[str, Any]:
    return {
        "id": entry.id,
        "name": entry.name,
        "kind": entry.kind,
        "category": entry.category,
        "url": entry.url,
        "description": entry.description,
        "platform": list(entry.platform) if hasattr(entry, "platform") else [],
        "official": entry.official,
        "tags": list(entry.tags),
    }


def _catalog() -> Catalog:
    return get_catalog()


@mcp.tool()
def search_catalog(query: str, kind: str = "", limit: int = 10) -> str:
    """Search the Awesome-OKF catalog by keywords across names, tags, and descriptions."""
    catalog = _catalog()
    resolved_kind = kind.strip() or None
    if resolved_kind and resolved_kind not in {"tool", "plugin", "skill", "proposal", "doc"}:
        return json.dumps({"error": f"invalid kind: {kind}"}, ensure_ascii=False)
    hits = catalog.search(query, kind=resolved_kind, limit=max(1, min(limit, 25)))
    return json.dumps({"query": query, "count": len(hits), "results": [_entry_to_dict(item) for item in hits]}, ensure_ascii=False, indent=2)


@mcp.tool()
def list_catalog(kind: str = "", limit: int = 25) -> str:
    """List catalog entries, optionally filtered by kind: server, client, registry, or framework."""
    catalog = _catalog()
    resolved_kind = kind.strip() or None
    if resolved_kind and resolved_kind not in {"tool", "plugin", "skill", "proposal", "doc"}:
        return json.dumps({"error": f"invalid kind: {kind}"}, ensure_ascii=False)
    entries = catalog.by_kind(resolved_kind) if resolved_kind else list(catalog.entries)
    entries = entries[: max(1, min(limit, 50))]
    return json.dumps({"count": len(entries), "results": [_entry_to_dict(item) for item in entries]}, ensure_ascii=False, indent=2)


@mcp.tool()
def get_catalog_entry(entry_id: str) -> str:
    """Fetch a single catalog entry by its stable id (e.g. github-mcp-server)."""
    catalog = _catalog()
    entry = catalog.by_id(entry_id.strip())
    if entry is None:
        return json.dumps({"error": f"unknown id: {entry_id}"}, ensure_ascii=False)
    return json.dumps(_entry_to_dict(entry), ensure_ascii=False, indent=2)


@mcp.tool()
def catalog_stats() -> str:
    """Return summary statistics for the Awesome-OKF catalog."""
    catalog = _catalog()
    return json.dumps(
        {
            "meta": {
                "version": catalog.meta.version,
                "updated": catalog.meta.updated,
                "description": catalog.meta.description,
            },
            "stats": catalog.stats(),
        },
        ensure_ascii=False,
        indent=2,
    )


def _parse_kv(text: str) -> list[dict]:
    """Generic key: value blocks → {title, url, description} entries.

    Key aliases: title/name, url/link/resource, description/desc/summary.
    A blank line or `---` starts a new entry.
    """
    import re

    def flush(cur: dict[str, str]) -> dict | None:
        title = cur.get("title") or cur.get("name") or ""
        if not title:
            return None
        return {
            "title": title,
            "url": cur.get("url") or cur.get("link") or cur.get("resource") or "",
            "description": cur.get("description") or cur.get("desc") or cur.get("summary") or title,
        }

    entries: list[dict] = []
    current: dict[str, str] = {}
    for line in text.splitlines():
        s = line.strip()
        if not s or s == "---":
            e = flush(current)
            if e:
                entries.append(e)
            current = {}
            continue
        m = re.match(r"^([A-Za-z_][\w .-]*)\s*[:=]\s*(.+)$", s)
        if m:
            current[m.group(1).strip().lower().replace(" ", "_")] = m.group(2).strip().strip("\"'")
    e = flush(current)
    if e:
        entries.append(e)
    return entries


def _parse_anything(content: str) -> list[dict]:
    """OKF Anything fallback chain: list → JSON → key-value → URLs → line-per-row."""
    import json as _json
    import re

    entries: list[dict] = []
    pattern = re.compile(r"^\s*[-*]\s+\[([^\]]+)]\(([^)]+)\)\s*(?:—\s*(.+))?", re.MULTILINE)
    for m in pattern.finditer(content):
        entries.append({
            "title": m.group(1).strip(),
            "url": m.group(2).strip(),
            "description": (m.group(3) or m.group(1)).strip(),
        })
    if not entries:
        try:
            data = _json.loads(content)
            if isinstance(data, dict):
                data = [data]
            if isinstance(data, list):
                entries = [
                    {"title": str(d.get("title", "")), "url": str(d.get("url", "")),
                     "description": str(d.get("description") or d.get("title", ""))}
                    for d in data if isinstance(d, dict)
                ]
        except ValueError:
            pass
    if not entries:
        entries = _parse_kv(content)
    if not entries:
        for line in content.splitlines():
            m = re.match(r"^\s*(https?://\S+)\s*$", line)
            if m:
                url = m.group(1)
                entries.append({
                    "title": url.rstrip("/").split("/")[-1] or url,
                    "url": url,
                    "description": url,
                })
    if not entries:
        entries = [
            {"title": line.strip(), "url": "", "description": line.strip()}
            for line in content.splitlines()
            if line.strip()
        ]
    return entries


@mcp.tool()
def convert_to_okf(content: str, format: str = "markdown", entry_type: str = "concept") -> str:
    """Convert content into OKF-formatted Markdown entries.

    Accepts markdown link lists (`- [Title](URL) — Description`),
    JSON/YAML arrays of {title, url, description}, CSV tables with
    title/url/description columns, generic key-value blocks (format="kv"),
    plain URL lists (format="urls"), a GitHub repo URL
    (format="github" — metadata + README fetched live), or arbitrary
    text (format="anything" — walks a parser fallback chain).
    Returns the OKF entries as YAML-frontmatter Markdown, ready to
    write into an OKF bundle directory.
    """
    import re
    from datetime import datetime, timezone

    def slugify(text: str) -> str:
        return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

    def build_entry(title: str, url: str, description: str, body: str = "", tags: list[str] | None = None) -> str:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        tag_str = ", ".join(tags) if tags else slugify(title).replace("-", ", ")
        body_text = body or description
        return (
            "---\n"
            f"type: {entry_type}\n"
            f"title: {title}\n"
            f"description: {description}\n"
            f"resource: {url}\n"
            f"tags: [{tag_str}]\n"
            "generated:\n"
            "  by: awesome-okf-mcp\n"
            f"  at: {now}\n"
            "---\n\n"
            f"# {title}\n\n{description}\n\n{body_text}\n"
        )

    entries: list[dict] = []
    if format == "json":
        import json as _json
        data = _json.loads(content)
        if isinstance(data, dict):
            data = [data]
        entries = [
            {"title": d.get("title", ""), "url": d.get("url", ""), "description": d.get("description", "")}
            for d in data
        ]
    elif format == "yaml":
        import yaml as _yaml
        data = _yaml.safe_load(content)
        if isinstance(data, dict):
            data = [data]
        entries = [
            {"title": str(d.get("title", "")), "url": str(d.get("url", "")),
             "description": str(d.get("description") or d.get("title", ""))}
            for d in data if isinstance(d, dict)
        ]
    elif format == "csv":
        import csv as _csv
        import io
        reader = _csv.DictReader(io.StringIO(content))
        rows = list(reader)
        if "title" in (reader.fieldnames or []):
            for r in rows:
                title = (r.get("title") or "").strip()
                if title:
                    entries.append({
                        "title": title,
                        "url": (r.get("url") or "").strip(),
                        "description": (r.get("description") or title).strip(),
                    })
        else:
            for r in rows:
                vals = [str(v).strip() for v in r.values()]
                title = vals[0] if vals else ""
                if title:
                    entries.append({
                        "title": title,
                        "url": vals[1] if len(vals) > 1 else "",
                        "description": vals[2] if len(vals) > 2 else title,
                    })
    elif format == "kv":
        entries = _parse_kv(content)
    elif format == "anything":
        entries = _parse_anything(content)
    elif format == "github":
        import urllib.error
        import urllib.request
        import json as _json

        m = re.match(r"https?://github\.com/([^/\s]+)/([^/\s]+?)(?:/.*)?$", content.strip())
        if not m:
            return json.dumps({"error": f"not a GitHub repo URL: {content}"}, ensure_ascii=False)
        owner, repo = m.group(1), m.group(2).removesuffix(".git")

        def api(path: str, raw: bool = False) -> str:
            headers = {"User-Agent": "awesome-okf-mcp"}
            if raw:
                headers["Accept"] = "application/vnd.github.raw"
            req = urllib.request.Request(f"https://api.github.com/{path}", headers=headers)
            with urllib.request.urlopen(req, timeout=15) as r:
                return r.read().decode("utf-8")

        try:
            meta = _json.loads(api(f"repos/{owner}/{repo}"))
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            return json.dumps({"error": f"GitHub fetch failed for {owner}/{repo}: {e}"}, ensure_ascii=False)
        readme = ""
        try:
            readme = api(f"repos/{owner}/{repo}/readme", raw=True)
        except (urllib.error.HTTPError, urllib.error.URLError):
            pass
        tags = list(meta.get("topics") or [])
        if not tags and meta.get("language"):
            tags = [meta["language"].lower()]
        entries = [{
            "title": meta.get("full_name", f"{owner}/{repo}"),
            "url": meta.get("html_url", content),
            "description": meta.get("description") or meta.get("full_name", content),
            "tags": tags,
            "body": readme,
        }]
    elif format == "urls":
        for line in content.splitlines():
            m = re.match(r"^\s*(https?://\S+)\s*$", line)
            if m:
                url = m.group(1)
                entries.append({
                    "title": url.rstrip("/").split("/")[-1] or url,
                    "url": url,
                    "description": url,
                })
    else:
        pattern = re.compile(r"^\s*[-*]\s+\[([^\]]+)]\(([^)]+)\)\s*(?:—\s*(.+))?", re.MULTILINE)
        for m in pattern.finditer(content):
            entries.append({
                "title": m.group(1).strip(),
                "url": m.group(2).strip(),
                "description": (m.group(3) or m.group(1)).strip(),
            })

    if not entries:
        return json.dumps({"error": "no parseable entries found in content"}, ensure_ascii=False)

    rendered = "\n".join(
        build_entry(e["title"], e["url"], e["description"], body=e.get("body", ""), tags=e.get("tags"))
        for e in entries
    )
    return json.dumps(
        {"count": len(entries), "okf_markdown": rendered},
        ensure_ascii=False,
        indent=2,
    )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
