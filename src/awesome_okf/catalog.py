"""Load and search the Awesome-MCP YAML catalog."""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

import yaml

Kind = Literal["tool", "skill", "plugin", "proposal", "doc"]
Platform = Literal["cli", "python", "web", "claude-code"]


@dataclass(frozen=True)
class CatalogEntry:
    id: str
    name: str
    kind: Kind
    category: str
    url: str
    description: str
    platform: tuple[str, ...] = ()
    official: bool = False
    tags: tuple[str, ...] = ()


@dataclass(frozen=True)
class CatalogMeta:
    version: int
    updated: str
    description: str


@dataclass(frozen=True)
class Catalog:
    meta: CatalogMeta
    categories: dict[str, dict[str, str]]
    entries: tuple[CatalogEntry, ...] = field(default_factory=tuple)

    def by_kind(self, kind: Kind) -> list[CatalogEntry]:
        return [entry for entry in self.entries if entry.kind == kind]

    def by_id(self, entry_id: str) -> CatalogEntry | None:
        for entry in self.entries:
            if entry.id == entry_id:
                return entry
        return None

    def search(self, query: str, *, kind: Kind | None = None, limit: int = 20) -> list[CatalogEntry]:
        if not query.strip():
            return []
        tokens = [token.lower() for token in query.split() if token.strip()]
        results: list[tuple[int, CatalogEntry]] = []
        for entry in self.entries:
            if kind is not None and entry.kind != kind:
                continue
            haystack = " ".join(
                [
                    entry.id,
                    entry.name,
                    entry.category,
                    entry.description,
                    " ".join(entry.tags),
                ]
            ).lower()
            score = sum(1 for token in tokens if token in haystack)
            if score:
                if entry.official:
                    score += 1
                results.append((score, entry))
        results.sort(key=lambda item: (-item[0], item[1].name.lower()))
        return [entry for _, entry in results[:limit]]

    def stats(self) -> dict[str, int]:
        counts: dict[str, int] = {"total": len(self.entries)}
        for entry in self.entries:
            counts[entry.kind] = counts.get(entry.kind, 0) + 1
            counts[f"category:{entry.category}"] = counts.get(f"category:{entry.category}", 0) + 1
        counts["official"] = sum(1 for entry in self.entries if entry.official)
        return counts


def default_catalog_path() -> Path:
    bundled = Path(__file__).resolve().parent / "catalog.yaml"
    if bundled.is_file():
        return bundled
    return Path(__file__).resolve().parents[2] / "data" / "catalog.yaml"


def _parse_entry(raw: dict[str, Any]) -> CatalogEntry:
    return CatalogEntry(
        id=str(raw["id"]),
        name=str(raw["name"]),
        kind=raw["kind"],
        category=str(raw.get("category", "misc")),
        url=str(raw["url"]),
        description=str(raw["description"]),
        platform=tuple(str(item) for item in raw.get("platform", [])),
        official=bool(raw.get("official", False)),
        tags=tuple(str(item) for item in raw.get("tags", [])),
    )


def load_catalog(path: Path | None = None) -> Catalog:
    catalog_path = path or default_catalog_path()
    if not catalog_path.is_file():
        raise FileNotFoundError(f"Catalog not found: {catalog_path}")

    payload = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
    meta_raw = payload.get("meta", {})
    meta = CatalogMeta(
        version=int(meta_raw.get("version", 1)),
        updated=str(meta_raw.get("updated", "")),
        description=str(meta_raw.get("description", "")),
    )
    entries = tuple(_parse_entry(item) for item in payload.get("entries", []))
    categories = dict(payload.get("categories", {}))
    return Catalog(meta=meta, categories=categories, entries=entries)


@lru_cache(maxsize=4)
def get_catalog(path_str: str | None = None) -> Catalog:
    path = Path(path_str) if path_str else None
    return load_catalog(path)
