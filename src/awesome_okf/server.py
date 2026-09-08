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


@mcp.tool()
def convert_to_okf(content: str, format: str = "markdown", entry_type: str = "concept") -> str:
    """Convert content into OKF-formatted Markdown entries.

    Accepts markdown link lists (`- [Title](URL) — Description`),
    JSON arrays of {title, url, description}, plain URL lists, or a
    GitHub repo URL (format="github" — metadata + README fetched live).
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
