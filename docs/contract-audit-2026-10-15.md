# Beget Hosting API Contract Audit

Audit date: `2026-10-15`

## Scope

The audit compared the complete official [Beget Hosting API documentation](https://beget.com/ru/kb/api/beget-api) with the preserved corpus and the MCP runtime catalog.

- Official inventory: 12 pages.
- Documented methods: 65.
- Read-only methods: 25.
- Side-effectful methods: 40.
- Extracted method parameters: 104.

No methods, endpoint method names, parameter names, or side-effect classifications were added, removed, or changed relative to the previous repository snapshot.

## Confirmed Documentation Updates

Eleven pages have newer Beget modification timestamps. The contract-relevant changes are:

- Beget now explicitly states that control-panel IP allow/deny restrictions also apply to API requests.
- Method pages now distinguish examples of `answer.result` from examples of the complete response envelope.
- The DNS page no longer requires internationalized domain names to be supplied in punycode. A live read-only `dns.getData` call with a Cyrillic domain succeeded without client-side conversion.

The official transport contract continues to allow GET, POST, or both and recommends POST. The MCP server keeps credentials and method input in a form-encoded POST body.

## Upstream Defects Preserved as Warnings

The source pages remain unmodified. Machine-readable records contain warnings instead of silently correcting source examples:

- `cron.edit`: one encoded example incorrectly targets `cron.add` and omits the edit identifier.
- `dns.changeRecords`: one decoded `input_data` example is invalid JSON.
- `domain.getPhpVersion`: one example uses HTTP and another percent-encodes the complete query string instead of values.
- `mail.forwardListAddMailbox`: one decoded `input_data` example is invalid JSON.
- `mail.forwardListDeleteMailbox`: one decoded `input_data` example is invalid JSON.
- `stat.getSiteListLoad`: the heading differs from the working `getSitesListLoad` endpoint.

The runtime always uses `https://api.beget.com` and maps `stat.getSiteListLoad` to `getSitesListLoad`.

## Live Read-Only Verification

The configured Beget account successfully returned data for:

- `user.getAccountInfo`;
- `domain.getList`, `domain.getZoneList`, and `domain.getSubdomainList`;
- `domain.getPhpVersion`;
- `dns.getData` for ASCII and internationalized domain names;
- `stat.getSiteListLoad` and `stat.getDbListLoad` through the documented aliases.

Backup, Cron, FTP, MySQL, site, and some directive calls returned Beget `AUTH_ERROR` responses stating that the account cannot access those method groups. This account-level limitation does not prove those method contracts invalid, so they remain documentation-verified rather than live-verified.

No write operation was executed during the audit.

## Runtime Corrections

- The generated documentation catalog and packaged MCP catalog are now written from the same source in one run.
- Tool arguments are type-checked server-side. In particular, only the JSON boolean `true` can satisfy `confirm_write`; a string cannot enable a write.
- Beget method failures are returned as MCP tool results with `isError=true`, preserving the MCP connection.
- Successful tool calls include both text content and structured content.
- API responses have a size limit, and credentials are removed from structured fields and free-form diagnostic strings.
- Dry runs no longer require configured credentials and never contact Beget.

## Regeneration and Validation

```powershell
python scripts/build_beget_docs.py
$env:PYTHONPATH = (Resolve-Path src).Path
python -m unittest discover -s tests -v
ruff check .
```

The generator stops if the official page inventory changes, forcing a section mapping review instead of silently omitting new documentation.
