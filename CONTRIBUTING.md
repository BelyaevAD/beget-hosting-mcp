# Contributing

Contributions are welcome through issues and pull requests.

## Development

```powershell
python -m pip install -e .
python -m compileall src scripts
beget-hosting-mcp --check-docs
beget-hosting-mcp --list-tools
```

Do not commit real Beget credentials, API passwords, account names, domain ownership data, or generated logs with secrets.

## Pull Requests

- Keep changes focused.
- Update documentation when behavior changes.
- Run the smoke checks above before submitting.
- For write-capable behavior, include dry-run examples and explain safety implications.
