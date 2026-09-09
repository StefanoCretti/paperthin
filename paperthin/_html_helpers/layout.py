import re
from collections.abc import Iterable

from .button import DownloadButton


def slugify(text: str) -> str:
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
        f'<input type="checkbox" id="pt-info-{slugify(title)}" class="pt-info-checkbox">'
        f'<label for="pt-info-{slugify(title)}" class="pt-info-icon" title="Description">i</label>'
        "</div>"
        f"{downloads_div}"
        "</div>"
        f'<div class="pt-desc-body">{info}</div>'
        "</div>"
    )

    return f"{description_bar}{display}"
