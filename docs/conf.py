import os
from pathlib import Path
from runpy import run_path

from paperthin import __version__

project = "paperthin"
copyright = "2026, Stefano Cretti"
author = "Stefano Cretti"
release = __version__.split("+")[0]
version = release

_scripts = Path(__file__).parent / "_scripts"

_examples = run_path(str(_scripts / "gen_examples.py"))
_examples["build_all"](force=bool(os.environ.get("PAPERTHIN_REBUILD_EXAMPLES")))

_switcher = run_path(str(_scripts / "gen_switcher.py"))
_switcher["build"]()

_rtd_version = os.environ.get("READTHEDOCS_VERSION", "")
_version_match = _rtd_version if _rtd_version else "latest"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "myst_parser",
    "sphinx_copybutton",
]

exclude_patterns = ["_build", "_scripts"]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

myst_enable_extensions = [
    "colon_fence",
    "substitution",
]
myst_heading_anchors = 2

napoleon_numpy_docstring = True
napoleon_google_docstring = False

autodoc_typehints = "description"
autodoc_member_order = "bysource"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pandas": ("https://pandas.pydata.org/docs", None),
    "polars": ("https://docs.pola.rs/api/python/stable", None),
    "matplotlib": ("https://matplotlib.org/stable", None),
}

html_title = project
html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_theme_options = {
    "github_url": "https://github.com/StefanoCretti/paperthin",
    "show_prev_next": False,
    "navigation_with_keys": True,
    "check_switcher": False,
    "switcher": {
        "json_url": "https://paperthin.readthedocs.io/en/latest/_static/switcher.json",
        "version_match": _version_match,
    },
    "navbar_end": ["version-switcher", "theme-switcher", "navbar-icon-links"],
}
