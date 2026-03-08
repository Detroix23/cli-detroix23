import dataclasses
from cli_detroix23.base import specials as specials
from cli_detroix23.compatibility import platform as platform
from typing import Final

class Key:
    def __init__(self, name: str, windows: bytes = b'', unix: bytes = b'') -> None: ...
    @staticmethod
    def new_common(name: str) -> Key: ...
    def __eq__(self, other: object) -> bool: ...
    def get(self, os: platform.Os = ...) -> str: ...
    def key(self, os: platform.Os = ...) -> bytes: ...
    @property
    def name(self) -> str: ...

class Keys:
    ESC: Final[Key]
    UP: Final[Key]
    DOWN: Final[Key]
    LEFT: Final[Key]
    RIGHT: Final[Key]
    RETURN: Final[Key]
    LINE: Final[Key]
    SPACE: Final[Key]
    INTERRUPT: Final[Key]
    @staticmethod
    def to_dict() -> dict[str, Key]: ...

@dataclasses.dataclass
class Info:
    running: bool = ...
    history: list[Key] = dataclasses.field(default_factory=list[Key])
    history_length: int = ...
    def new_key(self, key: Key) -> None: ...
    @property
    def current(self) -> Key | None: ...

KEYS_DICT: dict[str, Key]
ESC: Key
UP: Key
DOWN: Key
LEFT: Key
RIGHT: Key
RETURN: Key
LINE: Key
SPACE: Key
INTERRUPT: Key
