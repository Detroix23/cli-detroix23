"""
# CLI - Inputs.
src/cli_detroix23/inputs/windows.py 

_This file can be interpreted fully only on Windows systems._
"""

import os
from typing import Optional

from cli_detroix23.compatibility import platform
from cli_detroix23.base import specials
from cli_detroix23.inputs import keys

if os.name != "nt": 
    raise OSError("Tried to open an Windows-only script (src/cli_detroix23/inputs/windows.py).")

import msvcrt

def get_key(*, allow_keyboard_interrupt: bool) -> keys.Key:
    """
    Get key at one moment. \n
    Windows only, using `msvcrt`.
    """
    key: bytes = msvcrt.getch()  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
    # Special key prefix on Windows
    if key == specials.WINDOWS:  
        key += msvcrt.getch()
        # debug.debug_print(f"inputs.window.get_key() key: {key}")
    # Ctrl+C.
    elif key == b"\x03" and allow_keyboard_interrupt:
        raise KeyboardInterrupt(f"Keyboard interrupt while getting key ({repr(key)}).")
    
    key_object: Optional[keys.Key] = None
    
    if key[0] in specials.MSVCRT_GETCH_SPECIALS:
        for default_key in keys.Keys.to_dict().values():
            if key == default_key.key(platform.Os.WINDOWS):
                key_object = default_key
                break
        
        if key_object is None:
            raise KeyError(f"Specials key unbound ({repr(key)}).")

    else:
        key_object = keys.Key.new_common(key.decode(encoding='utf-8', errors='strict'))

    return key_object
