# Contributing

## Building both languages

The Chinese edition stays at the site root (for example, `/1-preparation/`), while the English edition uses `/en/`.

- `chapters/zh/` contains the complete Chinese manuscript; `mkdocs.yml` defines its contents and site configuration.
- `chapters/en/` contains the English manuscript; `mkdocs.en.yml` defines its contents and site configuration. Translated chapters appear in the English contents, while links to untranslated chapters are clearly marked as pointing to the Chinese edition.
- `chapters/shared/` contains images, styles, the cover, and templates shared by both languages. The build copies these assets into each language's temporary documentation directory so relative links such as `images/...` remain valid.

Install the documentation dependencies and build both editions:

```sh
python -m pip install -r requirements.txt
python scripts/build_docs.py
python scripts/check_docs.py
python -m http.server 8000 --directory site
```

Preview Chinese at `http://localhost:8000/` and English at `http://localhost:8000/en/`. Use the combined build script rather than a standalone `mkdocs build` or `mkdocs serve`: it supplies shared assets to both configurations. Re-run the script after editing. It builds each language in a separate temporary directory with strict validation, then replaces `site/` only after both builds succeed. Rebuilds also remove stale pages.

When translating a chapter, keep its Chinese filename (for example, `chapters/zh/preface.md` becomes `chapters/en/preface.md`). Add the translated chapter to `mkdocs.en.yml` and change its link in `chapters/en/README.md` to the relative Markdown filename. Do not copy untranslated chapters into the English directory. Keep the Chinese book-wide contents in `chapters/zh/README.md` and its navigation in `mkdocs.yml` in sync when adding or renaming Chinese chapters. The language selector links to each edition's home page, so it never points to a translation that does not exist. Each edition has its own search index.

### Netlify

`netlify.toml` keeps `site` as the publish directory and runs `pip install -r requirements.txt && python scripts/build_docs.py && python scripts/check_docs.py`. Both editions deploy together from one branch. No redirect, domain, or Netlify account change is required: existing Chinese page URLs remain at the root. The existing Netlify site must build from the repository root using this configuration; if its dashboard overrides the build command or publish directory, align those with `netlify.toml`. No account settings are changed by this repository update.
