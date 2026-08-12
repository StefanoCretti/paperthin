import polars as pl

from .. import html_helpers as hh
from ..contents import ConfigContent, Content, PlotContent, TabularContent, ValueContent
from ..contents.types import (
    ConfigOutput,
    PlotOutput,
    PlotSource,
    TabularOutput,
    TabularSource,
)


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
    content : Content
        Object implementing the `Content` protocol (`get_display`, `get_buttons`),
        responsible for rendering the display and download buttons.
    title : str
        The title of the subsection.
    info : str
        Description of the content to place in the collapsible info section.
        Supports HTML tags for formatting (bold, italics, ...).

    """

    def __init__(self, content: Content, *, title: str, info: str):
        self._content = content
        self._title = title
        self._info = info

    @classmethod
    def config(
        cls,
        content: dict | str,
        *,
        title: str,
        info: str,
        format: ConfigOutput = "yaml",
    ) -> "Subsection":
        """Create a subsection from a config (dict, yaml, or json).

        Parameters
        ----------
        content : dict or str
            The config to display as content. Can be a dict, or a path to a
            yaml or json file.
        title : str
            The title of the subsection.
        info : str
            Description of the content to place in the collapsible info section.
            Supports HTML tags for formatting (bold, italics, ...).
        format : {`yaml`, `json`}, optional
            Format used for the download button generated for this data.
            Default is `yaml`.

        """

        return Subsection(ConfigContent(content, format), title=title, info=info)

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
        content: PlotSource,
        *,
        title: str,
        info: str,
        data: TabularSource | None = None,
        format: PlotOutput = "svg+png",
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

        return Subsection(PlotContent(content, format, data), title=title, info=info)

    @classmethod
    def tabular(
        cls,
        content: TabularSource,
        *,
        title: str,
        info: str,
        format: TabularOutput = "tsv",
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

        return Subsection(TabularContent(content, format), title=title, info=info)

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

        return Subsection(ValueContent(content, "tsv"), title=title, info=info)

    def get_content(self) -> str:
        html = hh.get_html(
            self._content.get_display(),
            self._title,
            self._info,
            self._content.get_buttons(self._title),
        )
        return f"# %%\ndisplay(HTML({html!r}))"
