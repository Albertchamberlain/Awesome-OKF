# Changelog

All notable changes to Awesome-OKF will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **OKF Anything** concept — anything readable → OKF in three stages: Extract → Normalize → Bundle
- `--format anything` fallback chain: list → JSON → key-value → URLs → line-per-row
- `convert-to-okf` input coverage: GitHub, Obsidian, Notion, Feishu, Typora, YAML, CSV, key-value, text-layer PDF (pymupdf), OCR recipes for scans (PaddleOCR)
- MCP `convert_to_okf` formats: github, urls, yaml, csv, kv, anything
- `convert-to-okf` CLI — convert Markdown lists, JSON arrays, and URL lists into OKF bundles
- Multi-language README (English, 中文, 日本語, 한국어)
- "For AI Agents" section — agent-oriented contribution guide
- OKF logo (light/dark variants)

### Removed
- Star history chart (per maintainer request)

## [0.1.0] - 2026-09-07

### Added
- Initial release: data-driven OKF catalog with 29 entries
  - 4 tools (myokf-cli, OKF Validator, Python SDK, convert-to-okf)
  - 7 producer plugins (Feishu, Obsidian, Notion, GitHub, awesome, HTML, CLI)
  - 7 Claude Code skills (creation, import, conversion, publishing)
  - 5 proposals (sources, trust, lifecycle, discovery, computation)
  - 6 docs (specs, blog, examples)
- Catalog architecture: single-source `data/catalog.yaml` driving README, CLI, and MCP meta-server
- `awesome-okf` CLI: stats, list, search, validate, readme
- MCP meta-server: search_catalog, list_catalog, get_catalog_entry, catalog_stats
- Template-based README generation with CATALOG markers
