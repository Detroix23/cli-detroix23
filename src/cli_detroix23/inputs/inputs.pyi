import pathlib as path
from cli_detroix23.compatibility import defaults as defaults, types as types

symbol_mode: dict[str, list[str]]
symbol_component: dict[str, list[str]]
symbol_bool: dict[str, list[str]]

def list_directory(directory: path.Path) -> None: ...
def input(
    message: str, 
    symbols: types.InputSymbols = None, 
    default: int | None = None, 
    must_validate: bool = True, 
    allowed_type: type = ..., 
    error_message: str = ..., 
    max_iterations: int = 10000
) -> str: ...
def boolean_input(message: str, default: bool = True, error_message: str = ..., max_iterations: int = 10000) -> bool: ...
