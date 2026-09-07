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


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
