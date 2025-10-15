"""
CLI - Inputs
fetch.py
"""
import threading
from typing import Union

import test.debug
import compatibility.plateform as plateform
import inputs.keys

def get(*, allow_keyboard_interrupt: bool = True) -> inputs.keys.Key:
    """
    Get the user pressed key one time.
    """
    global inputs

    key: inputs.keys.Key

    if plateform.OS == plateform.Os.UNIX:
        import inputs.unix

        key = inputs.unix.get_key(
            allow_keyboard_interrupt=allow_keyboard_interrupt
        )

        return key

    # Windows
    elif plateform.OS == plateform.Os.WINDOWS: 
        import inputs.windows

        key = inputs.windows.get_key(
            allow_keyboard_interrupt=allow_keyboard_interrupt
        )

        return key
    
    # Failed to find os.
    else:
        raise OSError(f"(X) - Keys.get_key: Unrecognized OS ({plateform.OS}).")

def compare(key_a: Union[str, inputs.keys.Key], key_b: Union[str, inputs.keys.Key]) -> bool:
    """
    Test if 2 keys are the same. \r
    Used for inputs.
    """
    comparison: bool = key_a == key_b
    return comparison

def fetch_target(info: inputs.keys.Info) -> None:
    """
    Run a loop in a separate thread. \r
    Send pressed key by reference in the given `info` object.
    Here runs the main loop.
    """
    test.debug.debug_print("keys.fetch_target - Starting loop.")
    
    while info.running:
        current: inputs.keys.Key = get(allow_keyboard_interrupt=False)
        test.debug.debug_print(f"compare.fetch_target - Registred key: {current}")
        info.new_key(current)

    test.debug.debug_print("keys.fetch_target - Finished loop.")

def fetch(info: inputs.keys.Info) -> None:
    """
    Run a loop in a separate thread. \r
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
