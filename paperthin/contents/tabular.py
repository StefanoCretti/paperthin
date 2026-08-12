import pathlib
from collections.abc import Iterable
from html import escape

import pandas as pd
import polars as pl

from ..html_helpers import DownloadButton
from .types import TabularOutput, TabularSource


class TabularContent:
    def __init__(self, source: TabularSource, output: TabularOutput):

        if isinstance(source, pd.DataFrame):
            source = pl.from_pandas(source)

        elif isinstance(source, str):
            match pathlib.Path(source).suffix:
                case ".csv":
                    source = pl.read_csv(source, separator=",")
                case ".tsv":
                    source = pl.read_csv(source, separator="\t")
                case _:
                    raise ValueError(f"{source} is not a valid csv or tsv file.")

        self._data = source
        self._output: TabularOutput = output

    def get_display(self) -> str:

        header = "".join(f"<th>{escape(str(col))}</th>" for col in self._data.columns)
        rows = "".join(
            "<tr>"
            + "".join(f"<td>{escape(str(value))}</td>" for value in row)
            + "</tr>"
            for row in self._data.iter_rows()
        )
        return f'<table class="dataframe"><thead><tr>{header}</tr></thead><tbody>{rows}</tbody></table>'

    def get_buttons(self, title: str) -> Iterable[DownloadButton]:

        separator = "\t" if self._output == "tsv" else ","
        button = DownloadButton.from_format(
            title,
            self._data.write_csv(separator=separator).encode("utf-8"),
            self._output,
        )
        return (button,)
