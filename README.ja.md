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
  <strong>オープンナレッジフォーマット（OKF）の厳選リソースカタログ。</strong>
</p>

<p align="center">
  YAML駆動 · エージェント検索可能 · コミュニティ運営
</p>

<p align="center">
  <a href="https://github.com/Albertchamberlain/Awesome-OKF"><img alt="Awesome" src="https://cdn.jsdelivr.net/gh/sindresorhus/awesome@main/media/badge.svg"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-4c1?logo=open-source-initiative&logoColor=white"></a>
  <img alt="Catalog" src="https://img.shields.io/badge/catalog-29%20entries-7c3aed">
</p>

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh.md">中文</a> | <b>日本語</b> | <a href="README.ko.md">한국어</a>
</p>

<br>

<p align="center">
  <a href="#catalog"><b>カタログ</b></a> &ensp;·&ensp;
  <a href="#connect-to-your-agent"><b>エージェント接続</b></a> &ensp;·&ensp;
  <a href="#cli"><b>CLI</b></a> &ensp;·&ensp;
  <a href="#contributing"><b>貢献</b></a>
</p>

<br>

---

## OKF とは

[オープンナレッジフォーマット（OKF）](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)は、Google Cloud が公開したオープン仕様です。知識を Markdown ファイルのディレクトリとして定義し、YAML frontmatter と最小限の規約を加えたものです。ランタイムも SDK もありません。

## このプロジェクトの違い

Awesome OKF は、OKF エコシステム全体を**検証済みの単一 YAML カタログ**に集約し、閲覧可能なリスト、検索可能な CLI、そして AI エージェントが直接クエリできる MCP メタサーバーを生成します：

<div align="center">

```
                      catalog.yaml
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                 ▼
      README.md         CLI ツール       MCP サーバー
   （人が閲覧）        （検索可能）   （エージェント検索）
```

</div>

> **1 レコード編集。ドキュメント再生成。どこからでも再クエリ。**

---

## デモ

```text
ユーザー（またはエージェント）：
  "Obsidian の vault を OKF に変換するプラグインを探して。"

エージェント呼び出し：
  search_catalog({
    "query": "Obsidian",
    "kind": "plugin",
    "limit": 3
  })

Awesome-OKF の応答：
  ┌──────────────────────────────────────────────────────────────┐
  │ obsidian-to-okf                                plugin        │
  │ Obsidian vault を OKF に変換—wikilink が OKF リンクに。      │
  │ プラットフォーム: python · タグ: obsidian, wikilink          │
  └──────────────────────────────────────────────────────────────┘
```

*カタログが OKF を語る。*

---

## クイックスタート

### エージェントに接続

任意の MCP クライアントに Awesome OKF を追加：

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

## 🛠️ 私たちのツール

### convert-to-okf 🔄

様々な形式を OKF ナレッジバンドルに変換するゼロ依存 CLI：

| 📥 入力形式 | ✨ 機能 |
|---|---|
| 📋 Markdown awesome リスト | `- [タイトル](URL) — 説明` 項目 → OKF エントリ |
| 📊 JSON 配列 | `{title, url, description}` オブジェクト → OKF エントリ |
| 🔗 URL リスト | プレーンテキスト URL → OKF エントリ |

```bash
# 1 コマンドで OKF バンドルを即生成
python scripts/convert-to-okf.py README.md -o kb/ -t concept

# 出力: YAML frontmatter 付き Markdown ファイル 45 個
# そのまま: myokf validate kb/
```

### awesome-okf CLI 🎛️

データ駆動カタログ CLI（Awesome-MCP と同アーキテクチャ）：

| 🔍 コマンド | 📝 用途 |
|---|---|
| `awesome-okf search obsidian` | 全カタログ全文検索 |
| `awesome-okf list --kind plugin` | カテゴリで絞り込み |
| `awesome-okf readme` | catalog.yaml から README 再生成 |
| `awesome-okf-server` | MCP メタサーバー |

---

## 🔥 人気リポジトリ

| 🏆 リポジトリ | 📌 内容 |
|---|---|
| ⭐ [yzfly/awesome-okf](https://github.com/yzfly/awesome-okf) | 中国語 OKF ハブ — 7 プラグイン + 7 スキル + 3 提案 |
| ⭐ [linyiru/awesome-okf](https://github.com/linyiru/awesome-okf) | 英語 OKF ハブ — 仕様、ツール、サンプル |
| 📚 [GoogleCloudPlatform/knowledge-catalog](https://github.com/GoogleCloudPlatform/knowledge-catalog) | Google 公式 OKF 仕様・SDK |
| 🧠 [karpathy/llm-wiki](https://github.com/karpathy/llm-wiki) | OKF に影響を与えた LLM Wiki |

---

## カタログ

> **29 エントリ** · 4 ツール · 7 プラグイン · 7 スキル · 5 提案 · 6 ドキュメント
> *厳選—網羅的インデックスではありません。*

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

## データモデル

```yaml
- id: obsidian-to-okf
  name: obsidian-to-okf
  kind: plugin
  category: document
  url: https://github.com/yzfly/awesome-okf/tree/main/plugins/obsidian-to-okf
  description: Obsidian vault を OKF に変換。
  platform: [python]
  official: false
  tags: [obsidian, wikilink, markdown]
```

---

## 貢献

[`data/catalog.yaml`](data/catalog.yaml) にエントリを追加・編集して：

```bash
awesome-okf validate
awesome-okf readme
pytest
```

[`CONTRIBUTING.md`](CONTRIBUTING.md) を参照。
---

## 🤖 AI エージェント向け

このリポジトリで作業する AI エージェント（Claude Code、Codex、Cursor）向けの情報：

```
data/catalog.yaml          # 唯一のデータソース
README.template.md         # 英語テンプレート
README.template.zh.md      # 中国語テンプレート
README.template.ja.md      # 日本語テンプレート
README.template.ko.md      # 韓国語テンプレート
src/awesome_okf/           # CLI + MCP メタサーバー
scripts/convert-to-okf.py  # フォーマット変換ツール
```

**ルール（必須）：**

1. **README\*.md を直接編集しない**——生成物です。`data/catalog.yaml` を編集後、`awesome-okf readme` を実行。
2. **テンプレート内の CATALOG ブロックを編集しない**——`<!-- CATALOG:*:START/END -->` は自動生成。
3. **エントリ追加** = YAML ブロック追加 + 再生成 + テスト実行。
4. **コミット前に検証**：`awesome-okf validate && pytest`
5. **重複 id を作らない**——既存エントリをその場で編集。
6. **多言語**：テンプレートを変更する場合は 4 言語すべて同期。

**便利なコマンド：**

```bash
awesome-okf stats                    # カテゴリ別集計
awesome-okf list --kind plugin       # カテゴリで絞り込み
awesome-okf search <query>           # 全文検索
awesome-okf validate                 # スキーマ検証
awesome-okf readme                   # 全 README 再生成
awesome-okf-server                   # MCP メタサーバー
```

**MCP メタサーバー**：`awesome-okf-server` で 4 つのツールを公開。

---


---


## 📈 スター履歴

<p align="center">
  <img src="https://api.star-history.com/svg?repos=Albertchamberlain/Awesome-OKF&type=Date&sealed_token=1xyCNq0LSU304WvVyoz3q01A6O39ncWD9GT11VJhawLmHIxNsBKw1-YRnoAsuWgMBnRurnBB8omrhm-vRPkstQ8GqaUuUVhDqJaLv17-ct6SOiHHRYi14Q" alt="Star history chart" width="880" />
</p>

## 関連リスト

- [yzfly/awesome-okf](https://github.com/yzfly/awesome-okf) — 中国語 OKF ハブ
- [OKF 仕様](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) — Google Cloud 公式

---

<br>

<p align="center">
  <sub>MIT — <a href="LICENSE">LICENSE</a> 参照。カタログの説明は上流プロジェクトにリンク。</sub>
</p>