"""
# CLI - Inputs.
src/cli_detroix23/inputs/fetch.py  
"""
import threading
from typing import Union

from cli_detroix23.compatibility import platform, debug
from cli_detroix23.inputs import keys

def get(*, allow_keyboard_interrupt: bool = True) -> keys.Key:
    """
    Get the user pressed key one time.
    """

    key: keys.Key

    if platform.OS == platform.Os.UNIX:
        from cli_detroix23.inputs import unix

        key = unix.get_key(allow_keyboard_interrupt=allow_keyboard_interrupt)

    # Windows
    elif platform.OS == platform.Os.WINDOWS: 
        from cli_detroix23.inputs import windows

        key = windows.get_key(allow_keyboard_interrupt=allow_keyboard_interrupt)
    
    # Failed to find os.
    else:
        raise OSError(f"(X) - Keys.get_key: Unrecognized OS ({platform.OS}).")

    debug.debug_print(f"inputs.fetch.get() Key: {key}")

    return key

def compare(key_a: Union[str, keys.Key], key_b: Union[str, keys.Key]) -> bool:
    """
    Test if 2 keys are the same.

    Used for inputs.
    """
    comparison: bool = key_a == key_b
    return comparison

def fetch_target(info: keys.Info) -> None:
    """
    Run a loop in a **separate thread**.  
    Send pressed key by reference in the given `info` object.
    """
    debug.debug_print("inputs.fetch.fetch_target() Starting loop.")
    
    current: keys.Key
    while info.running:
        current = get(allow_keyboard_interrupt=False)
        debug.debug_print(f"compare.fetch_target - Registered key: {current}")
        info.new_key(current)

    debug.debug_print("inputs.fetch.fetch_target() Finished loop.")

def fetch(info: keys.Info) -> None:
    """
    Creates the thread, calling `fetch_target`.
    """
    debug.debug_print("keys.fetch - Starting thread.")
    key_thread = threading.Thread(
        target=fetch_target, 
        args=(info,), 
        daemon=True,
    )
    key_thread.start()
