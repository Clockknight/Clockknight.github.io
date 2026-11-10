# Tyler's Project Repository

Static rebuild of the old Jekyll/minima site. Same pages, same URLs, same links,
new design. No Jekyll needed: GitHub Pages serves the generated HTML as-is
(`.nojekyll` turns the Jekyll build off).

## Layout

```
index.html, About.html, homebrew/...   generated pages (what visitors see)
assets/site.css                        generated copy of the stylesheet
_src/
  build.py                             the build script
  layout.html                          shared header/footer
  pages/                               markdown sources (edit these)
  static/                              files copied over unchanged
                                       (images, CSS, redirects, CNAME, assets/site.css)
```

## Editing

```
pip install -r _src/requirements.txt
python _src/build.py
```

- Edit pages in `_src/pages/` (`homebrew/Weapons.md` becomes `homebrew/Weapons.html`).
- Edit the look in `_src/static/assets/site.css`; the header/footer in `_src/layout.html`.
- Site title, author, description and the nav live at the top of `build.py`.
- Optional front matter at the top of a page: `title:`, `class:` (body class for
  page-specific CSS), `notitle: true`.
- The build prints a warning for any local link that doesn't exist.

## Deploying

Copy everything in this folder into the repo root (replacing the old files), keep
`CNAME` and `.nojekyll`, and push. Delete the old root-level `.md` files,
`_config.yml`, `index.css` and `.idea/`; they're replaced by `_src/`.

## Known gaps carried over from the old site

- `homebrew/Files/Character.pdf` and `Group.pdf` are linked but were never in the repo.
- `[Intrigue System]`, `[Survival System]` and `[Cleric of Shapes]` had no
  destination; they show as "planned".
- Footnote `[^5]` (Grit) on the Monk page is referenced but never defined.
- Several pages are empty placeholders (Overall, Survival Rules, Evoker of Elements, Companions).
