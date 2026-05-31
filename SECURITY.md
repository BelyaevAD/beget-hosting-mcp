# Security Policy

## Credentials

Never commit Beget credentials, API passwords, tokens, session data, or real account identifiers.

The MCP server reads Beget credentials from environment variables:

- `BEGET_LOGIN`
- `BEGET_API_PASSWORD`

For local development, use your shell, OS secret store, MCP client secret handling, or a private untracked environment file. Do not add real secrets to `.env.example`.

## Write Access

Write operations are disabled by default. To enable them, the server process must have:

```text
BEGET_ALLOW_WRITE=true
```

Each side-effectful tool call must also pass:

```json
{
  "confirm_write": true
}
```

Agents should dry-run write operations and show the planned sanitized request before asking for approval.

## Reporting Issues

For public repositories, report vulnerabilities through the repository's private security advisory flow when available. Do not publish live credentials, account data, or exploitable details in public issues.

