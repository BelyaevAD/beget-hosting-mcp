# Beget API Documentation Corpus

Generated: `2026-05-31T05:56:45.763631+00:00`

This repository contains a local Markdown and JSON corpus for the official Beget hosting API documentation.

## Layout

- `source-pages/`: full Markdown copies of the official KB pages.
- `beget-hosting-api.md`: normalized technical reference for wrapper design.
- `method-index.md`: method list grouped by API section.
- `schema/pages.json`: page metadata and source URLs.
- `schema/methods.json`: method metadata, examples, source snippets, side-effect flags.
- `schema/errors.json`: common response envelope and error-handling notes.

## Regeneration

Run:

```powershell
python scripts/build_beget_docs.py
```

The generator reads the Nuxt `_payload.json` for each Beget KB page and does not require a browser.
