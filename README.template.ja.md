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