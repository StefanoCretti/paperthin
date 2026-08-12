from typing import Literal

import pandas as pd
import polars as pl
from matplotlib import figure

type TabularSource = pl.DataFrame | pd.DataFrame | str
type TabularOutput = Literal["csv", "tsv"]

type PlotSource = figure.Figure
type PlotOutput = Literal["png", "svg", "svg+png"]

type ConfigSource = dict | str
type ConfigOutput = Literal["json", "yaml"]

type ValueSource = str | float
type ValueOutput = Literal["tsv"]
