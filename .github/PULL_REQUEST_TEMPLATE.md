## Summary

Describe the problem and the outcome of this pull request.

## Related Issue

Link the related issue or write `N/A`.

## Changes

- Describe the main implementation changes.

## Validation

List the checks you ran and their results.

- [ ] `python -m unittest discover -s tests -v`
- [ ] `python -m compileall src scripts tests`
- [ ] `beget-hosting-mcp --check-docs`
- [ ] `beget-hosting-mcp --list-tools`

## Safety

- [ ] No credentials, account data, or generated trace logs are included.
- [ ] MCP tool inputs and outputs remain validated and appropriately redacted.
- [ ] Write-capable changes preserve `BEGET_ALLOW_WRITE=true` and per-call `confirm_write=true` safeguards.
- [ ] User-facing or operational behavior changes are documented.

## Additional Notes

Add migration, compatibility, rollout, or follow-up details when applicable.
