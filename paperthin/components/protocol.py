from typing import Protocol


class Component(Protocol):
    def get_content(self) -> str: ...
