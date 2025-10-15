"""
CLI - Inputs
keys.py
"""
import dataclasses
from typing import Union, Optional 

import compatibility.plateform as plateform
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


if __name__ == "__main__":
    print("cf. Exemples.")
