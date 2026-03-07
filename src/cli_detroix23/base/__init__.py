"""
# CLI
src/cli_detroix23/base/__init__.py

The main base, fundamentals to bring life to the terminal.
Custom handling of ANSI and VT100 formatting, using `sys.stdout`.
"""

from cli_detroix23.base import (
    specials, style, code, colors, controls, boxes, models, formatting, exemples  # pyright: ignore[reportUnusedImport]
)