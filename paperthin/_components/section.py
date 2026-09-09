class Section:
    """Separator to group results into sections.

    Inserts a title (h2) with highlighted background in the report.

    Parameters
    ----------
    title : str
        The title of the section.

    """

    def __init__(self, title: str):
        self._title = title

    @property
    def title(self) -> str:
        return self._title

    def get_content(self) -> str:
        """Return a markdown cell in jupytext percent format.

        Returns
        -------
        str

        """
        return f"# %% [markdown]\n# ## {self.title}"
