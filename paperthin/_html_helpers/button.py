import base64
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
