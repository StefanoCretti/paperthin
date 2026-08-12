import jupytext
from nbclient import NotebookClient
from nbconvert import HTMLExporter
from traitlets.config import Config

from . import html_helpers as hh
from ._typing import Component


class Report:
    """Container object to populate with results.

    A report can be populated with any provided or user-defined component.
    An object is a component if it implements the `get_content` method,
    which returns a string representing one or more jupyter notebook cells
    in jupytext percent format.

    Components can be added using the `add` method or the overloaded `__add__`.
    Components are rendered in the order they were added to the report.

    Parameters
    ----------
    title : str
        Title displayed at the top of the report (h1).

    """

    def __init__(self, title: str):
        self._title = title
        self._components: list[Component] = []

    def add(self, component: Component) -> "Report":
        """Add a component to the report.

        Returns self to allow chaining add operations.

        Parameters
        ----------
        component : object implementing the `Component` protocol, see constructor.
            An object to add at the end of the current queue of components.

        Returns
        -------
        Report

        """

        self._components.append(component)
        return self

    __add__ = add

    def make_report(self, path: str) -> None:
        """Generate the rendered HTML report at the provided path.

        Parameters
        ----------
        path : str
            Path where to generate the report.

        """

        content = "# %%\nfrom IPython.display import HTML\n\n"
        content += f"# %% [markdown]\n# # {self._title}\n\n"
        content += "\n\n".join(c.get_content() for c in self._components)
        nb = jupytext.reads(content, fmt="py:percent")
        NotebookClient(nb).execute()

        config = Config()
        config.HTMLExporter.exclude_input = True
        config.HTMLExporter.exclude_input_prompt = True
        config.HTMLExporter.exclude_output_prompt = True
        config.HTMLExporter.template_name = "classic"

        exporter = HTMLExporter(config=config)
        html, _ = exporter.from_notebook_node(nb)
        html = html.replace("</head>", f"<style>{hh.QC_STYLE}</style></head>")

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
