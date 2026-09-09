from typing import Protocol


class Component(Protocol):
    """Anything that can be added to a report.

    A component is responsible for turning itself into notebook cells, which
    the report executes and renders. `Entry` and `Section` both implement it.

    """

    def get_content(self) -> str:
        """Return one or more jupyter notebook cells in jupytext percent format.

        Returns
        -------
        str

        """
        ...
