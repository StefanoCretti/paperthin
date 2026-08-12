from collections.abc import Iterable
from html import escape

import polars as pl

from ..html_helpers import DownloadButton
from .tabular import TabularContent
from .types import ValueOutput, ValueSource


class ValueContent:
    def __init__(self, source: ValueSource, output: ValueOutput):
        self._value = source
        self._output: ValueOutput = output

    def get_display(self) -> str:
        return escape(str(self._value))

    def get_buttons(self, title: str) -> Iterable[DownloadButton]:
        df = pl.DataFrame({"stat": title, "value": self._value})
        return TabularContent(df, self._output).get_buttons(title)
