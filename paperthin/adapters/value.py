from collections.abc import Iterable
from html import escape

import polars as pl

from ..html_helpers import DownloadButton
from . import types as ct
from .tabular import TabularAdapter


class ValueAdapter:
    def __init__(self, source: ct.ValueSource, output: ct.ValueOutput):
        self._value = source
        self._output: ct.ValueOutput = output

    def get_display(self) -> str:
        return escape(str(self._value))

    def get_buttons(self, title: str) -> Iterable[DownloadButton]:
        df = pl.DataFrame({"stat": title, "value": self._value})
        return TabularAdapter(df, self._output).get_buttons(title)
