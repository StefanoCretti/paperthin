import base64
import re
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal

type DownloadFormat = Literal["png", "svg", "tsv", "csv", "json", "yaml"]
MIMES: dict[DownloadFormat, str] = {
    "png": "image/png",
    "svg": "image/svg+xml",
    "tsv": "text/tab-separated-values",
    "csv": "text/csv",
    "json": "application/json",
    "yaml": "application/yaml",
}
CSS_STYLE: str = (
    "h2 { background: #eef1f5; padding: 8px; border-radius: 6px; }"
    ".pt-download-btn {"
    "  margin-left: 6px; padding: 2px 10px; border: 1px solid #ccc; background: white;"
    "  border-radius: 4px; text-decoration: none; font-size: 0.8em; color: #333;"
    "}"
    ".pt-buttons .pt-download-btn:link,"
    ".pt-buttons .pt-download-btn:visited,"
    ".pt-buttons .pt-download-btn:hover,"
    ".pt-buttons .pt-download-btn:focus { text-decoration: none; }"
    ".pt-row { margin-bottom: 10px; }"
    ".pt-row-top { display: flex; align-items: baseline; gap: 8px; }"
    ".pt-row-title { min-width: 0; }"
    ".pt-row-title h3 { display: inline; margin: 0; }"
    ".pt-info-checkbox { position: absolute; opacity: 0; width: 0; height: 0; }"
    ".pt-info-icon {"
    "  display: inline-flex; align-items: center; justify-content: center;"
    "  vertical-align: middle; margin-left: 8px; cursor: pointer;"
    "  width: 17px; height: 17px; border-radius: 50%;"
    "  border: 1.3px solid #9aa4b0; color: #6b7280; font-size: 0.68rem;"
    "  font-weight: 700; font-family: Georgia, 'Times New Roman', serif;"
    "  line-height: 1;"
    "}"
    ".pt-info-checkbox:checked + .pt-info-icon {"
    "  background: #eef1f5; border-color: #6b7280; color: #1a1d21;"
    "}"
    ".pt-buttons { flex-shrink: 0; white-space: nowrap; margin-left: auto; }"
    ".pt-desc-body {"
    "  display: none; margin-top: 8px; color: #555; font-size: 0.9em; line-height: 1.5;"
    "}"
    ".pt-row:has(.pt-info-checkbox:checked) .pt-desc-body { display: block; }"
    # not needed yet: no figures in descriptions currently
    # "/* .pt-desc-body svg { max-width: 100%; height: auto; } */"
    "div.output_subarea { padding-top: 0 !important; max-width: 100% !important; }"
    ".output_html svg { display: block; margin: 0 auto; }"
    ".output_html img { display: block !important; margin: 0 auto !important; }"
    ".output_html table.dataframe { margin-left: auto; margin-right: auto; }"
)


@dataclass
class DownloadButton:
    label: str
    content: bytes
    mime: str
    file_name: str

    _EMBED_TEMPLATE = (
        '<a href="data:{mime};base64,{content}" '
        'download="{file_name}" '
        'class="pt-download-btn">'
        "{label}</a>"
    )

    def get_embeddable(self) -> str:
        """Create the raw html string for an individual content download button."""

        return self._EMBED_TEMPLATE.format(
            mime=self.mime,
            content=base64.b64encode(self.content).decode("ascii"),
            file_name=self.file_name,
            label=self.label,
        )

    @classmethod
    def from_format(
        cls,
        title: str,
        content: bytes,
        format: DownloadFormat,
    ) -> "DownloadButton":
        """Build a DownloadButton for the given format."""
        return cls(format.upper(), content, MIMES[format], f"{title}.{format}")


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def get_html(
    display: str,
    title: str,
    info: str,
    buttons: Iterable[DownloadButton],
) -> str:

    downloads_div = (
        f'<div class="pt-buttons">{"".join(b.get_embeddable() for b in buttons)}</div>'
        if buttons
        else ""
    )

    description_bar = (
        '<div class="pt-row">'
        '<div class="pt-row-top">'
        '<div class="pt-row-title">'
        f"<h3>{title}</h3>"
        f'<input type="checkbox" id="pt-info-{_slugify(title)}" class="pt-info-checkbox">'
        f'<label for="pt-info-{_slugify(title)}" class="pt-info-icon" title="Description">i</label>'
        "</div>"
        f"{downloads_div}"
        "</div>"
        f'<div class="pt-desc-body">{info}</div>'
        "</div>"
    )

    return f"{description_bar}{display}"
