"""
CLI - Test
debug.py
"""
import sys
from typing import Optional

from . import defaults
from cli_detroix23.base import style

ENABLE_DEBUG: bool = False
""" 
Enabling debug will print information at the same time and on the same screen
as the main application.   
Starts `False`, can be enabled at startup with the argument `-d`.
"""

def debug_print(
    message: str, 
    *, 
    end: str = "\n", 
    print_style: Optional[str] = defaults.LOG_DEBUG_COLOR, 
    prefix: str = defaults.LOG_DEBUG,
    flush: bool = False,
) -> None:
    """
    Debug print, if `ENABLE_DEBUG`.
    """
    if ENABLE_DEBUG and not style:
        sys.stdout.write(f"{prefix}{message}{end}")

    elif ENABLE_DEBUG:
        sys.stdout.write(f"{print_style}{prefix}{message}{end}{style.Style.END}")

    if flush:
        sys.stdout.flush()
    