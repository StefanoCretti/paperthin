import pathlib

import polars as pl

from ._typing import Tabular


def scan_tabular(source: Tabular) -> pl.DataFrame:

    if isinstance(source, pl.DataFrame):
        return source

    match pathlib.Path(source).suffix:
        case ".csv":
            return pl.read_csv(source, separator=",")
        case ".tsv":
            return pl.read_csv(source, separator="\t")
        case _:
            raise ValueError(f"{source} is not a valid csv or tsv file.")
