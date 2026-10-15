# Beget Hosting API Technical Reference

Generated: `2026-10-15T15:29:42.791628+00:00`

This document normalizes the official Beget hosting API documentation for later wrapper implementation. Full source pages are preserved in `docs/source-pages/`; machine-readable metadata is in `docs/schema/`.

## Scope

This corpus covers the Beget hosting API documented under `https://beget.com/ru/kb/api`. It does not cover the separate Beget cloud API at `https://developer.beget.com`.

## Transport

- Protocol: HTTPS.
- Base endpoint pattern: `https://api.beget.com/api/{section}/{method}`.
- Requests may use GET, POST, or a combination. Beget recommends POST to avoid URL length limits.
- The wrapper should keep a generic call primitive because all documented methods follow the same transport and response envelope.

## Authentication

Every API request must include:

- `login`: hosting account login.
- `passwd`: dedicated API password, URL-encoded before transmission.

Never log `passwd`, full request URLs containing credentials, or generated URLs with sensitive query parameters.

API authentication is disabled by default in Beget accounts. Operators must open `https://cp.beget.com/settings/security/api`, set a separate API password, and explicitly allow API authentication. The regular control-panel password should not be used as `BEGET_API_PASSWORD`.

If control-panel IP access restrictions are configured at `https://cp.beget.com/settings/security/ip`, they also apply to API requests. The MCP server machine must be allowed there.

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

## Eventual Consistency

Several operations are accepted by the API before every dependent system has applied the result. Wrapper and agent logic should separate "API accepted the request" from "the real-world effect is observable".

- DNS updates can be visible in Beget before recursive resolvers, browsers, mail providers, and external checkers see them. Verify authoritative nameservers first, then public resolvers after TTL/cache delay.
- Domain registration, renewal, deletion, and delegation fields can lag behind an accepted operation because registrar state is external.
- Site creation, deletion, and domain link/unlink operations can require web server routing reload time before HTTP checks are reliable.
- PHP version and directive changes can require runtime/web server reload time after API state changes.
- Backup restore/download methods create jobs. Use `backup.getLog` and wait for a final status before validating files, databases, or download availability.
- MySQL, mail, and Cron changes should be verified through their read methods first; application connections, message delivery, or scheduled execution can lag behind configuration state.

## Documentation Defects and Ambiguities

The source pages are preserved verbatim. Detected inconsistencies are recorded in each method's `notes` field so agents do not copy broken examples into live requests.

- `cron.edit`: Documentation contains an inconsistent example endpoint: `cron.add` instead of `cron.edit`.
- `dns.changeRecords`: Documentation contains an example whose decoded `input_data` is invalid JSON; construct JSON from structured parameters instead of copying the example verbatim.
- `domain.getPhpVersion`: Documentation contains a non-HTTPS example URL for `getPhpVersion`; use HTTPS.
- `domain.getPhpVersion`: Documentation contains an example with the entire query string percent-encoded; encode parameter values, not query separators.
- `mail.forwardListAddMailbox`: Documentation contains an example whose decoded `input_data` is invalid JSON; construct JSON from structured parameters instead of copying the example verbatim.
- `mail.forwardListDeleteMailbox`: Documentation contains an example whose decoded `input_data` is invalid JSON; construct JSON from structured parameters instead of copying the example verbatim.
- `stat.getSiteListLoad`: Documentation heading and example endpoint use different method names: heading `getSiteListLoad`, endpoint `getSitesListLoad`.

## Source Pages

- [Beget.API Хостинга](source-pages/beget-api.md), modified `2025-09-02T10:54:12.000Z`
- [Принципы работы с API](source-pages/obshhij-princzip-raboty-s-api.md), modified `2026-09-21T03:46:01.000Z`
- [Управление аккаунтом по API](source-pages/funkczii-upravleniya-akkauntom.md), modified `2026-07-16T18:43:08.000Z`
- [Управление бэкапами по API](source-pages/funkczii-upravleniya-bekapami.md), modified `2026-07-16T18:44:41.000Z`
- [Управление Cron по API](source-pages/funkczii-upravleniya-cron.md), modified `2026-07-16T18:50:22.000Z`
- [Управление DNS по API](source-pages/funkczii-upravleniya-dns.md), modified `2026-07-16T18:57:51.000Z`
- [Управление FTP по API](source-pages/funkczii-upravleniya-ftp.md), modified `2026-07-16T18:58:29.000Z`
- [Управление MySQL по API](source-pages/funkczii-upravleniya-mysql.md), modified `2026-07-16T18:59:18.000Z`
- [Управление сайтами по API](source-pages/funkczii-upravleniya-sajtami.md), modified `2026-07-16T19:00:05.000Z`
- [Управление доменами по API](source-pages/funkczii-dlya-raboty-s-domenami.md), modified `2026-07-16T19:02:29.000Z`
- [Управление почтой по API](source-pages/funkczii-dlya-raboty-s-pochtoj.md), modified `2026-07-16T19:03:23.000Z`
- [Сбор статистики по API](source-pages/funkczii-dlya-sbora-statistiki.md), modified `2026-07-16T19:04:26.000Z`
