# Entries

An {py:class}`~paperthin.Entry` is the fundamental unit of a report. Each entry
is composed of:

- one title
- one toggleable description
- one rendered result
- its download buttons

`Entry` has one classmethod constructor per built-in content type. Every
constructor takes the content as its first positional argument and the
required `title` and `info` keywords. Additionally, constructors can take
additional arguments depending on the content type.

| Constructor                       | Accepts                                          | Download format |
| --------------------------------- | ------------------------------------------------ | --------------- |
| {py:meth}`~paperthin.Entry.plot`  | matplotlib `Figure`                              | `png`, `svg`    |
| {py:meth}`~paperthin.Entry.image` | path to a `.png` or `.svg` file                  | `png`, `svg`    |
| {py:meth}`~paperthin.Entry.tabular` | polars or pandas `DataFrame`, `.csv`/`.tsv` path | `tsv`, `csv`    |
| {py:meth}`~paperthin.Entry.value` | a single `str` or `float`                        | `tsv`           |
| {py:meth}`~paperthin.Entry.config` | `dict`, or path to a `.yaml`/`.json` file       | `yaml`, `json`  |

See the [API reference](../api/entry.md) for the full parameter list and
defaults of each constructor. For content types not listed above, see
[Custom components](custom_components.md).

## Plot

{py:meth}`~paperthin.Entry.plot` embeds a matplotlib `Figure`, with download
buttons for the rendered image (`png`, `svg`, or both) and, optionally, the
data behind it.

```python
from matplotlib import pyplot as plt
from paperthin import Entry

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])

entry = Entry.plot(
    fig,
    title="Squares",
    info="y = x<sup>2</sup> for x in 1..3.",
    output="svg+png",
)
```

## Image

{py:meth}`~paperthin.Entry.image` embeds an existing `.png` or `.svg` file
instead of a matplotlib `Figure` you still hold in memory.

```python
from paperthin import Entry

entry = Entry.image(
    "figures/diagram.svg",
    title="Pipeline overview",
    info="Exported from the diagramming tool, not generated in this script.",
    scale=0.75,
)
```

## Tabular

{py:meth}`~paperthin.Entry.tabular` renders a table from a polars or pandas
`DataFrame`, or a path to a `.csv`/`.tsv` file, with a matching download
button.

```python
import polars as pl
from paperthin import Entry

df = pl.DataFrame({"sample": ["a", "b", "c"], "score": [0.91, 0.87, 0.95]})

entry = Entry.tabular(
    df,
    title="Sample scores",
    info="One row per sample, higher score is better.",
    output="tsv",
)
```

## Value

{py:meth}`~paperthin.Entry.value` displays a single `str` or `float`, useful
for a headline metric.

```python
from paperthin import Entry

entry = Entry.value(
    0.938,
    title="Overall accuracy",
    info="Computed on the held-out test split.",
)
```

## Config

{py:meth}`~paperthin.Entry.config` displays a `dict`, or a path to a
`.yaml`/`.json` file, pretty-printed as YAML, with a download button in
either format.

```python
from paperthin import Entry

entry = Entry.config(
    {"learning_rate": 1e-3, "batch_size": 64, "epochs": 20},
    title="Run configuration",
    info="Parameters used for this training run.",
    output="yaml",
)
```
