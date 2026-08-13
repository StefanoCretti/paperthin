from .. import html_helpers as hh
from ..adapters import (
    ConfigAdapter,
    ImageAdapter,
    PlotAdapter,
    TabularAdapter,
    ValueAdapter,
)
from ..adapters import types as ct


class Entry:
    """Fundamental unit of a report, corresponding to an individual result.

    An entry is a standardized way to display a result.
    It is always composed of the same elements:
        - A title (h3 size)
        - A toggleable description of the result
        - Some graphical representation of the result
        - Download buttons for the data

    Though it is possible to initialize an entry by providing all these
    elements to the main class constructor, in most cases you should
    use one of the data-type specific constructors.
    The base constructor should be used only to create entries for
    custom content types: pass any object implementing `get_display(self)
    -> str` (the rendered HTML) and `get_buttons(self, title: str) ->
    Iterable[DownloadButton]` (the download buttons).

    See Also
    --------
    config : Create an entry from configs (dict, yaml, json).
    image : Create an entry from an image (png, svg).
    plot : Create an entry from a plot (matplotlib Figure).
    tabular : Create an entry from tabular data (csv, tsv, df).
    value : Create an entry from an individual value (str, float).

    Parameters
    ----------
    content : Adapter
        Object responsible for rendering the display and download buttons
        (see above for the required shape).
    title : str
        The title of the entry.
    info : str
        Description of the content to place in the collapsible info section.
        Supports HTML tags for formatting (bold, italics, ...).

    """

    def __init__(self, content: ct.Adapter, *, title: str, info: str):
        self._content = content
        self._title = title
        self._info = info

    @classmethod
    def config(
        cls,
        source: ct.ConfigSource,
        *,
        title: str,
        info: str,
        output: ct.ConfigOutput = "yaml",
    ) -> "Entry":
        """Create an entry from a config (dict, yaml, or json).

        Parameters
        ----------
        source : dict or str
            The config to display as content. Can be a dict, or a path to a
            yaml or json file.
        title : str
            The title of the entry.
        info : str
            Description of the content to place in the collapsible info section.
            Supports HTML tags for formatting (bold, italics, ...).
        output : {`yaml`, `json`}, optional
            Format used for the download button generated for this data.
            Default is `yaml`.

        """

        return Entry(ConfigAdapter(source, output), title=title, info=info)

    @classmethod
    def image(
        cls,
        source: ct.ImageSource,
        *,
        title: str,
        info: str,
        data: ct.TabularSource | None = None,
        scale: float = 1.0,
    ) -> "Entry":
        """Create an entry from an image (png, svg).

        Parameters
        ----------
        source : str
            Path to a png or svg image file.
        title : str
            The title of the entry.
        info : str
            Description of the content to place in the collapsible info section.
            Supports HTML tags for formatting (bold, italics, ...).
        data : Tabular data, optional
            Data used to generate the image. If provided, creates an additional
            download button to fetch it as a tsv.
        scale : float, optional
            Factor applied to the image's natural width when displaying it
            (e.g. `0.5` for half size). Only affects png images; the
            downloaded file is always the original, unscaled source. Default
            is `1.0`.

        Note
        ----
        If trying to embed a matplotlib Figure directly, use the `plot`
        constructor instead.
        """

        return Entry(ImageAdapter(source, data, scale), title=title, info=info)

    @classmethod
    def plot(
        cls,
        source: ct.PlotSource,
        *,
        title: str,
        info: str,
        data: ct.TabularSource | None = None,
        output: ct.PlotOutput = "svg+png",
        dpi: int = 300,
    ) -> "Entry":
        """Create an entry from a plot (matplotlib Figure).

        Parameters
        ----------
        source : matplotlib Figure
            The plot to display as content.
        title : str
            The title of the entry.
        info : str
            Description of the content to place in the collapsible info section.
            Supports HTML tags for formatting (bold, italics, ...).
        data : Tabular data, optional
            Data used to generate the plot. If provided, creates an additional
            download button to fetch it as a tsv.
        output : {`svg`, `png`, `svg+png`}, optional
            Output formats for which to create a download button.
            Default is `svg+png`.
        dpi : int, optional
            Resolution used when rendering the png download. Default is `300`.

        Note
        ----
        If trying to embed an image file, use the `image` constructor.
        """

        return Entry(PlotAdapter(source, output, data, dpi), title=title, info=info)

    @classmethod
    def tabular(
        cls,
        source: ct.TabularSource,
        *,
        title: str,
        info: str,
        output: ct.TabularOutput = "tsv",
    ) -> "Entry":
        """Create an entry from tabular data (e.g. csv, tsv, df).

        Parameters
        ----------
        source : Tabular data
            The tabular data to display as content. Can be a polars or
            pandas DataFrame, or a path to a csv or tsv file.
        title : str
            The title of the entry.
        info : str
            Description of the content to place in the collapsible info section.
            Supports HTML tags for formatting (bold, italics, ...).
        output : {`tsv`, `csv`}, optional
            Format used for the download button generated for this data.
            Default is `tsv`.

        Note
        ----
        If trying to attach tabular data to a plot, use the `data` parameter
        of the `plot` constructor instead.
        """

        return Entry(TabularAdapter(source, output), title=title, info=info)

    @classmethod
    def value(
        cls,
        source: ct.ValueSource,
        *,
        title: str,
        info: str,
        output: ct.ValueOutput = "tsv",
    ) -> "Entry":
        """Create an entry from an individual value (str, float).

        Parameters
        ----------
        source : str or float
            The value to display as content.
        title : str
            The title of the entry.
        info : str
            Description of the content to place in the collapsible info section.
            Supports HTML tags for formatting (bold, italics, ...).
        output : {`tsv`}, optional
            Format used for the download button generated for this data.
            Default is `tsv`.

        """

        return Entry(ValueAdapter(source, output), title=title, info=info)

    def get_content(self) -> str:
        html = hh.get_html(
            self._content.get_display(),
            self._title,
            self._info,
            self._content.get_buttons(self._title),
        )
        return f"# %%\ndisplay(HTML({html!r}))"
