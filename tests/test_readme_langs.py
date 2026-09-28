"""Localized READMEs stay in sync with their templates and link to each other."""

from __future__ import annotations

from pathlib import Path

import pytest

from awesome_okf.catalog import load_catalog
from awesome_okf.readme import README_LANGS, render_readme

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ["README.template.md", *(f"README.template.{lang}.md" for lang in README_LANGS)]


def test_every_template_on_disk_is_registered() -> None:
    on_disk = {path.name for path in ROOT.glob("README.template*.md")}
    assert on_disk == set(TEMPLATES)


@pytest.mark.parametrize("lang", README_LANGS)
def test_localized_readme_matches_its_template(lang: str) -> None:
    template = (ROOT / f"README.template.{lang}.md").read_text(encoding="utf-8")
    generated = (ROOT / f"README.{lang}.md").read_text(encoding="utf-8")
    assert render_readme(load_catalog(), template=template) == generated


@pytest.mark.parametrize("template_name", TEMPLATES)
def test_language_switcher_lists_every_language(template_name: str) -> None:
    text = (ROOT / template_name).read_text(encoding="utf-8")
    own = template_name.removeprefix("README.template.").removesuffix("md").rstrip(".")
    for lang in ("", *README_LANGS):
        if lang == own:
            continue  # the current language is shown in bold, not as a link
        target = f"README.{lang}.md" if lang else "README.md"
        assert f'href="{target}"' in text, f"{template_name} does not link to {target}"


@pytest.mark.parametrize("template_name", TEMPLATES)
def test_catalog_markers_are_intact(template_name: str) -> None:
    text = (ROOT / template_name).read_text(encoding="utf-8")
    for kind in ("TOOLS", "PLUGINS", "SKILLS", "PROPOSALS", "DOCS"):
        assert text.count(f"<!-- CATALOG:{kind}:START -->") == 1
        assert text.count(f"<!-- CATALOG:{kind}:END -->") == 1
