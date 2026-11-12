#!/usr/bin/env python3
"""Generate production robots.txt and sitemap.xml after the public domain is known."""

from __future__ import annotations

import argparse
import ipaddress
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
ElementTree.register_namespace("", SITEMAP_NS)


class PageMetadata(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data


def public_url(site_url: str) -> str:
    parts = urlsplit(site_url)
    hostname = parts.hostname or ""
    if (
        parts.scheme != "https"
        or not parts.netloc
        or parts.path not in {"", "/"}
        or parts.username
        or parts.password
        or parts.query
        or parts.fragment
    ):
        raise ValueError("--site-url must be a public HTTPS origin without credentials, query, or fragment")
    if hostname == "localhost" or hostname.endswith((".local", ".localhost", ".test", ".example", ".invalid")):
        raise ValueError("--site-url must use the actual public production domain")
    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        pass
    else:
        if not address.is_global:
            raise ValueError("--site-url must not use a private or reserved IP address")
    return site_url.rstrip("/")


def page_routes(root: Path) -> list[str]:
    routes = []
    for path in sorted(root.rglob("*.html")):
        if any(part.startswith(".") or part in {"node_modules", "vendor"} for part in path.parts):
            continue
        parser = PageMetadata()
        parser.feed(path.read_text(encoding="utf-8"))
        if not parser.title.strip():
            raise ValueError(f"Missing page title: {path.relative_to(root)}")
        route = path.parent.relative_to(root).as_posix()
        routes.append("/" if route == "." else f"/{route}/")
    return routes


def generate(root: Path, site_url: str, indexable: bool) -> None:
    origin = public_url(site_url)
    if not root.is_dir():
        raise ValueError(f"Site root does not exist: {root}")

    robots = ["User-agent: *"]
    if indexable:
        robots.extend(["Allow: /", f"Sitemap: {origin}/sitemap.xml"])
    else:
        robots.append("Disallow: /")
    (root / "robots.txt").write_text("\n".join(robots) + "\n", encoding="utf-8")

    sitemap_path = root / "sitemap.xml"
    if not indexable:
        if sitemap_path.exists():
            raise FileExistsError(
                f"{sitemap_path} already exists. Review and remove the old sitemap before generating a non-indexable build."
            )
        return

    url_set = ElementTree.Element(f"{{{SITEMAP_NS}}}urlset")
    for route in page_routes(root):
        url = ElementTree.SubElement(url_set, f"{{{SITEMAP_NS}}}url")
        ElementTree.SubElement(url, f"{{{SITEMAP_NS}}}loc").text = f"{origin}{route}"
    ElementTree.indent(url_set, space="  ")
    ElementTree.ElementTree(url_set).write(
        sitemap_path,
        encoding="utf-8",
        xml_declaration=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-url", required=True, help="Public HTTPS origin, for example https://nuvex.de")
    parser.add_argument("--root", type=Path, default=ROOT, help="Website root directory")
    parser.add_argument("--indexable", action="store_true", help="Allow search indexing and write sitemap.xml")
    args = parser.parse_args()
    generate(args.root.resolve(), args.site_url, args.indexable)


if __name__ == "__main__":
    main()
