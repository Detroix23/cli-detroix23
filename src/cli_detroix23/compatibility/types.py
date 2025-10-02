"""
CLI - Compatibility
types.py
"""
from typing import Union

# Type - Attribute list for termios' fetch.
Attr = list[Union[int, list[Union[bytes, int]]]]
# Type - 2D tables, defined also in maths.maths.
table2D = list[list[str]]