import base64
import pathlib
import struct
from collections.abc import Iterable

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
        self._path = pathlib.Path(source)
        self._data = TabularAdapter(data, "tsv") if data is not None else None
        self._scale = scale

        self._output: ct.ImageOutput
        match self._path.suffix:
            case ".png":
                self._output = "png"
            case ".svg":
                self._output = "svg"
            case _:
                raise ValueError(f"{source} is not a valid png or svg file.")

    def get_display(self) -> str:
        if self._output == "svg":
            return self._path.read_text(encoding="utf-8")

        content = self._path.read_bytes()
        encoded = base64.b64encode(content).decode("ascii")

        # png width lives in the IHDR chunk, right after the signature/length/type
        width, _height = struct.unpack(">II", content[16:24])
        scaled_width = round(width * self._scale)

        return (
            f'<img width="{scaled_width}" '
            f'src="data:{MIMES[self._output]};base64,{encoded}">'
        )

    def get_buttons(self, title: str) -> Iterable[DownloadButton]:
        button = DownloadButton.from_format(
            title, self._path.read_bytes(), self._output
        )
        buttons = [button]

        if self._data is not None:
            buttons.extend(self._data.get_buttons(title))

        return buttons
