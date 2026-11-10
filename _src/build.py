#!/usr/bin/env python3
"""Build the static site.

    pip install -r _src/requirements.txt
    python _src/build.py

Markdown in _src/pages/ is rendered through _src/layout.html and written into
the site root (the folder above this one), keeping the same URLs the old Jekyll
site used: About.md -> About.html, homebrew/Weapons.md -> homebrew/Weapons.html.
Everything in _src/static/ is copied over unchanged.

Optional front matter at the top of a page:

    ---
    title: Page title        (defaults to the first <h1>, then the file name)
    class: some-body-class   (hook for page-specific CSS)
    notitle: true            (don't inject an <h1> when the page has none)
    ---
"""
from __future__ import annotations

import html
import re
import shutil
import sys
from pathlib import Path
from string import Template

try:
    import mistune
except ImportError:
    sys.exit("Missing dependency. Run: pip install -r _src/requirements.txt")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PAGES = HERE / "pages"
STATIC = HERE / "static"

SITE = {
    "title": "Tyler's Project Repository",
    "author": "Tyler Hanyin Wang",
    "description": (
        "Studying at EWU for Bachelor of Science in CS, specifically learning "
        "Java, SQL, and C. Self-taught in python, and C#."
    ),
}

# (label, page slug). Same two header pages as the old site, plus Projects (home).
NAV = [("Projects", "index"), ("About", "About"), ("Homebrew", "homebrew")]

markdown = mistune.create_markdown(escape=False, plugins=["footnotes", "table"])


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    m = re.match(r"---[ \t]*\n(.*?)\n---[ \t]*\n?", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta, text[m.end():]


def humanize(stem: str) -> str:
    return re.sub(r"[-_]+", " ", stem).strip().title()


def add_heading_ids(body: str) -> str:
    seen: dict[str, int] = {}

    def repl(m: re.Match) -> str:
        level, attrs, inner = m.groups()
        if "id=" in attrs:
            return m.group(0)
        text = html.unescape(re.sub(r"<[^>]+>", "", inner))
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "section"
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        if count:
            slug = f"{slug}-{count + 1}"
        return f'<h{level}{attrs} id="{slug}">{inner}</h{level}>'

    return re.sub(r"<h([1-6])([^>]*)>(.*?)</h\1>", repl, body, flags=re.S)


def fix_links(body: str) -> str:
    # Relative links to .md sources point at the rendered .html pages.
    body = re.sub(r'(href=")([^":]+?)\.md((?:#[^"]*)?")', r"\1\2.html\3", body)
    # A link with an empty destination is a placeholder for something not written yet.
    body = re.sub(
        r'<a href="">(.*?)</a>',
        r'<span class="planned" title="Not written yet">\1</span>',
        body,
        flags=re.S,
    )
    return body


def build_nav(slug: str, root: str) -> str:
    items = []
    for label, key in NAV:
        active = slug == key or (key == "homebrew" and slug.startswith("homebrew/"))
        current = ' aria-current="page"' if active else ""
        items.append(f'<a href="{root}{key}.html"{current}>{label}</a>')
    return "".join(items)


def render_page(src: Path, layout: Template) -> Path:
    rel = src.relative_to(PAGES)
    slug = rel.with_suffix("").as_posix()
    root = "../" * (len(rel.parts) - 1)

    meta, text = parse_front_matter(src.read_text(encoding="utf-8"))
    for key, value in SITE.items():
        text = text.replace("{{site.%s}}" % key, html.escape(value, quote=False))

    body = markdown(text)
    has_h1 = re.search(r"<h1\b", body) is not None

    title = meta.get("title")
    if not title:
        m = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
        title = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else humanize(src.stem)

    if not has_h1 and slug != "index" and meta.get("notitle") != "true":
        body = f"<h1>{html.escape(title, quote=False)}</h1>\n{body}"
    if not text.strip():
        body += '\n<p class="empty-note">Nothing here yet.</p>'

    body = fix_links(add_heading_ids(body))

    page_title = SITE["title"] if slug == "index" else f"{title} · {SITE['title']}"
    out = layout.substitute(
        page_title=html.escape(page_title, quote=False),
        description=html.escape(SITE["description"], quote=True),
        site_title=html.escape(SITE["title"], quote=False),
        author=html.escape(SITE["author"], quote=False),
        body_class=html.escape(meta.get("class", ""), quote=True),
        root=root,
        nav=build_nav(slug, root),
        content=body,
    )

    dest = ROOT / rel.with_suffix(".html")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out, encoding="utf-8")
    return dest


def check_links(pages: list[Path]) -> int:
    """Warn about local href/src targets that don't exist. Returns the count."""
    broken = 0
    for page in pages:
        for attr, target in re.findall(r'(href|src)="([^"]*)"', page.read_text(encoding="utf-8")):
            if not target or re.match(r"^(?:[a-z][a-z0-9+.-]*:|//|#)", target, re.I):
                continue
            path = target.split("#")[0].split("?")[0]
            resolved = (page.parent / path).resolve()
            if resolved.is_dir():
                resolved = resolved / "index.html"
            if not resolved.exists():
                broken += 1
                print(f"  warning: {page.relative_to(ROOT)} -> {target} does not exist")
    return broken


def main() -> None:
    layout = Template((HERE / "layout.html").read_text(encoding="utf-8"))

    static_files = {p.relative_to(STATIC).as_posix() for p in STATIC.rglob("*") if p.is_file()}
    shutil.copytree(STATIC, ROOT, dirs_exist_ok=True)

    built = []
    for src in sorted(PAGES.rglob("*.md")):
        dest = render_page(src, layout)
        if dest.relative_to(ROOT).as_posix() in static_files:
            sys.exit(f"{src.relative_to(HERE)} would overwrite a static file: {dest.relative_to(ROOT)}")
        built.append(dest)

    raw_pages = [ROOT / f for f in static_files if f.endswith(".html")]
    print(f"Built {len(built)} pages, copied {len(static_files)} static files into {ROOT}")
    broken = check_links(built + raw_pages)
    print(f"Link check: {broken} broken local link(s)")


if __name__ == "__main__":
    main()
