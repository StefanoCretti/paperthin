import base64
import re
from collections.abc import Iterable
from typing import Literal

type ContentType = Literal["png", "svg", "tsv", "csv"]
MIMES: dict[ContentType, str] = {
    "png": "image/png",
    "svg": "image/svg+xml",
    "tsv": "text/tab-separated-values",
    "csv": "text/csv",
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


def get_download_button(
    content: bytes | str,
    content_type: ContentType,
    content_name: str,
) -> str:
    """Create the raw html string for an individual content download button."""

    raw = content.encode("utf-8") if isinstance(content, str) else content
    encoded = base64.b64encode(raw).decode("ascii")
    uri = f"data:{MIMES[content_type]};base64,{encoded}"
    download_name = f"{content_name}.{content_type}"
    display_name = content_type.upper()

    return f'<a href="{uri}" download="{download_name}" class="qc-download-btn">{display_name}</a>'


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _get_downloads_div(buttons: Iterable[str]) -> str:
    return f'<div class="qc-buttons">{"".join(buttons)}</div>' if buttons else ""


def get_html(display: str, title: str, info: str, buttons: Iterable[str]) -> str:

    description_bar = (
        '<div class="qc-row">'
        '<div class="qc-row-top">'
        '<div class="qc-row-title">'
        f"<h3>{title}</h3>"
        f'<input type="checkbox" id="qc-info-{_slugify(title)}" class="qc-info-checkbox">'
        f'<label for="qc-info-{_slugify(title)}" class="qc-info-icon" title="Description">i</label>'
        "</div>"
        f"{_get_downloads_div(buttons)}"
        "</div>"
        f'<div class="qc-desc-body">{info}</div>'
        "</div>"
    )

    return f"{description_bar}{display}"
