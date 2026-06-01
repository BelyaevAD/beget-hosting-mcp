from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import traceback
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any


API_BASE = "https://api.beget.com/api"
PROTOCOL_VERSION = "2025-06-18"
SUPPORTED_PROTOCOL_VERSIONS = {"2025-06-18", "2024-11-05"}
WRITE_ENV = "BEGET_ALLOW_WRITE"


class BegetMcpError(Exception):
    def __init__(self, message: str, code: str = "BEGET_MCP_ERROR", data: Any = None) -> None:
        super().__init__(message)
        self.code = code
        self.data = data


class BegetApiError(BegetMcpError):
    pass


@dataclass(frozen=True)
class MethodMeta:
    section: str
    method: str
    endpoint: str
    endpoint_method: str
    side_effectful: bool
    source_url: str
    source_page: str
    documentation: str
    notes: list[str]

    @property
    def key(self) -> tuple[str, str]:
        return (self.section, self.method)


def bundled_methods_text() -> str:
    return resources.files("beget_mcp").joinpath("data/methods.json").read_text(encoding="utf-8")


def load_methods(path: str | None = None) -> dict[tuple[str, str], MethodMeta]:
    if path:
        raw_text = Path(path).read_text(encoding="utf-8")
    else:
        raw_text = bundled_methods_text()
    raw_methods = json.loads(raw_text)
    result: dict[tuple[str, str], MethodMeta] = {}
    for item in raw_methods:
        meta = MethodMeta(
            section=item["section"],
            method=item["method"],
            endpoint=item["endpoint"],
            endpoint_method=item.get("endpoint_method", item["method"]),
            side_effectful=bool(item.get("side_effectful")),
            source_url=item["source_url"],
            source_page=item["source_page"],
            documentation=item.get("documentation", ""),
            notes=list(item.get("notes") or []),
        )
        result[meta.key] = meta
    return result


METHODS = load_methods(os.getenv("BEGET_METHODS_JSON"))


def trace(event: str, **fields: Any) -> None:
    path = os.getenv("BEGET_MCP_TRACE_LOG")
    if not path:
        return
    record = {
        "ts": dt.datetime.now(dt.UTC).isoformat(),
        "event": event,
        **fields,
    }
    try:
        with Path(path).open("a", encoding="utf-8") as file:
            file.write(json.dumps(redact(record), ensure_ascii=False, separators=(",", ":")) + "\n")
    except Exception:
        pass


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        redacted: dict[str, Any] = {}
        for key, item in value.items():
            if key.lower() in {"passwd", "password", "token", "secret", "api_key"}:
                redacted[key] = "***REDACTED***"
            else:
                redacted[key] = redact(item)
        return redacted
    if isinstance(value, list):
        return [redact(item) for item in value]
    return value


def env_bool(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def credentials() -> tuple[str, str]:
    login = os.getenv("BEGET_LOGIN", "").strip()
    password = os.getenv("BEGET_API_PASSWORD", "")
    if not login or not password:
        raise BegetMcpError(
            "Missing BEGET_LOGIN or BEGET_API_PASSWORD environment variable.",
            code="MISSING_CREDENTIALS",
        )
    return login, password


def method_meta(section: str, method: str) -> MethodMeta:
    try:
        return METHODS[(section, method)]
    except KeyError as exc:
        raise BegetMcpError(
            f"Unknown Beget API method: {section}.{method}",
            code="UNKNOWN_METHOD",
            data={"section": section, "method": method},
        ) from exc


def sanitize_url(endpoint: str, params: dict[str, Any]) -> str:
    return endpoint + "?" + urllib.parse.urlencode(redact(params), doseq=True)


def build_request_data(login: str, password: str, params: dict[str, Any], input_format: str) -> dict[str, str]:
    if input_format not in {"json", "plain"}:
        raise BegetMcpError("input_format must be 'json' or 'plain'.", code="INVALID_INPUT_FORMAT")

    data: dict[str, str] = {"login": login, "passwd": password, "output_format": "json"}
    if input_format == "json":
        data["input_format"] = "json"
        data["input_data"] = json.dumps(params or {}, ensure_ascii=False, separators=(",", ":"))
    else:
        data["input_format"] = "plain"
        for key, value in (params or {}).items():
            data[key] = (
                json.dumps(value, ensure_ascii=False, separators=(",", ":"))
                if isinstance(value, (dict, list))
                else str(value)
            )
    return data


def parse_beget_response(raw: bytes) -> Any:
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise BegetApiError("Beget API returned non-JSON response.", code="NON_JSON_RESPONSE") from exc


def unwrap_response(envelope: Any, return_raw: bool) -> Any:
    if not isinstance(envelope, dict):
        raise BegetApiError("Beget API returned an unexpected response shape.", code="BAD_RESPONSE_SHAPE")
    if envelope.get("status") != "success":
        raise BegetApiError(
            envelope.get("error_text") or "Beget API top-level request failed.",
            code=str(envelope.get("error_code") or "REQUEST_FAILED"),
            data={"raw": redact(envelope)},
        )

    answer = envelope.get("answer")
    if not isinstance(answer, dict):
        return envelope if return_raw else answer
    if answer.get("status") == "error":
        raise BegetApiError(
            "Beget API method failed.",
            code="METHOD_ERROR",
            data={"errors": redact(answer.get("errors")), "raw": redact(envelope)},
        )
    if answer.get("status") == "success" and "result" in answer:
        return envelope if return_raw else answer.get("result")
    return envelope if return_raw else answer


def call_beget_api(
    section: str,
    method: str,
    params: dict[str, Any] | None = None,
    input_format: str = "json",
    dry_run: bool = False,
    confirm_write: bool = False,
    return_raw: bool = False,
) -> Any:
    meta = method_meta(section, method)
    params = params or {}
    if meta.side_effectful and not dry_run:
        if not env_bool(WRITE_ENV):
            raise BegetMcpError(
                f"{section}.{method} is side-effectful. Set {WRITE_ENV}=true and pass confirm_write=true to run it.",
                code="WRITE_DISABLED",
                data={"section": section, "method": method},
            )
        if confirm_write is not True:
            raise BegetMcpError(
                f"{section}.{method} is side-effectful. pass confirm_write=true to confirm this call.",
                code="WRITE_NOT_CONFIRMED",
                data={"section": section, "method": method},
            )

    login, password = credentials()
    endpoint = f"{API_BASE}/{section}/{meta.endpoint_method}"
    data = build_request_data(login, password, params, input_format)
    if dry_run:
        return {
            "dry_run": True,
            "side_effectful": meta.side_effectful,
            "method": {"section": section, "method": method, "endpoint_method": meta.endpoint_method},
            "request": {
                "method": "POST",
                "endpoint": endpoint,
                "body": redact(data),
                "sanitized_url": sanitize_url(endpoint, data),
            },
        }

    encoded = urllib.parse.urlencode(data).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=encoded,
        headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Accept": "application/json",
            "User-Agent": "beget-hosting-mcp/0.1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise BegetApiError(
            f"Beget API HTTP error {exc.code}.",
            code="HTTP_ERROR",
            data={"status": exc.code, "body_preview": detail},
        ) from exc
    except urllib.error.URLError as exc:
        raise BegetApiError(str(exc.reason), code="NETWORK_ERROR") from exc

    return unwrap_response(parse_beget_response(raw), return_raw=return_raw)


def list_methods(section: str | None = None, include_docs: bool = False) -> list[dict[str, Any]]:
    items = sorted(METHODS.values(), key=lambda item: (item.section, item.method))
    if section:
        items = [item for item in items if item.section == section]
    result: list[dict[str, Any]] = []
    for item in items:
        record: dict[str, Any] = {
            "section": item.section,
            "method": item.method,
            "endpoint": item.endpoint,
            "endpoint_method": item.endpoint_method,
            "side_effectful": item.side_effectful,
            "source_url": item.source_url,
            "notes": item.notes,
        }
        if include_docs:
            record["documentation"] = item.documentation
        result.append(record)
    return result


def get_method_docs(section: str, method: str) -> dict[str, Any]:
    item = method_meta(section, method)
    return {
        "section": item.section,
        "method": item.method,
        "endpoint": item.endpoint,
        "endpoint_method": item.endpoint_method,
        "side_effectful": item.side_effectful,
        "source_url": item.source_url,
        "source_page": item.source_page,
        "notes": item.notes,
        "documentation": item.documentation,
    }


TOOLS: list[dict[str, Any]] = [
    {
        "name": "beget_list_methods",
        "title": "List Beget API Methods",
        "description": "List documented Beget hosting API methods, optionally filtered by section.",
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
        "inputSchema": {
            "type": "object",
            "properties": {
                "section": {"type": "string", "description": "Optional API section, e.g. user, site, domain, dns, mail."},
                "include_docs": {"type": "boolean", "description": "Include preserved method documentation snippets.", "default": False},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "beget_get_method_docs",
        "title": "Get Beget Method Documentation",
        "description": "Return preserved documentation for one Beget API method.",
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
        "inputSchema": {
            "type": "object",
            "required": ["section", "method"],
            "properties": {"section": {"type": "string"}, "method": {"type": "string"}},
            "additionalProperties": False,
        },
    },
    {
        "name": "beget_call",
        "title": "Call Beget API",
        "description": "Call any documented Beget hosting API method. Side-effectful methods require BEGET_ALLOW_WRITE=true and confirm_write=true.",
        "annotations": {"readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True},
        "inputSchema": {
            "type": "object",
            "required": ["section", "method"],
            "properties": {
                "section": {"type": "string"},
                "method": {"type": "string"},
                "params": {"type": "object", "description": "Method parameters. For json input_format these become input_data.", "additionalProperties": True, "default": {}},
                "input_format": {"type": "string", "enum": ["json", "plain"], "default": "json"},
                "dry_run": {"type": "boolean", "description": "Return sanitized request details without calling Beget.", "default": False},
                "confirm_write": {"type": "boolean", "description": "Required for side-effectful methods when dry_run is false.", "default": False},
                "return_raw": {"type": "boolean", "description": "Return full Beget response envelope instead of answer.result.", "default": False},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "beget_get_account_info",
        "title": "Get Beget Account Info",
        "description": "Shortcut for user.getAccountInfo.",
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
        "inputSchema": {
            "type": "object",
            "properties": {"return_raw": {"type": "boolean", "default": False}},
            "additionalProperties": False,
        },
    },
]


def call_tool(name: str, args: dict[str, Any]) -> Any:
    if name == "beget_list_methods":
        return list_methods(args.get("section"), bool(args.get("include_docs", False)))
    if name == "beget_get_method_docs":
        return get_method_docs(str(args["section"]), str(args["method"]))
    if name == "beget_call":
        return call_beget_api(
            section=str(args["section"]),
            method=str(args["method"]),
            params=args.get("params") or {},
            input_format=str(args.get("input_format") or "json"),
            dry_run=bool(args.get("dry_run", False)),
            confirm_write=bool(args.get("confirm_write", False)),
            return_raw=bool(args.get("return_raw", False)),
        )
    if name == "beget_get_account_info":
        return call_beget_api("user", "getAccountInfo", {}, return_raw=bool(args.get("return_raw", False)))
    raise BegetMcpError(f"Unknown tool: {name}", code="UNKNOWN_TOOL")


def response_text(value: Any) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False, indent=2)}]}


def read_message() -> dict[str, Any] | None:
    headers: dict[str, str] = {}
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        line_text = line.decode("ascii", errors="replace").strip()
        if not line_text:
            break
        if ":" in line_text:
            key, value = line_text.split(":", 1)
            headers[key.lower()] = value.strip()
    length = int(headers.get("content-length", "0"))
    if length <= 0:
        return None
    return json.loads(sys.stdin.buffer.read(length).decode("utf-8"))


def write_message(message: dict[str, Any]) -> None:
    data = json.dumps(message, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(data)}\r\n\r\n".encode("ascii"))
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()


def make_error_response(message_id: Any, exc: Exception) -> dict[str, Any]:
    data: dict[str, Any] = {}
    if isinstance(exc, BegetMcpError):
        data["code"] = exc.code
        if exc.data is not None:
            data["data"] = redact(exc.data)
    else:
        data["code"] = "INTERNAL_ERROR"
        data["traceback"] = traceback.format_exc(limit=3)
    return {"jsonrpc": "2.0", "id": message_id, "error": {"code": -32000, "message": str(exc), "data": data}}


def handle_request(message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    message_id = message.get("id")
    params = message.get("params") or {}

    trace("request", id=message_id, method=method)
    if message_id is None and method and method.startswith("notifications/"):
        return None
    if method == "initialize":
        requested_protocol = str(params.get("protocolVersion") or "")
        protocol_version = requested_protocol if requested_protocol in SUPPORTED_PROTOCOL_VERSIONS else PROTOCOL_VERSION
        return {
            "jsonrpc": "2.0",
            "id": message_id,
            "result": {
                "protocolVersion": protocol_version,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "beget-hosting-api", "version": "0.1.0"},
                "instructions": (
                    "Use tools/list to discover Beget MCP tools. Start with beget_list_methods, "
                    "then beget_get_method_docs, and call Beget methods through beget_call. "
                    "Write operations require BEGET_ALLOW_WRITE=true and confirm_write=true."
                ),
            },
        }
    if method == "ping":
        return {"jsonrpc": "2.0", "id": message_id, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": message_id, "result": {"tools": TOOLS}}
    if method == "tools/call":
        result = call_tool(str(params.get("name")), params.get("arguments") or {})
        return {"jsonrpc": "2.0", "id": message_id, "result": response_text(result)}
    if method == "resources/list":
        return {"jsonrpc": "2.0", "id": message_id, "result": {"resources": []}}
    if method == "resources/templates/list":
        return {"jsonrpc": "2.0", "id": message_id, "result": {"resourceTemplates": []}}
    if method == "prompts/list":
        return {"jsonrpc": "2.0", "id": message_id, "result": {"prompts": []}}
    if method in {"completion/complete", "logging/setLevel"}:
        return {"jsonrpc": "2.0", "id": message_id, "result": {}}
    raise BegetMcpError(f"Unsupported MCP method: {method}", code="UNSUPPORTED_MCP_METHOD")


def serve_stdio() -> int:
    trace("serve_stdio_start", protocol=PROTOCOL_VERSION, methods=len(METHODS), tools=len(TOOLS), argv=sys.argv)
    while True:
        message = read_message()
        if message is None:
            trace("serve_stdio_eof")
            return 0
        try:
            response = handle_request(message)
        except Exception as exc:
            trace("error", id=message.get("id"), method=message.get("method"), error=str(exc))
            response = make_error_response(message.get("id"), exc)
        if response is not None:
            trace("response", id=response.get("id"), has_error="error" in response)
            write_message(response)


def cli() -> int:
    parser = argparse.ArgumentParser(description="MCP server for Beget hosting API.")
    parser.add_argument("--list-tools", action="store_true", help="Print tool definitions and exit.")
    parser.add_argument("--check-docs", action="store_true", help="Validate local method metadata and exit.")
    parser.add_argument("--dry-run-account-info", action="store_true", help="Print sanitized request for user.getAccountInfo.")
    args = parser.parse_args()

    if args.list_tools:
        print(json.dumps(TOOLS, ensure_ascii=False, indent=2))
        return 0
    if args.check_docs:
        print(json.dumps({"methods": len(METHODS)}, ensure_ascii=False, indent=2))
        return 0
    if args.dry_run_account_info:
        print(json.dumps(call_beget_api("user", "getAccountInfo", {}, dry_run=True), ensure_ascii=False, indent=2))
        return 0
    return serve_stdio()


if __name__ == "__main__":
    raise SystemExit(cli())
