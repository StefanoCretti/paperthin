from collections.abc import Iterable
from dataclasses import dataclass

import polars as pl
from matplotlib import figure

from . import embeddings as em
from . import html_helpers as hh
from . import scanners as sc
from ._typing import PlotFormat, Tabular, TabularFormat


@dataclass
class Section:
    """Separator to group results into sections.

    Inserts a title (h2) with highlighted background in the report.

    Parameters
    ----------
    title : str
        The title of the section.

    """

    title: str

    def get_content(self) -> str:
        """Return a markdown cell in jupytext percent format.

        Returns
        -------
        str

        """
        return f"# %% [markdown]\n# ## {self.title}"


class Subsection:
    """Fundamental unit of a report, corresponding to an individual result.

    A subsection is a standardized way to display a result.
    It is always composed of the same elements:
        - A title (h3 size)
        - A toggleable description of the result
        - Some graphical representation of the result
        - Download buttons for the data

    Though it is possible to initialize a subsection by providing all these
    elements to the main class constructor, in most cases you should
    use one of the data-type specific constructors.
    The base constructor should be used only to create subsections for
    custom content types.

    See Also
    --------
    config : Create a subsection from configs (dict, yaml, json).
    image : Create a subsection from an image (png, svg).
    plot : Create a subsection from a plot (matplotlib Figure).
    tabular : Create a subsection from tabular data (csv, tsv, df).
    value : Create a subsection from an individual value (str, float).

    Parameters
    ----------
    display : str
        The main content to display as an HTML embeddable utf-8 string.
    title : str
        The title of the subsection.
    info : str
        Description of the content to place in the collapsible info section.
        Supports HTML tags for formatting (bold, italics, ...).
    buttons : Iterable of DownloadButton
        Iterable of buttons to download the section data in multiple formats.

    """

    def __init__(
        self,
        display: str,
        *,
        title: str,
        info: str,
        buttons: Iterable[hh.DownloadButton],
    ):
        self._display = display
        self._title = title
        self._info = info
        self._buttons = buttons

    @classmethod
    def config(cls, content: dict | str, *, title: str, info: str) -> "Subsection": ...

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
    def plot(
        cls,
        content: figure.Figure,
        *,
        title: str,
        info: str,
        data: Tabular | None = None,
        format: PlotFormat = "svg+png",
    ) -> "Subsection":
        """Create a subsection from a plot (matplotlib Figure).

        Parameters
        ----------
        content : matplotlib Figure
            The plot to display as content.
        title : str
            The title of the subsection.
        info : str
            Description of the content to place in the collapsible info section.
            Supports HTML tags for formatting (bold, italics, ...).
        data : Tabular data, optional
            Data used to generate the plot. If provided, creates an additional
            download button to fetch it as a tsv.
        format : {`svg`, `png`, `svg+png`}, optional
            Output formats for which to create a download button.
            Default is `svg+png`.

        Note
        ----
        If trying to embed an image file, use the `image` constructor.
        """

        # svg plot is always created since it is used for display purposes
        svg_plot = em.svg_plot_string(content)

        buttons: Iterable[hh.DownloadButton] = []

        if format in ("svg", "svg+png"):
            buttons.append(hh.DownloadButton.from_format(title, svg_plot, "svg"))
        if format in ("png", "svg+png"):
            png_plot = em.png_plot_bytes(content)
            buttons.append(hh.DownloadButton.from_format(title, png_plot, "png"))

        if data is not None:
            tsv_data = em.df_to_tsv(sc.scan_tabular(data))
            buttons.append(hh.DownloadButton.from_format(title, tsv_data, "tsv"))

        return Subsection(
            svg_plot.decode("utf-8"), title=title, info=info, buttons=buttons
        )

    @classmethod
    def tabular(
        cls,
        content: Tabular,
        *,
        title: str,
        info: str,
        format: TabularFormat = "tsv",
    ) -> "Subsection":
        """Create a subsection from tabular data (e.g. csv, tsv, df).

        Parameters
        ----------
        content : Tabular data
            The tabular data to display as content. Can be a polars or
            pandas DataFrame, or a path to a csv or tsv file.
        title : str
            The title of the subsection.
        info : str
            Description of the content to place in the collapsible info section.
            Supports HTML tags for formatting (bold, italics, ...).
        format : {`tsv`, `csv`}, optional
            Format used for the download button generated for this data.
            Default is `tsv`.

        Note
        ----
        If trying to attach tabular data to a plot, use the `data` parameter
        of the `plot` constructor instead.
        """

        df = sc.scan_tabular(content)

        table_display = em.df_to_html(df)

        match format:
            case "tsv":
                button = hh.DownloadButton.from_format(title, em.df_to_tsv(df), "tsv")
            case "csv":
                button = hh.DownloadButton.from_format(title, em.df_to_csv(df), "csv")

        return Subsection(table_display, title=title, info=info, buttons=(button,))

    @classmethod
    def value(
        cls,
        content: str | float,
        *,
        title: str,
        info: str,
    ) -> "Subsection":
        """Create a subsection from an individual value (str, float).

        Parameters
        ----------
        content : str or float
            The value to display as content.
        title : str
            The title of the subsection.
        info : str
            Description of the content to place in the collapsible info section.
            Supports HTML tags for formatting (bold, italics, ...).

        """

        value_display = em.value_to_html(content)

        value_df = pl.DataFrame({"stat": title, "value": content})
        button = hh.DownloadButton.from_format(title, em.df_to_tsv(value_df), "tsv")

        return Subsection(value_display, title=title, info=info, buttons=(button,))

    def get_content(self) -> str:
        html = hh.get_html(self._display, self._title, self._info, self._buttons)
        return f"# %%\ndisplay(HTML({html!r}))"
