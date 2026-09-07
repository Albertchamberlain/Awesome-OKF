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
