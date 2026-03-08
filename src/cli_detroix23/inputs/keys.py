"""
$ CLI - Inputs.
src/cli_detroix23/inputs/keys.py  
"""

import dataclasses
from typing import Optional, Final

from cli_detroix23.compatibility import platform
from cli_detroix23.base import specials

class Key:
    """
    Store the name and the codes of a specific key. \r
    It is immutable. To get the OS corresponding key's raw ASCII code, use: \n
    ```python
        Key.get()
    ```
    To print the un-escaped, with possible interactions, use: \n
    ```python
        Key.key()
    ```

    Set to `\\000` when key is unknown one side.
    """
    _name: Final[str]
    _windows: Final[bytes]
    _unix: Final[bytes]   

    def __init__(self, name: str, windows: bytes = b"", unix: bytes = b"") -> None:
        self._name = name
        self._windows = windows
        self._unix = unix

    @staticmethod
    def new_common(name: str) -> 'Key':
        """
        Creates an instances for a common character.

        **Do not use this method for keys with _escape characters_!**
        """
        return Key(
            name,
            name.encode('utf-8', errors="strict"),
            name.encode('utf-8', errors="strict"),
        )

    def __repr__(self) -> str:
        return f"Key(name={repr(self._name)}, windows={repr(self._windows)}, unix={repr(self._unix)})"

    def __eq__(self, other: object) -> bool:
        """
        Compare keys **OS-wise**. With type of `other`:
        - `Key`: compare the result of both the `.key()
        """
        if isinstance(other, Key):
            return self.key() == other.key()
        elif isinstance(other, bytes):
            return self.key() == other
        else:
            return NotImplemented

    def get(self, os: platform.Os = platform.OS) -> str:
        """
        Return the key string, showing the representation `repr`. 
        """
        if os == platform.Os.UNIX:
            return repr(self._unix)
        elif os == platform.Os.WINDOWS:
            return repr(self._windows)

    def key(self, os: platform.Os = platform.OS) -> bytes:
        """
        Return the raw key `bytes`, un-escaped. \r
        Use for comparison.
        """
        if os == platform.Os.UNIX:
            return self._unix
        elif os == platform.Os.WINDOWS:
            return self._windows
    
    @property
    def name(self) -> str:
        return repr(self.name)


class Keys:
    """
    # `Keys`. List all supported specials keys.
    Common keys are directly mapped to their string equivalents (`Key.new_common`).

    All keys are using the `Key` class. _Example_:
    ```python
    UP = Key("Arrow up", "\\x1b[A", "\\x1b[A")
    ``` 
    """
    ESC: Final[Key] = Key("Escape", specials.WINDOWS, specials.ESC_BYTES)
    UP: Final[Key] = Key("Arrow up", specials.WINDOWS + b"H", specials.ESC_BYTES + b"[A")
    DOWN: Final[Key] = Key("Arrow down", specials.WINDOWS + b"P", specials.ESC_BYTES + b"[B")
    LEFT: Final[Key] = Key("Arrow left", specials.WINDOWS + b"K", specials.ESC_BYTES + b"[C")
    RIGHT: Final[Key] = Key("Arrow right", specials.WINDOWS + b"M", specials.ESC_BYTES + b"[D")
    RETURN: Final[Key] = Key("Carriage return", b"\r", b"\r")
    LINE: Final[Key] = Key("New line", b"\n", b"\n")
    SPACE: Final[Key] = Key("Space", b" ", b" ")
    INTERRUPT: Final[Key] = Key("Keyboard interrupt", b"\x03", b"\x03")

    _key_dict: Optional[dict[str, Key]] = None

    @staticmethod
    def to_dict() -> dict[str, Key]:
        """
        Returns a `dict` of the saved keys.
        """
        if Keys._key_dict is not None:
            return Keys._key_dict

        keys: dict[str, Key] = {}
        for name, value in Keys.__dict__.items():
            if name[0] != "_" and name != "to_dict":
                keys[name] = value
        
        Keys._key_dict = keys
        return keys


@dataclasses.dataclass
class Info:
    """
    An object to store keys information, modified by reference. \r
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


# Initialize the `Keys` constants attributes.
KEYS_DICT: dict[str, Key] = Keys.to_dict()
""" Dictionary form of the specials `Keys`. """

# Shortcuts.
ESC: Key = Keys.ESC
UP: Key = Keys.UP
DOWN: Key = Keys.DOWN
LEFT: Key = Keys.LEFT
RIGHT: Key = Keys.RIGHT
RETURN: Key = Keys.RETURN
LINE: Key = Keys.LINE
SPACE: Key = Keys.SPACE
INTERRUPT: Key = Keys.INTERRUPT


if __name__ == "__main__":
    exit("cf. Examples.")
