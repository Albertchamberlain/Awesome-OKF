"""
Generate README.md from a hand-written template + auto-generated catalog sections.

Template markers:
  <!-- CATALOG:SERVERS:START -->
  <!-- CATALOG:SERVERS:END -->
  ...same for CLIENTS, REGISTRIES, SDKS

The markers delimit sections that are auto-generated from catalog.yaml.
Everything outside those markers is hand-maintained Markdown.
"""

from __future__ import annotations

import re
from pathlib import Path

from .catalog import Catalog, Kind, load_catalog

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

TEMPLATE_NAME = "README.template.md"
OUTPUT_NAME = "README.md"

KIND_ORDER: tuple[Kind, ...] = ("tool", "plugin", "skill", "proposal", "doc")
KIND_TO_MARKER: dict[Kind, str] = {
    "tool": "CATALOG:TOOLS",
    "plugin": "CATALOG:PLUGINS",
    "skill": "CATALOG:SKILLS",
    "proposal": "CATALOG:PROPOSALS",
    "doc": "CATALOG:DOCS",
}

KIND_EMOJI: dict[str, str] = {
    "tool": "🛠️",
    "plugin": "🔌",
    "skill": "🤖",
    "proposal": "📝",
    "doc": "📖",
}


# ---------------------------------------------------------------------------
# Entry formatting
# ---------------------------------------------------------------------------

def _format_entry(entry, *, show_kind: bool = False) -> str:
    """Format a single catalog entry as a Markdown list item."""
    official = " ✅" if entry.official else ""
    transport = f" `{'`, `'.join(entry.transport)}`" if entry.transport else ""
    tags = ", ".join(f"`{tag}`" for tag in entry.tags[:4])
    tag_line = f" — {tags}" if tags else ""

    return (
        f"- [{entry.name}]({entry.url}){official}{transport} — "
        f"{entry.description}{tag_line}{platform}"
    )


# ---------------------------------------------------------------------------
# Section generation (one per kind: server / client / registry / framework)
# ---------------------------------------------------------------------------

def _section_for_kind(catalog: Catalog, kind: Kind) -> str:
    """Generate the full Markdown section for one kind of entry."""
    label = catalog.categories.get(kind, {}).get("label", kind.title())
    emoji = KIND_EMOJI.get(kind, "")

    lines: list[str] = [
        f"## {emoji} {label}",
        "",
    ]

    entries = catalog.by_kind(kind)
    if not entries:
        lines.append("_No entries yet._")
        lines.append("")
        return "\n".join(lines)

    # Group entries by category
    grouped: dict[str, list] = {}
    for entry in entries:
        grouped.setdefault(entry.category, []).append(entry)

    for category in sorted(grouped):
        # Fix display name: "developer-tools" → "Developer Tools"
        display = category.replace("-", " ").title()
        # Fix known abbreviations
        display = display.replace("Ai", "AI").replace("Ide", "IDE").replace("Sdk", "SDK")

        lines.append(f"### {display}")
        lines.append("")

        for entry in sorted(grouped[category], key=lambda item: item.name.lower()):
            lines.append(_format_entry(entry))
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Template-based rendering
# ---------------------------------------------------------------------------

_MARKER_RE = re.compile(
    r"<!--\s*(CATALOG:(?:SERVERS|CLIENTS|REGISTRIES|SDKS)):(START|END)\s*-->"
)


def render_readme(
    catalog: Catalog,
    template: str | None = None,
) -> str:
    """Render the full README from a template, replacing marker sections with
    auto-generated catalog content.

    Parameters
    ----------
    catalog : Catalog
        The loaded catalog.
    template : str | None
        Template text.  If None, reads ``README.template.md`` from the repo root.

    Returns
    -------
    str
        The complete README Markdown.
    """
    if template is None:
        template_path = Path(__file__).resolve().parents[2] / TEMPLATE_NAME
        if template_path.is_file():
            template = template_path.read_text(encoding="utf-8")
        else:
            # Fallback: pure auto-generated README (backward-compatible)
            return _render_fallback(catalog)

    lines = template.splitlines(keepends=True)
    result: list[str] = []

    i = 0
    inside: str | None = None  # marker name when inside a block, or None

    while i < len(lines):
        line = lines[i]
        m = _MARKER_RE.match(line.strip())
        if m:
            marker_name = m.group(1)       # e.g. "CATALOG:SERVERS"
            marker_kind = m.group(2)        # "START" or "END"

            if marker_kind == "START" and inside is None:
                # Entering an auto-generated block
                inside = marker_name
                result.append(line)         # preserve the START marker
                # Map marker name back to kind
                kind_map = {v: k for k, v in KIND_TO_MARKER.items()}
                kind = kind_map.get(marker_name)
                if kind:
                    result.append("\n")
                    result.append(_section_for_kind(catalog, kind))
                    result.append("\n")
                i += 1
            elif marker_kind == "END" and inside == marker_name:
                # Exiting the block
                inside = None
                result.append(line)         # preserve the END marker
                i += 1
            else:
                # Mismatched marker — pass through verbatim to avoid data loss
                result.append(line)
                i += 1
        elif inside is not None:
            # Skip lines inside the marker block (replaced by generated content)
            i += 1
        else:
            result.append(line)
            i += 1

    return "".join(result)


def _render_fallback(catalog: Catalog) -> str:
    """Pure auto-generated README — used when no template file exists."""
    stats = catalog.stats()
    body: list[str] = [
        "# Awesome-MCP",
        "",
        "![Awesome](https://cdn.jsdelivr.net/gh/sindresorhus/awesome@main/media/badge.svg)",
        "",
        "A **maintainable** curated list of Model Context Protocol (MCP) servers, "
        "clients, registries, and SDKs.",
        "",
        "Unlike a hand-edited markdown wall, this repo stores entries in "
        "[`data/catalog.yaml`](data/catalog.yaml) and ships tooling to **search**, "
        "**validate**, and **serve** the catalog as an MCP meta-server.",
        "",
        f"- **{stats['total']}** curated entries",
        f"- **{stats.get('server', 0)}** servers · "
        f"**{stats.get('client', 0)}** clients · "
        f"**{stats.get('registry', 0)}** registries · "
        f"**{stats.get('framework', 0)}** SDKs/tools",
        f"- **{stats.get('official', 0)}** official / reference projects",
        f"- Catalog updated: `{catalog.meta.updated}`",
        "",
        "## Quick Start",
        "",
        "```bash",
        "git clone https://github.com/Albertchamberlain/Awesome-MCP.git",
        "cd Awesome-MCP",
        "pip install -e .",
        "",
        "# CLI",
        "awesome-mcp stats",
        "awesome-mcp list --kind server",
        "awesome-mcp search playwright",
        "",
        "# Regenerate README from catalog.yaml",
        "awesome-mcp readme",
        "",
        "# Run the meta MCP server (search this catalog from any MCP client)",
        "awesome-mcp-server",
        "```",
        "",
        "## MCP Meta-Server",
        "",
        "This repo includes a small MCP server that exposes the catalog to agents:",
        "",
        "| Tool | Description |",
        "|---|---|",
        "| `search_catalog` | Full-text search across names, tags, and descriptions |",
        "| `list_catalog` | List entries filtered by kind (`server`, `client`, …) |",
        "| `get_catalog_entry` | Fetch one entry by stable `id` |",
        "| `catalog_stats` | Summary counts |",
        "",
        "**Cursor / Claude Desktop config example:**",
        "",
        "```json",
        "{",
        '  "mcpServers": {',
        '    "awesome-mcp": {',
        '      "command": "awesome-mcp-server",',
        '      "args": []',
        "    }",
        "  }",
        "}",
        "```",
        "",
        "## Contents",
        "",
    ]

    for kind in KIND_ORDER:
        body.append(_section_for_kind(catalog, kind))

    body.extend([
        "## Contributing",
        "",
        "Add or edit entries in [`data/catalog.yaml`](data/catalog.yaml), then run:",
        "",
        "```bash",
        "awesome-mcp readme",
        "pytest",
        "```",
        "",
        "See [CONTRIBUTING.md](CONTRIBUTING.md) for the entry schema and review checklist.",
        "",
        "## Related Lists",
        "",
        "- [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) — "
        "official reference servers",
        "- [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) — "
        "large community list",
        "- [MCP Registry](https://registry.modelcontextprotocol.io) — official registry",
        "",
        "## License",
        "",
        "MIT — see [LICENSE](LICENSE). Catalog descriptions link to upstream projects "
        "under their respective licenses.",
        "",
    ])

    return "\n".join(body)


# ---------------------------------------------------------------------------
# Write to disk
# ---------------------------------------------------------------------------

def write_readme(
    path: Path | None = None,
    catalog: Catalog | None = None,
    template: str | None = None,
) -> Path:
    """Render and write README.md to disk.

    Parameters
    ----------
    path : Path | None
        Output path.  Defaults to ``REPO_ROOT/README.md``.
    catalog : Catalog | None
        Catalog to render.  Loads the default catalog if omitted.
    template : str | None
        Template text.  Reads ``README.template.md`` if omitted.

    Returns
    -------
    Path
        Path to the written file.
    """
    resolved_catalog = catalog or load_catalog()
    readme_path = path or (Path(__file__).resolve().parents[2] / OUTPUT_NAME)
    readme_path.write_text(
        render_readme(resolved_catalog, template=template),
        encoding="utf-8",
        newline="\n",
    )
    return readme_path
