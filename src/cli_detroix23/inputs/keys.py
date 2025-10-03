"""
CLI - Inputs
keys.py
"""
import sys

import compatibility.plateform as plateform
if plateform.OS == plateform.Os.UNIX:
    import termios
    import tty
elif plateform.OS == plateform.Os.WINDOWS:
    import msvcrt
from typing import Union

import compatibility.types as types

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
            return self.key() == other.get()
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
    UP = Key("Arrow up", specials.ESC +"[A", specials.ESC + "[A")
    DOWN = Key("Arrow down", specials.ESC + "[B", specials.ESC + "[B")
    LEFT = Key("Arrow left", specials.ESC + "[C", specials.ESC + "[C")
    RIGHT = Key("Arrow down", specials.ESC + "[D", specials.ESC + "[D")
    RETURN = Key("Carriage return", "\r", "\r")
    LINE = Key("New line", "\n", "\n")
    SPACE = Key.new_common(" ")



def get_key(*, allow_keyboard_interrupt: bool = True) -> Key:
    """
    Get the user pressed key.
    """
    if plateform.OS == plateform.Os.UNIX:
        fd: int = sys.stdin.fileno()
        old_settings: types.Attr = termios.tcgetattr(fd)    # pyright: ignore[reportPossiblyUnboundVariable]
        try:
            tty.setraw(sys.stdin.fileno())                  # pyright: ignore[reportPossiblyUnboundVariable]
            key = sys.stdin.read(1)
            # Handle arrow keys (escape sequences).
            if key == specials.ESC:
                key += sys.stdin.read(2)
            # Ctrl+C.
            elif key == "\x03" and allow_keyboard_interrupt:
                raise KeyboardInterrupt(f"(X) - Keyboard interrupt while getting key ({repr(key)}).")
            
            return Key.new_common(key)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)      # pyright: ignore[reportPossiblyUnboundVariable]
    # Windows
    elif plateform.OS == plateform.Os.WINDOWS: 
        key: str = msvcrt.getch()       # pyright: ignore
        # Special key prefix on Windows
        if key == b"\xe0":  
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
    comp_a: str = key_a.get() if isinstance(key_a, Key) else key_a
    comp_b: str = key_b.get() if isinstance(key_b, Key) else key_b
    
    return comp_a == comp_b


if __name__ == "__main__":
    print("cf. Exemples.")