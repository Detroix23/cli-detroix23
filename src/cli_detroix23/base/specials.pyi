from typing import Final

ESC_BYTES: Final[bytes]
ESC: Final[str]
MSVCRT_GETCH_SPECIALS: Final[set[int]]
WINDOWS: Final[bytes]
NICE_MAP: Final[dict[str, str]]

def filter_map(current_map: dict[str, str], key: bytes) -> list[str]: ...
