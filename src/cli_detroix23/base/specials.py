"""
# CLI - Base.
src/cli_detroix23/base/specials.py

Special escape characters.
"""

from typing import Final

_POSSIBLE_ESC: Final[set[str]] = {"\033", "\x1b"}
ESC_BYTES: Final[bytes] = b"\x1b"
ESC: Final[str] = "\x1b"
""" General escape character. """

MSVCRT_GETCH_SPECIALS: Final[set[int]] = {b"\000"[0], b"\xe0"[0]}
WINDOWS: Final[bytes] = b"\xe0"

NICE_MAP: Final[dict[str, str]] = {
    "\x00": "Null",
    "\x01": "Heading start",
    "\x02": "Text start",
    "\x03": "Text end",
    "\x04": "Transmission end",
    "\x05": "Enquiry",
    "\x06": "Acknowledge",
    "\x07": "Alert",
    "\x1b": "Escape",
    "\x03": "Keyboard Interrupt",
    " ": "Space",
    "": "Empty string",
    "\x0b": "Tabulation vertical",
    "\t": "Tabulation horizontal",
    "\r": "Carriage return",
    "\n": "Return",
    "\x7f": "Backspace",
    "\x1b[2": "Insert",
    "\x1b[3": "Delete",
    "\x1b[6": "Page down",
    "\x1b[5": "Page up",
    "\x1b[F": "Fin",
    "\x1b[H": "Home",
    "\x1b[A": "Arrow up",
    "\x1b[B": "Arrow down",
    "\x1b[C": "Arrow left",
    "\x1b[D": "Arrow right",
    "\x1b[?25l": "Cursor hide",
    "\x1b[?25h": "Cursor show"
}

def filter_map(current_map: dict[str, str], key: bytes) -> list[str]:
    """
    Return a list of str with the corresponding string of the given map, if exists.
    Else, puts the character itself.
    """
    string = str(key)
    result: list[str] = list()
    if string in current_map:
        result = [current_map[string]]
        
    elif len(string) > 1:
        for char in string:
            if char in current_map:
                result.append(current_map[char])
            else:
                result.append(char)
    else:
        result = [string]

    return result
