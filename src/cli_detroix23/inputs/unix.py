"""
# CLI - Inputs.
src/cli_detroix23/inputs/unix.py  

_This file can be interpreted fully only on Unix systems._
"""

import os
import sys

from cli_detroix23.base import specials
from cli_detroix23.inputs import keys

if os.name != "posix":
    raise OSError("Tried to open an Unix-only script (src/cli_detroix23/inputs/unix.py).")

import tty

from cli_detroix23.compatibility import unix

def get_key(*, allow_keyboard_interrupt: bool) -> keys.Key:
    """
    Get the current pressed key on Unix systems. \r
    Old settings are stored in `compatibility.unix`.
    Return a key of class `inputs.keys.Key`.
    """
    key: str

    try:
        tty.setraw(unix.FILE_ID)

        # compatibility.unix.test_present_settings()

        key = sys.stdin.read(1)
        # Handle arrow keys (escape sequences).
        if key == specials.ESC:
            key += sys.stdin.read(2)
        # Ctrl+C.
        elif key == "\x03" and allow_keyboard_interrupt:
            raise KeyboardInterrupt(f"Keyboard interrupt while getting key ({repr(key)}).")
        
        unix.set_to_default()
        return keys.Key.new_common(key)

    finally:
        unix.set_to_default()
