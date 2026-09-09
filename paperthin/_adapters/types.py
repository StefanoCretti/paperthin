from collections.abc import Iterable
from typing import Literal, Protocol

import pandas as pd
import polars as pl
from matplotlib import figure

from .._html_helpers import DownloadButton

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
    """Content handler for an entry.

    An adapter knows how to render one kind of content as HTML, and how to
    package it for download. `Entry` holds one and delegates to it.

    """

    def get_display(self) -> str:
        """Return the HTML embedded in the body of the report.

        Returns
        -------
        str

        """
        ...

    def get_buttons(self, title: str) -> Iterable[DownloadButton]:
        """Return the download buttons shown next to the entry title.

        Parameters
        ----------
        title : str
            The title of the entry, used to name the downloaded files.

        Returns
        -------
        Iterable of DownloadButton
            Empty if the content offers no downloads.

        """
        ...
