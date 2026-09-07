"""Tests for Awesome-MCP catalog tooling."""

from pathlib import Path

import pytest

from awesome_mcp.catalog import load_catalog
from awesome_mcp.readme import render_readme


@pytest.fixture
def catalog_path() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "catalog.yaml"


def test_catalog_loads(catalog_path: Path) -> None:
    catalog = load_catalog(catalog_path)
    assert len(catalog.entries) >= 20
    assert catalog.by_id("github-mcp-server") is not None


def test_search_prefers_matching_entries(catalog_path: Path) -> None:
    catalog = load_catalog(catalog_path)
    hits = catalog.search("playwright browser", kind="server")
    assert hits
    assert hits[0].id == "playwright-mcp"


def test_readme_contains_sections(catalog_path: Path) -> None:
    catalog = load_catalog(catalog_path)
    readme = render_readme(catalog)
    # Template-based generation uses HTML headings; check for content regardless of format
    assert "Awesome MCP" in readme
    assert "MCP Servers" in readme
    assert "GitHub MCP Server" in readme
    assert "Playwright MCP" in readme
