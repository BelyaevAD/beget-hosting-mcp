# Changelog

All notable changes to this project are documented here.

## 0.1.2 - 2026-10-15

- Refreshed all 12 official Beget hosting API pages and all 65 method records.
- Added automatic page-inventory checks, structured parameter metadata, and warnings for broken upstream examples.
- Kept the packaged MCP method catalog synchronized with the generated documentation corpus.
- Added strict MCP argument validation so string values cannot satisfy boolean write confirmation.
- Return Beget failures as MCP tool errors and successful values as both text and structured content.
- Added support for the `2025-11-25` legacy MCP protocol revision while retaining older Cursor-compatible revisions.
- Added API response-size limits, free-form secret redaction, and credential-free dry runs.
- Documented Beget API IP access restrictions.

## 0.1.1 - 2026-07-21

- Fixed Cursor initialization timeouts by using newline-delimited JSON-RPC for MCP stdio.
- Preserved `Content-Length` framing compatibility for older custom MCP clients.
- Added subprocess tests for `initialize` and `tools/list` discovery.
- Documented a direct, wrapper-free Windows Cursor configuration.
- Stopped returning internal exception details and Python tracebacks to MCP clients.

## 0.1.0 - 2026-06-01

- Initial Beget hosting MCP server.
- Added preserved Beget hosting API documentation corpus.
- Added read-only tools for method discovery and account/domain inspection.
- Added guarded write support with `BEGET_ALLOW_WRITE=true` and per-call `confirm_write=true`.
- Added Cursor compatibility metadata for `tools/list`, prompts, and resources discovery.
- Added operational guidance for DNS propagation, background jobs, and other delayed verification cases.
