"""
# CLI - Compatibility.
src/cli_detroix23/compatibility/defaults.py
"""

from typing import Final

from cli_detroix23.base import style

LOG_DEBUG: Final[str] = " (D) "
LOG_INFO: Final[str] = "(?)"
LOG_WARNING: Final[str] = "(!)"
LOG_ERROR: Final[str] = "(X)"

LOG_DEBUG_COLOR: str = style.Color.CYAN

USER_INCORRECT_INPUT: Final[str] = LOG_WARNING + " Incorrect input. Please try again."

INPUTS_NO: Final[list[str]] = ["No", "NO", "no", "n", "N"]
INPUTS_YES: Final[list[str]] = ["Yes", "YES", "yes", "ye", "y", "Y"]
