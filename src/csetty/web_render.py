from __future__ import annotations

import html
import re

_INLINE = re.compile(
    r"`(?P<code>[^`\n]+)`|\*\*(?P<strong>[^*\n]+)\*\*|"
    r"\[(?P<label>[^\]\n]+)\]\((?P<url>https?://[^)\s]+)\)"
)


def _inline(value: str) -> str:
    rendered: list[str] = []
    cursor = 0
    for match in _INLINE.finditer(value):
        rendered.append(html.escape(value[cursor : match.start()]))
        if match.group("code") is not None:
            rendered.append(f"<code>{html.escape(match.group('code'))}</code>")
        elif match.group("strong") is not None:
            rendered.append(f"<strong>{html.escape(match.group('strong'))}</strong>")
        else:
            label = html.escape(match.group("label"))
            url = html.escape(match.group("url"), quote=True)
            rendered.append(
                f'<a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a>'
            )
        cursor = match.end()
    rendered.append(html.escape(value[cursor:]))
    return "".join(rendered)


def markdown_to_html(markdown: str) -> str:
    """Render the small, deliberately safe Markdown subset used by local packs."""
    output: list[str] = []
    paragraph: list[str] = []
    list_kind: str | None = None
    in_code = False
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{'<br>'.join(_inline(line) for line in paragraph)}</p>")
            paragraph.clear()

    def close_list() -> None:
        nonlocal list_kind
        if list_kind is not None:
            output.append(f"</{list_kind}>")
            list_kind = None

    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            flush_paragraph()
            close_list()
            if in_code:
                output.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
                code_lines.clear()
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not stripped:
            flush_paragraph()
            close_list()
            continue
        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            close_list()
            level = len(heading.group(1))
            output.append(f"<h{level}>{_inline(heading.group(2))}</h{level}>")
            continue
        unordered = re.match(r"^[-*]\s+(.+)$", stripped)
        ordered = re.match(r"^\d+[.)]\s+(.+)$", stripped)
        if unordered or ordered:
            flush_paragraph()
            wanted = "ul" if unordered else "ol"
            if list_kind != wanted:
                close_list()
                list_kind = wanted
                output.append(f"<{wanted}>")
            item = unordered.group(1) if unordered else ordered.group(1)  # type: ignore[union-attr]
            output.append(f"<li>{_inline(item)}</li>")
            continue
        if stripped.startswith("> "):
            flush_paragraph()
            close_list()
            output.append(f"<blockquote>{_inline(stripped[2:])}</blockquote>")
            continue
        paragraph.append(stripped)

    if in_code:
        output.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
    flush_paragraph()
    close_list()
    return "\n".join(output)

