from cli_detroix23.base import style as style
from typing import Iterable

def table(
    elements: Iterable[str], 
    max_per_col: int = 60, 
    row_prefix: str = '\t', 
    row_suffix: str = '', 
    spacer: str = ' ', 
    table_footer: str = '─', 
    color: str = ...
) -> str: ...
