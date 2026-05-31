# Beget Hosting API Technical Reference

Generated: `2026-05-31T05:56:45.763631+00:00`

This document normalizes the official Beget hosting API documentation for later wrapper implementation. Full source pages are preserved in `docs/source-pages/`; machine-readable metadata is in `docs/schema/`.

## Scope

This corpus covers the Beget hosting API documented under `https://beget.com/ru/kb/api`. It does not cover the separate Beget cloud API at `https://developer.beget.com`.

## Transport

- Protocol: HTTPS.
- Base endpoint pattern: `https://api.beget.com/api/{section}/{method}`.
- Requests use query parameters.
- The wrapper should keep a generic call primitive because all documented methods follow the same transport and response envelope.

## Authentication

Every API request must include:

- `login`: hosting account login.
- `passwd`: password/API password, URL-encoded before transmission.

Never log `passwd`, full request URLs containing credentials, or generated URLs with sensitive query parameters.

## Request Formats

- `input_format=plain`: parameters are passed directly as query parameters.
- `input_format=json`: method parameters are encoded as JSON and then URL-encoded into `input_data`.
- `output_format=json`: expected response format for wrapper usage.

The wrapper should expose both a high-level method API and a low-level `request(section, method, params, input_format='json')` escape hatch.

## Response Envelopes

All calls should first be decoded as a top-level request envelope:

- `status`: request-level status, usually `success` or `error`.
- `answer`: nested method result envelope when top-level status is `success`.
- `error_text`: error description on failure.
- `error_code`: error code on failure.

When the top-level request succeeds, Beget documents a nested method envelope inside `answer`:

- `status`: method-level `success` or `error`.
- `result`: method-specific payload when method status is `success`.
- `errors`: list of method-level errors when method status is `error`.

Wrapper behavior:

- Return `answer.result` for successful high-level calls.
- Raise a typed request exception for top-level non-success status.
- Raise a typed method exception when `answer.status` is `error`.
- Preserve raw envelope, nested errors, endpoint, and sanitized params in exceptions.

## Rate Limit

The official documentation states a limit of no more than 60 API requests per minute per user. Wrapper implementations should include optional throttling and retry/backoff hooks, but must not retry non-idempotent operations by default.

## Method Sections

- `user`: `getAccountInfo`, `toggleSsh`
- `backup`: `getFileBackupList`, `getMysqlBackupList`, `getFileList`, `getMysqlList`, `restoreFile`, `restoreMysql`, `downloadFile`, `downloadMysql`, `getLog`
- `cron`: `getList`, `add`, `edit`, `delete`, `changeHiddenState`, `getEmail`, `setEmail`
- `dns`: `getData`, `changeRecords`
- `ftp`: `getList`, `add`, `changePassword`, `delete`
- `mysql`: `getList`, `addDb`, `addAccess`, `dropDb`, `dropAccess`, `changeAccessPassword`
- `site`: `getList`, `add`, `delete`, `linkDomain`, `unlinkDomain`, `freeze`, `unfreeze`, `isSiteFrozen`
- `domain`: `getList`, `getZoneList`, `addVirtual`, `delete`, `getSubdomainList`, `addSubdomainVirtual`, `deleteSubdomain`, `checkDomainToRegister`, `getPhpVersion`, `changePhpVersion`, `getDirectives`, `addDirectives`, `removeDirectives`
- `mail`: `getMailboxList`, `changeMailboxPassword`, `createMailbox`, `dropMailbox`, `changeMailboxSettings`, `forwardListAddMailbox`, `forwardListDeleteMailbox`, `forwardListShow`, `setDomainMail`, `clearDomainMail`
- `stat`: `getSiteListLoad`, `getDbListLoad`, `getSiteLoad`, `getDbLoad`

## Side Effects

Methods whose names start with `add`, `change`, `clear`, `create`, `delete`, `download`, `drop`, `edit`, `freeze`, `link`, `remove`, `restore`, `set`, `toggle`, `unlink`, or `unfreeze` are marked as side-effectful in `docs/schema/methods.json`. Wrapper code should make these explicit and avoid hidden retries.

## Documentation Ambiguities

- The statistics page uses heading `getSiteListLoad`, while the documented example URL uses `getSitesListLoad`. This mismatch is preserved in `docs/schema/methods.json` via `method`, `endpoint_method`, and `notes`; wrapper implementation should decide whether to expose an alias after live API verification.

## Source Pages

- [Beget.API Хостинга](source-pages/beget-api.md), modified `2025-09-02T10:54:12+03:00`
- [Принципы работы с API](source-pages/obshhij-princzip-raboty-s-api.md), modified `2026-03-30T10:09:36+03:00`
- [Управление аккаунтом по API](source-pages/funkczii-upravleniya-akkauntom.md), modified `2025-09-02T11:05:44+03:00`
- [Управление бэкапами по API](source-pages/funkczii-upravleniya-bekapami.md), modified `2025-09-02T11:31:55+03:00`
- [Управление Cron по API](source-pages/funkczii-upravleniya-cron.md), modified `2025-09-02T11:42:42+03:00`
- [Управление DNS по API](source-pages/funkczii-upravleniya-dns.md), modified `2025-09-02T12:00:34+03:00`
- [Управление FTP по API](source-pages/funkczii-upravleniya-ftp.md), modified `2025-09-02T12:01:55+03:00`
- [Управление MySQL по API](source-pages/funkczii-upravleniya-mysql.md), modified `2025-09-02T12:04:11+03:00`
- [Управление сайтами по API](source-pages/funkczii-upravleniya-sajtami.md), modified `2025-09-02T12:07:06+03:00`
- [Управление доменами по API](source-pages/funkczii-dlya-raboty-s-domenami.md), modified `2025-09-02T12:10:47+03:00`
- [Управление почтой по API](source-pages/funkczii-dlya-raboty-s-pochtoj.md), modified `2025-09-02T12:14:14+03:00`
- [Сбор статистики по API](source-pages/funkczii-dlya-sbora-statistiki.md), modified `2026-05-03T19:05:58+03:00`
