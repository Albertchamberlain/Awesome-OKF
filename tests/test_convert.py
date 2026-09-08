"""Tests for the standalone convert-to-okf script."""

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "convert-to-okf.py"


def _load():
    spec = importlib.util.spec_from_file_location("convert_to_okf", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_parse_markdown_links():
    mod = _load()
    entries = mod.parse_markdown_links("- [Foo](https://foo.dev) — Bar baz.\n- [Qux](https://qux.dev)\n")
    assert entries == [
        {"title": "Foo", "url": "https://foo.dev", "description": "Bar baz."},
        {"title": "Qux", "url": "https://qux.dev", "description": "Qux"},
    ]


def test_parse_url_list():
    mod = _load()
    entries = mod.parse_url_list("https://example.com/a\nnot a url\n  https://example.com/b  \n")
    assert [e["url"] for e in entries] == ["https://example.com/a", "https://example.com/b"]
    assert entries[0]["title"] == "a"


def test_parse_markdown_dir_obsidian_wikilinks(tmp_path: Path):
    mod = _load()
    note = tmp_path / "my-note.md"
    note.write_text(
        "---\ntags: [x]\n---\n# My Note\n\nSee [[Other|alias]] and [[Solo]].\n", encoding="utf-8"
    )
    hidden = tmp_path / ".obsidian" / "config.md"
    hidden.parent.mkdir(parents=True)
    hidden.write_text("# cfg", encoding="utf-8")

    entries = mod.parse_markdown_dir(tmp_path, variant="obsidian")
    assert len(entries) == 1
    e = entries[0]
    assert e["title"] == "My Note"
    assert "[[" not in e["body"]
    assert "See alias and Solo." in e["body"]
    assert e["description"] == "See alias and Solo."


def test_build_bundle_unique_slugs_and_tags(tmp_path: Path):
    mod = _load()
    entries = [
        {"title": "A", "url": "u1", "description": "d1"},
        {"title": "A", "url": "u2", "description": "d2"},
        {"title": "B", "url": "u3", "description": "d3", "tags": ["x", "y"]},
    ]
    out = mod.build_bundle(entries, tmp_path, entry_type="concept")
    assert sorted(f.name for f in out.glob("*.md")) == ["a-2.md", "a.md", "b.md"]
    assert "tags: [x, y]" in (tmp_path / "b.md").read_text(encoding="utf-8")


def test_fetch_github_rejects_non_repo_url():
    mod = _load()
    with pytest.raises(SystemExit):
        mod.fetch_github("https://example.com/not-a-repo")


def test_parse_image_prints_ocr_recipe(tmp_path: Path):
    mod = _load()
    scan = tmp_path / "scan.png"
    scan.write_bytes(b"fake")
    with pytest.raises(SystemExit) as exc:
        mod.parse_image(scan)
    msg = str(exc.value)
    assert "OCR is not bundled" in msg
    assert "paddleocr ppocr" in msg
    assert "convert-to-okf.py ocr-text/" in msg


def test_parse_csv_with_and_without_title_column():
    mod = _load()
    entries = mod.parse_csv("title,url,description\na,http://a.dev,d1\n")
    assert entries[0] == {"title": "a", "url": "http://a.dev", "description": "d1"}
    fallback = mod.parse_csv("名称,链接\n笔记1,http://n.dev\n")
    assert fallback[0]["title"] == "笔记1"
    assert fallback[0]["url"] == "http://n.dev"


def test_parse_keyvalue_blocks_and_aliases():
    mod = _load()
    text = (
        "title: Note One\nlink: http://one.dev\ndesc: First note\n"
        "---\nname: Note Two\nurl: http://two.dev\n"
    )
    entries = mod.parse_keyvalue(text)
    assert len(entries) == 2
    assert entries[0]["title"] == "Note One"
    assert entries[0]["url"] == "http://one.dev"
    assert entries[0]["description"] == "First note"
    assert entries[1]["title"] == "Note Two"
    assert entries[1]["url"] == "http://two.dev"
