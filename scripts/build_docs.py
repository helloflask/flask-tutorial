"""Build Chinese at / and English at /en/ without overlapping clean steps."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import yaml

ROOT = Path(__file__).resolve().parents[1]


def main():
    with tempfile.TemporaryDirectory(prefix="flask-tutorial-") as temporary:
        staging = Path(temporary)
        outputs = {}
        for language, filename in (("zh", "mkdocs.yml"), ("en", "mkdocs.en.yml")):
            config = yaml.safe_load((ROOT / filename).read_text(encoding="utf-8"))
            docs = staging / language / "docs"
            shutil.copytree(ROOT / config["docs_dir"], docs)
            for asset in (ROOT / "chapters/shared").iterdir():
                if asset.name == "_templates":
                    continue
                target = docs / asset.name
                if asset.is_dir():
                    shutil.copytree(asset, target)
                else:
                    shutil.copy2(asset, target)
            output = staging / language / "site"
            config["docs_dir"] = str(docs)
            config["site_dir"] = str(output)
            config["theme"]["custom_dir"] = str(ROOT / config["theme"]["custom_dir"])
            config_path = staging / language / "mkdocs.yml"
            config_path.write_text(yaml.safe_dump(config, allow_unicode=True), encoding="utf-8")
            subprocess.run(
                [sys.executable, "-m", "mkdocs", "build", "--strict", "--config-file", str(config_path)],
                check=True,
                cwd=ROOT,
            )
            outputs[language] = output

        # Only replace the publish directory once both strict builds succeed.
        combined = outputs["zh"]
        shutil.copytree(outputs["en"], combined / "en")
        destination = ROOT / "site"
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(combined, destination)
        print(f"Built Chinese at {destination} and English at {destination / 'en'}")


if __name__ == "__main__":
    main()
