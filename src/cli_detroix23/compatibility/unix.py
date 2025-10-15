"""
CLI - Compatibility.
terminal_unix.py
"""
import sys
import termios
from typing import Final

import compatibility.types as types

FILE_ID: Final[int] = sys.stdin.fileno()
SETTINGS: Final[types.Attr] = termios.tcgetattr(FILE_ID)

def set_to_default() -> None:
    """
    Set back to the original settings the terminal.
    """
    termios.tcsetattr(FILE_ID, termios.TCSADRAIN, SETTINGS)
