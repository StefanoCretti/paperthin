import jupytext
from nbclient import NotebookClient
from nbconvert import HTMLExporter
from traitlets.config import Config

from . import html_helpers as hh
from ._typing import Component


class Report:
    """Container object to populate with the elements of the report.

    Components added to the report

    Parameters
    ----------
    title : str
        Title at the top of the report. Also used to build output name.
    """

    def __init__(self, title: str):
        self._title = title
        self._components: list[Component] = []

    def add(self, component: Component) -> "Report":
        self._components.append(component)
        return self

    __add__ = add

    def make_report(self, path: str):

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
