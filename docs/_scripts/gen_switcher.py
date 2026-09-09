"""Generate the version list backing the documentation's version dropdown.

The file is read by pydata-sphinx-theme from a single fixed URL, the copy
published by the `latest` build, so rebuilding `latest` is what refreshes the
list for every version.
"""

import json
import pathlib
import re
import subprocess

BASE_URL = "https://paperthin.readthedocs.io/en"
OUT_FILE = pathlib.Path(__file__).parent.parent / "_static" / "switcher.json"

_TAG_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")


def _tags() -> list[str]:
    try:
        out = subprocess.run(
            ["git", "tag", "--list", "v[0-9]*"],
            capture_output=True,
            text=True,
            check=True,
            cwd=OUT_FILE.parent.parent.parent,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []

    tags = [t for t in out.split() if _TAG_RE.match(t)]
    return sorted(
        tags,
        key=lambda t: tuple(int(n) for n in _TAG_RE.match(t).groups()),
        reverse=True,
    )


def build() -> None:
    entries = [{"name": "dev", "version": "latest", "url": f"{BASE_URL}/latest/"}]

    for index, tag in enumerate(_tags()):
        entry = {
            "name": tag.lstrip("v"),
            "version": tag,
            "url": f"{BASE_URL}/{tag}/",
        }
        if index == 0:
            entry["preferred"] = True
        entries.append(entry)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(entries, indent=2) + "\n")


if __name__ == "__main__":
    build()
