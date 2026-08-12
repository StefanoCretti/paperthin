from dataclasses import dataclass


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
