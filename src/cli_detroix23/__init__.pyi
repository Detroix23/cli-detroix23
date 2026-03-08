"""
# CLI.
src/cli_detroix23/__init__.py

This is a custom library made to animate programs running in the terminal.
The most useful will be found in:
- `base`
- `animations`.
"""

from base import *
from animations import *
from . import (
    animations as animations, 
    base as base, 
    compatibility as compatibility, 
    inputs as inputs, 
    maths as maths, 
    shapes as shapes,
)
