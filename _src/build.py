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

import hashlib
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

# (label, href relative to site root, section prefix that keeps the link highlighted)
NAV = [
    ("Projects", "index.html", None),
    ("About", "About.html", None),
    ("Homebrew", "homebrew.html", "homebrew/"),
    ("Companions", "companions/", "companions/"),
]

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
    for label, href, prefix in NAV:
        page = href[:-5] if href.endswith(".html") else href + "index"
        active = slug == page or (prefix is not None and slug.startswith(prefix))
        current = ' aria-current="page"' if active else ""
        items.append(f'<a href="{root}{href}"{current}>{label}</a>')
    return "".join(items)


def render_page(src: Path, layout: Template, subs: dict[str, str] | None = None) -> tuple[Path, str]:
    rel = src.relative_to(PAGES)
    slug = rel.with_suffix("").as_posix()
    root = "../" * (len(rel.parts) - 1)

    meta, text = parse_front_matter(src.read_text(encoding="utf-8"))
    for key, value in SITE.items():
        text = text.replace("{{site.%s}}" % key, html.escape(value, quote=False))

    for key, value in (subs or {}).items():
        text = text.replace("{{%s}}" % key, value)

    # {{hash:assets/x.js}} -> short content hash of that static file, used as ?v= so browsers
    # never pair a new page with a stale cached script or stylesheet.
    text = re.sub(
        r"\{\{hash:([^}]+)\}\}",
        lambda m: hashlib.sha1((STATIC / m.group(1)).read_bytes()).hexdigest()[:10],
        text,
    )

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
    return dest, title


# ----------------------------------------------------------------------------- sitemap
#
# A page containing {{sitemap}} gets an index of every page on the site plus a tree of how they
# nest. "Hidden" means no other page links to it (the header counts as a link).


def url_for(path: str) -> str:
    """Link target for a site path: directory index pages are linked as 'dir/'."""
    if path == "index.html":
        return path
    return path[: -len("index.html")] if path.endswith("/index.html") else path


def scan_raw_pages() -> dict[str, dict]:
    """Hand-written .html files in static/ (redirects, palette demos...)."""
    found: dict[str, dict] = {}
    for f in sorted(STATIC.rglob("*.html")):
        path = f.relative_to(STATIC).as_posix()
        text = f.read_text(encoding="utf-8", errors="replace")
        t = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
        r = re.search(r'http-equiv=["\']?refresh["\']?[^>]*URL=([^"\'>\s]+)', text, re.I)
        found[path[:-5]] = {
            "path": path,
            "title": path if r else (html.unescape(t.group(1)).strip() if t else Path(path).stem),
            "redirect": r.group(1) if r else None,
            "file": f,
        }
    return found


def inbound_links(pages: dict[str, dict]) -> dict[str, set[str]]:
    """slug -> set of slugs of other pages that link to it."""
    by_path = {info["path"]: slug for slug, info in pages.items()}
    inbound: dict[str, set[str]] = {slug: set() for slug in pages}
    for slug, info in pages.items():
        page_file = info["file"]
        text = page_file.read_text(encoding="utf-8", errors="replace")
        for target in re.findall(r'(?:href|URL)=["\']?([^"\'>\s]+)', text, re.I):
            target = re.sub(r"^https?://(?:www\.)?tylerhanyinwang\.com", "", target, flags=re.I)
            if re.match(r"^(?:[a-z][a-z0-9+.-]*:|//|#)", target, re.I):
                continue
            clean = target.split("#")[0].split("?")[0]
            base = ROOT if clean.startswith("/") else page_file.parent
            rel = (base / clean.lstrip("/")).resolve() if clean else page_file.resolve()
            if rel.is_dir():
                rel = rel / "index.html"
            try:
                rel_path = rel.relative_to(ROOT.resolve()).as_posix()
            except ValueError:
                continue
            hit = by_path.get(rel_path)
            if hit and hit != slug:
                inbound[hit].add(slug)
    return inbound


def build_tree(pages: dict[str, dict]) -> dict:
    """Nest pages by URL: a page's parent is the page that owns its directory, else a folder node."""
    nodes: dict[str, dict] = {}
    root_slug = "index"

    def get_dir(d: str, exclude: str) -> str | None:
        """Slug of the node standing for directory `d`, creating a folder node if no page owns it."""
        if d == "":
            return root_slug
        for cand in (d + "/index", d):
            if cand in pages and cand != exclude and not pages[cand].get("redirect"):
                return cand
        key = "dir:" + d
        if key not in nodes:
            nodes[key] = {"slug": key, "label": d.rsplit("/", 1)[-1], "folder": True, "children": []}
            attach(key, d.rsplit("/", 1)[0] if "/" in d else "", exclude)
        return key

    def attach(slug: str, directory: str, exclude: str) -> None:
        parent = get_dir(directory, exclude)
        if parent is None or parent == slug:
            parent = root_slug
        nodes[parent]["children"].append(slug)

    for slug, info in pages.items():
        nodes[slug] = {"slug": slug, "info": info, "children": []}
    for slug, info in list(pages.items()):
        if slug == root_slug:
            continue
        d = slug.rsplit("/", 1)[0] if "/" in slug else ""
        # a real directory index (companions/index) belongs to the directory above it
        if slug.endswith("/index") and not info.get("redirect"):
            d = d.rsplit("/", 1)[0] if "/" in d else ""
        attach(slug, d, slug)

    nav_order = {Path(h).stem if h.endswith(".html") else h.rstrip("/") + "/index": i for i, (_, h, _) in enumerate(NAV)}

    def label_of(slug: str) -> str:
        n = nodes[slug]
        return n["label"] if n.get("folder") else n["info"]["title"]

    def sort_key(slug: str):
        return (nav_order.get(slug, 99), nodes[slug].get("folder", False), label_of(slug).lower())

    for n in nodes.values():
        n["children"].sort(key=sort_key)
    return nodes


LEGEND = (
    '<p class="sm-legend">'
    '<span><span class="badge b-header">in header</span> linked from the header</span>'
    '<span><span class="badge b-linked">linked</span> linked from another page</span>'
    '<span><span class="badge b-hidden">hidden</span> nothing links to it</span>'
    '<span><span class="badge b-redirect">redirect</span> forwards elsewhere</span></p>'
)


def render_sitemap(pages: dict[str, dict]) -> str:
    inbound = inbound_links(pages)
    nav_targets = {Path(h).stem if h.endswith(".html") else h.rstrip("/") + "/index" for _, h, _ in NAV}
    nodes = build_tree(pages)

    def status(slug: str) -> tuple[str, str]:
        info = pages[slug]
        if info.get("redirect"):
            return "redirect", "redirect"
        if slug in nav_targets or slug == "index":
            return "header", "in header"
        if not inbound[slug]:
            return "hidden", "hidden"
        return "linked", "linked"

    def badge(slug: str) -> str:
        cls, text = status(slug)
        return f'<span class="badge b-{cls}">{text}</span>'

    def chain(path: str, linked: bool = True) -> str:
        """The address as a chain of slashes, with the hyperlink on its last step: /homebrew/Classes/<Mimeoblade.html>."""
        target = url_for(path)
        cut = target.rstrip("/").rfind("/") + 1          # keep a trailing "dir/" together as the last step
        head, last = target[:cut], target[cut:]
        end = html.escape(last, quote=False)
        if linked:
            end = f'<a href="{html.escape(target)}">{end}</a>'
        return f'<span class="chain"><span class="seg">/{html.escape(head, quote=False)}</span>{end}</span>'

    def row(slug: str) -> str:
        n = nodes[slug]
        if n.get("folder"):
            folder_path = slug[len("dir:"):] + "/"
            return f'<span class="t-title t-folder">{html.escape(n["label"], quote=False)}</span> <span class="chain"><span class="seg">/{html.escape(folder_path, quote=False)}</span></span>'
        info = n["info"]
        # a redirect's "title" is just its own address, so it's shown once, as the chain
        out = chain(info["path"]) if info.get("redirect") else f'<span class="t-title">{html.escape(info["title"], quote=False)}</span> {chain(info["path"])}'
        if info.get("redirect"):
            out += f' <span class="t-path">&rarr; {html.escape(info["redirect"], quote=False)}</span>'
        return f'{out} {badge(slug)}'

    def count_pages(slug: str) -> int:
        n = nodes[slug]
        return (0 if n.get("folder") else 1) + sum(count_pages(c) for c in n["children"])

    def tree(slug: str) -> str:
        n = nodes[slug]
        if not n["children"]:
            return f'<li><div class="row">{row(slug)}</div></li>'
        kids = "".join(tree(c) for c in n["children"])
        more = count_pages(slug) - (0 if n.get("folder") else 1)
        return (
            f'<li><details open><summary class="row">{row(slug)} '
            f'<span class="t-count">{more} inside</span></summary><ul>{kids}</ul></details></li>'
        )

    rows = []
    for slug, info in sorted(pages.items(), key=lambda kv: kv[1]["path"].lower()):
        target = f' <span class="t-path">&rarr; {html.escape(info["redirect"], quote=False)}</span>' if info.get("redirect") else ""
        rows.append(
            f'<tr><td>{"" if info.get("redirect") else html.escape(info["title"], quote=False)}{target}</td><td>{chain(info["path"])}</td><td>{badge(slug)}</td></tr>'
        )

    counts = {}
    for slug in pages:
        counts[status(slug)[0]] = counts.get(status(slug)[0], 0) + 1
    summary = (
        f'<p class="sm-summary">{len(pages)} pages: {counts.get("header", 0)} in the header, '
        f'{counts.get("linked", 0)} linked from other pages, {counts.get("hidden", 0)} hidden '
        f'(nothing links to them), {counts.get("redirect", 0)} redirects.</p>'
    )
    return (
        summary
        + LEGEND
        + '<h2>Tree</h2><div class="sitemap-tree"><ul class="tree">'
        + tree("index")
        + "</ul></div>"
        + '<h2>Index</h2><div class="sitemap-index"><table><thead><tr><th>Page</th><th>Address</th><th>Status</th></tr></thead><tbody>'
        + "".join(rows)
        + "</tbody></table></div>"
    )


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


MANIFEST = HERE / "manifest.txt"


def remove_stale(current: set[str]) -> list[str]:
    """Delete generated files that an earlier build wrote but this one no longer produces
    (a page whose .md was removed, a static file that was deleted). Only files listed in the
    manifest are ever touched, so hand-placed files in the site root are safe."""
    gone = []
    if MANIFEST.exists():
        for rel in MANIFEST.read_text(encoding="utf-8").split():
            if rel not in current and (ROOT / rel).is_file():
                (ROOT / rel).unlink()
                gone.append(rel)
                parent = (ROOT / rel).parent
                while parent != ROOT and not any(parent.iterdir()):
                    parent.rmdir()
                    parent = parent.parent
    MANIFEST.write_text("\n".join(sorted(current)) + "\n", encoding="utf-8")
    return gone


def main() -> None:
    layout = Template((HERE / "layout.html").read_text(encoding="utf-8"))

    static_files = {p.relative_to(STATIC).as_posix() for p in STATIC.rglob("*") if p.is_file()}
    shutil.copytree(STATIC, ROOT, dirs_exist_ok=True)

    built: list[Path] = []
    pages: dict[str, dict] = {}
    deferred = []
    for src in sorted(PAGES.rglob("*.md")):
        if "{{sitemap}}" in src.read_text(encoding="utf-8"):
            deferred.append(src)
            continue
        dest, title = render_page(src, layout)
        if dest.relative_to(ROOT).as_posix() in static_files:
            sys.exit(f"{src.relative_to(HERE)} would overwrite a static file: {dest.relative_to(ROOT)}")
        built.append(dest)
        rel = dest.relative_to(ROOT)
        pages[rel.with_suffix("").as_posix()] = {"path": rel.as_posix(), "title": title, "file": dest}

    for slug, info in scan_raw_pages().items():
        info["file"] = ROOT / info["path"]
        pages.setdefault(slug, info)

    for src in deferred:
        rel = src.relative_to(PAGES).with_suffix("")
        # the sitemap page itself is listed too (it is hidden: nothing links to it)
        pages[rel.as_posix()] = {"path": rel.with_suffix(".html").as_posix(), "title": "", "file": ROOT / rel.with_suffix(".html")}
        _, title = render_page(src, layout, {"sitemap": ""})   # first pass learns the title
        pages[rel.as_posix()]["title"] = title
        others = {k: v for k, v in pages.items() if k != rel.as_posix()}
        # the sitemap links to everything, so it is judged on what the rest of the site does
        full = dict(others)
        full[rel.as_posix()] = pages[rel.as_posix()]
        dest, _ = render_page(src, layout, {"sitemap": render_sitemap(full)})
        built.append(dest)

    produced = static_files | {p.relative_to(ROOT).as_posix() for p in built}
    for rel in remove_stale(produced):
        print(f"  removed stale file: {rel}")

    raw_pages = [ROOT / f for f in static_files if f.endswith(".html")]
    print(f"Built {len(built)} pages, copied {len(static_files)} static files into {ROOT}")
    broken = check_links(built + raw_pages)
    print(f"Link check: {broken} broken local link(s)")


if __name__ == "__main__":
    main()
