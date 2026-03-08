from cli_detroix23.base import controls as controls, style as style
from cli_detroix23.compatibility import debug as debug, defaults as defaults
from cli_detroix23.inputs import fetch as fetch, keys as keys

class SelectMenu:
    options: list[str]
    prompt: str
    selected_index: int
    select_character: str
    def __init__(self, options: list[str], prompt: str = 'Select an option:') -> None: ...
    def show(self) -> str: ...

def main() -> None: ...
