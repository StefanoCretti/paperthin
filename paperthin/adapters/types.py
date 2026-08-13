from collections.abc import Iterable
from typing import Literal, Protocol

import pandas as pd
import polars as pl
from matplotlib import figure

from ..html_helpers import DownloadButton

type TabularSource = pl.DataFrame | pd.DataFrame | str
type TabularOutput = Literal["csv", "tsv"]

type PlotSource = figure.Figure
type PlotOutput = Literal["png", "svg", "svg+png"]

type ConfigSource = dict | str
type ConfigOutput = Literal["json", "yaml"]

type ValueSource = str | float
type ValueOutput = Literal["tsv"]

type ImageSource = str
type ImageOutput = Literal["png", "svg"]


class Adapter(Protocol):
    def get_display(self) -> str: ...

    def get_buttons(self, title: str) -> Iterable[DownloadButton]: ...
