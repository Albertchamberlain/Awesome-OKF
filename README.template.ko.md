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

## 관련 목록

- [yzfly/awesome-okf](https://github.com/yzfly/awesome-okf) — 중국어 OKF 허브
- [OKF 사양](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) — Google Cloud 공식

---

<br>

<p align="center">
  <sub>MIT — <a href="LICENSE">LICENSE</a> 참조. 카탈로그 설명은 업스트림 프로젝트에 링크.</sub>
</p>