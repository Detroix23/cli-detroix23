from . import defaults as defaults
from cli_detroix23.base import style as style

ENABLE_DEBUG: bool

def debug_print(
    message: str, 
    *, 
    end: str = '\n', 
    print_style: str | None = ..., 
    prefix: str = ..., 
    flush: bool = False
) -> None: ...
