"""
CLI - Inputs
windows.py
"""
import msvcrt

import base.specials
import inputs.keys

def get_key(*, allow_keyboard_interrupt: bool) -> inputs.keys.Key:
    """
    Get key at one moment. \n
    Windows only, using `msvcrt`.
    """
    key: str = msvcrt.getch()       # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
    # Special key prefix on Windows
    if key == base.specials.WINDOWS:  
        key += msvcrt.getch()
    # Ctrl+C.
    elif key == b"\x03" and allow_keyboard_interrupt:
        raise KeyboardInterrupt(f"(X) - Keyboard interrupt while getting key ({repr(key)}).")
    
    return inputs.keys.Key.new_common(key.decode('utf-8', errors='ignore'))
