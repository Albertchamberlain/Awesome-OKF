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

import contextlib
import os
import re
import shutil
from collections.abc import Mapping
from pathlib import Path

from .catalog import Catalog, Kind, load_catalog

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

TEMPLATE_NAME = "README.template.md"
OUTPUT_NAME = "README.md"

# Localized READMEs: README.template.<lang>.md renders to README.<lang>.md.
# Adding a language = add its template and list its code here.
README_LANGS: tuple[str, ...] = ("zh", "ja", "ko", "ru")

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
    platform = f" `{'`, `'.join(entry.platform)}`" if getattr(entry, "platform", None) else ""
    tags = ", ".join(f"`{tag}`" for tag in entry.tags[:4])
    tag_line = f" — {tags}" if tags else ""

    return (
        f"- [{entry.name}]({entry.url}){official}{platform} — "
        f"{entry.description}{tag_line}"
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
    r"<!--\s*(CATALOG:(?:TOOLS|PLUGINS|SKILLS|PROPOSALS|DOCS)):(START|END)\s*-->"
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
# README set: one root directory, every language a sibling inside it
# ---------------------------------------------------------------------------

class ReadmeError(RuntimeError):
    """The README set cannot be rendered or written safely."""


def _check_lang(lang: str) -> str:
    """Reject language codes that are not registered in ``README_LANGS``."""
    if lang not in README_LANGS:
        raise ReadmeError(
            f"Unknown README language {lang!r}. Registered: {', '.join(README_LANGS)}."
        )
    return lang


def template_name(lang: str | None = None) -> str:
    """Template file name for ``lang`` (``None`` is the English default)."""
    return TEMPLATE_NAME if lang is None else f"README.template.{_check_lang(lang)}.md"


def output_name(lang: str | None = None) -> str:
    """README file name for ``lang`` (``None`` is the English default)."""
    return OUTPUT_NAME if lang is None else f"README.{_check_lang(lang)}.md"


def resolve_readme_root(root: Path | None = None) -> Path:
    """Resolve the single directory that holds the templates and the READMEs.

    Parameters
    ----------
    root : Path | None
        Explicit directory.  If None, the nearest directory at or above the
        current working directory that contains ``README.template.md``.

    The result never depends on where the package is installed, so a run can
    not end up writing into ``site-packages``.
    """
    if root is not None:
        resolved = root.resolve()
        if not (resolved / TEMPLATE_NAME).is_file():
            raise ReadmeError(f"{resolved} does not contain {TEMPLATE_NAME}.")
        return resolved

    cwd = Path.cwd().resolve()
    for candidate in (cwd, *cwd.parents):
        if (candidate / TEMPLATE_NAME).is_file():
            return candidate
    raise ReadmeError(
        f"No {TEMPLATE_NAME} in {cwd} or any parent directory. "
        "Run inside an Awesome-OKF checkout or pass --root."
    )


def _validate_template(text: str, source: Path) -> None:
    """Reject templates whose catalog markers would make rendering lossy.

    An unclosed START marker makes ``render_readme`` drop the rest of the file.
    """
    found = [m.groups() for line in text.splitlines() if (m := _MARKER_RE.match(line.strip()))]
    expected = [
        (name, edge) for name in sorted(KIND_TO_MARKER.values()) for edge in ("START", "END")
    ]
    # Blocks may come in any order, but each START must be followed by its own END
    blocks = sorted(zip(found[::2], found[1::2]))
    if len(found) % 2 or [marker for block in blocks for marker in block] != expected:
        raise ReadmeError(
            f"{source} must contain exactly one START/END marker pair for each of: "
            f"{', '.join(KIND_TO_MARKER.values())}."
        )


def read_template(root: Path, lang: str | None = None) -> str:
    """Read and validate the template for ``lang`` from ``root``.

    A missing template is an error: falling back to another language would
    overwrite a localized README with the wrong content.
    """
    path = root / template_name(lang)
    if not path.is_file():
        raise ReadmeError(f"Missing template {path}; {output_name(lang)} was not generated.")
    text = path.read_text(encoding="utf-8")
    _validate_template(text, path)
    return text


def render_readme_set(root: Path, catalog: Catalog) -> dict[Path, str]:
    """Render README.md and every localized README in memory.

    Nothing is written here, so a template problem in any language aborts the
    run before a single README on disk has changed.
    """
    return {
        root / output_name(lang): render_readme(catalog, template=read_template(root, lang))
        for lang in (None, *README_LANGS)
    }


def stale_readmes(rendered: Mapping[Path, str]) -> list[Path]:
    """Return the READMEs on disk that are missing or differ from ``rendered``."""
    return [
        path
        for path, text in rendered.items()
        if not path.is_file() or path.read_text(encoding="utf-8") != text
    ]


# ---------------------------------------------------------------------------
# Write to disk
# ---------------------------------------------------------------------------

def _restore(originals: Mapping[Path, bytes | None]) -> list[Path]:
    """Put back READMEs replaced by a failed run; returns those that could not be."""
    failed: list[Path] = []
    for target, original in originals.items():
        try:
            if original is None:
                target.unlink(missing_ok=True)
            else:
                target.write_bytes(original)
        except OSError:
            failed.append(target)
    return failed


def write_readme_set(rendered: Mapping[Path, str]) -> list[Path]:
    """Write already-rendered READMEs without leaving the set half-updated.

    Every file is first staged as a temporary sibling.  Targets are replaced
    (``os.replace``) only once all of them are staged, and a failed replacement
    restores the READMEs replaced before it.
    """
    staged: list[tuple[Path, Path]] = []
    replaced: dict[Path, bytes | None] = {}
    try:
        for target, text in rendered.items():
            tmp = target.with_name(f".{target.name}.{os.getpid()}.tmp")
            staged.append((tmp, target))
            tmp.write_bytes(text.encode("utf-8"))
            if target.is_file():
                shutil.copymode(target, tmp)
        for tmp, target in staged:
            original = target.read_bytes() if target.is_file() else None
            os.replace(tmp, target)
            replaced[target] = original
    except OSError as exc:
        unrestored = _restore(replaced)
        outcome = (
            f"Could not restore: {', '.join(str(path) for path in unrestored)}."
            if unrestored
            else "No README was changed."
        )
        raise ReadmeError(f"Failed to write READMEs: {exc}. {outcome}") from exc
    finally:
        for tmp, _ in staged:
            with contextlib.suppress(OSError):
                tmp.unlink(missing_ok=True)
    return list(rendered)


def _write_one(
    lang: str | None,
    path: Path | None,
    catalog: Catalog | None,
    template: str | None,
) -> Path:
    name = output_name(lang)  # validates lang before any path is built
    root = resolve_readme_root() if path is None or template is None else None
    text = template if template is not None else read_template(root, lang)
    out = path or root / name
    write_readme_set({out: render_readme(catalog or load_catalog(), template=text)})
    return out


def write_readme(
    path: Path | None = None,
    catalog: Catalog | None = None,
    template: str | None = None,
) -> Path:
    """Render and write README.md to disk.

    Parameters
    ----------
    path : Path | None
        Output path.  Defaults to ``README.md`` in the README root
        (see ``resolve_readme_root``).
    catalog : Catalog | None
        Catalog to render.  Loads the default catalog if omitted.
    template : str | None
        Template text.  Reads ``README.template.md`` from the README root if
        omitted; a missing template raises ``ReadmeError``.

    Returns
    -------
    Path
        Path to the written file.
    """
    return _write_one(None, path, catalog, template)


def write_readme_zh(
    path=None,
    catalog=None,
    template=None,
):
    """Render and write the Chinese README using README.template.zh.md."""
    return write_readme_lang("zh", path=path, catalog=catalog, template=template)


def write_readme_lang(lang: str, path=None, catalog=None, template=None):
    """Render a localized README from README.template.<lang>.md.

    ``lang`` must be registered in ``README_LANGS``; a missing template raises
    ``ReadmeError`` instead of falling back to the English one.
    """
    return _write_one(_check_lang(lang), path, catalog, template)
