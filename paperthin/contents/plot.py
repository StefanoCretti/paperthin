import io
from collections.abc import Iterable

from ..html_helpers import DownloadButton
from .tabular import TabularContent
from .types import PlotOutput, PlotSource, TabularSource

PNG_DPI = 300


class PlotContent:
    def __init__(
        self,
        source: PlotSource,
        output: PlotOutput,
        data: TabularSource | None = None,
    ):
        self._fig = source
        self._output: PlotOutput = output
        self._data = TabularContent(data, "tsv") if data is not None else None

        # svg is always generated since it is used for display, regardless of output
        buffer = io.BytesIO()
        self._fig.savefig(buffer, format="svg", bbox_inches="tight")
        self._svg = buffer.getvalue()

    def get_display(self) -> str:
        return self._svg.decode("utf-8")

    def get_buttons(self, title: str) -> Iterable[DownloadButton]:

        buttons: list[DownloadButton] = []

        if self._output in ("svg", "svg+png"):
            buttons.append(DownloadButton.from_format(title, self._svg, "svg"))

        if self._output in ("png", "svg+png"):
            buffer = io.BytesIO()
            self._fig.savefig(buffer, format="png", bbox_inches="tight", dpi=PNG_DPI)
            buttons.append(DownloadButton.from_format(title, buffer.getvalue(), "png"))

        if self._data is not None:
            buttons.extend(self._data.get_buttons(title))

        return buttons
