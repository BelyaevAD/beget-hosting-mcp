# Beget Hosting MCP

**Язык:** Русский | [English](README.en.md)

[![CI](https://github.com/BelyaevAD/beget-hosting-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/BelyaevAD/beget-hosting-mcp/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](pyproject.toml)
[![MCP](https://img.shields.io/badge/MCP-2025--06--18-purple.svg)](https://modelcontextprotocol.io/)

MCP-сервер для официального API хостинга Beget. Он предоставляет MCP-совместимым клиентам и агентам автоматизации операции управления аккаунтом, доменами, DNS, сайтами, FTP, MySQL, почтой, Cron, резервными копиями и статистикой.

Проект предоставляет MCP-клиентам и агентам контролируемый интерфейс инструментов для управления хостингом Beget: сведениями об аккаунте, сайтами, доменами, DNS, FTP, MySQL, почтой, Cron, резервными копиями и статистикой.

Корпус документации API сохранён в `docs/`; MCP-сервер использует подготовленные на его основе машиночитаемые метаданные методов.

## Ссылки

- Лендинг: https://belyaevad.github.io/beget-hosting-mcp/
- Репозиторий: https://github.com/BelyaevAD/beget-hosting-mcp
- Релизы: https://github.com/BelyaevAD/beget-hosting-mcp/releases
- Корпус документации: [docs/README.md](docs/README.md)
- Руководство оператора: [docs/operator-guide.md](docs/operator-guide.md)
- Настройки API Beget: https://cp.beget.com/settings/security/api
- Официальная документация API Beget: https://beget.com/ru/kb/api/beget-api

## Статус

Альфа-версия. Сначала используйте режим только для чтения. Операции записи намеренно защищены дополнительными ограничениями.

## Установка

Из локальной копии репозитория:

```powershell
python -m pip install .
```

Для глобальной системной установки CLI через `pipx`:

```powershell
pipx install .
```

После установки будет доступна команда:

```powershell
beget-hosting-mcp
```

Сторонние зависимости Python не требуются.

## Учётные данные

MCP использует транспорт stdio. MCP-клиент запускает сервер как локальный процесс и обменивается с ним данными через stdin/stdout.

Учётные данные Beget относятся к конфигурации процесса, а не к аутентификации транспорта MCP. Задайте их в конфигурации MCP-клиента или в окружении системной учётной записи, от имени которой запускается сервер:

```powershell
BEGET_LOGIN=your-login
BEGET_API_PASSWORD=your-api-password
```

В `BEGET_API_PASSWORD` нужно указать отдельный пароль API Beget, а не основной пароль панели управления. Откройте в панели Beget страницу `https://cp.beget.com/settings/security/api`, задайте пароль API и явно разрешите аутентификацию через API перед использованием сервера.

Если в панели Beget включены ограничения доступа по IP, они распространяются и на API. Адрес машины с MCP-сервером должен быть разрешён на странице `https://cp.beget.com/settings/security/ip`.

Не добавляйте учётные данные в коммиты и не отправляйте их в чаты.

Операции записи отключены, если не задано:

```powershell
BEGET_ALLOW_WRITE=true
```

Даже при включённой записи каждый вызов с побочным эффектом требует `confirm_write=true`.

## Конфигурация MCP-клиента

Конфигурация для установленной команды:

```json
{
  "mcpServers": {
    "beget-hosting": {
      "type": "stdio",
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

Для разработки из локальной копии:

```powershell
python -m pip install -e .
```

Для профиля с разрешённой записью добавьте:

```json
{
  "BEGET_ALLOW_WRITE": "true"
}
```

Для операций записи рекомендуется использовать отдельный профиль MCP.

### Cursor в Windows

Cursor читает глобальные MCP-серверы из `%USERPROFILE%\.cursor\mcp.json`. Графические приложения не всегда получают тот же `PATH`, что и интерактивный терминал, поэтому наиболее надёжная конфигурация Windows использует абсолютный путь к интерпретатору Python, в котором установлен этот пакет:

```powershell
py -0p
python -m pip install --upgrade .
```

```json
{
  "mcpServers": {
    "beget_hosting": {
      "type": "stdio",
      "command": "C:\\Path\\To\\python.exe",
      "args": ["-u", "-m", "beget_mcp.server"],
      "env": {
        "BEGET_LOGIN": "your-login",
        "BEGET_API_PASSWORD": "your-api-password"
      }
    }
  }
}
```

Замените `command` на путь к интерпретатору, который показала команда `py -0p` и который использовался при установке. Флаг `-u` включает небуферизованный stdio. Обёртка через `cmd.exe` или `run.cmd` не требуется: Cursor передаёт значения `env` непосредственно процессу, в том числе пароли со специальными символами оболочки.

Версия 0.1.1 исправляет обнаружение инструментов в Cursor благодаря использованию требуемого MCP построчного формата JSON-RPC в stdio. Если Cursor продолжает показывать `Loading tools`, проверьте установленную версию и запустите протокольные тесты:

```powershell
python -m pip show beget-hosting-mcp
python -m unittest discover -s tests -v
```

В трассировке сервера должен появиться `initialize`, а затем `tools/list`. Повторяющиеся события `serve_stdio_start` и `serve_stdio_eof`, между которыми нет запросов, обычно означают, что всё ещё установлена устаревшая версия до 0.1.1.

## Инструменты

- `beget_list_methods`: возвращает список документированных методов.
- `beget_get_method_docs`: возвращает сохранённую документацию одного метода Beget API.
- `beget_call`: вызывает любой документированный метод Beget API.
- `beget_get_account_info`: сокращённый вызов `user.getAccountInfo`.

MCP-клиенты должны обнаруживать эти инструменты через стандартный запрос `tools/list`. Для проверки метаданных инструментов вне клиента, например Cursor, сервер также поддерживает команду `beget-hosting-mcp --list-tools`.

Транспорт stdio записывает ровно одно компактное сообщение JSON-RPC в каждой строке, как требует MCP. Для совместимости со старыми пользовательскими клиентами сервер также принимает входящие сообщения в формате `Content-Length` и отвечает в том же формате.

## Модель безопасности

- Учётные данные загружаются только из переменных окружения.
- Запросы отправляются методом `POST`.
- Секреты скрываются в результатах dry-run и сообщениях об ошибках.
- Методы с побочными эффектами блокируются без `BEGET_ALLOW_WRITE=true`.
- Для вызовов с побочными эффектами дополнительно требуется `confirm_write=true`.
- Перед выполнением операции записи рекомендуется сначала запускать её в режиме dry-run.
- Сервер проверяет ошибки как верхнего уровня ответа Beget, так и вложенного результата метода.

## Задержки при проверке изменений

Успешный ответ некоторых методов Beget означает, что запрос принят, но связанным системам ещё требуется время, чтобы применить или увидеть изменение. Изменения DNS могут отображаться в Beget раньше, чем их увидят рекурсивные DNS-серверы и браузеры; перед признанием публичной проверки неуспешной дождитесь перезагрузки авторитетных DNS-серверов и обычного распространения в пределах TTL. Восстановление и загрузка резервных копий создают фоновые задания, поэтому перед проверкой восстановленных данных опрашивайте `backup.getLog`. Изменения сайтов, привязок доменов, PHP, почты, MySQL и Cron также могут потребовать небольшой задержки или наступления следующего запланированного запуска.

## Быстрые проверки

```powershell
beget-hosting-mcp --check-docs
beget-hosting-mcp --list-tools
python -m unittest discover -s tests -v
```

Проверка запроса без обращения к Beget:

```powershell
$env:BEGET_LOGIN = "demo-login"
$env:BEGET_API_PASSWORD = "demo-password"
beget-hosting-mcp --dry-run-account-info
```

## Корпус документации

- `docs/source-pages/`: полные Markdown-копии страниц документации Beget API.
- `docs/beget-hosting-api.md`: нормализованный технический справочник.
- `docs/contract-audit-2026-10-15.md`: результаты актуальной сверки контрактов и read-only проверки.
- `docs/method-index.md`: индекс методов.
- `docs/operator-guide.md`: правила использования и типовые сценарии.
- `docs/schema/methods.json`: машиночитаемые сведения о методах, параметрах и найденных ошибках примеров.
- `scripts/build_beget_docs.py`: генератор корпуса документации.

## Ошибки и неоднозначности в документации Beget

Исходные страницы сохраняются без исправлений. Генератор проверяет endpoint, HTTPS, percent-encoding и JSON в примерах, а найденные расхождения записывает в поле `notes` соответствующего метода. Среди подтверждённых проблем: `stat.getSiteListLoad` фактически вызывает endpoint `getSitesListLoad`, один пример `cron.edit` ошибочно ведёт на `cron.add`, а несколько примеров DNS и почты содержат повреждённый JSON.
