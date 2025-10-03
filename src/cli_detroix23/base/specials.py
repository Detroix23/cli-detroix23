"""
CLI - Style/ Base
specials.py
Special escape characters.
"""
from typing import Final

_POSSIBLE_ESC: Final[set[str]] = {"\033", "\x1b"}
ESC: Final[str] = "\x1b"
WINDOWS: Final[str] = "\xe0"

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

def filter_map(map: dict[str, str], string: str) -> list[str]:
    """
    Return a list of str with the corresping string of the given map, if existant.
    Else, puts the character itself.
    """
    result: list[str] = list()
    if string in map:
        result = [map[string]]
    elif len(string) > 1:
        for char in string:
            if char in map:
                result.append(map[char])
            else:
                result.append(char)
    else:
        result = [string]

    return result

