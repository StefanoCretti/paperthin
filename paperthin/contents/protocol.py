from collections.abc import Iterable
from typing import Protocol

from ..html_helpers import DownloadButton


class Content(Protocol):
    def get_display(self) -> str: ...

    def get_buttons(self, title: str) -> Iterable[DownloadButton]: ...
