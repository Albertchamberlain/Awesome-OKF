"""CLI for browsing and maintaining the Awesome-OKF catalog."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .catalog import Kind, load_catalog
from .readme import render_readme, write_readme

app = typer.Typer(
    add_completion=False, no_args_is_help=True, help="Browse and maintain the Awesome-OKF catalog."
)
console = Console()


def _catalog_path_option(path: Optional[Path]) -> Path | None:
    return path


@app.command("stats")
def stats(
    catalog_path: Optional[Path] = typer.Option(None, "--catalog", help="Path to catalog.yaml"),
) -> None:
    """Show catalog summary counts."""
    catalog = load_catalog(catalog_path)
    data = catalog.stats()
    table = Table(title="Awesome-OKF Catalog")
    table.add_column("Metric")
    table.add_column("Count", justify="right")
    for key in ("total", "server", "client", "registry", "framework", "official"):
        if key in data:
            table.add_row(key, str(data[key]))
    console.print(table)
    console.print(f"[dim]Updated {catalog.meta.updated}[/dim]")


@app.command("list")
def list_entries(
    kind: Optional[Kind] = typer.Option(None, "--kind", "-k", help="Filter by entry kind"),
    limit: int = typer.Option(50, "--limit", "-n"),
    catalog_path: Optional[Path] = typer.Option(None, "--catalog"),
) -> None:
    """List catalog entries."""
    catalog = load_catalog(catalog_path)
    entries = catalog.by_kind(kind) if kind else list(catalog.entries)
    entries = entries[:limit]
    table = Table(title=f"Catalog entries ({len(entries)} shown)")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Kind")
    table.add_column("Category")
    for entry in entries:
        table.add_row(entry.id, entry.name, entry.kind, entry.category)
    console.print(table)


@app.command("search")
def search(
    query: str = typer.Argument(..., help="Search terms"),
    kind: Optional[Kind] = typer.Option(None, "--kind", "-k"),
    limit: int = typer.Option(10, "--limit", "-n"),
    catalog_path: Optional[Path] = typer.Option(None, "--catalog"),
) -> None:
    """Search the catalog by name, tags, and description."""
    catalog = load_catalog(catalog_path)
    hits = catalog.search(query, kind=kind, limit=limit)
    if not hits:
        console.print("[yellow]No matches.[/yellow]")
        raise typer.Exit(code=1)
    for entry in hits:
        official = " [green]official[/green]" if entry.official else ""
        console.print(f"[bold]{entry.name}[/bold] ({entry.id}) - {entry.kind}{official}")
        console.print(f"  {entry.description}")
        console.print(f"  [link={entry.url}]{entry.url}[/link]")
        if entry.tags:
            console.print(f"  tags: {', '.join(entry.tags)}")
        console.print()


@app.command("get")
def get_entry(
    entry_id: str = typer.Argument(..., help="Stable catalog id"),
    catalog_path: Optional[Path] = typer.Option(None, "--catalog"),
) -> None:
    """Show one catalog entry."""
    catalog = load_catalog(catalog_path)
    entry = catalog.by_id(entry_id)
    if entry is None:
        console.print(f"[red]Unknown id:[/red] {entry_id}")
        raise typer.Exit(code=1)
    console.print(entry)


@app.command("readme")
def generate_readme(
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="README path"),
    catalog_path: Optional[Path] = typer.Option(None, "--catalog"),
    check: bool = typer.Option(False, "--check", help="Exit 1 if README would change"),
) -> None:
    """Generate README.md from catalog.yaml."""
    catalog = load_catalog(catalog_path)
    target = output or Path("README.md")
    if check:
        expected = render_readme(catalog)
        actual = target.read_text(encoding="utf-8") if target.is_file() else None
        if actual != expected:
            console.print("[red]README.md is out of date. Run: awesome-mcp readme[/red]")
            raise typer.Exit(code=1)
        console.print(f"[green]README.md is current:[/green] {target}")
        return
    written_path = write_readme(target, catalog)
    console.print(f"Wrote [bold]{written_path}[/bold]")


@app.command("validate")
def validate(catalog_path: Optional[Path] = typer.Option(None, "--catalog")) -> None:
    """Validate catalog.yaml structure and unique ids."""
    catalog = load_catalog(catalog_path)
    seen: set[str] = set()
    for entry in catalog.entries:
        if entry.id in seen:
            console.print(f"[red]Duplicate id:[/red] {entry.id}")
            raise typer.Exit(code=1)
        seen.add(entry.id)
        if not entry.url.startswith("http"):
            console.print(f"[red]Invalid url for {entry.id}:[/red] {entry.url}")
            raise typer.Exit(code=1)
    console.print(f"[green]OK[/green] - {len(catalog.entries)} entries validated")


if __name__ == "__main__":
    app()
