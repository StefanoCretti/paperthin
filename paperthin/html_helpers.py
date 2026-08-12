import base64
import re
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal

type ContentType = Literal["png", "svg", "tsv", "csv", "json", "yaml"]
MIMES: dict[ContentType, str] = {
    "png": "image/png",
    "svg": "image/svg+xml",
    "tsv": "text/tab-separated-values",
    "csv": "text/csv",
    "json": "application/json",
    "yaml": "application/yaml",
}
QC_STYLE: str = (
    "h2 { background: #eef1f5; padding: 8px; border-radius: 6px; }"
    ".qc-download-btn {"
    "  margin-left: 6px; padding: 2px 10px; border: 1px solid #ccc; background: white;"
    "  border-radius: 4px; text-decoration: none; font-size: 0.8em; color: #333;"
    "}"
    ".qc-buttons .qc-download-btn:link,"
    ".qc-buttons .qc-download-btn:visited,"
    ".qc-buttons .qc-download-btn:hover,"
    ".qc-buttons .qc-download-btn:focus { text-decoration: none; }"
    ".qc-row { margin-bottom: 10px; }"
    ".qc-row-top { display: flex; align-items: baseline; gap: 8px; }"
    ".qc-row-title { min-width: 0; }"
    ".qc-row-title h3 { display: inline; margin: 0; }"
    ".qc-info-checkbox { position: absolute; opacity: 0; width: 0; height: 0; }"
    ".qc-info-icon {"
    "  display: inline-flex; align-items: center; justify-content: center;"
    "  vertical-align: middle; margin-left: 8px; cursor: pointer;"
    "  width: 17px; height: 17px; border-radius: 50%;"
    "  border: 1.3px solid #9aa4b0; color: #6b7280; font-size: 0.68rem;"
    "  font-weight: 700; font-family: Georgia, 'Times New Roman', serif;"
    "  line-height: 1;"
    "}"
    ".qc-info-checkbox:checked + .qc-info-icon {"
    "  background: #eef1f5; border-color: #6b7280; color: #1a1d21;"
    "}"
    ".qc-buttons { flex-shrink: 0; white-space: nowrap; margin-left: auto; }"
    ".qc-desc-body {"
    "  display: none; margin-top: 8px; color: #555; font-size: 0.9em; line-height: 1.5;"
    "}"
    ".qc-row:has(.qc-info-checkbox:checked) .qc-desc-body { display: block; }"
    # not needed yet: no figures in descriptions currently
    # "/* .qc-desc-body svg { max-width: 100%; height: auto; } */"
    "div.output_subarea { padding-top: 0 !important; max-width: 100% !important; }"
    ".output_html svg { display: block; margin: 0 auto; }"
    ".output_html table.dataframe { margin-left: auto; margin-right: auto; }"
)


@dataclass
class DownloadButton:
    label: str
    content: bytes
    mime: str
    download_path: str

    _EMBED_TEMPLATE = (
        '<a href="data:{mime};base64,{content}" '
        'download="{path}" '
        'class="qc-download-btn">'
        "{label}</a>"
    )

    def get_embeddable(self) -> str:
        """Create the raw html string for an individual content download button."""

        return self._EMBED_TEMPLATE.format(
            mime=self.mime,
            content=base64.b64encode(self.content).decode("ascii"),
            path=self.download_path,
            label=self.label,
        )

    @classmethod
    def from_format(
        cls,
        title: str,
        content: bytes,
        format: ContentType,
    ) -> "DownloadButton":
        """Create the raw html string for an individual content download button."""
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
        f'<div class="qc-buttons">{"".join(b.get_embeddable() for b in buttons)}</div>'
        if buttons
        else ""
    )

    description_bar = (
        '<div class="qc-row">'
        '<div class="qc-row-top">'
        '<div class="qc-row-title">'
        f"<h3>{title}</h3>"
        f'<input type="checkbox" id="qc-info-{_slugify(title)}" class="qc-info-checkbox">'
        f'<label for="qc-info-{_slugify(title)}" class="qc-info-icon" title="Description">i</label>'
        "</div>"
        f"{downloads_div}"
        "</div>"
        f'<div class="qc-desc-body">{info}</div>'
        "</div>"
    )

    return f"{description_bar}{display}"
