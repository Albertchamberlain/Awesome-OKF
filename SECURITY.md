# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Awesome-OKF, please **do not open a public issue**.

Instead, report it privately:

- **Email**: [albert7king@gmail.com](mailto:albert7king@gmail.com)
- Include: description, affected version, reproduction steps, and potential impact

## Response Process

1. We will acknowledge receipt within **48 hours**
2. We will investigate and provide an initial assessment within **5 business days**
3. A fix will be prepared and released as soon as practical
4. Credit will be given to the reporter (unless anonymity is requested)

## Scope

The Awesome-OKF project consists of:

- `src/awesome_okf/` — Python catalog tooling and MCP meta-server
- `scripts/convert-to-okf.py` — format converter
- `data/catalog.yaml` — catalog data

The MCP meta-server (`awesome-okf-server`) is a read-only stdio service that
exposes the catalog. It does not handle user credentials, network requests to
untrusted hosts, or arbitrary code execution from catalog data.

## Security Notes

- Catalog URLs are treated as **data**, not trusted endpoints — they are
  displayed and returned to agents but never fetched server-side
- `convert-to-okf` parses untrusted Markdown/JSON input. It uses only
  standard-library parsers and never executes the input content
- If you are embedding `awesome-okf-server` in an agent that fetches catalog
  URLs, validate and sandbox those fetches at the agent level

## Supported Versions

| Version | Supported |
|---|---|
| 0.1.x | ✅ |
