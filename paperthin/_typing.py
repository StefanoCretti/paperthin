from typing import Literal, Protocol

import pandas as pd
import polars as pl


class Component(Protocol):
    def get_content(self) -> str: ...


type PlotFormat = Literal["png", "svg", "svg+png"]
type TabularFormat = Literal["csv", "tsv"]
type Tabular = pl.DataFrame | pd.DataFrame | str
