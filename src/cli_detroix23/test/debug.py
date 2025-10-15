"""
CLI - Test
debug.py
"""
import sys
from typing import Optional

ENABLE_DEBUG: bool = False

def debug_print(message: str, *, end: str = "\n", style: Optional[str] = None, prefix: str = " ! ") -> None:
    """
    Debug print, if `ENABLE_DEBUG`.
    """
    if ENABLE_DEBUG and not style:
        sys.stdout.write(f"{prefix}{message}{end}")
    elif ENABLE_DEBUG:
        sys.stdout.write(f"{style}{prefix}{message}{end}\0x1b[0m")
