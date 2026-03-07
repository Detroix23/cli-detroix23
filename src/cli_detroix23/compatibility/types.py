"""
# CLI - Compatibility
src/cli_detroix23/compatibility/types.py
"""

from typing import Union

Attr = list[Union[int, list[Union[bytes, int]]]]
"""
**Type** Attribute list for termios' fetch.
"""
Table2D = list[list[str]]
"""
**Type** 2D tables, made of `list` of `list` of `str`.
"""
InputSymbols = Union[dict[str, list[str]], list[str], None]
"""
**Type** `InputSymbols` define the allowed keywords that the user can enter in a terminal input.
    - `None`: no restriction
    - `list[str]`: Only one keyword for each symbol, itself
    - `dict[str, list[str]]`: Each symbol can have multiple keywords.
"""
