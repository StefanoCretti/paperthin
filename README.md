# Paperthin

## About
Paperthin is a lightweight Python library to easily create HTML reports.

The idea is very simple:

- You provide various items to add to the report (plots, figures, tables...).
- Paperthin stitches them into a nicely formatted HTML report.
- You can then share the report with collaborators (no installations needed on their side).

Why use Paperthin over a plain Jupyter Notebook?

- As it is plain Python, it is very easy to automate (no papermill variable
  injection, takes care of the rendering).
- Minimal but clean formatting (sections, collapsible descriptions, rendering
  presets for many types of data).
- Embeds the data in the report and provides download buttons to retrieve it.
- Easy to inspect in git diffs (no need to learn Jupytext syntax).

## Installation

```bash
pip install paperthin
```

Requires Python 3.12+.

## Quick start

- Create a `Report` object
- Add `Section`s (graphical dividers) and `Entry` items with `+`
- Call `report.make_report(path)`.

```python
from matplotlib import pyplot as plt
from paperthin import Entry, Report, Section

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])

report = (
    Report("My report")
    + Section("Plots")
    + Entry.plot(
        fig,
        title="Squares",
        info="A simple plot with its underlying data attached.",
    )
)

report.make_report("report.html")
```

This produces a single, self-contained `report.html` file you can open in a
browser or send to anyone: no Python or Jupyter required on their end.


## Entries

`Entry` currently provides constructors for the following data types:

| Constructor           | Source                                     |
| --------------------- | ------------------------------------------ |
| `Entry.plot(...)`     | matplotlib `Figure`                        |
| `Entry.image(...)`    | path to a `.png` or `.svg` file            |
| `Entry.tabular(...)`  | polars/pandas `DataFrame`, or csv/tsv path |
| `Entry.value(...)`    | a single `str` or `float`                  |
| `Entry.config(...)`   | `dict`, or path to a yaml/json file        |

## Documentation
This README covers the basics. Extended documentation is planned, including
how to create custom entries, and will be linked here once available.

## Citation
If paperthin is useful in your work, please consider citing the repo:
https://github.com/StefanoCretti/paperthin

## License
BSD-3-Clause. See [LICENSE](LICENSE) for details.
