# How it works

A report is built in three steps:

1. [Initializing a report](#initializing-a-report)
2. [Adding sections and entries](#adding-sections-and-entries)
3. [Writing the HTML file](#writing-the-html-file)

```python
from matplotlib import pyplot as plt
from paperthin import Entry, Report, Section

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])

# Step 1: Initializing a report
report = Report("My report")

# Step 2: Adding sections and entries
report = (
    report
    + Section("Plots")
    + Entry.plot(
        fig,
        title="Squares",
        info="A simple plot with its underlying data attached.",
    )
)

# Step 3: Writing the HTML file
report.make_report("report.html")
```

## Initializing a report

A {py:class}`~paperthin.Report` is an empty container. Its only argument is the
title shown at the top of the finished document.

```python
report = Report("My report")
```

Nothing is rendered at this point, and no file is touched. The report will
simply hold the components you add to it, in order, until you ask for the HTML.

## Adding sections and entries

Anything you add to a report is a *component*. Paperthin ships two of them,
and you can write your own (see [Custom components](custom_components.md)).

A {py:class}`~paperthin.Section` is a purely visual divider: a highlighted
heading used to group what follows it. It holds no content of its own.

An {py:class}`~paperthin.Entry` is the unit that carries content. Every entry
has the same four parts:

- a **title**,
- an **info** description, hidden behind the `i` toggle next to the title,
- the **rendered result** itself,
- **download buttons** for the underlying data, next to the title.

You never build an entry from its base constructor for built-in content.
Instead, each supported content type has its own classmethod, such as
{py:meth}`~paperthin.Entry.plot` or {py:meth}`~paperthin.Entry.tabular`. There
is no auto-detection of the input type: you name the kind of entry you want,
which keeps the behaviour predictable and the error messages specific. See
[Entries](entries.md) for the full list.

`report + component` and `report.add(component)` are the same operation: both
append the component and return the report, so calls can be chained as in the
example above. Components are rendered in the order they were added.

## Writing the HTML file

{py:meth}`~paperthin.Report.make_report` takes a path and produces the
document.

```python
report.make_report("report.html")
```

Under the hood, each component turns itself into one or more notebook cells in
[jupytext percent format](https://jupytext.readthedocs.io/en/latest/formats-scripts.html).
Paperthin assembles those cells into a notebook, executes it, and exports the
result to HTML with the input cells stripped out.
