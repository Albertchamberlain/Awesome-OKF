<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <img alt="Awesome OKF" src="assets/logo.svg" width="128">
  </picture>
</p>

<p align="center">
  <h1 align="center">Awesome OKF</h1>
</p>

<p align="center">
  <strong>The curated catalog of Open Knowledge Format resources.</strong>
</p>

<p align="center">
  YAML-driven. Agent-searchable. Community-curated.
</p>

<p align="center">
  <a href="https://github.com/Albertchamberlain/Awesome-OKF"><img alt="Awesome" src="https://cdn.jsdelivr.net/gh/sindresorhus/awesome@main/media/badge.svg"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-4c1?logo=open-source-initiative&logoColor=white"></a>
  <img alt="Catalog" src="https://img.shields.io/badge/catalog-29%20entries-7c3aed">
</p>

<p align="center">
  <b>English</b> | <a href="README.zh.md">中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.ko.md">한국어</a>
</p>

<br>

<p align="center">
  <a href="#catalog"><b>Catalog</b></a> &ensp;·&ensp;
  <a href="#connect-to-your-agent"><b>Connect an Agent</b></a> &ensp;·&ensp;
  <a href="#cli"><b>CLI</b></a> &ensp;·&ensp;
  <a href="#contributing"><b>Contributing</b></a>
</p>

<br>

---

## What is OKF

[Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) is an open specification by Google Cloud — define knowledge as a directory of Markdown files with YAML frontmatter and a small set of conventions. No runtime, no SDK.

## What's Different Here

Awesome OKF keeps the entire OKF ecosystem in **one validated YAML catalog**, then turns it into a browsable list, a searchable CLI, and an MCP meta-server that AI agents can query directly:

<div align="center">

```
                      catalog.yaml
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                 ▼
      README.md         CLI tools        MCP server
   (human-browsable)  (searchable)   (agent-searchable)
```

</div>

> **Edit one record. Regenerate the docs. Re-query from anywhere.**

---

## See It in Action

```text
User (or Agent):
  "Find an OKF plugin for Obsidian vault conversion."

Agent calls:
  search_catalog({
    "query": "Obsidian",
    "kind": "plugin",
    "limit": 3
  })

Awesome-OKF responds:
  ┌──────────────────────────────────────────────────────────────┐
  │ obsidian-to-okf                                plugin        │
  │ Convert Obsidian vaults to OKF — wikilinks become OKF links. │
  │ Platform: python  ·  Tags: obsidian, wikilink, markdown      │
  └──────────────────────────────────────────────────────────────┘
```

*The catalog speaks OKF.*

---

## Quick Start

### Connect to Your Agent

Add Awesome OKF to any MCP client so your agent can discover OKF resources:

```bash
pipx install awesome-okf
```

```json
{
  "mcpServers": {
    "awesome-okf": {
      "command": "awesome-okf-server"
    }
  }
}
```

### CLI

```bash
awesome-okf stats
awesome-okf list --kind plugin
awesome-okf search obsidian
awesome-okf readme
```

---

## 🛠️ Our Tools

### convert-to-okf 🔄

Zero-dependency CLI that converts content from your favorite platforms into OKF knowledge bundles:

| 📥 Input Format | ✨ What It Does |
|---|---|
| 📋 Markdown awesome-xx lists | Extracts `- [Title](URL) — Description` items → OKF entries |
| 📊 JSON arrays | Converts `{title, url, description}` objects → OKF entries |
| 🔗 URL lists | Plain text URL collections → OKF entries |
| 🧾 YAML files | Lists/mappings of `{title, url, description}` — needs pyyaml (optional) |
| 📑 CSV tables | `title/url/description` columns; first column wins when there's no title column |
| 🗂️ Key-value text | Generic `key: value` blocks — frontmatter, properties files, custom formats |
| 🐙 GitHub repos | Paste a repo URL — metadata + README fetched live → OKF entry |
| 📓 Obsidian vaults | Local vault directory → one entry per note, wikilinks resolved |
| 📝 Notion exports | Notion "Export → Markdown" directory → one entry per page |
| 🦩 Feishu docs | Feishu-exported Markdown → one entry per document |
| 🖋️ Typora notes | Plain `.md` files — point at a file or folder, done |
| 📕 PDF documents | Text layer extracted via pymupdf (optional dep); scanned pages print an OCR recipe |
| 🖼️ Scans & images | No bundled OCR — prints a ready-to-run PaddleOCR recipe instead |

```bash
# Every platform, one command
python scripts/convert-to-okf.py README.md -o kb/ -t concept
python scripts/convert-to-okf.py https://github.com/GoogleCloudPlatform/knowledge-catalog --format github -o kb/
python scripts/convert-to-okf.py my-vault/ --format obsidian -o kb/
python scripts/convert-to-okf.py notion-export/ --format notion -o kb/
python scripts/convert-to-okf.py feishu-doc.md --format feishu -o kb/

# Structured data
python scripts/convert-to-okf.py data.yaml --format yaml -o kb/   # needs: pip install pyyaml
python scripts/convert-to-okf.py table.csv --format csv -o kb/
python scripts/convert-to-okf.py notes.properties --format kv -o kb/

# Text-layer PDFs
pip install pymupdf
python scripts/convert-to-okf.py paper.pdf --format pdf -o kb/

# Scans / image-only PDFs → OKF: OCR first (your local engine, never our model), then convert
python scripts/convert-to-okf.py scan.png --format image    # prints the OCR recipe
pip install paddleocr paddlepaddle
paddleocr ppocr -i scans/ --type ocr --lang en -o ocr-text/
python scripts/convert-to-okf.py ocr-text/ --format notion -o kb/

# Output: kb/ with Markdown files, each with YAML frontmatter
# Ready for: myokf validate kb/
```

### awesome-okf CLI 🎛️

The data-driven catalog CLI (same architecture as Awesome-MCP):

| 🔍 Command | 📝 Purpose |
|---|---|
| `awesome-okf search obsidian` | Full-text search across all 29 entries |
| `awesome-okf list --kind plugin` | Filter by category |
| `awesome-okf readme` | Regenerate this README from catalog.yaml |
| `awesome-okf-server` | MCP meta-server — let AI agents query the catalog |

---

## 🔥 Popular Repositories

| 🏆 Repository | 📌 What It Offers |
|---|---|
| ⭐ [yzfly/awesome-okf](https://github.com/yzfly/awesome-okf) | 中文世界第一个 OKF 落点 — 7 plugins + 7 skills + 3 proposals |
| ⭐ [linyiru/awesome-okf](https://github.com/linyiru/awesome-okf) | English OKF resource hub — spec, tools, samples, guides |
| 📚 [GoogleCloudPlatform/knowledge-catalog](https://github.com/GoogleCloudPlatform/knowledge-catalog) | Official OKF spec, SDK, and proposals by Google |
| 🧠 [karpathy/llm-wiki](https://github.com/karpathy/llm-wiki) | The original LLM Wiki that inspired OKF |

---

## Catalog

> **29 curated entries** · 4 tools · 7 plugins · 7 skills · 5 proposals · 6 docs
> *Deliberately curated — not an exhaustive index.*

<!-- CATALOG:TOOLS:START -->

## 🛠️ Tools & CLI

### Cli

- [myokf-cli](https://github.com/yzfly/awesome-okf) `cli` — Unified CLI for OKF — pull from GitHub, validate, and package to single-file web. — `cli`, `python`, `validation`, `packaging`

### Conversion

- [convert-to-okf](https://github.com/Albertchamberlain/Awesome-OKF) `cli` — CLI tool to convert Markdown awesome-xx lists, JSON arrays, and URL lists into OKF knowledge bundles — zero dependencies, standard library only. — `conversion`, `cli`, `markdown`, `json`

### Quality

- [OKF Validator (myokf)](https://github.com/yzfly/awesome-okf) `cli` — Built-in OKF schema validator — checks YAML frontmatter, link integrity, and spec compliance. — `validation`, `quality`, `schema`

### SDK

- [OKF Python SDK](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/tools/python) ✅ `python` — Official Python SDK for reading, validating, and writing OKF bundles — referenced by Google as the reference implementation. — `sdk`, `python`, `official`

<!-- CATALOG:TOOLS:END -->

<!-- CATALOG:PLUGINS:START -->

## 🔌 Producer Plugins

### Cli

- [myokf-cli (plugin entry)](https://github.com/yzfly/awesome-okf/tree/main/plugins/myokf-cli) `python` — Unified CLI entry point wrapping all seven producer plugins. — `cli`, `aggregator`, `zero-dependency`

### Code

- [github-to-okf](https://github.com/yzfly/awesome-okf/tree/main/plugins/github-to-okf) `python` — Extract code symbols from GitHub repositories into OKF. — `github`, `code`, `symbols`, `zero-dependency`

### Document

- [feishu-to-okf](https://github.com/yzfly/awesome-okf/tree/main/plugins/feishu-to-okf) `python` — Convert Feishu (Lark) knowledge spaces and documents into OKF. — `feishu`, `lark`, `document`, `zero-dependency`
- [notion-to-okf](https://github.com/yzfly/awesome-okf/tree/main/plugins/notion-to-okf) `python` — Convert Notion Markdown exports into OKF. — `notion`, `markdown`, `zero-dependency`
- [obsidian-to-okf](https://github.com/yzfly/awesome-okf/tree/main/plugins/obsidian-to-okf) `python` — Convert Obsidian vaults to OKF — wikilinks become OKF links. — `obsidian`, `wikilink`, `markdown`, `zero-dependency`

### List

- [awesome-to-okf](https://github.com/yzfly/awesome-okf/tree/main/plugins/awesome-to-okf) `python` — Convert GitHub awesome-xx lists into structured OKF knowledge bases. — `awesome-list`, `conversion`, `zero-dependency`

### Web

- [html-to-okf](https://github.com/yzfly/awesome-okf/tree/main/plugins/html-to-okf) `python` — Convert HTML files into OKF. — `html`, `web`, `zero-dependency`

<!-- CATALOG:PLUGINS:END -->

<!-- CATALOG:SKILLS:START -->

## 🤖 Claude Code Skills

### Conversion

- [book-to-okf](https://github.com/yzfly/awesome-okf/tree/main/skills/book-to-okf) `claude-code` — Split books and long-form articles into interlinked concept knowledge bases. — `book`, `long-form`, `concepts`
- [code-to-okf](https://github.com/yzfly/awesome-okf/tree/main/skills/code-to-okf) `claude-code` — Convert codebases into OKF with Claude Code. — `code`, `repository`, `enrichment`

### Creation

- [okf-creator](https://github.com/yzfly/awesome-okf/tree/main/skills/okf-creator) `claude-code` — Create high-quality OKF knowledge bases from scratch with Claude Code. — `creation`, `knowledge-base`

### Import

- [awesome-to-okf (skill)](https://github.com/yzfly/awesome-okf/tree/main/skills/awesome-to-okf) `claude-code` — Import awesome lists and enrich them into OKF with Claude Code. — `awesome-list`, `import`, `enrichment`
- [github-to-okf (skill)](https://github.com/yzfly/awesome-okf/tree/main/skills/github-to-okf) `claude-code` — Repository to OKF enrichment workflow with Claude Code. — `github`, `repository`, `enrichment`

### Publishing

- [okf-to-book](https://github.com/yzfly/awesome-okf/tree/main/skills/okf-to-book) `claude-code` — Publish OKF knowledge bases as VitePress documentation sites. — `vitepress`, `publishing`, `docs`
- [okf-to-web](https://github.com/yzfly/awesome-okf/tree/main/skills/okf-to-web) `claude-code` — Package OKF into a single-file web page with interactive knowledge graph. — `web`, `single-file`, `knowledge-graph`

<!-- CATALOG:SKILLS:END -->

<!-- CATALOG:PROPOSALS:START -->

## 📝 Proposals & Extensions

### Upstream

- [Attested Computation Proposal](https://github.com/yzfly/awesome-okf/tree/main/proposals/attested-computation.md) `web` — Propose verifiable computation records for OKF knowledge entries. — `computation`, `verification`, `upstream`
- [Lifecycle & Staleness Proposal](https://github.com/yzfly/awesome-okf/tree/main/proposals/lifecycle-staleness.md) `web` — Propose `status` and `stale_after` lifecycle fields for OKF v0.2. — `lifecycle`, `staleness`, `upstream`
- [OKF Discovery Protocol (KEP-1)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/proposals/discovery.md) ✅ `web` — Proposal for a standard discovery mechanism that lets agents find OKF bundles without hardcoding paths. — `discovery`, `upstream`, `kep`
- [Sources & Provenance Extension](https://github.com/yzfly/awesome-okf/tree/main/proposals/sources-provenance.md) `web` — Propose `sources` field and provenance tracking for OKF v0.2. — `sources`, `provenance`, `upstream`
- [Trust Signals (KEP-2)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/proposals/trust-signals.md) ✅ `web` — Proposal for verification chains and trust tiering so consumers can distinguish machine-confirmed from human-reviewed content. — `trust`, `verification`, `upstream`, `kep`

<!-- CATALOG:PROPOSALS:END -->

<!-- CATALOG:DOCS:START -->

## 📖 Documentation & Specifications

### Example

- [Karpathy's LLM Wiki (OKF)](https://github.com/yzfly/awesome-okf/blob/main/docs/karpathy-llm-wiki-zh.md) `web` — Karpathy's LLM knowledge base converted to OKF — a real-world example of OKF in action. — `example`, `llm`, `karpathy`
- [LLM Wiki (Karpathy)](https://github.com/karpathy/llm-wiki) `web` — The original LLM knowledge base by Andrej Karpathy that inspired OKF — a living wiki of LLM concepts as Markdown files. — `example`, `llm`, `karpathy`, `inspiration`
- [OKF Market Concept](https://github.com/yzfly/awesome-okf/blob/main/docs/okf-market.md) `web` — A conceptual OKF knowledge market — imagine a marketplace where knowledge entries are traded as verifiable assets. — `market`, `concept`, `knowledge-economy`
- [OKF Super Corpus](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf-super-corpus) ✅ `web` — A large-scale example OKF bundle curated by Google Cloud — demonstrates the format at scale across multiple domains. — `example`, `large-scale`, `google`

### Guide

- [OKF Blog Post (Chinese)](https://github.com/yzfly/awesome-okf/blob/main/docs/blog-zh.md) `web` — Chinese translation of the OKF launch blog post. — `blog`, `translation`, `chinese`

### Spec

- [OKF Specification (Chinese)](https://github.com/yzfly/awesome-okf/blob/main/docs/okf-spec-zh.md) `web` — Full Chinese translation of the OKF specification, with mandatory requirements and gaps annotated. — `spec`, `translation`, `chinese`
- [OKF Specification (English)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) ✅ `web` — Official OKF specification by Google Cloud — v0.2 with sources, trust, lifecycle, and attested computation. — `spec`, `english`, `official`
- [OKF Specification (Official)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) ✅ `web` — Google's official OKF v0.2 specification — the canonical reference for the format. — `spec`, `official`, `google`

<!-- CATALOG:DOCS:END -->

---

## Data Model

```yaml
- id: obsidian-to-okf
  name: obsidian-to-okf
  kind: plugin
  category: document
  url: https://github.com/yzfly/awesome-okf/tree/main/plugins/obsidian-to-okf
  description: Convert Obsidian vaults to OKF — wikilinks become OKF links.
  platform: [python]
  official: false
  tags: [obsidian, wikilink, markdown]
```

---

## Contributing

Add or edit entries in [`data/catalog.yaml`](data/catalog.yaml), then:

```bash
awesome-okf validate
awesome-okf readme
pytest
```

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the entry schema.

---

## 🤖 For AI Agents

If you are an AI agent (Claude Code, Codex, Cursor) working on this repo, here's what you need to know:

### Project structure

```
data/catalog.yaml          # SINGLE SOURCE OF TRUTH — all entries live here
README.template.md         # English template (hand-written narrative)
README.template.zh.md      # Chinese template
README.template.ja.md      # Japanese template
README.template.ko.md      # Korean template
src/awesome_okf/           # CLI + MCP meta-server (Python)
scripts/convert-to-okf.py  # Format converter tool
```

### Rules (non-negotiable)

1. **Never edit README\*.md directly** — they are generated. Edit `data/catalog.yaml`, then regenerate.
2. **Never edit the CATALOG blocks** in templates — the `<!-- CATALOG:*:START/END -->` markers are auto-generated.
3. **Adding an entry** = append a YAML block to `data/catalog.yaml` + regenerate + run tests. Schema:
   ```yaml
   - id: kebab-case-id          # unique, never reused
     name: Human Readable Name
     kind: tool|plugin|skill|proposal|doc
     category: free-form-group
     url: https://...
     description: One sentence, no marketing fluff.
     platform: [cli|python|web|claude-code]
     official: false            # true ONLY for Google/vendor official
     tags: [3-5 short tags]
   ```
4. **Validate before commit**: `awesome-okf validate && pytest`
5. **Never create duplicate ids** — edit the existing entry in place.
6. **Multi-language**: if you touch a template, mirror the change in all four templates.

### Useful commands

```bash
awesome-okf stats                    # entry counts by kind
awesome-okf list --kind plugin       # filter by kind
awesome-okf search <query>           # full-text search
awesome-okf validate                 # schema + duplicate-id check
awesome-okf readme                   # regenerate all READMEs
awesome-okf-server                   # MCP meta-server (stdio)
```

### MCP meta-server

The catalog is exposed to agents via `awesome-okf-server` with four tools:
`search_catalog`, `list_catalog`, `get_catalog_entry`, `catalog_stats`, `convert_to_okf`.
Connect it to your MCP client to query OKF resources programmatically.

---


## Related Lists

- [yzfly/awesome-okf](https://github.com/yzfly/awesome-okf) — the original Chinese OKF resource hub
- [OKF Specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) — official Google Cloud spec

---

<br>

<p align="center">
  <sub>MIT — see <a href="LICENSE">LICENSE</a>. Catalog descriptions link to upstream projects under their respective licenses.</sub>
</p>