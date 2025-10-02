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

import compatibility.types as types

# import base.specials as specials

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

    def __init__(self, name: str, windows: str, unix: str) -> None:
        self._name = name
        self._windows = windows
        self._unix = unix

    def get(self, os: plateform.Os = plateform.OS) -> str:
        """
        Return the key string, un-escaped. 
        """
        if os == plateform.Os.UNIX:
            return repr(self._unix)
        elif os == plateform.Os.WINDOWS:
            return repr(self._windows)

    def key(self, os: plateform.Os = plateform.OS) -> str:
        """
        Return the key string, un-escaped. 
        """
        if os == plateform.Os.UNIX:
            return self._unix
        elif os == plateform.Os.WINDOWS:
            return self._windows
    
    @property
    def name(self) -> str:
        return repr(self.name)
    
    def __repr__(self) -> str:
        return f"Key(name={self._name}, windows={repr(self._windows)}, unix={repr(self._unix)})"


def get_key(*, allow_keyboard_interrupt: bool = True) -> str:
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
            if key == "\x1b":
                key += sys.stdin.read(2)
            # Ctrl+C.
            elif key == "\x03" and allow_keyboard_interrupt:
                raise KeyboardInterrupt(f"(X) - Keyboard interrupt while getting key ({repr(key)}).")
            return key
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
        return key.decode('utf-8', errors='ignore')     # pyright: ignore
    
    # Failed to find os.
    else:
        raise OSError(f"(X) - Keys.get_key: Unrecognized OS ({plateform.OS}).")

if __name__ == "__main__":
    print("cf. Exemples.")