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
  <strong>Каталог избранных ресурсов по Open Knowledge Format.</strong>
</p>

<p align="center">
  Данные в YAML. Поиск для агентов. Наполняется сообществом.
</p>

<p align="center">
  <a href="https://github.com/Albertchamberlain/Awesome-OKF"><img alt="Awesome" src="https://cdn.jsdelivr.net/gh/sindresorhus/awesome@main/media/badge.svg"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-4c1?logo=open-source-initiative&logoColor=white"></a>
  <img alt="Catalog" src="https://img.shields.io/badge/catalog-29%20entries-7c3aed">
  <img alt="OKF Anything" src="https://img.shields.io/badge/OKF-Anything-7c3aed">
</p>

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh.md">中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.ko.md">한국어</a> | <b>Русский</b>
</p>

<br>

<p align="center">
  <a href="#каталог"><b>Каталог</b></a> &ensp;·&ensp;
  <a href="#подключение-к-агенту"><b>Подключение к агенту</b></a> &ensp;·&ensp;
  <a href="#cli"><b>CLI</b></a> &ensp;·&ensp;
  <a href="#участие-в-проекте"><b>Участие в проекте</b></a>
</p>

<br>

---

## Что такое OKF

[Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) — открытая спецификация от Google Cloud. Знания описываются как папка с файлами Markdown, у которых есть YAML frontmatter, плюс небольшой набор соглашений. Не нужны ни среда выполнения, ни SDK.

## Чем отличается этот проект

Awesome OKF хранит всю экосистему OKF в **одном YAML-каталоге с проверкой данных**. Из него получаются список для чтения, CLI с поиском и метасервер MCP, к которому ИИ-агенты могут обращаться напрямую:

<div align="center">

```
                      catalog.yaml
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                 ▼
      README.md        Утилиты CLI       Сервер MCP
     (для чтения)      (с поиском)     (для агентов)
```

</div>

> **Измените одну запись. Пересоберите документацию. Запрашивайте данные откуда угодно.**

---

## 🌐 OKF Anything

**Всё, что можно прочитать, можно превратить в OKF.** Любой поддерживаемый формат, как и любой придуманный вами, сначала приводится к одной промежуточной структуре, а затем собирается в OKF:

```
        ┌──────── ИЗВЛЕЧЕНИЕ ─────────┐   ┌─ НОРМАЛИЗАЦИЯ ─┐   ┌──── СБОРКА ────┐
        │  Markdown · Typora · PDF    │   │  title         │   │  # заголовок   │
        │  Obsidian · Notion · Feishu │ → │  url           │ → │  описание      │
        │  GitHub · JSON · YAML       │   │  description   │   │  ресурс        │
        │  CSV · ключ-значение · OCR  │   │  body / tags   │   │  для myokf     │
        └─────────────────────────────┘   └────────────────┘   └────────────────┘
```

1. **Извлечение**: из любого источника достаётся читаемый текст. Для этого используются штатный экспорт платформ и локальные движки (pymupdf, PaddleOCR). **Через нашу модель ничего не проходит**.
2. **Нормализация**: любой формат сводится к полям `title / url / description` (и необязательным `body`, `tags`).
3. **Сборка**: из промежуточной структуры получается папка OKF, которую можно проверить через myokf.

`--format anything` делает то же самое автоматически: передайте произвольный текст, и он пройдёт по цепочке парсеров (список → JSON → ключ-значение → URL → построчно), пока один из них не подойдёт:

```bash
python scripts/convert-to-okf.py whatever.txt --format anything -o kb/
```

Инструмент MCP `convert_to_okf` работает так же: агент передаёт произвольный текст и получает обратно OKF.

---

## Как это выглядит

```text
Пользователь (или агент):
  "Найди плагин OKF для конвертации хранилища Obsidian."

Агент вызывает:
  search_catalog({
    "query": "Obsidian",
    "kind": "plugin",
    "limit": 3
  })

Awesome-OKF отвечает:
  ┌──────────────────────────────────────────────────────────────┐
  │ obsidian-to-okf                                plugin        │
  │ Конвертирует хранилища Obsidian в OKF, wikilinks → ссылки.   │
  │ Платформа: python  ·  Теги: obsidian, wikilink, markdown     │
  └──────────────────────────────────────────────────────────────┘
```

*Каталог говорит на языке OKF.*

---

## Быстрый старт

### Подключение к агенту

Добавьте Awesome OKF в любой MCP-клиент, чтобы ваш агент мог находить ресурсы OKF:

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

## 🛠️ Наши инструменты

### convert-to-okf 🔄

CLI без зависимостей. Превращает содержимое с привычных вам платформ в наборы знаний OKF:

| 📥 Формат на входе | ✨ Что делает |
|---|---|
| 📋 Списки awesome-xx в Markdown | Извлекает пункты вида `- [Title](URL) — Description` → записи OKF |
| 📊 Массивы JSON | Преобразует объекты `{title, url, description}` → записи OKF |
| 🔗 Списки URL | Обычный текстовый список адресов → записи OKF |
| 🧾 Файлы YAML | Списки и словари с полями `{title, url, description}`. Нужен pyyaml (необязательная зависимость) |
| 📑 Таблицы CSV | Столбцы `title/url/description`. Если столбца title нет, берётся первый столбец |
| 🗂️ Текст «ключ-значение» | Блоки вида `key: value`: frontmatter, файлы properties, собственные форматы |
| 🐙 Репозитории GitHub | Укажите ссылку на репозиторий: метаданные и README загружаются на лету → запись OKF |
| 📓 Хранилища Obsidian | Локальная папка хранилища → одна запись на заметку, wikilinks преобразуются в ссылки |
| 📝 Экспорт из Notion | Папка, полученная через «Export → Markdown» → одна запись на страницу |
| 🦩 Документы Feishu | Markdown, экспортированный из Feishu → одна запись на документ |
| 🖋️ Заметки Typora | Обычные файлы `.md`: достаточно указать файл или папку |
| 📕 Документы PDF | Текстовый слой извлекается через pymupdf (необязательная зависимость). Для сканов выводится инструкция по OCR |
| 🖼️ Сканы и изображения | Встроенного OCR нет. Вместо этого выводится готовая инструкция для PaddleOCR |

```bash
# Любая платформа, одна команда
python scripts/convert-to-okf.py README.md -o kb/ -t concept
python scripts/convert-to-okf.py https://github.com/GoogleCloudPlatform/knowledge-catalog --format github -o kb/
python scripts/convert-to-okf.py my-vault/ --format obsidian -o kb/
python scripts/convert-to-okf.py notion-export/ --format notion -o kb/
python scripts/convert-to-okf.py feishu-doc.md --format feishu -o kb/

# Структурированные данные
python scripts/convert-to-okf.py data.yaml --format yaml -o kb/   # нужно: pip install pyyaml
python scripts/convert-to-okf.py table.csv --format csv -o kb/
python scripts/convert-to-okf.py notes.properties --format kv -o kb/

# PDF с текстовым слоем
pip install pymupdf
python scripts/convert-to-okf.py paper.pdf --format pdf -o kb/

# Сканы и PDF из картинок → OKF: сначала OCR (ваш локальный движок, не наша модель), затем конвертация
python scripts/convert-to-okf.py scan.png --format image    # выводит инструкцию по OCR
pip install paddleocr paddlepaddle
paddleocr ppocr -i scans/ --type ocr --lang en -o ocr-text/
python scripts/convert-to-okf.py ocr-text/ --format notion -o kb/

# Результат: папка kb/ с файлами Markdown, у каждого есть YAML frontmatter
# Дальше можно запускать: myokf validate kb/
```

### awesome-okf CLI 🎛️

CLI для работы с каталогом. Всё содержимое берётся из `catalog.yaml`, архитектура та же, что у Awesome-MCP:

| 🔍 Команда | 📝 Назначение |
|---|---|
| `awesome-okf search obsidian` | Полнотекстовый поиск по всем 29 записям |
| `awesome-okf list --kind plugin` | Фильтр по типу записи |
| `awesome-okf readme` | Пересобрать README из catalog.yaml |
| `awesome-okf-server` | Метасервер MCP: через него ИИ-агенты обращаются к каталогу |

---

## 🔥 Популярные репозитории

| 🏆 Репозиторий | 📌 Что в нём есть |
|---|---|
| ⭐ [yzfly/awesome-okf](https://github.com/yzfly/awesome-okf) | Первый ресурс по OKF на китайском языке: 7 плагинов, 7 навыков (skills) и 3 предложения (proposals) |
| ⭐ [linyiru/awesome-okf](https://github.com/linyiru/awesome-okf) | Собрание ресурсов по OKF на английском: спецификация, инструменты, примеры, руководства |
| 📚 [GoogleCloudPlatform/knowledge-catalog](https://github.com/GoogleCloudPlatform/knowledge-catalog) | Официальная спецификация OKF, SDK и предложения от Google |
| 🧠 [karpathy/llm-wiki](https://github.com/karpathy/llm-wiki) | Та самая LLM Wiki, с которой начался OKF |

---

## Каталог

> **29 отобранных записей** · 4 инструмента · 7 плагинов · 7 навыков · 5 предложений · 6 документов
> *Это осознанная подборка, а не полный перечень.*

<!-- CATALOG:TOOLS:START -->

## 🛠️ Tools & CLI

### Cli

- [myokf-cli](https://github.com/yzfly/awesome-okf) `cli` — Unified CLI for OKF — pull from GitHub, validate, and package to single-file web. — `cli`, `python`, `validation`, `packaging`

### Conversion

- [binder](https://github.com/ghchinoy/binder) `cli` — Go CLI that converts an existing plain-markdown corpus into a conformant OKF v0.2 bundle, resolving the corpus link web (markdown links and wikilinks) into OKF relationships — with validate, a stdio MCP server, and an agent plugin. — `conversion`, `go`, `markdown`, `wikilink`
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

## Модель данных

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

## Участие в проекте

Добавьте или измените записи в [`data/catalog.yaml`](data/catalog.yaml), затем выполните:

```bash
awesome-okf validate
awesome-okf readme
pytest
```

Схема записи описана в [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## 🤖 Для ИИ-агентов

Если вы ИИ-агент (Claude Code, Codex, Cursor) и работаете с этим репозиторием, вот что нужно знать:

### Структура проекта

```
data/catalog.yaml          # ЕДИНСТВЕННЫЙ ИСТОЧНИК ДАННЫХ: все записи хранятся здесь
README.template.md         # английский шаблон (текст пишется вручную)
README.template.zh.md      # китайский шаблон
README.template.ja.md      # японский шаблон
README.template.ko.md      # корейский шаблон
README.template.ru.md      # русский шаблон
src/awesome_okf/           # CLI и метасервер MCP (Python)
scripts/convert-to-okf.py  # утилита конвертации форматов
```

### Правила (обязательные)

1. **Никогда не редактируйте README\*.md напрямую**: эти файлы генерируются. Измените `data/catalog.yaml` и пересоберите их.
2. **Никогда не редактируйте блоки CATALOG** в шаблонах: всё между маркерами `<!-- CATALOG:*:START/END -->` генерируется автоматически.
3. **Чтобы добавить запись**, допишите блок YAML в `data/catalog.yaml`, пересоберите README и запустите тесты. Схема:
   ```yaml
   - id: kebab-case-id          # уникальный, повторно не используется
     name: Human Readable Name
     kind: tool|plugin|skill|proposal|doc
     category: free-form-group
     url: https://...
     description: One sentence, no marketing fluff.
     platform: [cli|python|web|claude-code]
     official: false            # true ТОЛЬКО для официальных проектов Google или вендора
     tags: [3-5 short tags]
   ```
4. **Проверяйте перед коммитом**: `awesome-okf validate && pytest`
5. **Никогда не создавайте дубликаты id**: редактируйте существующую запись.
6. **Несколько языков**: если меняете один шаблон, внесите то же изменение во все пять шаблонов.

### Полезные команды

```bash
awesome-okf stats                    # число записей по типам
awesome-okf list --kind plugin       # фильтр по типу
awesome-okf search <query>           # полнотекстовый поиск
awesome-okf validate                 # проверка схемы и дубликатов id
awesome-okf readme                   # пересобрать все README
awesome-okf-server                   # метасервер MCP (stdio)
```

### Метасервер MCP

Каталог доступен агентам через `awesome-okf-server`. Сервер предоставляет пять инструментов:
`search_catalog`, `list_catalog`, `get_catalog_entry`, `catalog_stats`, `convert_to_okf`.
Подключите его к своему MCP-клиенту, чтобы запрашивать ресурсы OKF из кода.

---


## Похожие списки

- [yzfly/awesome-okf](https://github.com/yzfly/awesome-okf) — первое собрание ресурсов по OKF, на китайском языке
- [Спецификация OKF](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) — официальная спецификация от Google Cloud

---

<br>

<p align="center">
  <sub>Лицензия MIT, см. <a href="LICENSE">LICENSE</a>. Описания в каталоге ведут на исходные проекты, у каждого из которых своя лицензия.</sub>
</p>