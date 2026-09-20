"""Check the combined build's local targets and language/URL boundaries."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.language = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.links.extend(attrs[key] for key in ("href", "src") if attrs.get(key))
        if tag == "html":
            self.language = attrs.get("lang")


def main():
    assert (SITE / "index.html").is_file(), "Build the site first"
    checked = 0
    for path in SITE.rglob("*.html"):
        page = Page()
        page.feed(path.read_text(encoding="utf-8"))
        expected_language = "en" if path.relative_to(SITE).parts[0] == "en" else "zh"
        assert page.language == expected_language, (path, page.language)
        assert "/en/" in page.links and "/" in page.links, f"Missing language selector: {path}"
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc or not url.path:
                continue
            target = SITE / unquote(url.path.lstrip("/")) if url.path.startswith("/") else path.parent / unquote(url.path)
            if target.is_dir():
                target /= "index.html"
            assert target.exists(), f"Missing local target: {path}: {link}"
            checked += 1

    for language, prefix in (("zh", SITE), ("en", SITE / "en")):
        for source in (ROOT / "chapters" / language).glob("*.md"):
            target = prefix / "index.html" if source.name == "README.md" else prefix / source.stem / "index.html"
            assert target.is_file(), f"Missing chapter URL: {target}"
        index = json.loads((prefix / "search/search_index.json").read_text(encoding="utf-8"))
        assert index["docs"], f"Empty search index: {language}"

    for name in ("pay", "alipay", "wechat_pay"):
        assert not (SITE / name).exists(), f"Payment page returned: {name}"
    print(f"Verified language navigation, chapter URLs, search indexes and {checked} local targets.")


if __name__ == "__main__":
    main()
