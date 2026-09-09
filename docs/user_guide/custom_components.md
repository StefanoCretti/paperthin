# Custom components

Paperthin is meant to be extended. You can add your own visual elements to a
report, and you can teach `Entry` to display content types it does not ship
with.

Neither is done through inheritance. Paperthin describes what it needs with
[protocols](https://peps.python.org/pep-0544/),
so there is no base class to subclass and nothing to register: as long as an
object provides the expected methods, it can be added to a report.

## Generic components

Everything you add to a {py:class}`~paperthin.Report` is a *component*, which
means it satisfies the {py:class}`~paperthin.protocols.Component`
protocol. That protocol asks for a single method:

```python
class Component(Protocol):
    def get_content(self) -> str: ...
```

`get_content` returns a string holding one or more notebook cells in
[jupytext percent format](https://jupytext.readthedocs.io/en/latest/formats-scripts.html).
During {py:meth}`~paperthin.Report.make_report` those cells are executed and
their output becomes part of the document.

You will most likely write a component when you want a new graphical element,
that is, something that is not an entry. A divider carrying a subtitle, for
example:

```python
class TitledSection:
    def __init__(self, title: str, subtitle: str):
        self._title = title
        self._subtitle = subtitle

    def get_content(self) -> str:
        return f"# %% [markdown]\n# ## {self._title}\n# *{self._subtitle}*"
```

It is then added like anything else:

```python
from paperthin import Report

report = Report("My report") + TitledSection("Results", "run 42")
```

Because the returned cells are executed, a component can also run code rather
than emit markdown. Keep in mind that all cells share a single kernel and run
in the order the components were added.

## Custom entries

An {py:class}`~paperthin.Entry` is a component that already carries the logic
to display some content and to make it available for download. Rather than
reimplementing all of that logic for every new content format, you extend
`Entry` through [composition](https://en.wikipedia.org/wiki/Object_composition):
you write an *adapter* for your format and pass it to the `Entry` constructor.

An adapter satisfies the {py:class}`~paperthin.protocols.Adapter`
protocol, which asks for two methods:

```python
class Adapter(Protocol):
    def get_display(self) -> str: ...

    def get_buttons(self, title: str) -> Iterable[DownloadButton]: ...
```

`get_display` returns the HTML embedded in the body of the report. Turning
your content into markup a browser can render is the adapter's job, so this is
where a figure becomes an `<img>` tag or a table becomes a `<table>`.

`get_buttons` returns the {py:class}`~paperthin.helpers.DownloadButton`
objects shown next to the entry's title, or an empty tuple for no downloads.
Reports are self-contained, so each button carries its payload inline. That
means you also have to convert your data into raw bytes and declare the
[MIME type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types)
that describes them.

```python
from html import escape

from paperthin import Entry
from paperthin.helpers import DownloadButton


class TextAdapter:
    def __init__(self, text: str):
        self._text = text

    def get_display(self) -> str:
        return f"<pre>{escape(self._text)}</pre>"

    def get_buttons(self, title: str) -> list[DownloadButton]:
        return [
            DownloadButton(
                label="TXT",
                content=self._text.encode("utf-8"),
                mime="text/plain",
                file_name=f"{title}.txt",
            )
        ]


entry = Entry(
    TextAdapter("Full run log goes here..."),
    title="Run log",
    info="Raw stdout captured during the run.",
)
```

The resulting entry is added to a report exactly like a built-in one:

```python
from paperthin import Report, Section

report = Report("My report") + Section("Logs") + entry
report.make_report("report.html")
```
