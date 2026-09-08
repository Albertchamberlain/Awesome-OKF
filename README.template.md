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

Zero-dependency CLI that converts various formats into OKF knowledge bundles:

| 📥 Input Format | ✨ What It Does |
|---|---|
| 📋 Markdown awesome-xx lists | Extracts `- [Title](URL) — Description` items → OKF entries |
| 📊 JSON arrays | Converts `{title, url, description}` objects → OKF entries |
| 🔗 URL lists | Plain text URL collections → OKF entries |

```bash
# One command, instant OKF bundle
python scripts/convert-to-okf.py README.md -o kb/ -t concept

# Output: kb/ with 45 Markdown files, each with YAML frontmatter
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

<!-- CATALOG:TOOLS:END -->

<!-- CATALOG:PLUGINS:START -->

<!-- CATALOG:PLUGINS:END -->

<!-- CATALOG:SKILLS:START -->

<!-- CATALOG:SKILLS:END -->

<!-- CATALOG:PROPOSALS:START -->

<!-- CATALOG:PROPOSALS:END -->

<!-- CATALOG:DOCS:START -->

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