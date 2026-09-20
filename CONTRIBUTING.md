# 贡献指南 / Contributing

## 双语文档构建 / Building both languages

中文继续使用网站根路径（例如 `/1-preparation/`），英文使用 `/en/`。

- `chapters/zh/`：完整中文书稿；`mkdocs.yml`：中文目录和站点配置。
- `chapters/en/`：英文书稿；`mkdocs.en.yml`：英文目录和站点配置。目前只有英文介绍页，未翻译章节明确链接到中文版。
- `chapters/shared/`：两种语言共用的图片、样式、封面和模板。构建时复制到各语言的临时文档目录，保持书稿中的 `images/...` 等相对链接有效。

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
