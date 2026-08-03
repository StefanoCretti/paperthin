from collections.abc import Iterable

import polars as pl
from matplotlib import figure

from . import embeddings as em
from . import html_helpers as hh
from . import scanners as sc
from ._typing import PlotFormat, Tabular, TabularFormat


class Section:
    def __init__(self, title: str):
        self._title = title

    @property
    def title(self) -> str:
        return self._title

    def get_content(self) -> str:
        return f"# %% [markdown]\n# ## {self._title}"


class Subsection:
    def __init__(
        self,
        display: str,
        *,
        title: str,
        info: str,
        buttons: Iterable[str],
    ):
        self._display = display
        self._title = title
        self._info = info
        self._buttons = buttons

    @classmethod
    def plot(
        cls,
        content: figure.Figure,
        *,
        title: str,
        info: str,
        data: Tabular | None = None,
        format: PlotFormat = "svg+png",
    ) -> "Subsection":

        # svg plot is always created since it is used for display purposes
        svg_plot = em.svg_plot_string(content)

        buttons = []

        if format in ("svg", "svg+png"):
            buttons.append(hh.get_download_button(svg_plot, "svg", title))
        if format in ("png", "svg+png"):
            png_plot = em.png_plot_bytes(content)
            buttons.append(hh.get_download_button(png_plot, "png", title))

        if data is not None:
            tsv_data = em.df_to_tsv(sc.scan_tabular(data))
            buttons.append(hh.get_download_button(tsv_data, "tsv", title))

        return Subsection(svg_plot, title=title, info=info, buttons=buttons)

    @classmethod
    def tabular(
        cls,
        content: Tabular,
        *,
        title: str,
        info: str,
        format: TabularFormat = "tsv",
    ) -> "Subsection":

        df = sc.scan_tabular(content)

        # TODO: How to display?
        table_display: str = ""

        match format:
            case "tsv":
                buttons = (hh.get_download_button(em.df_to_tsv(df), "tsv", title),)
            case "csv":
                buttons = (hh.get_download_button(em.df_to_csv(df), "csv", title),)

        return Subsection(table_display, title=title, info=info, buttons=buttons)

    @classmethod
    def value(
        cls,
        content: str | float,
        *,
        title: str,
        info: str,
    ) -> "Subsection":

        # TODO: How to display?
        value_display: str = ""

        value_df = pl.DataFrame({"stat": title, "value": content})
        buttons = (hh.get_download_button(em.df_to_tsv(value_df), "tsv", title),)

        return Subsection(value_display, title=title, info=info, buttons=buttons)

    @classmethod
    def image(
        cls,
        content: str,
        *,
        title: str,
        info: str,
        data: pl.DataFrame | None = None,
    ) -> "Subsection": ...

    @classmethod
    def config(cls, content: dict | str, *, title: str, info: str) -> "Subsection": ...

    def get_content(self) -> str:
        html = hh.get_html(self._display, self._title, self._info, self._buttons)
        return f"# %%\ndisplay(HTML({html!r}))"
