# Beget Hosting MCP

MCP server for the official Beget hosting API.

This project gives MCP clients and agents a controlled tool interface for Beget hosting management: account info, sites, domains, DNS, FTP, MySQL, mail, cron, backups, and statistics.

The API documentation corpus is preserved in `docs/`; the MCP server uses the machine-readable method metadata from that corpus.

## Status

Alpha. Use read-only mode first. Write operations are intentionally gated.

## Installation

From a local checkout:

```powershell
python -m pip install .
```

For a global system-wide CLI managed by `pipx`:

```powershell
pipx install .
```

After installation, the command is:

```powershell
beget-hosting-mcp
```

No third-party Python dependencies are required.

## Credentials

The MCP transport is stdio. The MCP client starts this server as a local process and communicates with it over stdin/stdout.

Beget credentials are process configuration, not MCP transport credentials. Set them in the MCP client config or in the environment of the service account that runs the server:

```powershell
BEGET_LOGIN=your-login
BEGET_API_PASSWORD=your-api-password
```

Do not commit credentials or paste them into chat clients.

Write operations are disabled unless:

```powershell
BEGET_ALLOW_WRITE=true
```

Even then, side-effectful tool calls still require `confirm_write=true`.

## MCP Client Config

Installed command:

```json
{
  "mcpServers": {
    "beget-hosting": {
      "command": "beget-hosting-mcp",
      "args": [],
      "env": {
        "BEGET_LOGIN": "your-login",
        "BEGET_API_PASSWORD": "your-api-password"
      }
    }
  }
}
```

For development from a local checkout:

```powershell
python -m pip install -e .
```

For a write-enabled profile, add:

```json
{
  "BEGET_ALLOW_WRITE": "true"
}
```

Prefer a separate MCP profile for write access.

## Tools

- `beget_list_methods`: list documented methods.
- `beget_get_method_docs`: return preserved documentation for one method.
- `beget_call`: call any documented Beget hosting API method.
- `beget_get_account_info`: shortcut for `user.getAccountInfo`.

## Safety Model

- Credentials only come from environment variables.
- Requests are sent with `POST`.
- Secrets are redacted in dry-run and error output.
- Side-effectful methods are blocked unless `BEGET_ALLOW_WRITE=true`.
- Side-effectful calls also require `confirm_write=true`.
- Operators should dry-run write operations before execution.
- The server checks both top-level Beget errors and nested method-level errors.

## Smoke Tests

```powershell
beget-hosting-mcp --check-docs
beget-hosting-mcp --list-tools
```

Dry-run a request without calling Beget:

```powershell
$env:BEGET_LOGIN = "demo-login"
$env:BEGET_API_PASSWORD = "demo-password"
beget-hosting-mcp --dry-run-account-info
```

## Documentation Corpus

- `docs/source-pages/`: full Markdown copies of Beget KB API pages.
- `docs/beget-hosting-api.md`: normalized technical reference.
- `docs/method-index.md`: method index.
- `docs/operator-guide.md`: usage rules and common workflows.
- `docs/schema/methods.json`: machine-readable methods.
- `scripts/build_beget_docs.py`: documentation corpus builder.

## Known Beget Documentation Ambiguity

The statistics page heading says `stat.getSiteListLoad`, but the example endpoint uses `getSitesListLoad`. The server preserves this as `method=getSiteListLoad` and `endpoint_method=getSitesListLoad`.
