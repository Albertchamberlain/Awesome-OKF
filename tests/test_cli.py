"""Tests for the Awesome-MCP command-line interface."""

from pathlib import Path

from typer.testing import CliRunner

from awesome_mcp.cli import app


def test_readme_check_detects_drift_without_rewriting(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[1]
    readme_path = tmp_path / "README.md"
    stale_content = "stale readme\n"
    readme_path.write_text(stale_content, encoding="utf-8")

    result = CliRunner().invoke(
        app,
        [
            "readme",
            "--catalog",
            str(project_root / "data" / "catalog.yaml"),
            "--output",
            str(readme_path),
            "--check",
        ],
    )

    assert result.exit_code == 1
    assert "README.md is out of date" in result.stdout
    assert readme_path.read_text(encoding="utf-8") == stale_content


def test_readme_check_does_not_create_missing_output(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[1]
    readme_path = tmp_path / "missing.md"

    result = CliRunner().invoke(
        app,
        [
            "readme",
            "--catalog",
            str(project_root / "data" / "catalog.yaml"),
            "--output",
            str(readme_path),
            "--check",
        ],
    )

    assert result.exit_code == 1
    assert "README.md is out of date" in result.stdout
    assert not readme_path.exists()


def test_readme_check_accepts_current_custom_output(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[1]
    readme_path = tmp_path / "README.md"
    generate_result = CliRunner().invoke(
        app,
        [
            "readme",
            "--catalog",
            str(project_root / "data" / "catalog.yaml"),
            "--output",
            str(readme_path),
        ],
    )
    current_content = readme_path.read_text(encoding="utf-8")

    result = CliRunner().invoke(
        app,
        [
            "readme",
            "--catalog",
            str(project_root / "data" / "catalog.yaml"),
            "--output",
            str(readme_path),
            "--check",
        ],
    )

    assert generate_result.exit_code == 0
    assert result.exit_code == 0
    assert "README.md is current" in result.stdout
    assert readme_path.read_text(encoding="utf-8") == current_content
