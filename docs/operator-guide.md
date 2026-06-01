# Operator Guide for Beget Hosting MCP

Use the `beget-hosting` MCP server to manage Beget hosting through the official hosting API.

## Core Rules

1. Do not request or store Beget credentials in chat.
2. Configure credentials in the MCP server environment as `BEGET_LOGIN` and `BEGET_API_PASSWORD`.
3. Use a separate Beget API password for `BEGET_API_PASSWORD`. Enable API authentication in the control panel at `https://cp.beget.com/settings/security/api`.
4. Use `beget_list_methods` to discover available methods.
5. Use `beget_get_method_docs` before using any method for the first time.
6. Prefer read-only inspection before changing anything.
7. Treat side-effectful methods as risky. Side-effectful methods include create, add, edit, delete, drop, restore, download, DNS changes, password changes, link/unlink, freeze/unfreeze, forwarding, and mail routing changes.
8. Before a side-effectful method, call `beget_call` with `dry_run=true` and explain the planned operation.
9. Execute a side-effectful method only after explicit approval and only with `confirm_write=true`.
10. Never display raw passwords, tokens, secrets, or unsanitized URLs.
11. If a Beget response has top-level `status=error`, report `error_code` and `error_text`.
12. If `answer.status=error`, report the method-level `errors` list.
13. Do not retry side-effectful methods automatically.
14. After changes that depend on DNS, background jobs, scheduler timing, web server reloads, mail routing, or registrar state, wait before deciding that the operation failed.

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

DNS changes are not instant. `dns.getData` may show the new records on Beget before recursive resolvers, browsers, mail providers, or external verification tools see them. After `dns.changeRecords`, wait at least a few minutes before checking Beget nameservers directly and allow up to the previous DNS TTL, sometimes longer, before treating public propagation as failed. For real-domain checks, query both authoritative nameservers and public resolvers before reporting the final state.

## Verification Delays

Some Beget API methods return `true` when a request was accepted, not when every downstream system has already observed the result.

- DNS records and nameserver changes: wait for authoritative Beget DNS to reload, then for recursive DNS caches to expire. Public checks can lag behind panel/API state.
- Domain add, delete, register, renew, and delegation changes: re-check `domain.getList` for order/status fields and expect registrar or delegation state to lag.
- Site add/delete and domain link/unlink: re-check `site.getList` and `domain.getList`, then allow time for web server virtual host routing to reload before testing the real hostname.
- PHP version and directive changes: verify with `domain.getPhpVersion` or `domain.getDirectives`, then allow time for runtime/web server reload before testing application behavior.
- Backup restore and download requests: these create background jobs. Poll `backup.getLog` until the job status is final before checking restored files, databases, or download availability.
- MySQL create/drop/access/password changes: re-check `mysql.getList`, then allow a short delay before testing a live application connection.
- Mailbox, forward, and domain mail changes: re-check mail API state first. Delivery tests can be delayed by MX/DNS cache, remote mail provider queues, and spam filtering.
- Cron add/edit/enable changes: `cron.getList` verifies configuration, but execution cannot be proven until the next matching schedule window.

When checking after a delayed operation, report the verification source: Beget API state, authoritative DNS, public resolver, HTTP response, mail delivery, cron output, backup log, or application-level test.

## Cursor Tool List

This MCP server exposes its functions through the standard `tools/list` MCP method. Expected tools:

- `beget_list_methods`
- `beget_get_method_docs`
- `beget_call`
- `beget_get_account_info`

If Cursor connects but does not show the tool list, first verify the server outside Cursor with `beget-hosting-mcp --list-tools`. Then restart the MCP server entry in Cursor or restart Cursor. A connected client should call `initialize`, then `tools/list`; the initialize response advertises tool capability with `listChanged=false`.

## Known Documentation Ambiguity

The statistics page heading says `stat.getSiteListLoad`, but the example endpoint uses `getSitesListLoad`. The MCP server preserves this as `method=getSiteListLoad` and `endpoint_method=getSitesListLoad`. Verify behavior before relying on this method in automation.
