# Operator Guide for Beget Hosting MCP

Use the `beget-hosting` MCP server to manage Beget hosting through the official hosting API.

## Core Rules

1. Do not request or store Beget credentials in chat.
2. Configure credentials in the MCP server environment as `BEGET_LOGIN` and `BEGET_API_PASSWORD`.
3. Use `beget_list_methods` to discover available methods.
4. Use `beget_get_method_docs` before using any method for the first time.
5. Prefer read-only inspection before changing anything.
6. Treat side-effectful methods as risky. Side-effectful methods include create, add, edit, delete, drop, restore, download, DNS changes, password changes, link/unlink, freeze/unfreeze, forwarding, and mail routing changes.
7. Before a side-effectful method, call `beget_call` with `dry_run=true` and explain the planned operation.
8. Execute a side-effectful method only after explicit approval and only with `confirm_write=true`.
9. Never display raw passwords, tokens, secrets, or unsanitized URLs.
10. If a Beget response has top-level `status=error`, report `error_code` and `error_text`.
11. If `answer.status=error`, report the method-level `errors` list.
12. Do not retry side-effectful methods automatically.

## Common Workflows

### Inspect Account

```json
{
  "tool": "beget_get_account_info",
  "arguments": {}
}
```

### List Sites

```json
{
  "tool": "beget_call",
  "arguments": {
    "section": "site",
    "method": "getList",
    "params": {}
  }
}
```

### Add a Site

First dry-run:

```json
{
  "tool": "beget_call",
  "arguments": {
    "section": "site",
    "method": "add",
    "params": {
      "name": "example.ru"
    },
    "dry_run": true
  }
}
```

After explicit approval:

```json
{
  "tool": "beget_call",
  "arguments": {
    "section": "site",
    "method": "add",
    "params": {
      "name": "example.ru"
    },
    "confirm_write": true
  }
}
```

### Change DNS

Inspect current DNS first:

```json
{
  "tool": "beget_call",
  "arguments": {
    "section": "dns",
    "method": "getData",
    "params": {
      "fqdn": "example.ru"
    }
  }
}
```

Then dry-run `dns.changeRecords`, show the planned records, and wait for explicit approval before `confirm_write=true`.

## Known Documentation Ambiguity

The statistics page heading says `stat.getSiteListLoad`, but the example endpoint uses `getSitesListLoad`. The MCP server preserves this as `method=getSiteListLoad` and `endpoint_method=getSitesListLoad`. Verify behavior before relying on this method in automation.

