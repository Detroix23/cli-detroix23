"""
CLI - Inputs
unix.py
"""
import sys
import tty

import compatibility.unix
import base.specials
import inputs.keys


def get_key(*, allow_keyboard_interrupt: bool) -> inputs.keys.Key:
    """
    Get the current pressed key on Unix systems. \r
    Old settings are stored in `compatibility.unix`.
    Return a key of class `inputs.keys.Key`.
    """
    key: str

    try:
        tty.setraw(compatibility.unix.FILE_ID)

        # compatibility.unix.test_present_settings()

        key = sys.stdin.read(1)
        # Handle arrow keys (escape sequences).
        if key == base.specials.ESC:
            key += sys.stdin.read(2)
        # Ctrl+C.
        elif key == "\x03" and allow_keyboard_interrupt:
            raise KeyboardInterrupt(f"(X) - Keyboard interrupt while getting key ({repr(key)}).")

        compatibility.unix.set_to_default()
        return inputs.keys.Key.new_common(key)
    
    finally:
        compatibility.unix.set_to_default()
