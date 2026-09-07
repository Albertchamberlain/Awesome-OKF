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
  <img alt="Catalog" src="https://img.shields.io/badge/catalog-25%20entries-7c3aed">
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

## Catalog

> **25 curated entries** · 1 tool · 7 plugins · 7 skills · 3 proposals · 4 docs
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

## Related Lists

- [yzfly/awesome-okf](https://github.com/yzfly/awesome-okf) — the original Chinese OKF resource hub
- [OKF Specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) — official Google Cloud spec

---

<br>

<p align="center">
  <sub>MIT — see <a href="LICENSE">LICENSE</a>. Catalog descriptions link to upstream projects under their respective licenses.</sub>
</p>