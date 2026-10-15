from __future__ import annotations

import html
import json
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

BASE_URL = "https://beget.com"
API_BASE_URL = f"{BASE_URL}/ru/kb/api"
ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
SOURCE_DIR = DOCS_DIR / "source-pages"
SCHEMA_DIR = DOCS_DIR / "schema"
PACKAGE_METHODS_PATH = ROOT / "src" / "beget_mcp" / "data" / "methods.json"

PAGES = [
    ("beget-api", "overview"),
    ("obshhij-princzip-raboty-s-api", "principles"),
    ("funkczii-upravleniya-akkauntom", "user"),
    ("funkczii-upravleniya-bekapami", "backup"),
    ("funkczii-upravleniya-cron", "cron"),
    ("funkczii-upravleniya-dns", "dns"),
    ("funkczii-upravleniya-ftp", "ftp"),
    ("funkczii-upravleniya-mysql", "mysql"),
    ("funkczii-upravleniya-sajtami", "site"),
    ("funkczii-dlya-raboty-s-domenami", "domain"),
    ("funkczii-dlya-raboty-s-pochtoj", "mail"),
    ("funkczii-dlya-sbora-statistiki", "stat"),
]

SECTION_BY_SLUG = {slug: section for slug, section in PAGES}

METHOD_SECTION_PREFIX = {
    "user": "user",
    "backup": "backup",
    "cron": "cron",
    "dns": "dns",
    "ftp": "ftp",
    "mysql": "mysql",
    "site": "site",
    "domain": "domain",
    "mail": "mail",
    "stat": "stat",
}

SIDE_EFFECT_WORDS = (
    "add",
    "change",
    "clear",
    "create",
    "delete",
    "download",
    "drop",
    "edit",
    "forwardListAdd",
    "forwardListDelete",
    "freeze",
    "link",
    "remove",
    "restore",
    "set",
    "toggle",
    "unlink",
    "unfreeze",
)

METHOD_HEADING_RE = re.compile(
    r"^(?:get|add|change|check|clear|create|delete|download|drop|edit|forward|freeze|is|link|remove|restore|set|toggle|unfreeze|unlink)[A-Za-z0-9]*$"
)

PARAMETER_RE = re.compile(r"^-\s+\*\*([^*]+)\*\*\s*(?:[-–—]\s*)?(.*)$")


def fetch_text(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; beget-api-docs-builder/1.0)",
            "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def find_payload_url(page_html: str) -> str:
    match = re.search(r'data-src="([^"]+_payload\.json\?[^"]+)"', page_html)
    if not match:
        raise ValueError("Nuxt payload URL was not found")
    return html.unescape(match.group(1))


def discover_api_slugs(page_html: str) -> set[str]:
    slugs: set[str] = set()
    for href in re.findall(r'href=["\']([^"\']+)["\']', page_html):
        path = urllib.parse.urlsplit(html.unescape(href)).path.rstrip("/")
        prefix = "/ru/kb/api/"
        if path.startswith(prefix):
            slug = path.removeprefix(prefix)
            if slug and "/" not in slug:
                slugs.add(slug)
    return slugs


class DevalueDecoder:
    def __init__(self, data: list[Any]):
        self.data = data
        self.memo: dict[int, Any] = {}

    def decode(self, index: int = 0) -> Any:
        if index in self.memo:
            return self.memo[index]
        node = self.data[index]
        result = self._decode_node(node)
        self.memo[index] = result
        return result

    def _decode_ref(self, value: Any) -> Any:
        if isinstance(value, int) and -1 <= value < len(self.data):
            if value == -1:
                return None
            return self.decode(value)
        return self._decode_node(value)

    def _decode_node(self, node: Any) -> Any:
        if isinstance(node, dict):
            return {key: self._decode_ref(value) for key, value in node.items()}
        if isinstance(node, list):
            if len(node) >= 2 and node[0] in {
                "Reactive",
                "Ref",
                "ShallowReactive",
                "EmptyRef",
                "Set",
            }:
                if node[0] == "EmptyRef":
                    return self._decode_ref(node[1])
                if node[0] == "Set":
                    return [self._decode_ref(value) for value in node[1:]]
                return self._decode_ref(node[1])
            return [self._decode_ref(value) for value in node]
        return node


def find_page_object(decoded: Any, slug: str) -> dict[str, Any]:
    target = f"/kb/api/{slug}"
    stack = [decoded]
    seen: set[int] = set()
    while stack:
        item = stack.pop()
        if id(item) in seen:
            continue
        seen.add(id(item))
        if isinstance(item, dict):
            route = item.get("route")
            if isinstance(route, dict) and route.get("path") == target and item.get("content"):
                return item
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)
    raise ValueError(f"Page object was not found for {slug}")


def slugify_anchor(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\wа-яёА-ЯЁ.-]+", "-", text, flags=re.IGNORECASE)
    return re.sub(r"-+", "-", text).strip("-")


class MarkdownConverter(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.links: list[str] = []
        self.list_stack: list[str] = []
        self.in_pre = False
        self.in_code = False
        self.skip_depth = 0
        self.href_stack: list[str | None] = []

    def emit(self, text: str) -> None:
        if self.skip_depth == 0:
            self.parts.append(text)

    def ensure_blank(self) -> None:
        if not self.parts:
            return
        current = "".join(self.parts)
        if not current.endswith("\n\n"):
            if current.endswith("\n"):
                self.parts.append("\n")
            else:
                self.parts.append("\n\n")

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {key: value or "" for key, value in attrs}
        classes = attrs_dict.get("class", "")
        if tag in {"script", "style"}:
            self.skip_depth += 1
            return
        if tag == "div" and "wp-block-beget-image" in classes:
            self.ensure_blank()
        if tag in {"p", "blockquote"}:
            self.ensure_blank()
        elif tag in {"h1", "h2", "h3", "h4"}:
            self.ensure_blank()
            level = int(tag[1])
            self.emit("#" * level + " ")
        elif tag in {"strong", "b"}:
            self.emit("**")
        elif tag in {"em", "i"}:
            self.emit("_")
        elif tag == "br":
            self.emit("\n")
        elif tag in {"ul", "ol"}:
            self.ensure_blank()
            self.list_stack.append(tag)
        elif tag == "li":
            self.emit("\n")
            marker = "1." if self.list_stack and self.list_stack[-1] == "ol" else "-"
            self.emit(f"{marker} ")
        elif tag == "pre":
            self.ensure_blank()
            self.in_pre = True
            self.emit("```text\n")
        elif tag == "code" and not self.in_pre:
            self.in_code = True
            self.emit("`")
        elif tag == "a":
            self.href_stack.append(attrs_dict.get("href"))
            self.emit("[")
        elif tag == "img":
            src = attrs_dict.get("src", "")
            alt = attrs_dict.get("alt", "")
            if src:
                self.ensure_blank()
                self.emit(f"![{alt}]({src})\n")
        elif tag == "table":
            self.ensure_blank()
        elif tag in {"tr", "td", "th"}:
            self.emit(" ")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"}:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if self.skip_depth:
            return
        if tag in {"p", "blockquote", "h1", "h2", "h3", "h4", "table"}:
            self.ensure_blank()
        elif tag in {"strong", "b"}:
            self.emit("**")
        elif tag in {"em", "i"}:
            self.emit("_")
        elif tag in {"ul", "ol"}:
            if self.list_stack:
                self.list_stack.pop()
            self.ensure_blank()
        elif tag == "li":
            self.emit("\n")
        elif tag == "pre":
            self.emit("\n```\n")
            self.in_pre = False
            self.ensure_blank()
        elif tag == "code" and self.in_code:
            self.emit("`")
            self.in_code = False
        elif tag == "a":
            href = self.href_stack.pop() if self.href_stack else None
            if href:
                if href.startswith("/"):
                    href = BASE_URL + href
                self.emit(f"]({href})")
            else:
                self.emit("]")
        elif tag == "tr":
            self.emit("\n")

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        if self.in_pre:
            self.emit(data)
            return
        text = re.sub(r"\s+", " ", data)
        if text.strip():
            self.emit(text)

    def markdown(self) -> str:
        text = "".join(self.parts)
        text = text.replace("\xa0", " ")
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r" +", " ", text)
        return text.strip() + "\n"


def html_to_markdown(content: str) -> str:
    converter = MarkdownConverter()
    converter.feed(content)
    return converter.markdown()


def clean_heading(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).replace("\xa0", " ").strip()


def extract_headings(content: str) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    for match in re.finditer(r"<h([1-4])[^>]*>(.*?)</h\1>", content, re.DOTALL):
        headings.append((int(match.group(1)), clean_heading(match.group(2))))
    return headings


def extract_method_blocks(content: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"<h([2-3])[^>]*>(.*?)</h\1>", content, re.DOTALL))
    method_positions: list[tuple[int, int, str]] = []
    for match in matches:
        name = clean_heading(match.group(2))
        if METHOD_HEADING_RE.match(name):
            method_positions.append((match.start(), match.end(), name))
    blocks: list[tuple[str, str]] = []
    for index, (_, end, name) in enumerate(method_positions):
        next_start = method_positions[index + 1][0] if index + 1 < len(method_positions) else len(content)
        blocks.append((name, content[end:next_start]))
    return blocks


def extract_code_samples(markdown: str) -> list[str]:
    return [match.group(1).strip() for match in re.finditer(r"```text\n(.*?)\n```", markdown, re.DOTALL)]


def extract_urls(text: str) -> list[str]:
    urls = re.findall(r"https?://api\.beget\.com/api/[^\s)`\"<>]+", text)
    seen: set[str] = set()
    ordered: list[str] = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            ordered.append(url)
    return ordered


def extract_parameters(markdown: str) -> list[dict[str, Any]]:
    match = re.search(r"### Дополнительные параметры\n(.*?)(?=\n### |\Z)", markdown, re.DOTALL)
    if not match:
        return []

    parameters: list[dict[str, Any]] = []
    for line in match.group(1).splitlines():
        parameter_match = PARAMETER_RE.match(line.strip())
        if not parameter_match:
            continue
        name = parameter_match.group(1).strip()
        description = parameter_match.group(2).strip().rstrip(";")
        normalized = description.lower()
        optional = any(
            marker in normalized
            for marker in ("необязатель", "если не задан", "если не указан", "если не передан", "по умолчанию")
        )
        type_hint: str | None = None
        if "массив" in normalized or "список" in normalized:
            type_hint = "array"
        elif "тип int" in normalized:
            type_hint = "integer"
        elif "boolean" in normalized:
            type_hint = "boolean"
        parameters.append(
            {
                "name": name,
                "description": description,
                "required": False if optional else None,
                "type_hint": type_hint,
                "sensitive": any(marker in name.lower() for marker in ("password", "passwd", "token", "secret")),
            }
        )
    return parameters


def inspect_example_urls(
    section: str,
    method: str,
    documented_endpoint_method: str,
    urls: list[str],
) -> list[str]:
    warnings: list[str] = []

    def warn(message: str) -> None:
        if message not in warnings:
            warnings.append(message)

    for url in urls:
        parsed = urllib.parse.urlsplit(url)
        parts = parsed.path.rstrip("/").split("/")
        example_section = parts[-2] if len(parts) >= 2 else ""
        example_method = parts[-1] if parts else ""
        if parsed.scheme != "https":
            warn(f"Documentation contains a non-HTTPS example URL for `{method}`; use HTTPS.")
        if example_section != section:
            warn(
                f"Documentation example targets section `{example_section}` instead of `{section}`."
            )
        if example_method != documented_endpoint_method:
            warn(
                "Documentation contains an inconsistent example endpoint: "
                f"`{example_section}.{example_method}` instead of "
                f"`{section}.{documented_endpoint_method}`."
            )

        query = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
        if (
            parsed.query
            and not {"login", "passwd"}.issubset(query)
            and ("%3d" in parsed.query.lower() or "%26" in parsed.query.lower())
        ):
            warn(
                "Documentation contains an example with the entire query string percent-encoded; "
                "encode parameter values, not query separators."
            )
        for input_data in query.get("input_data", []):
            if len(input_data) <= 1 or not input_data.lstrip().startswith(("{", "[")):
                continue
            try:
                json.loads(input_data)
            except json.JSONDecodeError:
                warn(
                    "Documentation contains an example whose decoded `input_data` is invalid JSON; "
                    "construct JSON from structured parameters instead of copying the example verbatim."
                )
    return warnings


def is_side_effectful(method: str) -> bool:
    return any(method.startswith(word) for word in SIDE_EFFECT_WORDS)


def infer_endpoint(section: str, method: str, markdown: str) -> str:
    urls = extract_urls(markdown)
    for url in urls:
        if re.search(rf"/{re.escape(method)}(?:\?|$)", url):
            return f"https://api.beget.com{urllib.parse.urlsplit(url).path}"
    if urls:
        return f"https://api.beget.com{urllib.parse.urlsplit(urls[0]).path}"
    api_section = METHOD_SECTION_PREFIX.get(section, section)
    return f"https://api.beget.com/api/{api_section}/{method}"


def endpoint_method(endpoint: str) -> str:
    return endpoint.rstrip("/").rsplit("/", 1)[-1]


@dataclass
class PageData:
    slug: str
    section: str
    source_url: str
    payload_url: str
    title: str
    excerpt: str
    published_at: str
    modified_at: str
    content_html: str
    markdown: str
    headings: list[tuple[int, str]]


def load_page(slug: str, section: str) -> PageData:
    source_url = f"{API_BASE_URL}/{slug}"
    page_html = fetch_text(source_url)
    payload_url = find_payload_url(page_html)
    payload = json.loads(fetch_text(payload_url))
    decoded = DevalueDecoder(payload).decode()
    page = find_page_object(decoded, slug)
    content_html = page["content"]
    markdown = html_to_markdown(content_html)
    return PageData(
        slug=slug,
        section=section,
        source_url=source_url,
        payload_url=payload_url,
        title=page.get("title", slug),
        excerpt=page.get("excerpt", ""),
        published_at=page.get("published_at", ""),
        modified_at=page.get("modified_at", ""),
        content_html=content_html,
        markdown=markdown,
        headings=extract_headings(content_html),
    )


def page_markdown(page: PageData) -> str:
    frontmatter = [
        "---",
        f"title: {json.dumps(page.title, ensure_ascii=False)}",
        f"source_url: {page.source_url}",
        f"payload_url: {page.payload_url}",
        f"published_at: {page.published_at}",
        f"modified_at: {page.modified_at}",
        f"section: {page.section}",
        "---",
        "",
        f"# {page.title}",
        "",
        f"Source: [{page.source_url}]({page.source_url})",
        "",
    ]
    return "\n".join(frontmatter) + page.markdown


def build_method_records(pages: list[PageData]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for page in pages:
        if page.section in {"overview", "principles"}:
            continue
        for method, block_html in extract_method_blocks(page.content_html):
            block_md = html_to_markdown(block_html)
            examples = extract_code_samples(block_md)
            endpoint = infer_endpoint(page.section, method, block_md)
            notes: list[str] = []
            documented_endpoint_method = endpoint_method(endpoint)
            if documented_endpoint_method != method:
                notes.append(
                    "Documentation heading and example endpoint use different method names: "
                    f"heading `{method}`, endpoint `{documented_endpoint_method}`."
                )
            urls = extract_urls(block_md)
            notes.extend(
                inspect_example_urls(page.section, method, documented_endpoint_method, urls)
            )
            records.append(
                {
                    "section": page.section,
                    "method": method,
                    "endpoint": endpoint,
                    "endpoint_method": documented_endpoint_method,
                    "source_url": page.source_url,
                    "source_page": f"../source-pages/{page.slug}.md",
                    "anchor": slugify_anchor(method),
                    "side_effectful": is_side_effectful(method),
                    "parameters": extract_parameters(block_md),
                    "examples": examples,
                    "api_urls_found": urls,
                    "notes": notes,
                    "documentation": block_md,
                }
            )
    return records


def build_pages_schema(pages: list[PageData], generated_at: str) -> list[dict[str, Any]]:
    return [
        {
            "slug": page.slug,
            "section": page.section,
            "title": page.title,
            "source_url": page.source_url,
            "payload_url": page.payload_url,
            "local_file": f"docs/source-pages/{page.slug}.md",
            "published_at": page.published_at,
            "modified_at": page.modified_at,
            "generated_at": generated_at,
            "headings": [{"level": level, "text": text} for level, text in page.headings],
        }
        for page in pages
    ]


def build_errors_schema() -> dict[str, Any]:
    return {
        "top_level_envelope": {
            "status": "success|error",
            "answer": "Method execution envelope when top-level status is success",
            "error_text": "Human-readable error message when status is error",
            "error_code": "Numeric error code when status is error",
        },
        "method_envelope": {
            "status": "success|error",
            "result": "Method-specific payload when method status is success",
            "errors": "List of method-level errors when method status is error",
        },
        "request_error_codes": [
            {
                "code": "AUTH_ERROR",
                "meaning": "Authentication failed or required login/passwd parameters are invalid.",
                "source": "docs/source-pages/obshhij-princzip-raboty-s-api.md",
            },
            {
                "code": "INCORRECT_REQUEST",
                "meaning": "The API request is malformed or uses invalid top-level request parameters.",
                "source": "docs/source-pages/obshhij-princzip-raboty-s-api.md",
            },
            {
                "code": "NO_SUCH_METHOD",
                "meaning": "The requested API method does not exist.",
                "source": "docs/source-pages/obshhij-princzip-raboty-s-api.md",
            },
        ],
        "method_error_codes": [
            {
                "code": "INVALID_DATA",
                "meaning": "Validation failed for method input data.",
                "source": "docs/source-pages/obshhij-princzip-raboty-s-api.md",
            },
            {
                "code": "LIMIT_ERROR",
                "meaning": "A limit was reached, including account limits or the documented API limit of no more than 60 requests per minute per user.",
                "source": "docs/source-pages/obshhij-princzip-raboty-s-api.md",
            },
            {
                "code": "METHOD_FAILED",
                "meaning": "Internal error while executing the method.",
                "source": "docs/source-pages/obshhij-princzip-raboty-s-api.md",
            },
        ],
        "notes": [
            "Wrapper code must check both the top-level response status and the nested method status in answer.",
            "Wrapper exceptions should expose raw error_code/error_text for top-level failures and raw errors for method-level failures.",
        ],
    }


def build_method_index(records: list[dict[str, Any]]) -> str:
    lines = [
        "# Beget Hosting API Method Index",
        "",
        "This index is generated from the preserved Beget KB pages.",
        "",
    ]
    for section in METHOD_SECTION_PREFIX:
        section_records = [record for record in records if record["section"] == section]
        if not section_records:
            continue
        lines.extend([f"## `{section}`", ""])
        for record in section_records:
            side = " side-effectful" if record["side_effectful"] else ""
            source_link = record["source_page"].removeprefix("../")
            lines.append(
                f"- `{record['method']}` -> `{record['endpoint']}`{side}; source: "
                f"[{Path(record['source_page']).name}]({source_link})"
            )
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def build_api_spec(pages: list[PageData], records: list[dict[str, Any]], generated_at: str) -> str:
    source_lines = "\n".join(
        f"- [{page.title}](source-pages/{page.slug}.md), modified `{page.modified_at}`"
        for page in pages
    )
    section_lines = []
    for section in METHOD_SECTION_PREFIX:
        section_records = [record for record in records if record["section"] == section]
        if section_records:
            methods = ", ".join(f"`{record['method']}`" for record in section_records)
            section_lines.append(f"- `{section}`: {methods}")
    warning_lines = []
    for record in records:
        for note in record["notes"]:
            warning_lines.append(f"- `{record['section']}.{record['method']}`: {note}")
    if not warning_lines:
        warning_lines.append("- No documentation inconsistencies detected.")
    return f"""# Beget Hosting API Technical Reference

Generated: `{generated_at}`

This document normalizes the official Beget hosting API documentation for later wrapper implementation. Full source pages are preserved in `docs/source-pages/`; machine-readable metadata is in `docs/schema/`.

## Scope

This corpus covers the Beget hosting API documented under `{API_BASE_URL}`. It does not cover the separate Beget cloud API at `https://developer.beget.com`.

## Transport

- Protocol: HTTPS.
- Base endpoint pattern: `https://api.beget.com/api/{{section}}/{{method}}`.
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

{chr(10).join(section_lines)}

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

{chr(10).join(warning_lines)}

## Source Pages

{source_lines}
"""


def build_readme(generated_at: str) -> str:
    return f"""# Beget API Documentation Corpus

Generated: `{generated_at}`

This repository contains a local Markdown and JSON corpus for the official Beget hosting API documentation.

## Layout

- `source-pages/`: full Markdown copies of the official KB pages.
- `beget-hosting-api.md`: normalized technical reference for wrapper design.
- `contract-audit-2026-10-15.md`: dated contract comparison and live read-only verification notes.
- `method-index.md`: method list grouped by API section.
- `schema/pages.json`: page metadata and source URLs.
- `schema/methods.json`: method metadata, examples, source snippets, side-effect flags.
- `schema/methods.json` also includes extracted parameter descriptions and warnings for inconsistent examples.
- `schema/errors.json`: common response envelope and error-handling notes.

## Regeneration

Run:

```powershell
python scripts/build_beget_docs.py
```

The generator reads the Nuxt `_payload.json` for each Beget KB page and does not require a browser.
"""


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(UTC).isoformat()

    overview_html = fetch_text(f"{API_BASE_URL}/beget-api")
    discovered_slugs = discover_api_slugs(overview_html)
    expected_slugs = {slug for slug, _ in PAGES}
    if discovered_slugs != expected_slugs:
        added = sorted(discovered_slugs - expected_slugs)
        removed = sorted(expected_slugs - discovered_slugs)
        raise RuntimeError(
            "Beget API page inventory changed. "
            f"Add mappings for new pages or review removed pages. added={added}, removed={removed}"
        )

    pages = [load_page(slug, section) for slug, section in PAGES]
    records = build_method_records(pages)
    keys = [(record["section"], record["method"]) for record in records]
    if len(keys) != len(set(keys)):
        raise RuntimeError("Duplicate Beget API method keys were generated.")

    for page in pages:
        (SOURCE_DIR / f"{page.slug}.md").write_text(page_markdown(page), encoding="utf-8")

    (DOCS_DIR / "beget-hosting-api.md").write_text(
        build_api_spec(pages, records, generated_at), encoding="utf-8"
    )
    (DOCS_DIR / "method-index.md").write_text(build_method_index(records), encoding="utf-8")
    (DOCS_DIR / "README.md").write_text(build_readme(generated_at), encoding="utf-8")
    write_json(SCHEMA_DIR / "pages.json", build_pages_schema(pages, generated_at))
    write_json(SCHEMA_DIR / "methods.json", records)
    write_json(PACKAGE_METHODS_PATH, records)
    write_json(SCHEMA_DIR / "errors.json", build_errors_schema())

    print(f"Generated {len(pages)} pages and {len(records)} methods.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
