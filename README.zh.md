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
  <strong>开放知识格式（OKF）精选资源目录。</strong>
</p>

<p align="center">
  YAML 驱动 · Agent 可搜索 · 社区共建
</p>

<p align="center">
  <a href="https://github.com/Albertchamberlain/Awesome-OKF"><img alt="Awesome" src="https://cdn.jsdelivr.net/gh/sindresorhus/awesome@main/media/badge.svg"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-4c1?logo=open-source-initiative&logoColor=white"></a>
  <img alt="Catalog" src="https://img.shields.io/badge/catalog-29%20entries-7c3aed">
</p>

<p align="center">
  <a href="README.md">English</a> | <b>中文</b> | <a href="README.ja.md">日本語</a> | <a href="README.ko.md">한국어</a>
</p>

<br>

<p align="center">
  <a href="#catalog"><b>目录</b></a> &ensp;·&ensp;
  <a href="#connect-to-your-agent"><b>接入 Agent</b></a> &ensp;·&ensp;
  <a href="#cli"><b>CLI</b></a> &ensp;·&ensp;
  <a href="#contributing"><b>贡献</b></a>
</p>

<br>

---

## 什么是 OKF

[开放知识格式（OKF）](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) 是 Google Cloud 发布的一份开放规范——把知识定义为一个目录的 Markdown 文件，带 YAML frontmatter，加一小套约定。没有运行时，没有 SDK。

## 本项目有何不同

Awesome OKF 把整个 OKF 生态收进**一个经过校验的 YAML 目录**，然后生成可浏览的列表、可搜索的 CLI，以及一个 AI Agent 可以直接查询的 MCP meta-server：

<div align="center">

```
                      catalog.yaml
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                 ▼
      README.md         CLI 工具        MCP 服务
    （人类可浏览）     （可搜索）    （Agent 可查询）
```

</div>

> **改一条记录。重新生成文档。随处查询。**

---

## 效果演示

```text
用户（或 Agent）：
  "找一个能把 Obsidian 仓库转成 OKF 的插件。"

Agent 调用：
  search_catalog({
    "query": "Obsidian",
    "kind": "plugin",
    "limit": 3
  })

Awesome-OKF 返回：
  ┌──────────────────────────────────────────────────────────────┐
  │ obsidian-to-okf                                plugin        │
  │ 将 Obsidian vault 转为 OKF——wikilink 变成 OKF 链接。          │
  │ 平台: python  ·  标签: obsidian, wikilink, markdown          │
  └──────────────────────────────────────────────────────────────┘
```

*让目录开口说 OKF。*

---

## 快速开始

### 接入你的 Agent

把 Awesome OKF 添加到任意 MCP 客户端，让 Agent 能发现 OKF 资源：

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

## 🛠️ 我们的工具

### convert-to-okf 🔄

零依赖 CLI，把各种格式转成 OKF 知识库：

| 📥 输入格式 | ✨ 功能 |
|---|---|
| 📋 Markdown awesome 列表 | 提取 `- [标题](URL) — 描述` 条目 → OKF 条目 |
| 📊 JSON 数组 | 转换 `{title, url, description}` 对象 → OKF 条目 |
| 🔗 URL 列表 | 纯文本 URL 集合 → OKF 条目 |

```bash
# 一条命令，即刻生成 OKF 知识库
python scripts/convert-to-okf.py README.md -o kb/ -t concept

# 输出：kb/ 目录下 45 个带 YAML frontmatter 的 Markdown 文件
# 可直接：myokf validate kb/
```

### awesome-okf CLI 🎛️

数据驱动的目录 CLI（与 Awesome-MCP 同架构）：

| 🔍 命令 | 📝 用途 |
|---|---|
| `awesome-okf search obsidian` | 全目录全文搜索 |
| `awesome-okf list --kind plugin` | 按类别筛选 |
| `awesome-okf readme` | 从 catalog.yaml 重新生成 README |
| `awesome-okf-server` | MCP meta-server——让 AI Agent 查询目录 |

---

## 🔥 热门仓库

| 🏆 仓库 | 📌 内容 |
|---|---|
| ⭐ [yzfly/awesome-okf](https://github.com/yzfly/awesome-okf) | 中文世界第一个 OKF 落点 — 7 插件 + 7 Skill + 3 提案 |
| ⭐ [linyiru/awesome-okf](https://github.com/linyiru/awesome-okf) | 英文 OKF 资源中心 — 规范、工具、示例、指南 |
| 📚 [GoogleCloudPlatform/knowledge-catalog](https://github.com/GoogleCloudPlatform/knowledge-catalog) | Google 官方 OKF 规范、SDK 与提案 |
| 🧠 [karpathy/llm-wiki](https://github.com/karpathy/llm-wiki) | 启发 OKF 的 LLM Wiki |

---

## 目录

> **29 条精选资源** · 4 工具 · 7 插件 · 7 Skill · 5 提案 · 6 文档
> *精挑细选——不是穷尽索引。*

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

## 数据模型

```yaml
- id: obsidian-to-okf
  name: obsidian-to-okf
  kind: plugin
  category: document
  url: https://github.com/yzfly/awesome-okf/tree/main/plugins/obsidian-to-okf
  description: 将 Obsidian vault 转为 OKF——wikilink 变成 OKF 链接。
  platform: [python]
  official: false
  tags: [obsidian, wikilink, markdown]
```

---

## 贡献

在 [`data/catalog.yaml`](data/catalog.yaml) 中添加或编辑条目，然后：

```bash
awesome-okf validate
awesome-okf readme
pytest
```

详见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。
---

## 🤖 写给 AI Agent

如果你是在本仓库工作的 AI Agent（Claude Code、Codex、Cursor），这是你需要知道的：

```
data/catalog.yaml          # 唯一数据源——所有条目在这里
README.template.md         # 英文模板（手写叙事）
README.template.zh.md      # 中文模板
README.template.ja.md      # 日文模板
README.template.ko.md      # 韩文模板
src/awesome_okf/           # CLI + MCP meta-server
scripts/convert-to-okf.py  # 格式转换工具
```

**规则（不可违反）：**

1. **永远不要直接编辑 README\*.md**——它们是生成的。改 `data/catalog.yaml` 后运行 `awesome-okf readme`。
2. **不要编辑模板中的 CATALOG 区块**——`<!-- CATALOG:*:START/END -->` 标记之间是自动生成的。
3. **添加条目** = 在 `data/catalog.yaml` 追加 YAML 块 + 重新生成 + 跑测试。
4. **提交前验证**：`awesome-okf validate && pytest`
5. **不要创建重复 id**——原地编辑现有条目。
6. **多语言**：改一个模板时，四个模板同步修改。

**常用命令：**

```bash
awesome-okf stats                    # 按类别统计
awesome-okf list --kind plugin       # 按类别筛选
awesome-okf search <query>           # 全文搜索
awesome-okf validate                 # schema + 重复 id 检查
awesome-okf readme                   # 重新生成所有 README
awesome-okf-server                   # MCP meta-server
```

**MCP meta-server**：通过 `awesome-okf-server` 暴露四个工具（`search_catalog`、`list_catalog`、`get_catalog_entry`、`catalog_stats`），可编程查询 OKF 资源。

---


---


## 📈 Star 趋势

<p align="center">
  <img src="https://api.star-history.com/svg?repos=Albertchamberlain/Awesome-OKF&type=Date&sealed_token=1xyCNq0LSU304WvVyoz3q01A6O39ncWD9GT11VJhawLmHIxNsBKw1-YRnoAsuWgMBnRurnBB8omrhm-vRPkstQ8GqaUuUVhDqJaLv17-ct6SOiHHRYi14Q" alt="Star history chart" width="880" />
</p>

## 相关列表

- [yzfly/awesome-okf](https://github.com/yzfly/awesome-okf) — 中文 OKF 资源中心
- [OKF 规范](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) — Google Cloud 官方规范

---

<br>

<p align="center">
  <sub>MIT — 见 <a href="LICENSE">LICENSE</a>。目录描述链接到上游项目，遵循其各自许可证。</sub>
</p>