import json
import pathlib
from collections.abc import Iterable
from html import escape

import yaml

from ..html_helpers import DownloadButton
from . import types as ct


class ConfigAdapter:
    def __init__(self, source: ct.ConfigSource, output: ct.ConfigOutput):

        if isinstance(source, str):
            match pathlib.Path(source).suffix:
                case ".json":
                    with open(source) as f:
                        source = json.load(f)
                case ".yaml" | ".yml":
                    with open(source) as f:
                        source = yaml.safe_load(f)
                case _:
                    raise ValueError(f"{source} is not a valid json or yaml file.")

        self._data = source
        self._output: ct.ConfigOutput = output

    def get_display(self) -> str:
        text = yaml.safe_dump(self._data, sort_keys=False, default_flow_style=False)
        return f'<pre class="pt-config">{escape(text)}</pre>'

    def get_buttons(self, title: str) -> Iterable[DownloadButton]:

        match self._output:
            case "yaml":
                content = yaml.safe_dump(
                    self._data, sort_keys=False, default_flow_style=False
                ).encode("utf-8")
            case "json":
                content = json.dumps(self._data, indent=2, default=str).encode("utf-8")

        button = DownloadButton.from_format(title, content, self._output)
        return (button,)
