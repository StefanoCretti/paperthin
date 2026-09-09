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


def _has_docs(tag: str) -> bool:
    """Check whether a tag predates the documentation and cannot be built."""

    return (
        subprocess.run(
            ["git", "cat-file", "-e", f"{tag}:docs/conf.py"],
            capture_output=True,
            check=False,
            cwd=OUT_FILE.parent.parent.parent,
        ).returncode
        == 0
    )


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

    found: list[tuple[tuple[int, ...], str]] = []
    for tag in out.split():
        match = _TAG_RE.match(tag)
        if match is None or not _has_docs(tag):
            continue
        found.append((tuple(int(n) for n in match.groups()), tag))

    return [tag for _, tag in sorted(found, reverse=True)]


def build() -> None:
    entries: list[dict[str, str | bool]] = [
        {"name": "dev", "version": "latest", "url": f"{BASE_URL}/latest/"}
    ]

    for index, tag in enumerate(_tags()):
        entry: dict[str, str | bool] = {
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
