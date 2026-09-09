"""Generate the example reports embedded in the documentation.

Each function decorated with `@example` writes one self-contained report into
`docs/_static/examples/`, which the docs pages then embed in an iframe.
"""

import pathlib

import matplotlib

matplotlib.use("Agg")

from matplotlib import pyplot as plt

from paperthin import Entry, Report, Section

OUT_DIR = pathlib.Path(__file__).parent.parent / "_static" / "examples"

_AUTOSIZE = """<script>
(function () {
  function send() {
    parent.postMessage(
      { ptPreviewHeight: document.documentElement.scrollHeight },
      "*"
    );
  }
  window.addEventListener("load", send);
  if (window.ResizeObserver) {
    new ResizeObserver(send).observe(document.documentElement);
  }
})();
</script>
</body>"""


def _inject_autosize(path: pathlib.Path) -> None:
    """Make an embedded report tell its parent page how tall it is."""

    html = path.read_text(encoding="utf-8")
    path.write_text(html.replace("</body>", _AUTOSIZE, 1), encoding="utf-8")


_EXAMPLES = {}


def example(func):
    _EXAMPLES[func.__name__] = func
    return func


@example
def quickstart(path: str) -> None:
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

    report.make_report(path)
    plt.close(fig)


def build_all(force: bool = False) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, func in _EXAMPLES.items():
        target = OUT_DIR / f"{name}.html"
        if target.exists() and not force:
            continue
        func(str(target))
        _inject_autosize(target)


if __name__ == "__main__":
    build_all(force=True)
