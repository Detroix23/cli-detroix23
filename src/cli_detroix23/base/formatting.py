"""
# CLI.
src/cli_detroix23/base/formatting.py
"""

from typing import Iterable

from cli_detroix23.base import style

def table(
    elements: Iterable[str], 
    max_per_col: int = 60,
    row_prefix: str = "\t",
    row_suffix: str = "",
    spacer: str = " ",
    table_footer: str = "─",
    color: str = style.Color.GREEN
) -> str:
    """
    Return a formatted string of row-col table.
    Counts the character number.
    """
    table: str = row_prefix
    char_count: int = 0
    for element in elements:
        char_count += len(element)
        if char_count > max_per_col and len(element) <= max_per_col:
            table += f"{row_suffix}\n{row_prefix}"
        else:
            table += f"{spacer}{color}{element}{style.Style.END}"

    if table_footer:
        table += f"\n{row_prefix}{table_footer * max_per_col}"

    return table