import base64
import io
import pathlib
from collections.abc import Iterable

from PIL import Image

from ..html_helpers import MIMES, DownloadButton
from . import types as ct
from .tabular import TabularAdapter


class ImageAdapter:
    def __init__(
        self,
        source: ct.ImageSource,
        data: ct.TabularSource | None = None,
        scale: float = 1.0,
    ):
        path = pathlib.Path(source)
        self._content = path.read_bytes()
        self._data = TabularAdapter(data, "tsv") if data is not None else None
        self._scale = scale

        self._output: ct.ImageOutput
        match path.suffix:
            case ".png":
                self._output = "png"
            case ".svg":
                self._output = "svg"
            case _:
                raise ValueError(f"{source} is not a valid png or svg file.")

    def get_display(self) -> str:
        if self._output == "svg":
            return self._content.decode("utf-8")

        encoded = base64.b64encode(self._content).decode("ascii")

        width, _height = Image.open(io.BytesIO(self._content)).size
        scaled_width = round(width * self._scale)

        return (
            f'<img width="{scaled_width}" '
            f'src="data:{MIMES[self._output]};base64,{encoded}">'
        )

    def get_buttons(self, title: str) -> Iterable[DownloadButton]:
        button = DownloadButton.from_format(title, self._content, self._output)
        buttons = [button]

        if self._data is not None:
            buttons.extend(self._data.get_buttons(title))

        return buttons
