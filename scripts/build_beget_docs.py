from __future__ import annotations

import html
import json
import re
import sys
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


BASE_URL = "https://beget.com"
API_BASE_URL = f"{BASE_URL}/ru/kb/api"
ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
SOURCE_DIR = DOCS_DIR / "source-pages"
SCHEMA_DIR = DOCS_DIR / "schema"

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


def is_side_effectful(method: str) -> bool:
    return any(method.startswith(word) for word in SIDE_EFFECT_WORDS)


def infer_endpoint(section: str, method: str, markdown: str) -> str:
    urls = extract_urls(markdown)
    for url in urls:
        if re.search(rf"/{re.escape(method)}(?:\?|$)", url):
            return url.split("?")[0]
    if urls:
        return urls[0].split("?")[0]
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
                    "examples": examples,
                    "api_urls_found": extract_urls(block_md),
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
    return f"""# Beget Hosting API Technical Reference

Generated: `{generated_at}`

This document normalizes the official Beget hosting API documentation for later wrapper implementation. Full source pages are preserved in `docs/source-pages/`; machine-readable metadata is in `docs/schema/`.

## Scope

This corpus covers the Beget hosting API documented under `{API_BASE_URL}`. It does not cover the separate Beget cloud API at `https://developer.beget.com`.

## Transport

- Protocol: HTTPS.
- Base endpoint pattern: `https://api.beget.com/api/{{section}}/{{method}}`.
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

{chr(10).join(section_lines)}

## Side Effects

Methods whose names start with `add`, `change`, `clear`, `create`, `delete`, `download`, `drop`, `edit`, `freeze`, `link`, `remove`, `restore`, `set`, `toggle`, `unlink`, or `unfreeze` are marked as side-effectful in `docs/schema/methods.json`. Wrapper code should make these explicit and avoid hidden retries.

## Documentation Ambiguities

- The statistics page uses heading `getSiteListLoad`, while the documented example URL uses `getSitesListLoad`. This mismatch is preserved in `docs/schema/methods.json` via `method`, `endpoint_method`, and `notes`; wrapper implementation should decide whether to expose an alias after live API verification.

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
- `method-index.md`: method list grouped by API section.
- `schema/pages.json`: page metadata and source URLs.
- `schema/methods.json`: method metadata, examples, source snippets, side-effect flags.
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
    generated_at = datetime.now(timezone.utc).isoformat()

    pages = [load_page(slug, section) for slug, section in PAGES]
    records = build_method_records(pages)

    for page in pages:
        (SOURCE_DIR / f"{page.slug}.md").write_text(page_markdown(page), encoding="utf-8")

    (DOCS_DIR / "beget-hosting-api.md").write_text(
        build_api_spec(pages, records, generated_at), encoding="utf-8"
    )
    (DOCS_DIR / "method-index.md").write_text(build_method_index(records), encoding="utf-8")
    (DOCS_DIR / "README.md").write_text(build_readme(generated_at), encoding="utf-8")
    write_json(SCHEMA_DIR / "pages.json", build_pages_schema(pages, generated_at))
    write_json(SCHEMA_DIR / "methods.json", records)
    write_json(SCHEMA_DIR / "errors.json", build_errors_schema())

    print(f"Generated {len(pages)} pages and {len(records)} methods.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
