"""`awesome-okf readme` writes the whole README set into one directory, or nothing."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

from awesome_okf.catalog import load_catalog
from awesome_okf.cli import app
from awesome_okf.readme import (
    README_LANGS,
    ReadmeError,
    output_name,
    render_readme,
    render_readme_set,
    template_name,
    write_readme,
    write_readme_lang,
    write_readme_set,
    write_readme_zh,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = [output_name(lang) for lang in (None, *README_LANGS)]

runner = CliRunner()


@pytest.fixture
def checkout(tmp_path: Path) -> Path:
    """A throwaway checkout: the real templates plus READMEs generated from them."""
    root = tmp_path / "checkout"
    root.mkdir()
    for template in ROOT.glob("README.template*.md"):
        shutil.copy(template, root / template.name)
    write_readme_set(render_readme_set(root, load_catalog()))
    return root


@pytest.fixture
def elsewhere(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """An unrelated working directory outside any checkout."""
    cwd = tmp_path / "elsewhere"
    cwd.mkdir()
    monkeypatch.chdir(cwd)
    return cwd


def _snapshot(directory: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(directory)): path.read_bytes()
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    }


def _make_stale(root: Path) -> dict[str, bytes]:
    for name in OUTPUTS:
        (root / name).write_text(f"stale {name}\n", encoding="utf-8")
    return _snapshot(root)


def _reported_stale(output: str) -> set[str]:
    prefix = "Out of date: "
    return {Path(line[len(prefix):]).name for line in output.splitlines() if line.startswith(prefix)}


# ---------------------------------------------------------------------------
# One output directory, whatever the cwd
# ---------------------------------------------------------------------------

def test_run_from_subdirectory_writes_every_language_into_the_root(
    checkout: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _make_stale(checkout)
    nested = checkout / "src" / "pkg"
    nested.mkdir(parents=True)
    monkeypatch.chdir(nested)

    result = runner.invoke(app, ["readme"])

    assert result.exit_code == 0, result.output
    expected = render_readme_set(checkout, load_catalog())
    assert {path.name for path in expected} == set(OUTPUTS)
    for path, text in expected.items():
        assert path.read_text(encoding="utf-8") == text
    assert list(nested.iterdir()) == []


def test_run_outside_a_checkout_fails_and_writes_nothing(elsewhere: Path) -> None:
    result = runner.invoke(app, ["readme"])

    assert result.exit_code == 2
    assert "README.template.md" in result.output
    assert list(elsewhere.iterdir()) == []


def test_root_option_selects_the_directory(checkout: Path, elsewhere: Path) -> None:
    _make_stale(checkout)

    result = runner.invoke(app, ["readme", "--root", str(checkout)])

    assert result.exit_code == 0, result.output
    for path, text in render_readme_set(checkout, load_catalog()).items():
        assert path.read_text(encoding="utf-8") == text
    assert list(elsewhere.iterdir()) == []


def test_root_without_templates_is_rejected(elsewhere: Path) -> None:
    result = runner.invoke(app, ["readme", "--root", str(elsewhere)])

    assert result.exit_code == 2
    assert list(elsewhere.iterdir()) == []


# ---------------------------------------------------------------------------
# Installed-package layout (no templates next to the package)
# ---------------------------------------------------------------------------

def _run_installed(venv: Path, cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    site_packages = venv / "lib" / "site-packages"
    script = (
        "import sys, awesome_okf\n"
        f"assert awesome_okf.__file__.startswith({str(site_packages)!r}), awesome_okf.__file__\n"
        "from awesome_okf.cli import app\n"
        "app()\n"
    )
    env = {**os.environ, "PYTHONPATH": str(site_packages), "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.run(
        [sys.executable, "-c", script, *args],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture
def venv(tmp_path: Path) -> Path:
    """The package as a wheel would install it: code + bundled catalog, no templates."""
    root = tmp_path / "venv"
    package = root / "lib" / "site-packages" / "awesome_okf"
    shutil.copytree(
        ROOT / "src" / "awesome_okf", package, ignore=shutil.ignore_patterns("__pycache__")
    )
    shutil.copy(ROOT / "data" / "catalog.yaml", package / "catalog.yaml")
    return root


def test_installed_package_outside_a_checkout_touches_nothing(venv: Path, tmp_path: Path) -> None:
    cwd = tmp_path / "elsewhere"
    cwd.mkdir()
    before = _snapshot(venv)

    result = _run_installed(venv, cwd, "readme")

    assert result.returncode == 2, result.stdout + result.stderr
    assert "README.template.md" in result.stdout
    assert _snapshot(venv) == before
    assert list(cwd.iterdir()) == []


def test_installed_package_writes_into_the_checkout_only(venv: Path, checkout: Path) -> None:
    _make_stale(checkout)
    before = _snapshot(venv)

    result = _run_installed(venv, checkout, "readme")

    assert result.returncode == 0, result.stdout + result.stderr
    for path, text in render_readme_set(checkout, load_catalog()).items():
        assert path.read_text(encoding="utf-8") == text
    assert _snapshot(venv) == before


# ---------------------------------------------------------------------------
# --check
# ---------------------------------------------------------------------------

def test_check_passes_when_every_readme_is_current(
    checkout: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(checkout)

    result = runner.invoke(app, ["readme", "--check"])

    assert result.exit_code == 0, result.output
    assert _reported_stale(result.output) == set()


def test_check_names_each_stale_localized_readme(
    checkout: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(checkout)
    (checkout / "README.ru.md").write_text("edited by hand\n", encoding="utf-8")
    (checkout / "README.ja.md").unlink()
    before = _snapshot(checkout)

    result = runner.invoke(app, ["readme", "--check"])

    assert result.exit_code == 1
    assert _reported_stale(result.output) == {"README.ru.md", "README.ja.md"}
    assert _snapshot(checkout) == before


# ---------------------------------------------------------------------------
# Missing or broken templates fail closed
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("args", [["readme"], ["readme", "--check"]])
def test_missing_localized_template_fails_without_writing(
    checkout: Path, monkeypatch: pytest.MonkeyPatch, args: list[str]
) -> None:
    monkeypatch.chdir(checkout)
    (checkout / "README.template.ru.md").unlink()
    before = _make_stale(checkout)

    result = runner.invoke(app, args)

    assert result.exit_code == 2
    assert "README.template.ru.md" in result.output
    assert _snapshot(checkout) == before


def test_write_readme_lang_does_not_fall_back_to_english(
    checkout: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(checkout)
    (checkout / "README.template.zh.md").unlink()
    before = _make_stale(checkout)

    with pytest.raises(ReadmeError, match="README.template.zh.md"):
        write_readme_lang("zh", catalog=load_catalog())
    with pytest.raises(ReadmeError, match="README.template.zh.md"):
        write_readme_zh(catalog=load_catalog())

    assert _snapshot(checkout) == before


def test_unbalanced_catalog_markers_fail_without_writing(
    checkout: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(checkout)
    template = checkout / "README.template.ja.md"
    text = template.read_text(encoding="utf-8")
    template.write_text(text.replace("<!-- CATALOG:TOOLS:END -->", ""), encoding="utf-8")
    before = _make_stale(checkout)

    result = runner.invoke(app, ["readme"])

    assert result.exit_code == 2
    assert "README.template.ja.md" in result.output
    assert _snapshot(checkout) == before


# ---------------------------------------------------------------------------
# Language codes
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("lang", ["en", "RU", "", "../../etc/passwd", "ru/../zh"])
def test_unregistered_language_is_rejected(
    checkout: Path, monkeypatch: pytest.MonkeyPatch, lang: str
) -> None:
    monkeypatch.chdir(checkout)
    before = _snapshot(checkout)

    for build_name in (template_name, output_name):
        with pytest.raises(ReadmeError, match="Unknown README language"):
            build_name(lang)
    with pytest.raises(ReadmeError, match="Unknown README language"):
        write_readme_lang(lang, catalog=load_catalog(), template="# injected\n")

    assert _snapshot(checkout) == before


# ---------------------------------------------------------------------------
# Partial write failure
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("failing_call", range(1, len(OUTPUTS) + 1))
def test_failed_replace_leaves_the_whole_set_untouched(
    checkout: Path, monkeypatch: pytest.MonkeyPatch, failing_call: int
) -> None:
    monkeypatch.chdir(checkout)
    before = _make_stale(checkout)
    real_replace = os.replace
    calls: list[str] = []

    def flaky_replace(src, dst) -> None:
        calls.append(str(dst))
        if len(calls) == failing_call:
            raise OSError("disk full")
        real_replace(src, dst)

    monkeypatch.setattr("awesome_okf.readme.os.replace", flaky_replace)

    result = runner.invoke(app, ["readme"])

    assert result.exit_code == 2
    assert "disk full" in result.output
    assert len(calls) == failing_call
    assert _snapshot(checkout) == before  # also proves no temp files are left behind


def test_failed_staging_leaves_the_whole_set_untouched(
    checkout: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(checkout)
    before = _make_stale(checkout)
    real_write_bytes = Path.write_bytes

    def flaky_write_bytes(self: Path, data: bytes) -> int:
        if "README.ko.md" in self.name:
            raise OSError("read-only file system")
        return real_write_bytes(self, data)

    monkeypatch.setattr(Path, "write_bytes", flaky_write_bytes)

    result = runner.invoke(app, ["readme"])

    assert result.exit_code == 2
    assert "No README was changed" in result.output
    assert _snapshot(checkout) == before


def test_readme_that_did_not_exist_is_removed_on_rollback(checkout: Path) -> None:
    (checkout / "README.md").unlink()
    (checkout / "README.ru.md").unlink()
    (checkout / "README.ru.md").mkdir()  # cannot be replaced by a file
    before = _snapshot(checkout)

    with pytest.raises(ReadmeError):
        write_readme_set(render_readme_set(checkout, load_catalog()))

    assert not (checkout / "README.md").exists()
    assert _snapshot(checkout) == before


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX permission bits")
def test_replacing_a_readme_keeps_its_permissions(checkout: Path) -> None:
    target = checkout / "README.ru.md"
    target.write_text("stale\n", encoding="utf-8")
    target.chmod(0o640)

    write_readme_set(render_readme_set(checkout, load_catalog()))

    assert target.stat().st_mode & 0o777 == 0o640


# ---------------------------------------------------------------------------
# --output: the English README only
# ---------------------------------------------------------------------------

def test_output_writes_only_the_english_readme(
    checkout: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(checkout)
    before = _make_stale(checkout)
    export = tmp_path / "export"
    export.mkdir()

    result = runner.invoke(app, ["readme", "--output", str(export / "EN.md")])

    assert result.exit_code == 0, result.output
    english = (checkout / "README.template.md").read_text(encoding="utf-8")
    assert _snapshot(export) == {
        "EN.md": render_readme(load_catalog(), template=english).encode("utf-8")
    }
    assert _snapshot(checkout) == before


def test_output_check_covers_only_that_file(
    checkout: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(checkout)
    target = tmp_path / "EN.md"
    shutil.copy(checkout / "README.md", target)
    _make_stale(checkout)  # stale READMEs in the checkout are not part of this check

    current = runner.invoke(app, ["readme", "--output", str(target), "--check"])
    target.write_text("edited by hand\n", encoding="utf-8")
    stale = runner.invoke(app, ["readme", "--output", str(target), "--check"])

    assert current.exit_code == 0, current.output
    assert stale.exit_code == 1
    assert _reported_stale(stale.output) == {"EN.md"}
    assert target.read_text(encoding="utf-8") == "edited by hand\n"


def test_output_into_a_missing_directory_fails_cleanly(
    checkout: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(checkout)

    result = runner.invoke(app, ["readme", "--output", str(tmp_path / "missing" / "README.md")])

    assert result.exit_code == 2
    assert not (tmp_path / "missing").exists()


def test_write_readme_defaults_to_the_root_of_the_cwd(
    checkout: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _make_stale(checkout)
    nested = checkout / "docs"
    nested.mkdir()
    monkeypatch.chdir(nested)

    written = write_readme(catalog=load_catalog())

    english = (checkout / "README.template.md").read_text(encoding="utf-8")
    assert written == checkout.resolve() / "README.md"
    assert written.read_text(encoding="utf-8") == render_readme(load_catalog(), template=english)
    assert list(nested.iterdir()) == []
