"""
CLI - Inputs
keys.py
"""
import sys
import threading
import dataclasses
from typing import Union, Optional 

import test.debug
import compatibility.plateform as plateform
if plateform.OS == plateform.Os.UNIX:
    import termios
    import tty
    
    import compatibility.unix
elif plateform.OS == plateform.Os.WINDOWS:
    import msvcrt

import base.specials as specials

class Key:
    """
    Store the name and the codes of a specific key. \r
    It is immmutable. To get the OS corresponding key's raw ASCII code, use: \n
    ```python
        Key.get()
    ```
    To print the un-escaped, with possible interactions, use: \n
    ```python
        Key.key()
    ```
    """
    _name: str
    _windows: str
    _unix: str

    def __init__(self, name: str, windows: str = "", unix: str = "") -> None:
        self._name = name
        self._windows = windows
        self._unix = unix

    @staticmethod
    def new_common(name: str) -> 'Key':
        """
        Creates an instances for a common character.
        """
        return Key(
            name,
            name,
            name,
        )

    def __repr__(self) -> str:
        return f"Key(name={repr(self._name)}, windows={repr(self._windows)}, unix={repr(self._unix)})"

    def __eq__(self, other: Union['Key', str]) -> bool: # pyright: ignore[reportIncompatibleMethodOverride]
        """
        Compare keys, `str` or `Key`.
        """
        if isinstance(other, Key):
            return self.key() == other.key()
        else:
            return self.key() == other

    def get(self, os: plateform.Os = plateform.OS) -> str:
        """
        Return the key string, showing the representation `repr`. 
        """
        if os == plateform.Os.UNIX:
            return repr(self._unix)
        elif os == plateform.Os.WINDOWS:
            return repr(self._windows)

    def key(self, os: plateform.Os = plateform.OS) -> str:
        """
        Return the key string, un-escaped. \r
        Use for comparison.
        """
        if os == plateform.Os.UNIX:
            return self._unix
        elif os == plateform.Os.WINDOWS:
            return self._windows
    
    @property
    def name(self) -> str:
        return repr(self.name)


class Keys:
    """
    Contains all specials keys. \r
    Common keys are directly mapped to their string equivalents. \r
    All keys are using the `Key` class. \n
    ```python
        UP = Key("Arrow up", "\\x1b[A", "\\x1b[A")
    ``` 
    """
    ESC = Key("Escape", specials.ESC, specials.ESC)
    UP = Key("Arrow up", specials.WINDOWS + "H", specials.ESC +"[A")
    DOWN = Key("Arrow down", specials.WINDOWS + "P", specials.ESC + "[B")
    LEFT = Key("Arrow left", specials.WINDOWS + "[C", specials.ESC + "[C")
    RIGHT = Key("Arrow down", specials.WINDOWS + "[D", specials.ESC + "[D")
    RETURN = Key("Carriage return", "\r", "\r")
    LINE = Key("New line", "\n", "\n")
    SPACE = Key.new_common(" ")
    INTERRUPT = Key("Keyboard interrupt", "\x03", "\x03")


@dataclasses.dataclass
class Info:
    """
    An object to store keys informations, modified by reference. \r
    Used for threading.
    """
    running: bool = False
    history: list[Key] = dataclasses.field(default_factory=list[Key])
    history_length: int = 23

    def new_key(self, key: Key) -> None:
        """
        Update the current key and the history with the given `key`.
        """
        self.history.insert(0, key)

    @property
    def current(self) -> Optional[Key]:
        """
        Return the current key.
        """
        if self.history:
            return self.history[0]
        else:
            return


def get_key(*, allow_keyboard_interrupt: bool = True) -> Key:
    """
    Get the user pressed key.
    """
    if plateform.OS == plateform.Os.UNIX:
        # Old settings are stored in `compatibility.unix`.
        try:
            tty.setraw(compatibility.unix.FILE_ID)          # pyright: ignore[reportPossiblyUnboundVariable]
            key = sys.stdin.read(1)
            # Handle arrow keys (escape sequences).
            if key == specials.ESC:
                key += sys.stdin.read(2)
            # Ctrl+C.
            elif key == "\x03" and allow_keyboard_interrupt:
                raise KeyboardInterrupt(f"(X) - Keyboard interrupt while getting key ({repr(key)}).")

            return Key.new_common(key)
        
        finally:
            termios.tcsetattr(                  # pyright: ignore[reportPossiblyUnboundVariable]
                compatibility.unix.FILE_ID,     # pyright: ignore[reportPossiblyUnboundVariable]
                termios.TCSADRAIN,              # pyright: ignore[reportPossiblyUnboundVariable]
                compatibility.unix.SETTINGS     # pyright: ignore[reportPossiblyUnboundVariable]
            )      
    # Windows
    elif plateform.OS == plateform.Os.WINDOWS: 
        key: str = msvcrt.getch()       # pyright: ignore
        # Special key prefix on Windows
        if key == specials.WINDOWS:  
            key += msvcrt.getch()       # pyright: ignore
        # Ctrl+C.
        elif key == b"\x03" and allow_keyboard_interrupt:
            raise KeyboardInterrupt(f"(X) - Keyboard interrupt while getting key ({repr(key)}).")
        
        return Key.new_common(key.decode('utf-8', errors='ignore'))     # pyright: ignore
    
    # Failed to find os.
    else:
        raise OSError(f"(X) - Keys.get_key: Unrecognized OS ({plateform.OS}).")

def compare(key_a: Union[str, Key], key_b: Union[str, Key]) -> bool:
    """
    Test if 2 keys are the same. \r
    Used for inputs.
    """
    comparison: bool = key_a == key_b
    return comparison

def fetch_target(info: Info) -> None:
    """
    Run a loop in a separate thread. \r
    Send pressed key by reference in the given `info` object.
    Here runs the main loop.
    """
    test.debug.debug_print("keys.fetch_target - Starting loop.")
    while info.running:
        current: Key = get_key(allow_keyboard_interrupt=False)
        test.debug.debug_print(f"compare.fetch_target - Registred key: {current}")
        info.new_key(current)

    test.debug.debug_print("keys.fetch_target - Finished loop.")

def fetch(info: Info) -> None:
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


if __name__ == "__main__":
    print("cf. Exemples.")
