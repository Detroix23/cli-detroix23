"""
# CLI - Compatibility
src/cli_detroix23/compatibility/platform.py
"""
import os
from typing import Final
from enum import Enum

class Os(Enum):
    """
    List supported systems.
    - `WINDOWS`;
    - `UNIX`;
    """
    WINDOWS = 0
    UNIX = 1

OS: Final[Os] = Os.UNIX if os.name == 'posix' else Os.WINDOWS
"""
Define **current** OS.
"""

