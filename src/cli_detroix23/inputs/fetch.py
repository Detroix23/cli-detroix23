"""
# CLI - Inputs.
src/cli_detroix23/inputs/fetch.py  
"""
import threading
from typing import Union

from cli_detroix23 import test
from cli_detroix23.compatibility import plateform
from cli_detroix23.inputs import keys

def get(*, allow_keyboard_interrupt: bool = True) -> keys.Key:
    """
    Get the user pressed key one time.
    """

    key: keys.Key

    if plateform.OS == plateform.Os.UNIX:
        from cli_detroix23.inputs import unix

        key = unix.get_key(
            allow_keyboard_interrupt=allow_keyboard_interrupt
        )

    # Windows
    elif plateform.OS == plateform.Os.WINDOWS: 
        from cli_detroix23.inputs import windows

        key = windows.get_key(
            allow_keyboard_interrupt=allow_keyboard_interrupt
        )
    
    # Failed to find os.
    else:
        raise OSError(f"(X) - Keys.get_key: Unrecognized OS ({plateform.OS}).")

    test.debug.debug_print(f"\ninputs.fetch.get() Key: {key}")

    return key

def compare(key_a: Union[str, keys.Key], key_b: Union[str, keys.Key]) -> bool:
    """
    Test if 2 keys are the same.

    Used for inputs.
    """
    comparison: bool = key_a == key_b
    return comparison

def fetch_target(info: keys.Info, delay: float = 0.02) -> None:
    """
    Run a loop in a separate thread.  

    Send pressed key by reference in the given `info` object.

    Here runs the main loop.
    """
    test.debug.debug_print("keys.fetch_target - Starting loop.")
    
    current: keys.Key
    while info.running:
        current = get(allow_keyboard_interrupt=False)
        test.debug.debug_print(f"compare.fetch_target - Registered key: {current}")
        info.new_key(current)

    test.debug.debug_print("keys.fetch_target - Finished loop.")

def fetch(info: keys.Info) -> None:
    """
    Run a loop in a separate thread.  

    Send pressed key by reference in the given `info` object.
    
    Here is created the thread, calling `fetch_target`.
    """
    test.debug.debug_print("keys.fetch - Starting thread.")
    key_thread = threading.Thread(
        target=fetch_target, 
        args=(info,), 
        daemon=True,
    )
    key_thread.start()
