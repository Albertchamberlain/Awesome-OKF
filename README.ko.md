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
  <strong>오픈 지식 포맷(OKF) 큐레이션 리소스 카탈로그.</strong>
</p>

<p align="center">
  YAML 기반 · 에이전트 검색 가능 · 커뮤니티 운영
</p>

<p align="center">
  <a href="https://github.com/Albertchamberlain/Awesome-OKF"><img alt="Awesome" src="https://cdn.jsdelivr.net/gh/sindresorhus/awesome@main/media/badge.svg"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-4c1?logo=open-source-initiative&logoColor=white"></a>
  <img alt="Catalog" src="https://img.shields.io/badge/catalog-29%20entries-7c3aed">
</p>

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh.md">中文</a> | <a href="README.ja.md">日本語</a> | <b>한국어</b>
</p>

<br>

<p align="center">
  <a href="#catalog"><b>카탈로그</b></a> &ensp;·&ensp;
  <a href="#connect-to-your-agent"><b>에이전트 연결</b></a> &ensp;·&ensp;
  <a href="#cli"><b>CLI</b></a> &ensp;·&ensp;
  <a href="#contributing"><b>기여</b></a>
</p>

<br>

---

## OKF란 무엇인가

[오픈 지식 포맷(OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)은 Google Cloud가 공개한 개방형 사양입니다. 지식을 Markdown 파일 디렉터리로 정의하고, YAML frontmatter와 최소한의 규칙을 더합니다. 런타임도 SDK도 없습니다.

## 이 프로젝트의 차별점

Awesome OKF는 OKF 생태계 전체를 **검증된 단일 YAML 카탈로그**로 통합하여, 탐색 가능한 목록, 검색 가능한 CLI, 그리고 AI 에이전트가 직접 쿼리할 수 있는 MCP 메타 서버를 생성합니다:

<div align="center">

```
                      catalog.yaml
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                 ▼
      README.md         CLI 도구        MCP 서버
   (사람이 탐색)      (검색 가능)   (에이전트 검색)
```

</div>

> **레코드 하나 편집. 문서 재생성. 어디서든 재쿼리.**

---

## 데모

```text
사용자(또는 에이전트):
  "Obsidian vault를 OKF로 변환하는 플러그인을 찾아줘."

에이전트 호출:
  search_catalog({
    "query": "Obsidian",
    "kind": "plugin",
    "limit": 3
  })

Awesome-OKF 응답:
  ┌──────────────────────────────────────────────────────────────┐
  │ obsidian-to-okf                                plugin        │
  │ Obsidian vault를 OKF로 변환—wikilink가 OKF 링크로.           │
  │ 플랫폼: python · 태그: obsidian, wikilink, markdown          │
  └──────────────────────────────────────────────────────────────┘
```

*카탈로그가 OKF를 말한다.*

---

## 빠른 시작

### 에이전트에 연결

MCP 클라이언트에 Awesome OKF 추가:

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

## 🛠️ 우리의 도구

### convert-to-okf 🔄

다양한 형식을 OKF 지식 번들로 변환하는 무의존성 CLI:

| 📥 입력 형식 | ✨ 기능 |
|---|---|
| 📋 Markdown awesome 목록 | `- [제목](URL) — 설명` 항목 → OKF 항목 |
| 📊 JSON 배열 | `{title, url, description}` 객체 → OKF 항목 |
| 🔗 URL 목록 | 일반 텍스트 URL → OKF 항목 |

```bash
# 명령 하나로 OKF 번들 즉시 생성
python scripts/convert-to-okf.py README.md -o kb/ -t concept

# 출력: YAML frontmatter가 있는 Markdown 파일 45개
# 바로: myokf validate kb/
```

### awesome-okf CLI 🎛️

데이터 기반 카탈로그 CLI (Awesome-MCP와 동일 아키텍처):

| 🔍 명령 | 📝 용도 |
|---|---|
| `awesome-okf search obsidian` | 전체 카탈로그 검색 |
| `awesome-okf list --kind plugin` | 카테고리 필터 |
| `awesome-okf readme` | catalog.yaml에서 README 재생성 |
| `awesome-okf-server` | MCP 메타 서버 |

---

## 🔥 인기 저장소

| 🏆 저장소 | 📌 내용 |
|---|---|
| ⭐ [yzfly/awesome-okf](https://github.com/yzfly/awesome-okf) | 중국어 OKF 허브 — 7 플러그인 + 7 스킬 + 3 제안 |
| ⭐ [linyiru/awesome-okf](https://github.com/linyiru/awesome-okf) | 영어 OKF 허브 — 사양, 도구, 샘플 |
| 📚 [GoogleCloudPlatform/knowledge-catalog](https://github.com/GoogleCloudPlatform/knowledge-catalog) | Google 공식 OKF 사양·SDK |
| 🧠 [karpathy/llm-wiki](https://github.com/karpathy/llm-wiki) | OKF에 영감을 준 LLM Wiki |

---

## 카탈로그

> **29 항목** · 4 도구 · 7 플러그인 · 7 스킬 · 5 제안 · 6 문서
> *엄선—포괄적 인덱스가 아닙니다.*

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

## 데이터 모델

```yaml
- id: obsidian-to-okf
  name: obsidian-to-okf
  kind: plugin
  category: document
  url: https://github.com/yzfly/awesome-okf/tree/main/plugins/obsidian-to-okf
  description: Obsidian vault를 OKF로 변환.
  platform: [python]
  official: false
  tags: [obsidian, wikilink, markdown]
```

---

## 기여

[`data/catalog.yaml`](data/catalog.yaml)에 항목을 추가·편집한 후:

```bash
awesome-okf validate
awesome-okf readme
pytest
```

[`CONTRIBUTING.md`](CONTRIBUTING.md) 참조.
---

## 🤖 AI 에이전트용

이 저장소에서 작업하는 AI 에이전트(Claude Code, Codex, Cursor)를 위한 정보:

```
data/catalog.yaml          # 단일 데이터 소스
README.template.md         # 영어 템플릿
README.template.zh.md      # 중국어 템플릿
README.template.ja.md      # 일본어 템플릿
README.template.ko.md      # 한국어 템플릿
src/awesome_okf/           # CLI + MCP 메타 서버
scripts/convert-to-okf.py  # 형식 변환 도구
```

**규칙(필수):**

1. **README\*.md를 직접 편집하지 마세요**—생성된 파일입니다. `data/catalog.yaml` 편집 후 `awesome-okf readme` 실행.
2. **템플릿의 CATALOG 블록을 편집하지 마세요**—`<!-- CATALOG:*:START/END -->`는 자동 생성.
3. **항목 추가** = YAML 블록 추가 + 재생성 + 테스트 실행.
4. **커밋 전 검증**: `awesome-okf validate && pytest`
5. **중복 id 금지**—기존 항목을 제자리에서 편집.
6. **다국어**: 템플릿 변경 시 4개 언어 모두 동기화.

**유용한 명령:**

```bash
awesome-okf stats                    # 카테고리별 집계
awesome-okf list --kind plugin       # 카테고리 필터
awesome-okf search <query>           # 전체 텍스트 검색
awesome-okf validate                 # 스키마 검증
awesome-okf readme                   # 모든 README 재생성
awesome-okf-server                   # MCP 메타 서버
```

**MCP 메타 서버**: `awesome-okf-server`로 4개 도구 노출.

---


---

## 관련 목록

- [yzfly/awesome-okf](https://github.com/yzfly/awesome-okf) — 중국어 OKF 허브
- [OKF 사양](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) — Google Cloud 공식

---

<br>

<p align="center">
  <sub>MIT — <a href="LICENSE">LICENSE</a> 참조. 카탈로그 설명은 업스트림 프로젝트에 링크.</sub>
</p>