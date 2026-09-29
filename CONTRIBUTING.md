# Contributing to Awesome-OKF

Thanks for helping grow the catalog.

## Adding an entry

1. Edit [`data/catalog.yaml`](data/catalog.yaml)
2. Run validation and regenerate docs:

```bash
pip install -e ".[dev]"
awesome-okf validate
awesome-okf readme
pytest
```

3. Open a PR with a short note on why the project belongs in the list

## Regenerating READMEs

`README.md` and every localized `README.<lang>.md` are generated — edit `README.template*.md` and `data/catalog.yaml`, never the READMEs themselves.

| Command | What it does |
|---|---|
| `awesome-okf readme` | Renders the complete set (English + every language in `README_LANGS`) and writes it next to the templates |
| `awesome-okf readme --check` | Writes nothing; exits 1 and names every README of the complete set that is out of date |
| `awesome-okf readme --output FILE` | Renders only the English README to `FILE`; localized READMEs are not touched |
| `awesome-okf readme --output FILE --check` | Checks only `FILE` against the English README |
| `awesome-okf readme --root DIR` | Uses the templates in `DIR` instead of looking for them from the current directory |

- The templates and the READMEs live in one directory: `--root`, or the nearest parent of the current directory that contains `README.template.md`. Outside a checkout the command fails instead of writing anywhere else.
- A missing or malformed template (each `CATALOG:*` block needs exactly one `START`/`END` pair) is an error, exit code 2. A localized README is never filled from the English template.
- Everything is rendered before anything is written, and files are replaced atomically: a failed run leaves all READMEs as they were.

To add a language, create `README.template.<lang>.md`, add its code to `README_LANGS` in `src/awesome_okf/readme.py`, link it from the language switcher of every template, and run `awesome-okf readme`.

## Entry schema

```yaml
- id: unique-kebab-case-id
  name: Human-readable name
  kind: tool          # tool | client | registry | skill
  category: document     # free-form grouping within the kind
  url: https://github.com/org/project
  description: One sentence on what it does for OKF users.
  platform: [cli]    # optional: cli, web, python
  official: false       # true for OKF steering-group / vendor official projects
  tags: [document, automation]
```

## Review checklist

- Link resolves and points to the canonical repo or product page
- Description is accurate and not marketing fluff
- Prefer actively maintained projects with clear OKF support
- Avoid duplicate entries — search the catalog first: `awesome-okf search <name>`
- Do not submit paid/spam listings

## OKF meta-tool

The catalog is also exposed as an OKF tool (`awesome-okf-tool`) so agents can discover resources programmatically. If you add fields to the YAML schema, update:

- `src/awesome_mcp/catalog.py`
- `src/awesome_mcp/tool.py`
- tests in `tests/`

## License

By contributing, you agree your commits are licensed under the repository MIT license.
