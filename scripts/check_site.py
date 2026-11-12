#!/usr/bin/env python3
"""Check static HTML structure, local links, metadata, form labels, and basic contrast."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER = re.compile(r"\[[^\]]+\]|ergänzen|Platzhalter", re.IGNORECASE)


class PageCheck(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.title = ""
        self.description = ""
        self.h1_count = 0
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.labels: set[str] = set()
        self.controls: list[tuple[str, str, str]] = []
        self.links: list[tuple[str, str, str]] = []
        self.forms: list[tuple[str, str]] = []
        self.images_without_alt = 0
        self.unsafe_blank_links = 0
        self.in_title = False
        self.title_parts: list[str] = []
        self.form_count = 0
        self.external_scripts = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.lang = values.get("lang", "") or ""
        elif tag == "title":
            self.in_title = True
        elif tag == "meta" and values.get("name", "").lower() == "description":
            self.description = values.get("content", "") or ""
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "form":
            self.form_count += 1
            self.forms.append((values.get("method", "get").lower(), values.get("action", "") or ""))
        elif tag in {"input", "select", "textarea"}:
            if values.get("type", "").lower() not in {"hidden", "submit", "button"}:
                self.controls.append((values.get("id", ""), values.get("name", ""), tag))
        elif tag == "label" and values.get("for"):
            self.labels.add(values["for"] or "")
        elif tag == "img" and "alt" not in values:
            self.images_without_alt += 1
        elif tag == "a":
            href = values.get("href", "") or ""
            self.links.append((href, values.get("target", "") or "", values.get("rel", "") or ""))
            if values.get("target") == "_blank" and not {"noopener", "noreferrer"}.issubset(
                set((values.get("rel", "") or "").split())
            ):
                self.unsafe_blank_links += 1
        elif tag == "script":
            src = values.get("src", "") or ""
            if src.startswith(("https://", "http://")):
                self.external_scripts += 1
        if values.get("id"):
            element_id = values["id"] or ""
            if element_id in self.ids:
                self.duplicate_ids.add(element_id)
            self.ids.add(element_id)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)


def relative_target(root: Path, current_page: Path, href: str) -> Path | None:
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        return None
    if not parsed.path:
        return current_page if parsed.fragment else None
    target = root / parsed.path.lstrip("/") if parsed.path.startswith("/") else current_page.parent / parsed.path
    if target.is_dir():
        target = target / "index.html"
    elif not target.suffix:
        target = target / "index.html"
    return target


def luminance(hex_color: str) -> float:
    channels = [int(hex_color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(foreground: str, background: str) -> float:
    first, second = sorted((luminance(foreground), luminance(background)), reverse=True)
    return (first + 0.05) / (second + 0.05)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    pages = sorted(ROOT.rglob("*.html"))
    titles: set[str] = set()
    descriptions: set[str] = set()
    placeholder_count = 0
    form_count = 0

    if not pages:
        print("FAIL: no HTML pages found")
        return 1

    for path in pages:
        parser = PageCheck()
        text = path.read_text(encoding="utf-8")
        parser.feed(text)
        parser.title = "".join(parser.title_parts).strip()
        relative = path.relative_to(ROOT)
        form_count += parser.form_count

        if not parser.lang:
            errors.append(f"{relative}: missing html lang")
        if not parser.title:
            errors.append(f"{relative}: missing title")
        elif parser.title in titles:
            errors.append(f"{relative}: duplicate title: {parser.title}")
        titles.add(parser.title)
        if not parser.description:
            errors.append(f"{relative}: missing meta description")
        elif parser.description in descriptions:
            errors.append(f"{relative}: duplicate meta description")
        descriptions.add(parser.description)
        if parser.h1_count != 1:
            errors.append(f"{relative}: expected one h1, found {parser.h1_count}")
        if parser.duplicate_ids:
            errors.append(f"{relative}: duplicate id(s): {', '.join(sorted(parser.duplicate_ids))}")
        if parser.images_without_alt:
            errors.append(f"{relative}: {parser.images_without_alt} image(s) missing alt attribute")
        if parser.unsafe_blank_links:
            errors.append(f"{relative}: target=_blank links missing noopener/noreferrer")
        if parser.external_scripts:
            warnings.append(f"{relative}: loads {parser.external_scripts} third-party script(s)")
        for control_id, control_name, tag in parser.controls:
            if not control_id or control_id not in parser.labels:
                errors.append(f"{relative}: {tag} {control_name!r} has no associated label")
        for href, _, _ in parser.links:
            target = relative_target(ROOT, path, href)
            if target and not target.exists():
                errors.append(f"{relative}: broken local link {href}")
            if href.startswith("#") and href[1:] not in parser.ids:
                errors.append(f"{relative}: missing fragment target {href}")

        placeholder_count += len(PLACEHOLDER.findall(text))

    for path in ROOT.rglob("*.css"):
        css = path.read_text(encoding="utf-8")
        if re.search(r"@import\s+['\"]?https?://|url\(\s*['\"]?https?://", css, re.IGNORECASE):
            warnings.append(f"{path.relative_to(ROOT)}: references a remote asset; review privacy and licensing.")

    if form_count:
        warnings.append(
            "Contact form uses a client-side mailto handoff; server-side validation, delivery, rate limiting, and spam protection are not implemented."
        )
    warnings.append("Production HTTPS, security headers, hosting logs, backups, and restore tests require deployment configuration.")
    if placeholder_count:
        warnings.append(f"{placeholder_count} editorial/legal placeholder(s) remain; do not launch until reviewed.")

    color_pairs = [
        ("muted on paper", "#656b76", "#f5f3ee"),
        ("muted on white", "#656b76", "#fffefa"),
        ("white on blue", "#ffffff", "#2459d3"),
        ("blue on paper", "#2459d3", "#f5f3ee"),
        ("white on ink", "#ffffff", "#171d2a"),
        ("ink on lime", "#171d2a", "#b8f16b"),
    ]
    for name, foreground, background in color_pairs:
        ratio = contrast(foreground, background)
        if ratio < 4.5:
            errors.append(f"contrast {name}: {ratio:.2f}:1 (minimum 4.5:1)")

    print(f"Checked {len(pages)} HTML pages, {form_count} form(s), and {placeholder_count} content/legal placeholder(s).")
    for warning in warnings:
        print(f"GAP: {warning}")
    for error in errors:
        print(f"FAIL: {error}")
    if errors:
        return 1
    print("PASS: structure, unique metadata, local links, labels, image alt attributes, external-link safety, and selected brand contrast.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
