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
  <img alt="OKF Anything" src="https://img.shields.io/badge/OKF-Anything-7c3aed">
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

## 🌐 OKF Anything

**읽을 수 있는 모든 것은 OKF로.** 위의 모든 형식—그리고 여러분이 만드는 어떤 형식도—하나의 중간 구조로 수렴한 뒤 OKF로 번들링됩니다:

```
        ┌────────── EXTRACT ──────────┐   ┌── NORMALIZE ──┐   ┌──── BUNDLE ────┐
        │  Markdown · Typora · PDF    │   │  title         │   │  # title       │
        │  Obsidian · Notion · Feishu │ → │  url           │ → │  description   │
        │  GitHub · JSON · YAML       │   │  description   │   │  resource      │
        │  CSV · key-value · OCR      │   │  body / tags   │   │  myokf-ready   │
        └─────────────────────────────┘   └────────────────┘   └────────────────┘
```

1. **Extract** — 어떤 소스에서든 읽을 수 있는 텍스트를 추출. 플랫폼 내보내기와 로컬 엔진(pymupdf, PaddleOCR)이 담당—**우리 모델은 사용하지 않음**.
2. **Normalize** — 모든 형식을 `title / url / description`(+ 선택 `body`, `tags`)으로 환원.
3. **Bundle** — 중간 구조를 myokf 검증 가능한 OKF 디렉터리로 렌더링.

`--format anything`은 프로그램적 형태: 임의 텍스트를 넣으면 파서 체인(리스트 → JSON → 키-값 → URL → 줄 단위)을 순서대로 시도:

```bash
python scripts/convert-to-okf.py whatever.txt --format anything -o kb/
```

MCP 도구 `convert_to_okf`도 같은 아이디어—에이전트가 임의 텍스트를 주면 OKF를 돌려줍니다.

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

좋아하는 플랫폼의 콘텐츠를 OKF 지식 번들로 변환하는 무의존성 CLI:

| 📥 입력 형식 | ✨ 기능 |
|---|---|
| 📋 Markdown awesome 목록 | `- [제목](URL) — 설명` 항목 → OKF 항목 |
| 📊 JSON 배열 | `{title, url, description}` 객체 → OKF 항목 |
| 🔗 URL 목록 | 일반 텍스트 URL → OKF 항목 |
| 🧾 YAML 파일 | `{title, url, description}` 목록/매핑 — pyyaml(선택) 필요 |
| 📑 CSV 테이블 | `title/url/description` 열; title 열이 없으면 첫 열 사용 |
| 🗂️ 키-값 텍스트 | 범용 `key: value` 블록 — frontmatter, properties, 커스텀 형식 |
| 🐙 GitHub 저장소 | 저장소 URL만 붙여넣기 — 메타데이터 + README 실시간 가져오기 → OKF 항목 |
| 📓 Obsidian vault | 로컬 vault 디렉터리 → 노트마다 항목 하나, wikilink 자동 해석 |
| 📝 Notion 내보내기 | Notion「Markdown으로 내보내기」→ 페이지마다 항목 하나 |
| 🦩 Feishu 문서 | Feishu에서 내보낸 Markdown → 문서마다 항목 하나 |
| 🖋️ Typora 노트 | 일반 `.md` 파일 — 변환 불필요, 파일/폴더만 지정 |
| 📕 PDF 문서 | pymupdf(선택 의존성)로 텍스트 레이어 추출; 스캔 페이지는 OCR 레시피 출력 |
| 🖼️ 스캔/이미지 | OCR 미내장 — 바로 실행 가능한 PaddleOCR 레시피 출력 |

```bash
# 어떤 플랫폼이든 명령 하나
python scripts/convert-to-okf.py README.md -o kb/ -t concept
python scripts/convert-to-okf.py https://github.com/GoogleCloudPlatform/knowledge-catalog --format github -o kb/
python scripts/convert-to-okf.py my-vault/ --format obsidian -o kb/
python scripts/convert-to-okf.py notion-export/ --format notion -o kb/
python scripts/convert-to-okf.py feishu-doc.md --format feishu -o kb/

# 구조화 데이터
python scripts/convert-to-okf.py data.yaml --format yaml -o kb/   # 필요: pip install pyyaml
python scripts/convert-to-okf.py table.csv --format csv -o kb/
python scripts/convert-to-okf.py notes.properties --format kv -o kb/

# 텍스트 레이어 PDF
pip install pymupdf
python scripts/convert-to-okf.py paper.pdf --format pdf -o kb/

# 스캔/이미지 전용 PDF → OKF: 로컬 OCR 먼저(로컬 엔진, 우리 모델 미사용), 그다음 변환
python scripts/convert-to-okf.py scan.png --format image    # OCR 레시피 출력
pip install paddleocr paddlepaddle
paddleocr ppocr -i scans/ --type ocr --lang en -o ocr-text/
python scripts/convert-to-okf.py ocr-text/ --format notion -o kb/

# 출력: YAML frontmatter가 있는 Markdown 파일
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

**MCP 메타 서버**: `awesome-okf-server`로 5개 도구 노출 (`convert_to_okf`로 OKF 변환 가능).

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